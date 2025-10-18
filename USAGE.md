# Jason Usage Guide

## Quick Start

1. **Setup Reddit API Credentials**
   ```bash
   ./quick_start.sh
   ```
   Then edit `.env` with your Reddit API credentials.

2. **Run Jason**
   ```bash
   python3 jason.py
   ```

## Command Line Options

### Run All Phases (Default)
```bash
python3 jason.py
```
This will execute all four phases in sequence:
- Phase 1: Scouting
- Phase 2: Scraping  
- Phase 3: Training
- Phase 4: Finalizing

### Run Specific Phases

**Scouting Only**
```bash
python3 jason.py --start-phase 1 --end-phase 1
```

**Scraping Only** (requires completed scouting)
```bash
python3 jason.py --start-phase 2 --end-phase 2
```

**Training Only** (requires completed scraping)
```bash
python3 jason.py --start-phase 3 --end-phase 3
```

**Finalizing Only** (requires completed training)
```bash
python3 jason.py --start-phase 4 --end-phase 4
```

**Scouting + Scraping** (skip training)
```bash
python3 jason.py --start-phase 1 --end-phase 2
```

**Training + Finalizing** (if data already exists)
```bash
python3 jason.py --start-phase 3 --end-phase 4
```

## Understanding the Phases

### Phase 1: Scouting 🔍
**Purpose**: Discover subreddits by analyzing user activity

**What it does**:
- Starts with 8 predefined subreddits
- Scans posts with >2 upvotes and comments with >1 upvote
- Checks user profiles to discover more subreddits
- Discovers up to 15 new subreddits per user
- Maximum 50 total subreddits

**Output**: `data/discovered_subreddits.json`

**Duration**: 15-30 minutes (depending on Reddit API rate limits)

### Phase 2: Scraping 📊
**Purpose**: Collect posts and comments from discovered subreddits

**What it does**:
- Scrapes ~100,000 posts per subreddit
- Scrapes ~100,000 comments per subreddit
- Uses multiple sorting methods (hot, top, new)
- Respects rate limits with built-in delays
- Filters content based on upvote thresholds

**Output**: `data/scraped_data.jsonl`

**Duration**: Several hours to days (depending on number of subreddits and content availability)

**Expected data size**: 
- ~5-10 million items total (for 50 subreddits)
- File size: 1-5 GB (uncompressed JSONL)

### Phase 3: Training 🤖
**Purpose**: Train a GPT-2 based language model

**What it does**:
- Loads and preprocesses scraped data
- Initializes GPT-2 model with ~100M parameters
- Trains for 3 epochs
- Saves checkpoints every 1000 steps
- Uses AdamW optimizer with warmup

**Output**: `models/jason/` (model files and checkpoints)

**Duration**: Hours to days (depending on hardware)
- GPU (RTX 3090): ~6-12 hours
- GPU (GTX 1080): ~12-24 hours
- CPU: Several days

**Hardware requirements**:
- GPU with 8GB+ VRAM (recommended)
- 16GB+ RAM
- 10GB+ disk space

### Phase 4: Finalizing 📄
**Purpose**: Generate comprehensive reports

**What it does**:
- Analyzes all collected data
- Counts posts, comments, and subreddits
- Calculates model statistics
- Generates final report

**Output**: `data/jason_report.json`

**Duration**: < 1 minute

## Configuration

### Default Configuration

Edit `config.py` to change defaults:

```python
# Scouting
initial_subreddits = [
    "AskReddit", "todayilearned", "science", 
    "technology", "programming", "MachineLearning",
    "datascience", "Python"
]
min_post_upvotes = 2
min_comment_upvotes = 1
discovery_quota = 15
max_subreddits = 50
users_per_subreddit = 100

# Scraping
target_posts_per_subreddit = 100000
target_comments_per_subreddit = 100000

# Training
num_parameters = 100_000_000
batch_size = 8
learning_rate = 5e-5
num_epochs = 3
```

### Custom Configuration (Programmatic)

See `example_usage.py` for examples of custom configurations.

## Output Files

