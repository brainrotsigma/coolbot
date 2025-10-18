import os
import json
from datetime import datetime
from typing import Dict, Any

from config import JasonConfig


class Finalizer:
    def __init__(self, config: JasonConfig):
        self.config = config
        
    def finalize(self, subreddits: list, data_file: str, model_dir: str) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("PHASE 4: FINALIZING")
        print("=" * 60)
        
        print("\nGenerating final report...")
        
        report = self._generate_report(subreddits, data_file, model_dir)
        
        report_file = os.path.join(self.config.data_dir, "jason_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'=' * 60}")
        print("JASON EXECUTION COMPLETE")
        print(f"{'=' * 60}")
        print(f"\n📊 Final Statistics:")
        print(f"  Subreddits discovered: {report['statistics']['subreddits_count']}")
        print(f"  Total posts scraped: {report['statistics']['posts_count']:,}")
        print(f"  Total comments scraped: {report['statistics']['comments_count']:,}")
        print(f"  Total items: {report['statistics']['total_items']:,}")
        print(f"  Model parameters: {report['model']['parameters']:,}")
        print(f"  Model location: {report['model']['location']}")
        print(f"\n📄 Report saved to: {report_file}")
        print(f"\n✨ Jason has completed all phases successfully!")
        
        return report
    
    def _generate_report(self, subreddits: list, data_file: str, model_dir: str) -> Dict[str, Any]:
        posts_count = 0
        comments_count = 0
        
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                for line in f:
                    try:
                        item = json.loads(line)
                        if item["type"] == "post":
                            posts_count += 1
                        elif item["type"] == "comment":
                            comments_count += 1
                    except Exception:
                        pass
        
        model_params = 0
        if os.path.exists(os.path.join(model_dir, "config.json")):
            with open(os.path.join(model_dir, "config.json"), 'r') as f:
                config_data = json.load(f)
                n_layer = config_data.get("n_layer", 0)
                n_embd = config_data.get("n_embd", 0)
                vocab_size = config_data.get("vocab_size", 0)
                if n_layer and n_embd and vocab_size:
                    model_params = self._estimate_params(n_layer, n_embd, vocab_size)
        
        report = {
            "jason_version": "1.0",
            "completed_at": datetime.utcnow().isoformat(),
            "phases": {
                "phase_1_scouting": "completed",
                "phase_2_scraping": "completed",
                "phase_3_training": "completed",
                "phase_4_finalizing": "completed",
            },
            "statistics": {
                "subreddits_count": len(subreddits),
                "posts_count": posts_count,
                "comments_count": comments_count,
                "total_items": posts_count + comments_count,
            },
            "subreddits": subreddits,
            "model": {
                "location": model_dir,
                "parameters": model_params,
                "type": "GPT2",
            },
            "data": {
                "scraped_data": data_file,
                "data_directory": self.config.data_dir,
            },
            "config": {
                "min_post_upvotes": self.config.scouting.min_post_upvotes,
                "min_comment_upvotes": self.config.scouting.min_comment_upvotes,
                "discovery_quota": self.config.scouting.discovery_quota,
                "max_subreddits": self.config.scouting.max_subreddits,
                "target_posts_per_subreddit": self.config.scraping.target_posts_per_subreddit,
                "target_comments_per_subreddit": self.config.scraping.target_comments_per_subreddit,
            }
        }
        
        return report
    
    def _estimate_params(self, n_layer: int, n_embd: int, vocab_size: int) -> int:
        params = vocab_size * n_embd
        params += n_embd
        params += n_layer * (4 * n_embd * n_embd + 5 * n_embd)
        params += n_embd * vocab_size
        return params
