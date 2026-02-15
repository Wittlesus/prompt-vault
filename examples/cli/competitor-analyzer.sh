#!/bin/bash
# Competitor Analyzer CLI Wrapper
# Analyzes competitor websites and generates SWOT analysis
#
# Usage:
#   ./competitor-analyzer.sh "https://competitor.com" "Your Product"
#
# Example:
#   ./competitor-analyzer.sh "https://vercel.com" "LaunchFast"

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/../python/competitor_analyzer.py"

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable not set"
    echo "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Check if arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: ./competitor-analyzer.sh <competitor_url> <your_product_name>"
    echo ""
    echo "Example:"
    echo "  ./competitor-analyzer.sh \"https://vercel.com\" \"LaunchFast\""
    exit 1
fi

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "ERROR: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed"
    echo "Install it with: apt-get install python3 (Ubuntu) or brew install python3 (Mac)"
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "ERROR: anthropic package not installed"
    echo "Install it with: pip install anthropic requests beautifulsoup4"
    exit 1
fi

if ! python3 -c "import requests" 2>/dev/null; then
    echo "ERROR: requests package not installed"
    echo "Install it with: pip install requests beautifulsoup4"
    exit 1
fi

if ! python3 -c "import bs4" 2>/dev/null; then
    echo "ERROR: beautifulsoup4 package not installed"
    echo "Install it with: pip install beautifulsoup4"
    exit 1
fi

# Run the Python script
python3 "$PYTHON_SCRIPT" "$1" "$2"
