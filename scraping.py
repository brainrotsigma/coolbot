import praw
import time
import json
import os
from typing import List, Dict, Any
from tqdm import tqdm
from datetime import datetime

from config import JasonConfig


class RedditScraper:
    def __init__(self, config: JasonConfig):
        self.config = config
        self.reddit = praw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent,
        )
        self.scraped_data: List[Dict[str, Any]] = []
        
    def scrape(self, subreddits: List[str]) -> str:
        print("\n" + "=" * 60)
        print("PHASE 2: SCRAPING")
        print("=" * 60)
        print(f"\nScraping {len(subreddits)} subreddits...")
        print(f"Target: ~{self.config.scraping.target_posts_per_subreddit:,} posts + {self.config.scraping.target_comments_per_subreddit:,} comments per subreddit")
        
        os.makedirs(self.config.data_dir, exist_ok=True)
        output_file = os.path.join(self.config.data_dir, "scraped_data.jsonl")
        
        total_posts = 0
        total_comments = 0
        
        with open(output_file, 'w') as f:
            for subreddit_name in tqdm(subreddits, desc="Scraping subreddits"):
                posts, comments = self._scrape_subreddit(subreddit_name, f)
                total_posts += posts
                total_comments += comments
                time.sleep(1)
        
        print(f"\n✓ Scraping complete!")
        print(f"  Total posts: {total_posts:,}")
        print(f"  Total comments: {total_comments:,}")
        print(f"  Total items: {total_posts + total_comments:,}")
        print(f"  Saved to: {output_file}")
        
        return output_file
    
    def _scrape_subreddit(self, subreddit_name: str, file_handle) -> tuple:
        posts_count = 0
        comments_count = 0
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            posts_target = self.config.scraping.target_posts_per_subreddit
            comments_target = self.config.scraping.target_comments_per_subreddit
            
            time_filters = ['all', 'year', 'month']
            sort_methods = ['hot', 'top', 'new']
            
            for sort_method in sort_methods:
                if posts_count >= posts_target and comments_count >= comments_target:
                    break
                
                if sort_method == 'top':
                    for time_filter in time_filters:
                        if posts_count >= posts_target and comments_count >= comments_target:
                            break
                        
                        try:
                            posts = subreddit.top(time_filter=time_filter, limit=None)
                            p, c = self._process_posts(posts, subreddit_name, file_handle, posts_target, comments_target, posts_count, comments_count)
                            posts_count += p
                            comments_count += c
                        except Exception:
                            pass
                        
                        time.sleep(0.5)
                else:
                    try:
                        if sort_method == 'hot':
                            posts = subreddit.hot(limit=None)
                        elif sort_method == 'new':
                            posts = subreddit.new(limit=None)
                        else:
                            continue
                        
                        p, c = self._process_posts(posts, subreddit_name, file_handle, posts_target, comments_target, posts_count, comments_count)
                        posts_count += p
                        comments_count += c
                    except Exception:
                        pass
                    
                    time.sleep(0.5)
                    
        except Exception as e:
            pass
        
        return posts_count, comments_count
    
    def _process_posts(self, posts, subreddit_name: str, file_handle, posts_target: int, comments_target: int, current_posts: int, current_comments: int) -> tuple:
        posts_added = 0
        comments_added = 0
        
        try:
            for post in posts:
                if current_posts + posts_added >= posts_target and current_comments + comments_added >= comments_target:
                    break
                
                if post.score > self.config.scouting.min_post_upvotes:
                    if current_posts + posts_added < posts_target:
                        post_data = {
                            "type": "post",
                            "subreddit": subreddit_name,
                            "id": post.id,
                            "title": post.title,
                            "text": post.selftext,
                            "score": post.score,
                            "created_utc": post.created_utc,
                            "num_comments": post.num_comments,
                            "author": str(post.author) if post.author else "[deleted]",
                        }
                        file_handle.write(json.dumps(post_data) + '\n')
                        posts_added += 1
                    
                    if current_comments + comments_added < comments_target:
                        try:
                            post.comments.replace_more(limit=0)
                            for comment in post.comments.list():
                                if current_comments + comments_added >= comments_target:
                                    break
                                
                                if comment.score > self.config.scouting.min_comment_upvotes:
                                    comment_data = {
                                        "type": "comment",
                                        "subreddit": subreddit_name,
                                        "id": comment.id,
                                        "post_id": post.id,
                                        "text": comment.body,
                                        "score": comment.score,
                                        "created_utc": comment.created_utc,
                                        "author": str(comment.author) if comment.author else "[deleted]",
                                    }
                                    file_handle.write(json.dumps(comment_data) + '\n')
                                    comments_added += 1
                        except Exception:
                            pass
                
                time.sleep(0.1)
                
        except Exception:
            pass
        
        return posts_added, comments_added
