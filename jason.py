#!/usr/bin/env python3

import sys
import argparse
from typing import Optional

from config import load_config_from_env, JasonConfig
from scouting import SubredditScout
from scraping import RedditScraper
from training import ModelTrainer
from finalizing import Finalizer


class Jason:
    def __init__(self, config: Optional[JasonConfig] = None):
        if config is None:
            config = load_config_from_env()
        
        self.config = config
        self.validate_config()
        
    def validate_config(self):
        if not self.config.reddit_client_id:
            raise ValueError("REDDIT_CLIENT_ID not set. Please configure .env file.")
        if not self.config.reddit_client_secret:
            raise ValueError("REDDIT_CLIENT_SECRET not set. Please configure .env file.")
    
    def run(self, start_phase: int = 1, end_phase: int = 4):
        print("\n" + "=" * 60)
        print("🤖 JASON - Reddit Scraping & Training System")
        print("=" * 60)
        print(f"\nConfiguration:")
        print(f"  Initial subreddits: {len(self.config.scouting.initial_subreddits)}")
        print(f"  Max subreddits: {self.config.scouting.max_subreddits}")
        print(f"  Min post upvotes: {self.config.scouting.min_post_upvotes}")
        print(f"  Min comment upvotes: {self.config.scouting.min_comment_upvotes}")
        print(f"  Discovery quota per user: {self.config.scouting.discovery_quota}")
        print(f"  Target posts per subreddit: {self.config.scraping.target_posts_per_subreddit:,}")
        print(f"  Target comments per subreddit: {self.config.scraping.target_comments_per_subreddit:,}")
        print(f"  Target model parameters: ~{self.config.training.num_parameters:,}")
        
        subreddits = []
        data_file = ""
        model_dir = ""
        
        if start_phase <= 1 <= end_phase:
            scout = SubredditScout(self.config)
            subreddits = scout.scout()
        
        if start_phase <= 2 <= end_phase:
            if not subreddits:
                import json
                import os
                subreddit_file = os.path.join(self.config.data_dir, "discovered_subreddits.json")
                if os.path.exists(subreddit_file):
                    with open(subreddit_file, 'r') as f:
                        data = json.load(f)
                        subreddits = data.get("subreddits", [])
                else:
                    raise ValueError("No subreddits found. Please run phase 1 first.")
            
            scraper = RedditScraper(self.config)
            data_file = scraper.scrape(subreddits)
        
        if start_phase <= 3 <= end_phase:
            if not data_file:
                import os
                data_file = os.path.join(self.config.data_dir, "scraped_data.jsonl")
                if not os.path.exists(data_file):
                    raise ValueError("No scraped data found. Please run phase 2 first.")
            
            trainer = ModelTrainer(self.config)
            model_dir = trainer.train(data_file)
        
        if start_phase <= 4 <= end_phase:
            if not subreddits:
                import json
                import os
                subreddit_file = os.path.join(self.config.data_dir, "discovered_subreddits.json")
                if os.path.exists(subreddit_file):
                    with open(subreddit_file, 'r') as f:
                        data = json.load(f)
                        subreddits = data.get("subreddits", [])
            
            if not data_file:
                import os
                data_file = os.path.join(self.config.data_dir, "scraped_data.jsonl")
            
            if not model_dir:
                model_dir = self.config.training.output_dir
            
            finalizer = Finalizer(self.config)
            report = finalizer.finalize(subreddits, data_file, model_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Jason - Reddit Scraping & Training System"
    )
    parser.add_argument(
        "--start-phase",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Phase to start from (1=scouting, 2=scraping, 3=training, 4=finalizing)",
    )
    parser.add_argument(
        "--end-phase",
        type=int,
        default=4,
        choices=[1, 2, 3, 4],
        help="Phase to end at (1=scouting, 2=scraping, 3=training, 4=finalizing)",
    )
    
    args = parser.parse_args()
    
    if args.start_phase > args.end_phase:
        print("Error: start-phase must be <= end-phase")
        sys.exit(1)
    
    try:
        jason = Jason()
        jason.run(start_phase=args.start_phase, end_phase=args.end_phase)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
