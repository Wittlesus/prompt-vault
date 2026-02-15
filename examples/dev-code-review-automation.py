#!/usr/bin/env python3
"""
Automated Code Review Workflow
Run AI-powered code review on git diffs before committing.

Usage:
    # Review staged changes
    python dev-code-review-automation.py

    # Review specific commit
    python dev-code-review-automation.py --commit abc123

Requirements:
    pip install anthropic gitpython
"""

import os
import subprocess
import argparse
from anthropic import Anthropic

def get_git_diff(commit=None):
    """Get git diff for review."""
    if commit:
        cmd = ["git", "show", commit]
    else:
        cmd = ["git", "diff", "--staged"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def review_code(diff_content):
    """Run AI code review on the diff."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""You are a senior software engineer performing a code review. Analyze this git diff:

```diff
{diff_content}
```

Review checklist:
1. **Bugs & Logic Errors**: Any obvious bugs, off-by-one errors, null pointer risks?
2. **Security**: SQL injection, XSS, auth bypasses, secrets in code?
3. **Performance**: N+1 queries, unnecessary loops, memory leaks?
4. **Readability**: Confusing variable names, missing comments on complex logic?
5. **Error Handling**: Missing try/catch, unhandled edge cases?
6. **Testing**: Does this need tests? What edge cases are uncovered?

Format:
- If no issues: "✅ LGTM - No critical issues found."
- If issues found: List each issue with severity (🔴 Critical, 🟡 Warning, 🔵 Suggestion) and line reference.

Be specific. Reference actual code from the diff."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated code review")
    parser.add_argument("--commit", help="Specific commit hash to review")
    args = parser.parse_args()

    print("🔍 Running AI code review...")
    print("=" * 70)

    diff = get_git_diff(args.commit)

    if not diff.strip():
        print("No changes to review.")
        exit(0)

    review = review_code(diff)

    print(review)
    print("=" * 70)
