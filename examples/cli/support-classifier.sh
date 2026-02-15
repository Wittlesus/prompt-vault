#!/bin/bash
# Support Classifier CLI Wrapper
# Classifies support emails and drafts responses
#
# Usage:
#   ./support-classifier.sh email.txt
#   cat email.txt | ./support-classifier.sh -
#
# Example:
#   ./support-classifier.sh customer_email.txt

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/../python/support_classifier.py"

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable not set"
    echo "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./support-classifier.sh <email_file>"
    echo "       ./support-classifier.sh -    (read from stdin)"
    echo ""
    echo "Examples:"
    echo "  ./support-classifier.sh customer_email.txt"
    echo "  cat email.txt | ./support-classifier.sh -"
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
if [ "$1" = "-" ]; then
    python3 "$PYTHON_SCRIPT" -
else
    python3 "$PYTHON_SCRIPT" "$1"
fi
