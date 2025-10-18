#!/bin/bash

echo "======================================"
echo "Jason Quick Start Setup"
echo "======================================"
echo ""

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please edit .env and add your Reddit API credentials:"
    echo "   - REDDIT_CLIENT_ID"
    echo "   - REDDIT_CLIENT_SECRET"
    echo ""
    echo "Get your credentials at: https://www.reddit.com/prefs/apps"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"
echo ""

echo "Installing dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Reddit API credentials"
echo "2. Run: python3 jason.py"
echo ""
echo "For specific phases, use:"
echo "  python3 jason.py --start-phase 1 --end-phase 1  # Scouting only"
echo "  python3 jason.py --start-phase 2 --end-phase 2  # Scraping only"
echo "  python3 jason.py --start-phase 3 --end-phase 3  # Training only"
echo "  python3 jason.py --start-phase 4 --end-phase 4  # Finalizing only"
echo ""