```
project/
├── data/
│   ├── discovered_subreddits.json  # Phase 1 output
│   ├── scraped_data.jsonl          # Phase 2 output
│   └── jason_report.json           # Phase 4 output
│
└── models/
    └── jason/
        ├── config.json              # Model config
        ├── pytorch_model.bin        # Model weights
        ├── tokenizer_config.json    # Tokenizer config
        ├── vocab.json               # Vocabulary
        ├── merges.txt               # BPE merges
        └── checkpoint-*/            # Training checkpoints
```

## Common Workflows

### Full Pipeline (Recommended for first run)
```bash
python3 jason.py
```

### Data Collection Only
```bash
python3 jason.py --start-phase 1 --end-phase 2
```
Useful if you want to:
- Inspect scraped data before training
- Train later on different hardware
- Export data to another system

### Re-train with Different Parameters
1. Keep existing scraped data
2. Modify `config.py` training parameters
3. Run:
```bash
python3 jason.py --start-phase 3 --end-phase 4
```

### Continue from Checkpoint
If training was interrupted:
1. Checkpoints are saved in `models/jason/checkpoint-*`
2. Modify `training.py` to load from checkpoint
3. Resume training from last checkpoint

## Tips & Best Practices

### Rate Limiting
- Reddit API has rate limits (60 requests/minute)
- Built-in delays help avoid hitting limits
- If you get rate limit errors, the script will retry
- Consider running during off-peak hours

### Disk Space
- Monitor disk space during scraping
- 100K items ≈ 100-200 MB (varies by content)
- Model checkpoints ≈ 400-500 MB each
- Keep at least 10GB free

### Memory Usage
**Scouting**: ~500 MB
**Scraping**: ~1-2 GB
**Training**: 
- GPU: 6-8 GB VRAM + 4-8 GB RAM
- CPU: 8-16 GB RAM

### GPU vs CPU Training
**With GPU (CUDA)**:
```bash
python3 jason.py --start-phase 3 --end-phase 4
```

**Force CPU only**:
```bash
CUDA_VISIBLE_DEVICES="" python3 jason.py --start-phase 3 --end-phase 4
```

Reduce batch size if you get out-of-memory errors:
- Edit `config.py`: `batch_size = 4` (or even 2)

## Troubleshooting

### No data collected
- Check Reddit API credentials in `.env`
- Verify subreddits are accessible (not private/banned)
- Check internet connection
- Review console output for specific errors

### Training fails
- Reduce batch size in `config.py`
- Check available disk space
- Verify scraped data file exists and is not empty
- Try CPU-only training if GPU has issues

### Process interrupted
- Each phase can be re-run independently
- Previous phase outputs are preserved
- Use `--start-phase` to resume from specific phase

## Advanced Usage

### Custom Subreddit List
Edit `config.py`:
```python
initial_subreddits = [
    "YourSubreddit1",
    "YourSubreddit2",
    # ... add more
]
```

### Adjust Quality Thresholds
Higher quality but less data:
```python
min_post_upvotes = 10
min_comment_upvotes = 5
```

Lower quality but more data:
```python
min_post_upvotes = 1
min_comment_upvotes = 0
```

### Smaller/Faster Training
```python
target_posts_per_subreddit = 10000
target_comments_per_subreddit = 10000
num_epochs = 1
batch_size = 16
```

### Larger Model
```python
num_parameters = 200_000_000
num_epochs = 5
```

## Getting Help

If you encounter issues:
1. Check console output for error messages
2. Review `data/jason_report.json` for statistics
3. Verify `.env` configuration
4. Check Reddit API status
5. Review troubleshooting section above

## Example Timeline

For a complete run with default settings:

| Phase | Duration | Output Size |
|-------|----------|-------------|
| Scouting | 15-30 min | ~5 KB |
| Scraping | 4-12 hours | 1-5 GB |
| Training | 6-24 hours | ~2 GB |
| Finalizing | <1 min | ~10 KB |
| **Total** | **~12-36 hours** | **~3-7 GB** |

*Actual times vary based on Reddit API responsiveness and hardware*
