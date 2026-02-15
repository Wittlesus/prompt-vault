#!/usr/bin/env python3
"""
Code Reviewer - Automated Code Review
Takes a git diff → reviews for bugs, security, performance → outputs structured feedback

Usage:
    python code_reviewer.py path/to/file.diff
    git diff | python code_reviewer.py -
    git diff main...feature-branch | python code_reviewer.py -

Requirements:
    pip install anthropic

Environment:
    ANTHROPIC_API_KEY - Your Anthropic API key
"""

import os
import sys
import anthropic
from typing import Dict, Any
import json

# Model to use for all API calls
MODEL = "claude-sonnet-4-5-20250929"

def create_client() -> anthropic.Anthropic:
    """Create and return an Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)

def read_diff(source: str) -> str:
    """Read diff content from file or stdin."""
    try:
        if source == "-":
            # Read from stdin
            diff_content = sys.stdin.read()
        else:
            # Read from file
            with open(source, 'r', encoding='utf-8') as f:
                diff_content = f.read()

        if not diff_content.strip():
            print("ERROR: Diff content is empty", file=sys.stderr)
            sys.exit(1)

        return diff_content

    except FileNotFoundError:
        print(f"ERROR: File not found: {source}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR reading diff: {e}", file=sys.stderr)
        sys.exit(1)

def analyze_diff(client: anthropic.Anthropic, diff_content: str) -> Dict[str, Any]:
    """Analyze the diff and provide a summary."""
    print(f"\n{'='*80}")
    print("STEP 1: Diff Analysis")
    print(f"{'='*80}\n")

    prompt = f"""Analyze this git diff and provide a structured summary:

DIFF:
{diff_content}

Provide a JSON response with:
{{
  "files_changed": number,
  "lines_added": number,
  "lines_removed": number,
  "languages": ["list", "of", "languages"],
  "change_type": "feature|bugfix|refactor|docs|test|config|other",
  "complexity": "low|medium|high",
  "risk_level": "low|medium|high",
  "summary": "one-sentence description of changes",
  "files": [
    {{"path": "file.js", "change_summary": "what changed in this file"}}
  ]
}}

Only output valid JSON, no other text."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis_text = message.content[0].text
        # Extract JSON from potential markdown code blocks
        if "```json" in analysis_text:
            analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
        elif "```" in analysis_text:
            analysis_text = analysis_text.split("```")[1].split("```")[0].strip()

        analysis = json.loads(analysis_text)

        print("Diff Summary:")
        print(json.dumps(analysis, indent=2))

        return analysis

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON response: {e}", file=sys.stderr)
        print(f"Raw response: {analysis_text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR analyzing diff: {e}", file=sys.stderr)
        sys.exit(1)

