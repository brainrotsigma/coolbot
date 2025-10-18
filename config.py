import os
from dataclasses import dataclass
from typing import List


@dataclass
class ScoutingConfig:
    initial_subreddits: List[str]
    min_post_upvotes: int = 2
    min_comment_upvotes: int = 1
    discovery_quota: int = 15
    max_subreddits: int = 50
    users_per_subreddit: int = 100


@dataclass
class ScrapingConfig:
    target_posts_per_subreddit: int = 100000
    target_comments_per_subreddit: int = 100000
    batch_size: int = 100
    max_retries: int = 3


@dataclass
class TrainingConfig:
    model_name: str = "gpt2"
    num_parameters: int = 100_000_000
    batch_size: int = 8
    learning_rate: float = 5e-5
    num_epochs: int = 3
    max_length: int = 512
    warmup_steps: int = 500
    save_steps: int = 1000
    output_dir: str = "models/jason"


@dataclass
class JasonConfig:
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str = "Jason/1.0"
    scouting: ScoutingConfig = None
    scraping: ScrapingConfig = None
    training: TrainingConfig = None
    data_dir: str = "data"
    
    def __post_init__(self):
        if self.scouting is None:
            self.scouting = ScoutingConfig(
                initial_subreddits=[
                    "AskReddit",
                    "todayilearned",
                    "science",
                    "technology",
                    "programming",
                    "MachineLearning",
                    "datascience",
                    "Python",
                ]
            )
        if self.scraping is None:
            self.scraping = ScrapingConfig()
        if self.training is None:
            self.training = TrainingConfig()


def load_config_from_env() -> JasonConfig:
    from dotenv import load_dotenv
    load_dotenv()
    
    return JasonConfig(
        reddit_client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        reddit_client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
        reddit_user_agent=os.getenv("REDDIT_USER_AGENT", "Jason/1.0"),
    )
