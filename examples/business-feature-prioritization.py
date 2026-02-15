#!/usr/bin/env python3
"""
Feature Prioritization Workflow
Analyze feature requests and generate RICE scores + recommendations.

Usage:
    python business-feature-prioritization.py --features features.json

Requirements:
    pip install anthropic
"""

import os
import json
import argparse
from anthropic import Anthropic

def prioritize_features(features_data):
    """Generate RICE scores and prioritization recommendations."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    features_list = "\n".join([
        f"- {f['name']}: {f.get('description', 'No description')}"
        for f in features_data['features']
    ])

    context = features_data.get('context', {})

    prompt = f"""You are a product manager analyzing feature requests for prioritization.

Product context:
- Stage: {context.get('stage', 'Not specified')}
- Monthly users: {context.get('monthly_users', 'Not specified')}
- Team size: {context.get('team_size', 'Not specified')}
- Current focus: {context.get('focus', 'Not specified')}

Feature requests:
{features_list}

Task:
1. Score each feature using RICE framework:
   - Reach: How many users affected? (1-10)
   - Impact: Value per user? (0.25/0.5/1/2/3)
   - Confidence: How sure are we? (50%/80%/100%)
   - Effort: Person-months (estimate)
   - RICE Score = (Reach × Impact × Confidence) / Effort

2. Rank features by RICE score (highest first)

3. For top 3 features, provide:
   - Why it ranks high
   - Key risks/assumptions
   - Quick win vs. strategic bet?

4. Recommend: Ship now, Ship next quarter, or Backlog

Format as markdown table + analysis."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Feature prioritization with RICE scoring")
    parser.add_argument("--features", required=True, help="Path to features JSON file")
    args = parser.parse_args()

    with open(args.features, 'r') as f:
        features_data = json.load(f)

    print("📊 Analyzing feature requests...")
    print("=" * 70)

    analysis = prioritize_features(features_data)

    print(analysis)
    print("=" * 70)
