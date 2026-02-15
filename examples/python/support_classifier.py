#!/usr/bin/env python3
"""
Support Email Classifier - Automated Support Triage
Takes a support email → categorizes → drafts response → suggests priority

Usage:
    python support_classifier.py "path/to/email.txt"
    echo "Email content here" | python support_classifier.py -

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

def read_email(source: str) -> str:
    """Read email content from file or stdin."""
    try:
        if source == "-":
            # Read from stdin
            email_content = sys.stdin.read()
        else:
            # Read from file
            with open(source, 'r', encoding='utf-8') as f:
                email_content = f.read()

        if not email_content.strip():
            print("ERROR: Email content is empty", file=sys.stderr)
            sys.exit(1)

        return email_content

    except FileNotFoundError:
        print(f"ERROR: File not found: {source}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR reading email: {e}", file=sys.stderr)
        sys.exit(1)

def classify_email(client: anthropic.Anthropic, email_content: str) -> Dict[str, Any]:
    """Classify the support email into categories."""
    print(f"\n{'='*80}")
    print("STEP 1: Email Classification")
    print(f"{'='*80}\n")

    prompt = f"""Analyze this support email and classify it:

EMAIL CONTENT:
{email_content}

Provide a JSON response with the following structure:
{{
  "category": "bug|feature|question|billing|account|technical|other",
  "subcategory": "more specific classification",
  "priority": "critical|high|medium|low",
  "sentiment": "frustrated|neutral|positive",
  "product_area": "which part of the product this relates to",
  "requires_technical_team": true/false,
  "estimated_resolution_time": "immediate|< 1 hour|< 1 day|< 1 week|requires investigation",
  "key_points": ["list", "of", "main", "points"],
  "customer_request": "concise summary of what they want"
}}

Only output valid JSON, no other text."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        classification_text = message.content[0].text
        # Extract JSON from potential markdown code blocks
        if "```json" in classification_text:
            classification_text = classification_text.split("```json")[1].split("```")[0].strip()
        elif "```" in classification_text:
            classification_text = classification_text.split("```")[1].split("```")[0].strip()

        classification = json.loads(classification_text)

        print("Classification Results:")
        print(json.dumps(classification, indent=2))

        return classification

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON response: {e}", file=sys.stderr)
        print(f"Raw response: {classification_text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR classifying email: {e}", file=sys.stderr)
        sys.exit(1)

def draft_response(client: anthropic.Anthropic, email_content: str, classification: Dict[str, Any]) -> str:
    """Draft an appropriate response based on classification."""
    print(f"\n{'='*80}")
    print("STEP 2: Drafting Response")
    print(f"{'='*80}\n")

    prompt = f"""Draft a professional support response to this email:

ORIGINAL EMAIL:
{email_content}

CLASSIFICATION:
- Category: {classification['category']}
- Priority: {classification['priority']}
- Sentiment: {classification['sentiment']}
- Customer Request: {classification['customer_request']}

Draft a response that:
1. Acknowledges their issue with empathy (especially if frustrated)
2. Addresses their specific concern
3. Provides clear next steps or solutions
4. Sets appropriate expectations for resolution time
5. Maintains a professional, helpful tone
6. Is concise but complete (200-300 words)

If this is a bug report, acknowledge it and explain the escalation process.
If this is a feature request, thank them and explain how you track requests.
If this is a billing issue, provide clear steps or escalation.
If this is a question, answer directly and offer additional help.

Write the response email now:"""

    try:
        print("Generating response (streaming)...\n")

        response = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response += text

        print("\n")
        return response

    except Exception as e:
        print(f"\nERROR drafting response: {e}", file=sys.stderr)
        sys.exit(1)

def suggest_actions(client: anthropic.Anthropic, classification: Dict[str, Any]) -> str:
    """Suggest internal actions and priority."""
    print(f"\n{'='*80}")
    print("STEP 3: Internal Action Items")
    print(f"{'='*80}\n")

    prompt = f"""Based on this support ticket classification, suggest internal actions:

CLASSIFICATION:
{json.dumps(classification, indent=2)}

Provide:
1. **Recommended Assignment**: Which team/person should handle this
2. **Priority Justification**: Why this priority level is appropriate
3. **Action Items**: Specific steps the assigned person should take
4. **Follow-up Timeline**: When to check back with the customer
5. **Related Issues**: Potential connections to other tickets or known issues
6. **Escalation Triggers**: What would require escalating this ticket

Keep it concise and actionable."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        actions = message.content[0].text
        print(actions)
        return actions

    except Exception as e:
        print(f"ERROR generating action items: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main classifier execution."""
    if len(sys.argv) < 2:
        print("Usage: python support_classifier.py <email_file>")
        print("       python support_classifier.py -    (read from stdin)")
        print("\nExample:")
        print('  python support_classifier.py customer_email.txt')
        print('  echo "I found a bug..." | python support_classifier.py -')
        sys.exit(1)

    source = sys.argv[1]

    print(f"\n{'#'*80}")
    print("# SUPPORT EMAIL CLASSIFIER")
    print(f"{'#'*80}")

    # Initialize client
    client = create_client()

    # Read email
    email_content = read_email(source)

    print("\nOriginal Email:")
    print("-" * 80)
    print(email_content[:500] + ("..." if len(email_content) > 500 else ""))
    print("-" * 80)

    # Execute classification pipeline
    classification = classify_email(client, email_content)
    response = draft_response(client, email_content, classification)
    actions = suggest_actions(client, classification)

    print(f"\n{'#'*80}")
    print("# CLASSIFICATION COMPLETE")
    print(f"{'#'*80}")
    print(f"\nCategory: {classification['category'].upper()}")
    print(f"Priority: {classification['priority'].upper()}")
    print(f"Sentiment: {classification['sentiment']}")
    print(f"\nDraft response and action items generated above.")

if __name__ == "__main__":
    main()
