#!/usr/bin/env python3

import sys

def test_imports():
    print("Testing imports...")
    
    try:
        from config import JasonConfig, ScoutingConfig, ScrapingConfig, TrainingConfig, load_config_from_env
        print("  ✓ config module imports successfully")
    except Exception as e:
        print(f"  ✗ config module import failed: {e}")
        return False
    
    try:
        from scouting import SubredditScout
        print("  ✓ scouting module imports successfully")
    except Exception as e:
        print(f"  ✗ scouting module import failed: {e}")
        return False
    
    try:
        from scraping import RedditScraper
        print("  ✓ scraping module imports successfully")
    except Exception as e:
        print(f"  ✗ scraping module import failed: {e}")
        return False
    
    try:
        from training import ModelTrainer, RedditDataset
        print("  ✓ training module imports successfully")
    except Exception as e:
        print(f"  ✗ training module import failed: {e}")
        return False
    
    try:
        from finalizing import Finalizer
        print("  ✓ finalizing module imports successfully")
    except Exception as e:
        print(f"  ✗ finalizing module import failed: {e}")
        return False
    
    try:
        from jason import Jason
        print("  ✓ jason module imports successfully")
    except Exception as e:
        print(f"  ✗ jason module import failed: {e}")
        return False
    
    return True


def test_config_creation():
    print("\nTesting configuration creation...")
    
    try:
        from config import JasonConfig, ScoutingConfig, ScrapingConfig, TrainingConfig
        
        scouting = ScoutingConfig(
            initial_subreddits=["test"],
            min_post_upvotes=2,
            min_comment_upvotes=1,
            discovery_quota=15,
            max_subreddits=50,
        )
        print("  ✓ ScoutingConfig created")
        
        scraping = ScrapingConfig(
            target_posts_per_subreddit=100000,
            target_comments_per_subreddit=100000,
        )
        print("  ✓ ScrapingConfig created")
        
        training = TrainingConfig(
            model_name="gpt2",
            num_parameters=100_000_000,
        )
        print("  ✓ TrainingConfig created")
        
        config = JasonConfig(
            reddit_client_id="test_id",
            reddit_client_secret="test_secret",
            scouting=scouting,
            scraping=scraping,
            training=training,
        )
        print("  ✓ JasonConfig created")
        
        assert config.scouting.max_subreddits == 50
        assert config.scraping.target_posts_per_subreddit == 100000
        assert config.training.num_parameters == 100_000_000
        print("  ✓ Configuration values correct")
        
        return True
    except Exception as e:
        print(f"  ✗ Configuration creation failed: {e}")
        return False


def test_class_instantiation():
    print("\nTesting class instantiation...")
    
    try:
        from config import JasonConfig
        from scouting import SubredditScout
        from scraping import RedditScraper
        from training import ModelTrainer
        from finalizing import Finalizer
        
        config = JasonConfig(
            reddit_client_id="test_id",
            reddit_client_secret="test_secret",
        )
        
        scout = SubredditScout(config)
        print("  ✓ SubredditScout instantiated")
        
        scraper = RedditScraper(config)
        print("  ✓ RedditScraper instantiated")
        
        trainer = ModelTrainer(config)
        print("  ✓ ModelTrainer instantiated")
        
        finalizer = Finalizer(config)
        print("  ✓ Finalizer instantiated")
        
        return True
    except Exception as e:
        print(f"  ✗ Class instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    print("\nTesting file structure...")
    import os
    
    required_files = [
        "jason.py",
        "config.py",
        "scouting.py",
        "scraping.py",
        "training.py",
        "finalizing.py",
        "__init__.py",
        "requirements.txt",
        "README.md",
        "USAGE.md",
        ".env.example",
        ".gitignore",
        "setup.py",
        "quick_start.sh",
        "example_usage.py",
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            all_exist = False
    
    return all_exist


def main():
    print("=" * 60)
    print("Jason Structure Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Config Creation", test_config_creation()))
    results.append(("Class Instantiation", test_class_instantiation()))
    results.append(("File Structure", test_file_structure()))
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