def review_bugs(client: anthropic.Anthropic, diff_content: str) -> str:
    """Review the code for potential bugs."""
    print(f"\n{'='*80}")
    print("STEP 2: Bug Detection")
    print(f"{'='*80}\n")

    prompt = f"""Review this code diff for potential bugs:

DIFF:
{diff_content}

Identify:
1. **Logical Errors**: Off-by-one errors, incorrect conditionals, wrong operators
2. **Null/Undefined Issues**: Missing null checks, potential undefined access
3. **Edge Cases**: Unhandled edge cases, boundary conditions
4. **Error Handling**: Missing try-catch, unhandled promise rejections
5. **Type Issues**: Type mismatches, incorrect type assumptions
6. **Race Conditions**: Async/await issues, concurrent access problems

For each issue found, provide:
- File and line reference
- Severity (critical|high|medium|low)
- Description of the bug
- Suggested fix

If no bugs found, say "No bugs detected" and explain why the code looks safe.

Format clearly with headers and bullet points."""

    try:
        print("Analyzing for bugs...\n")

        message = client.messages.create(
            model=MODEL,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        bugs = message.content[0].text
        print(bugs)
        return bugs

    except Exception as e:
        print(f"ERROR reviewing bugs: {e}", file=sys.stderr)
        sys.exit(1)

def review_security(client: anthropic.Anthropic, diff_content: str) -> str:
    """Review the code for security issues."""
    print(f"\n{'='*80}")
    print("STEP 3: Security Analysis")
    print(f"{'='*80}\n")

    prompt = f"""Review this code diff for security vulnerabilities:

DIFF:
{diff_content}

Check for:
1. **Injection Attacks**: SQL injection, XSS, command injection
2. **Authentication/Authorization**: Missing auth checks, privilege escalation
3. **Data Exposure**: Sensitive data in logs, insecure storage
4. **Cryptography**: Weak algorithms, hardcoded secrets, poor key management
5. **Input Validation**: Missing validation, insufficient sanitization
6. **API Security**: Missing rate limiting, insecure endpoints
7. **Dependencies**: Known vulnerable packages

For each issue found, provide:
- File and line reference
- Severity (critical|high|medium|low)
- Vulnerability type (OWASP category if applicable)
- Attack vector
- Recommended fix

If no security issues found, say "No security vulnerabilities detected" and explain the security posture.

Format clearly with headers and bullet points."""

    try:
        print("Analyzing for security issues...\n")

        message = client.messages.create(
            model=MODEL,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        security = message.content[0].text
        print(security)
        return security

    except Exception as e:
        print(f"ERROR reviewing security: {e}", file=sys.stderr)
        sys.exit(1)

def review_performance(client: anthropic.Anthropic, diff_content: str) -> str:
    """Review the code for performance issues."""
    print(f"\n{'='*80}")
    print("STEP 4: Performance Review")
    print(f"{'='*80}\n")

    prompt = f"""Review this code diff for performance issues:

DIFF:
{diff_content}

Check for:
1. **Algorithmic Complexity**: O(n²) where O(n) possible, nested loops
2. **Database Queries**: N+1 queries, missing indexes, inefficient joins
3. **Memory Usage**: Memory leaks, excessive allocations, large object retention
4. **Network Calls**: Unnecessary requests, missing caching, no connection pooling
5. **Rendering**: Unnecessary re-renders, missing memoization
6. **Bundle Size**: Large dependencies, unused code
7. **Resource Management**: Missing cleanup, unclosed connections

For each issue found, provide:
- File and line reference
- Impact (high|medium|low)
- Performance problem
- Suggested optimization

If performance looks good, say "No performance issues detected" and note positive patterns.

Format clearly with headers and bullet points."""

    try:
        print("Analyzing for performance issues...\n")

        message = client.messages.create(
            model=MODEL,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        performance = message.content[0].text
        print(performance)
        return performance

    except Exception as e:
        print(f"ERROR reviewing performance: {e}", file=sys.stderr)
        sys.exit(1)

def generate_summary(client: anthropic.Anthropic, analysis: Dict[str, Any], bugs: str, security: str, performance: str) -> str:
    """Generate final review summary and recommendation."""
    print(f"\n{'='*80}")
    print("STEP 5: Review Summary")
    print(f"{'='*80}\n")

    prompt = f"""Based on this code review, provide a final summary and recommendation:

DIFF ANALYSIS:
{json.dumps(analysis, indent=2)}

BUGS FOUND:
{bugs[:1000]}...

SECURITY ISSUES:
{security[:1000]}...

PERFORMANCE ISSUES:
{performance[:1000]}...

Provide:
1. **Overall Assessment**: APPROVED | APPROVED_WITH_COMMENTS | CHANGES_REQUESTED | BLOCKED
2. **Summary**: 2-3 sentence overview of the changes and review
3. **Critical Issues**: List any blocking issues (if any)
4. **Recommendations**: Top 3 actions before merging (if any)
5. **Positive Notes**: What was done well in this PR

Keep it concise and actionable."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        summary = message.content[0].text
        print(summary)
        return summary

    except Exception as e:
        print(f"ERROR generating summary: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main code review execution."""
    if len(sys.argv) < 2:
        print("Usage: python code_reviewer.py <diff_file>")
        print("       python code_reviewer.py -    (read from stdin)")
        print("\nExamples:")
        print("  git diff | python code_reviewer.py -")
        print("  git diff main...feature | python code_reviewer.py -")
        print("  python code_reviewer.py changes.diff")
        sys.exit(1)

    source = sys.argv[1]

    print(f"\n{'#'*80}")
    print("# AUTOMATED CODE REVIEW")
    print(f"{'#'*80}")

    # Initialize client
    client = create_client()

    # Read diff
    diff_content = read_diff(source)

    print(f"\nDiff size: {len(diff_content)} characters")

    # Execute review pipeline
    analysis = analyze_diff(client, diff_content)
    bugs = review_bugs(client, diff_content)
    security = review_security(client, diff_content)
    performance = review_performance(client, diff_content)
    summary = generate_summary(client, analysis, bugs, security, performance)

    print(f"\n{'#'*80}")
    print("# CODE REVIEW COMPLETE")
    print(f"{'#'*80}")
    print(f"\nRisk Level: {analysis['risk_level'].upper()}")
    print(f"Complexity: {analysis['complexity'].upper()}")
    print(f"\nReview complete. See detailed findings above.")

if __name__ == "__main__":
    main()
