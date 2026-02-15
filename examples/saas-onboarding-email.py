#!/usr/bin/env python3
"""
SaaS Onboarding Email Workflow
Generate personalized onboarding emails based on user signup data.

Usage:
    python saas-onboarding-email.py --user-data user.json

Requirements:
    pip install anthropic
"""

import os
import json
import argparse
from anthropic import Anthropic

def generate_onboarding_email(user_data):
    """Generate personalized onboarding email using Claude."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""You are a SaaS email copywriter. Generate a personalized onboarding email.

User data:
- Name: {user_data['name']}
- Company: {user_data.get('company', 'Not provided')}
- Role: {user_data.get('role', 'Not provided')}
- Plan: {user_data.get('plan', 'free')}
- Signup source: {user_data.get('source', 'direct')}

Email requirements:
1. Subject line (under 50 chars)
2. Personalized greeting
3. Quick win: One action they can take in under 60 seconds
4. Value reminder: Why they signed up
5. Next steps: 2-3 specific actions with links
6. CTA: Schedule onboarding call (if paid plan)

Tone: Friendly, helpful, not salesy. Format as plain text email."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SaaS onboarding emails")
    parser.add_argument("--user-data", required=True, help="Path to user JSON file")
    args = parser.parse_args()

    # Load user data
    with open(args.user_data, 'r') as f:
        user_data = json.load(f)

    # Generate email
    email = generate_onboarding_email(user_data)

    print("=" * 70)
    print("GENERATED ONBOARDING EMAIL")
    print("=" * 70)
    print(email)
    print("=" * 70)
