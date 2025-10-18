# Jason - Reddit Scraping & Training System

Jason is a comprehensive Reddit scraping and machine learning training system that operates in four distinct phases: Scouting, Scraping, Training, and Finalizing.

## Overview

Jason automates the process of:
1. **Scouting** - Discovering subreddits by analyzing user activity
2. **Scraping** - Collecting posts and comments from discovered subreddits
3. **Training** - Training a GPT-2 based language model (~100M parameters)
4. **Finalizing** - Generating comprehensive reports and statistics

## Features

- 🔍 **Smart Subreddit Discovery**: Starts with predefined subreddits and discovers new ones by analyzing user activity
- 📊 **Quality Filtering**: Only collects posts with >2 upvotes and comments with >1 upvote
- 🎯 **Configurable Targets**: Aims to scrape ~100,000 posts and comments per subreddit
- 🤖 **Model Training**: Trains a GPT-2 based model with approximately 100M parameters
- 📈 **Progress Tracking**: Real-time progress bars and detailed logging
- 💾 **Checkpoint System**: Saves model checkpoints during training
- 📄 **Comprehensive Reports**: Generates detailed JSON reports of all activities

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd coolbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Reddit API credentials:
```bash
cp .env.example .env
```

Edit `.env` and add your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=Jason/1.0
```

### Getting Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Fill in the required fields
5. Copy the client ID (under the app name) and client secret

## Usage

### Run All Phases

```bash
python jason.py
```

### Run Specific Phases

Run only scouting:
```bash
python jason.py --start-phase 1 --end-phase 1
```

Run scraping and training:
```bash
python jason.py --start-phase 2 --end-phase 3
```

Run only training (if data already exists):
```bash
python jason.py --start-phase 3 --end-phase 3
```

## Configuration

Default configuration in `config.py`:

### Scouting Config
- **Initial Subreddits**: 8 predefined subreddits (AskReddit, todayilearned, etc.)
- **Min Post Upvotes**: 2
- **Min Comment Upvotes**: 1
- **Discovery Quota**: 15 subreddits per user
- **Max Subreddits**: 50 total
- **Users Per Subreddit**: 100

### Scraping Config
- **Target Posts Per Subreddit**: 100,000
- **Target Comments Per Subreddit**: 100,000
- **Batch Size**: 100
- **Max Retries**: 3

### Training Config
- **Base Model**: GPT-2
- **Target Parameters**: ~100,000,000
- **Batch Size**: 8
- **Learning Rate**: 5e-5
- **Epochs**: 3
- **Max Length**: 512 tokens
- **Warmup Steps**: 500
- **Save Steps**: 1000

## Output Structure

```
data/
├── discovered_subreddits.json  # List of discovered subreddits
├── scraped_data.jsonl          # All scraped posts and comments
└── jason_report.json           # Final execution report

models/
└── jason/
    ├── config.json             # Model configuration
    ├── pytorch_model.bin       # Trained model weights
    ├── tokenizer_config.json   # Tokenizer configuration
    └── checkpoint-*/           # Training checkpoints
```

## Phases Explained

### Phase 1: Scouting
- Starts with 8 predefined subreddits
- Analyzes users who post quality content (>2 upvotes for posts, >1 for comments)
- Discovers new subreddits from user activity
- Quota: 15 subreddits per user, max 50 total subreddits

### Phase 2: Scraping
- Scrapes posts and comments from all discovered subreddits
- Target: ~100,000 posts + ~100,000 comments per subreddit
- Uses multiple sorting methods (hot, top, new) and time filters
- Respects Reddit's rate limits with built-in delays
- Outputs to JSONL format for efficient processing

### Phase 3: Training
- Loads scraped data and prepares it for training
- Initializes GPT-2 model with ~100M parameters
- Trains on Reddit posts and comments
- Saves checkpoints every 1000 steps
- Uses AdamW optimizer with linear warmup schedule

### Phase 4: Finalizing
- Generates comprehensive statistics
- Creates detailed execution report
- Summarizes all collected data
- Reports model information and location

## Data Format

### Scraped Data (JSONL)

Posts:
```json
{
  "type": "post",
  "subreddit": "AskReddit",
  "id": "abc123",
  "title": "Post title",
  "text": "Post content",
  "score": 150,
  "created_utc": 1234567890,
  "num_comments": 42,
  "author": "username"
}
```

Comments:
```json
{
  "type": "comment",
  "subreddit": "AskReddit",
  "id": "def456",
  "post_id": "abc123",
  "text": "Comment text",
  "score": 25,
  "created_utc": 1234567890,
  "author": "username"
}
```

## Hardware Requirements

- **CPU**: Multi-core processor recommended
- **RAM**: 8GB minimum, 16GB+ recommended
- **GPU**: CUDA-compatible GPU recommended for training (optional but faster)
- **Storage**: 10GB+ free space for data and models
- **Network**: Stable internet connection for Reddit API access

## Rate Limiting & Best Practices

- Built-in delays between API calls to respect Reddit's rate limits
- Uses PRAW (Python Reddit API Wrapper) for reliable API access
- Handles errors gracefully and continues processing
- Saves progress regularly to prevent data loss

## Troubleshooting

### "REDDIT_CLIENT_ID not set"
- Make sure you've created a `.env` file with your Reddit API credentials

### "Rate limit exceeded"
- The script includes delays, but you may need to reduce scraping speed
- Consider reducing `users_per_subreddit` or `target_posts_per_subreddit`

### "CUDA out of memory"
- Reduce `batch_size` in training config
- Use CPU training instead (slower but works with less memory)

### "No module named 'praw'"
- Run `pip install -r requirements.txt` to install dependencies

## License

This project is provided as-is for educational and research purposes.

## Disclaimer

- Respect Reddit's Terms of Service and API usage guidelines
- Be mindful of rate limits and server load
- Use responsibly and ethically
- This tool is for research and educational purposes only
- Always comply with data privacy regulations and Reddit's policies

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Architecture

```
jason.py          # Main entry point and orchestrator
├── config.py     # Configuration management
├── scouting.py   # Phase 1: Subreddit discovery
├── scraping.py   # Phase 2: Data collection
├── training.py   # Phase 3: Model training
└── finalizing.py # Phase 4: Report generation
```
