# Jason - Project Overview

## What is Jason?

Jason is a complete, production-ready Reddit scraping and machine learning training system. It automates the entire pipeline from discovering subreddits to training a language model.

## Key Features

✅ **4-Phase Architecture**: Modular design allows running phases independently
✅ **Smart Discovery**: Finds relevant subreddits through user activity analysis  
✅ **Quality Filtering**: Only collects high-quality content (>2 upvotes for posts, >1 for comments)
✅ **Massive Scale**: Targets ~100,000 items per subreddit across up to 50 subreddits
✅ **ML Training**: Trains a GPT-2 model with ~100M parameters
✅ **Progress Tracking**: Real-time progress bars and detailed logging
✅ **Comprehensive Reports**: Generates detailed JSON reports with statistics

## The Four Phases

### 1. Scouting 🔍
**Goal**: Discover interesting subreddits

**Process**:
- Start with 8 predefined subreddits
- Find quality posts/comments (based on upvotes)
- Check user profiles to discover more subreddits
- Discover up to 15 new subreddits per user
- Stop at 50 total subreddits

**Output**: `data/discovered_subreddits.json`

### 2. Scraping 📊
**Goal**: Collect massive amounts of Reddit data

**Process**:
- Scrape discovered subreddits systematically
- Collect ~100,000 posts per subreddit
- Collect ~100,000 comments per subreddit
- Use multiple sorting methods (hot, top, new)
- Apply quality filters

**Output**: `data/scraped_data.jsonl` (1-5 GB)

### 3. Training 🤖
**Goal**: Train a language model on Reddit data

**Process**:
- Load and preprocess scraped data
- Initialize GPT-2 architecture (~100M parameters)
- Train for 3 epochs with AdamW optimizer
- Save checkpoints every 1000 steps
- Generate final model

**Output**: `models/jason/` (2-3 GB)

### 4. Finalizing 📄
**Goal**: Generate comprehensive reports

**Process**:
- Analyze all collected data
- Count posts, comments, subreddits
- Calculate model statistics
- Create detailed execution report

**Output**: `data/jason_report.json`

## Quick Start

```bash
# 1. Setup
./quick_start.sh

# 2. Configure Reddit API credentials
nano .env  # Add your credentials

# 3. Run Jason
python3 jason.py
```

## Configuration

All parameters are configurable in `config.py`:

```python
# Scouting parameters
initial_subreddits = [...]
min_post_upvotes = 2
min_comment_upvotes = 1
discovery_quota = 15
max_subreddits = 50

# Scraping parameters
target_posts_per_subreddit = 100000
target_comments_per_subreddit = 100000

# Training parameters
num_parameters = 100_000_000
batch_size = 8
learning_rate = 5e-5
num_epochs = 3
```

## Usage Examples

### Run Everything
```bash
python3 jason.py
```

### Run Specific Phases
```bash
# Scouting only
python3 jason.py --start-phase 1 --end-phase 1

# Scraping only (after scouting)
python3 jason.py --start-phase 2 --end-phase 2

# Training only (after scraping)
python3 jason.py --start-phase 3 --end-phase 3

# Finalizing only
python3 jason.py --start-phase 4 --end-phase 4
```

### Programmatic Usage
```python
from jason import Jason
from config import JasonConfig

config = JasonConfig(
    reddit_client_id="your_id",
    reddit_client_secret="your_secret",
)

jason = Jason(config)
jason.run()
```

## Expected Results

### Data Volume
- **Subreddits**: 50 (configurable)
- **Posts**: ~5 million (50 subreddits × 100K each)
- **Comments**: ~5 million (50 subreddits × 100K each)
- **Total Items**: ~10 million
- **Data Size**: 3-7 GB

### Model
- **Architecture**: GPT-2
- **Parameters**: ~100 million
- **Training Time**: 6-24 hours (GPU-dependent)
- **Model Size**: ~400 MB

### Timeline
- **Scouting**: 15-30 minutes
- **Scraping**: 4-12 hours
- **Training**: 6-24 hours
- **Finalizing**: <1 minute
- **Total**: ~12-36 hours

