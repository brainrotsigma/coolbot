import praw
import time
from typing import Set, List, Dict
from collections import defaultdict
from tqdm import tqdm
import json
import os

from config import JasonConfig


class SubredditScout:
    def __init__(self, config: JasonConfig):
        self.config = config
        self.reddit = praw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent,
        )
        self.discovered_subreddits: Set[str] = set()
        self.user_subreddit_map: Dict[str, Set[str]] = defaultdict(set)
        
    def scout(self) -> List[str]:
        print("=" * 60)
        print("PHASE 1: SCOUTING")
        print("=" * 60)
        
        initial = self.config.scouting.initial_subreddits
        print(f"\nStarting with {len(initial)} initial subreddits: {initial}")
        
        for subreddit_name in initial:
            self.discovered_subreddits.add(subreddit_name.lower())
        
        print(f"\nDiscovering new subreddits (quota: {self.config.scouting.discovery_quota}, max: {self.config.scouting.max_subreddits})...")
        
        for subreddit_name in tqdm(initial, desc="Scanning initial subreddits"):
            if len(self.discovered_subreddits) >= self.config.scouting.max_subreddits:
                break
                
            self._discover_from_subreddit(subreddit_name)
            time.sleep(0.5)
        
        final_subreddits = list(self.discovered_subreddits)[:self.config.scouting.max_subreddits]
        
        print(f"\n✓ Scouting complete!")
        print(f"  Total discovered subreddits: {len(final_subreddits)}")
        
        self._save_discovered_subreddits(final_subreddits)
        
        return final_subreddits
    
    def _discover_from_subreddit(self, subreddit_name: str):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            users_checked = 0
            discovered_count = 0
            
            for post in subreddit.hot(limit=50):
                if len(self.discovered_subreddits) >= self.config.scouting.max_subreddits:
                    break
                
                if post.score > self.config.scouting.min_post_upvotes:
                    if users_checked >= self.config.scouting.users_per_subreddit:
                        break
                    
                    new_subs = self._check_user(post.author)
                    discovered_count += new_subs
                    users_checked += 1
                    
                    try:
                        post.comments.replace_more(limit=5)
                        for comment in post.comments.list()[:20]:
                            if len(self.discovered_subreddits) >= self.config.scouting.max_subreddits:
                                break
                            if users_checked >= self.config.scouting.users_per_subreddit:
                                break
                                
                            if comment.score > self.config.scouting.min_comment_upvotes:
                                new_subs = self._check_user(comment.author)
                                discovered_count += new_subs
                                users_checked += 1
                    except Exception:
                        pass
                    
                time.sleep(0.1)
                
        except Exception as e:
            print(f"\nError processing r/{subreddit_name}: {e}")
    
    def _check_user(self, author) -> int:
        if author is None or author.name == "[deleted]":
            return 0
        
        try:
            discovered_before = len(self.discovered_subreddits)
            
            for comment in author.comments.new(limit=self.config.scouting.discovery_quota):
                if len(self.discovered_subreddits) >= self.config.scouting.max_subreddits:
                    break
                    
                try:
                    subreddit_name = comment.subreddit.display_name.lower()
                    if subreddit_name not in self.discovered_subreddits:
                        self.discovered_subreddits.add(subreddit_name)
                        self.user_subreddit_map[author.name].add(subreddit_name)
                except Exception:
                    pass
            
            for post in author.submissions.new(limit=self.config.scouting.discovery_quota):
                if len(self.discovered_subreddits) >= self.config.scouting.max_subreddits:
                    break
                    
                try:
                    subreddit_name = post.subreddit.display_name.lower()
                    if subreddit_name not in self.discovered_subreddits:
                        self.discovered_subreddits.add(subreddit_name)
                        self.user_subreddit_map[author.name].add(subreddit_name)
                except Exception:
                    pass
            
            return len(self.discovered_subreddits) - discovered_before
            
        except Exception:
            return 0
    
    def _save_discovered_subreddits(self, subreddits: List[str]):
        os.makedirs(self.config.data_dir, exist_ok=True)
        
        output_file = os.path.join(self.config.data_dir, "discovered_subreddits.json")
        with open(output_file, 'w') as f:
            json.dump({
                "subreddits": subreddits,
                "count": len(subreddits),
            }, f, indent=2)
        
        print(f"  Saved to: {output_file}")
