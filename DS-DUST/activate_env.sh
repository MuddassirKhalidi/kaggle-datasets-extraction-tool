#!/bin/bash
# Activation script for DS-DUST virtual environment

echo "🚀 Activating DS-DUST virtual environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run the setup commands first."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "Available commands:"
echo "  python setup_kaggle_auth.py    - Set up Kaggle API authentication"
echo "  python test_kaggle_api.py      - Run Kaggle API tests"
echo "  jupyter notebook               - Start Jupyter notebook"
echo ""
echo "To deactivate, run: deactivate"
echo ""
