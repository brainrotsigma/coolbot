#!/usr/bin/env python3

from config import JasonConfig, ScoutingConfig, ScrapingConfig, TrainingConfig
from jason import Jason


def example_basic_usage():
    print("Example 1: Basic usage with default config")
    print("=" * 60)
    
    jason = Jason()
    jason.run()


def example_custom_config():
    print("\nExample 2: Custom configuration")
    print("=" * 60)
    
    custom_scouting = ScoutingConfig(
        initial_subreddits=[
            "programming",
            "Python",
            "learnprogramming",
            "coding",
        ],
        min_post_upvotes=5,
        min_comment_upvotes=2,
        discovery_quota=10,
        max_subreddits=25,
        users_per_subreddit=50,
    )
    
    custom_scraping = ScrapingConfig(
        target_posts_per_subreddit=50000,
        target_comments_per_subreddit=50000,
        batch_size=100,
    )
    
    custom_training = TrainingConfig(
        model_name="gpt2",
        num_parameters=100_000_000,
        batch_size=4,
        learning_rate=3e-5,
        num_epochs=2,
    )
    
    config = JasonConfig(
        reddit_client_id="your_client_id",
        reddit_client_secret="your_client_secret",
        reddit_user_agent="Jason/1.0",
        scouting=custom_scouting,
        scraping=custom_scraping,
        training=custom_training,
        data_dir="custom_data",
    )
    
    jason = Jason(config)
    jason.run()


def example_phase_by_phase():
    print("\nExample 3: Running phases individually")
    print("=" * 60)
    
    jason = Jason()
    
    print("\n--- Running Phase 1: Scouting ---")
    jason.run(start_phase=1, end_phase=1)
    
    print("\n--- Running Phase 2: Scraping ---")
    jason.run(start_phase=2, end_phase=2)
    
    print("\n--- Running Phase 3: Training ---")
    jason.run(start_phase=3, end_phase=3)
    
    print("\n--- Running Phase 4: Finalizing ---")
    jason.run(start_phase=4, end_phase=4)


def example_skip_training():
    print("\nExample 4: Scouting and scraping only (no training)")
    print("=" * 60)
    
    jason = Jason()
    jason.run(start_phase=1, end_phase=2)


if __name__ == "__main__":
    print("Jason Usage Examples")
    print("=" * 60)
    print("\nThese are example usage patterns for Jason.")
    print("Uncomment the example you want to run.\n")
    
    example_basic_usage()
