from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jason-reddit-scraper",
    version="1.0.0",
    author="Jason",
    description="Reddit scraping and training system with 4 phases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "praw>=7.7.0",
        "prawcore>=2.3.0",
        "requests>=2.31.0",
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "tqdm>=4.65.0",
        "python-dotenv>=1.0.0",
        "datasets>=2.14.0",
        "accelerate>=0.20.0",
    ],
    entry_points={
        "console_scripts": [
            "jason=jason:main",
        ],
    },
)