## Technical Details

### Dependencies
- `praw` - Reddit API wrapper
- `torch` - Deep learning framework
- `transformers` - Pre-trained models and tokenizers
- `tqdm` - Progress bars
- `python-dotenv` - Environment variables

### Hardware Requirements
- **CPU**: Multi-core recommended
- **RAM**: 8GB minimum, 16GB+ recommended
- **GPU**: 8GB+ VRAM for training (optional but recommended)
- **Storage**: 10GB+ free space

### Rate Limiting
- Built-in delays to respect Reddit API limits
- Automatic retry on rate limit errors
- ~60 requests per minute (Reddit's limit)

## File Structure

```
jason-reddit-scraper/
├── jason.py              # Main entry point
├── config.py             # Configuration
├── scouting.py          # Phase 1 implementation
├── scraping.py          # Phase 2 implementation
├── training.py          # Phase 3 implementation
├── finalizing.py        # Phase 4 implementation
├── requirements.txt     # Dependencies
├── README.md            # Main documentation
├── USAGE.md            # Detailed usage guide
├── OVERVIEW.md         # This file
├── .env.example        # Configuration template
├── .gitignore          # Git ignore rules
├── setup.py            # Package setup
├── quick_start.sh      # Setup script
├── example_usage.py    # Usage examples
├── validate.py         # Validation script
└── test_structure.py   # Structure tests
```

## Data Format

### Scraped Data (JSONL)

Each line is a JSON object:

```json
{
  "type": "post",
  "subreddit": "AskReddit",
  "id": "abc123",
  "title": "What's your favorite...",
  "text": "I'm curious to know...",
  "score": 150,
  "created_utc": 1234567890,
  "num_comments": 42,
  "author": "username"
}
```

```json
{
  "type": "comment",
  "subreddit": "AskReddit",
  "id": "def456",
  "post_id": "abc123",
  "text": "I really like...",
  "score": 25,
  "created_utc": 1234567891,
  "author": "username"
}
```

## Use Cases

1. **Research**: Study Reddit communities and discourse patterns
2. **ML Training**: Train language models on conversational data
3. **Data Analysis**: Analyze trends and topics across subreddits
4. **Bot Development**: Create Reddit bots with trained models
5. **Content Generation**: Generate Reddit-style text

## Best Practices

1. **Start Small**: Test with fewer subreddits first
2. **Monitor Progress**: Watch console output and logs
3. **Check Disk Space**: Ensure adequate storage before starting
4. **Use GPU**: Training is much faster with GPU
5. **Respect Reddit**: Follow API guidelines and rate limits

## Troubleshooting

### Common Issues

**"No module named 'praw'"**
→ Run: `pip install -r requirements.txt`

**"REDDIT_CLIENT_ID not set"**
→ Create `.env` file with your credentials

**"CUDA out of memory"**
→ Reduce `batch_size` in config.py

**Rate limit exceeded**
→ Built-in delays should prevent this, but if it happens, the script will retry

### Getting Help

1. Check console output for errors
2. Review `USAGE.md` for detailed instructions
3. Run `python3 validate.py` to check setup
4. Check Reddit API status
5. Review error messages in console

## Validation

Run validation before starting:

```bash
python3 validate.py
```

This checks:
- Python syntax in all files
- File structure
- Configuration completeness
- Required dependencies
- Phase implementations

## Future Enhancements

Possible improvements:
- Multi-threading for faster scraping
- Database storage instead of JSONL
- Real-time monitoring dashboard
- Model serving API
- Scheduled automatic runs
- Support for other social media platforms

## License

This project is provided as-is for educational and research purposes.

## Disclaimer

⚠️ **Important**: 
- Respect Reddit's Terms of Service
- Use responsibly and ethically
- Follow API usage guidelines
- Comply with data privacy regulations
- This is for research and educational purposes only

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Credits

Built with:
- PRAW (Python Reddit API Wrapper)
- PyTorch
- Hugging Face Transformers
- Python standard library

---

**Ready to get started?**

Run: `./quick_start.sh` or see `USAGE.md` for detailed instructions.
