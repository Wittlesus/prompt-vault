#!/bin/bash
# Content Pipeline CLI Wrapper
# Generates full content: outline → draft → SEO → social posts
#
# Usage:
#   ./content-pipeline.sh "Your topic here"
#
# Example:
#   ./content-pipeline.sh "How to build a SaaS in 2026"

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/../python/content_pipeline.py"

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable not set"
    echo "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Check if topic argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./content-pipeline.sh \"Your topic here\""
    echo "Example: ./content-pipeline.sh \"How to build a SaaS in 2026\""
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

# Check if anthropic package is installed
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "ERROR: anthropic package not installed"
    echo "Install it with: pip install anthropic"
    exit 1
fi

# Run the Python script
python3 "$PYTHON_SCRIPT" "$1"
