"""
Jason - Reddit Scraping & Training System

A comprehensive Reddit scraping and machine learning training system
that operates in four distinct phases: Scouting, Scraping, Training, and Finalizing.
"""

__version__ = "1.0.0"
__author__ = "Jason"

from .jason import Jason
from .config import (
    JasonConfig,
    ScoutingConfig,
    ScrapingConfig,
    TrainingConfig,
    load_config_from_env,
)
from .scouting import SubredditScout
from .scraping import RedditScraper
from .training import ModelTrainer
from .finalizing import Finalizer

__all__ = [
    "Jason",
    "JasonConfig",
    "ScoutingConfig",
    "ScrapingConfig",
    "TrainingConfig",
    "load_config_from_env",
    "SubredditScout",
    "RedditScraper",
    "ModelTrainer",
    "Finalizer",
]
