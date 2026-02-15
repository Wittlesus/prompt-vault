#!/usr/bin/env python3
"""
Competitor Analyzer - Competitive Intelligence
Takes a competitor URL → extracts key info → compares to your product → outputs SWOT analysis

Usage:
    python competitor_analyzer.py "https://competitor.com" "Your Product Name"

Requirements:
    pip install anthropic requests beautifulsoup4

Environment:
    ANTHROPIC_API_KEY - Your Anthropic API key
"""

import os
import sys
import anthropic
from typing import Dict, Any
import json

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Missing dependencies. Install with:", file=sys.stderr)
    print("  pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

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

def fetch_webpage(url: str) -> str:
    """Fetch and extract text content from a webpage."""
    print(f"\n{'='*80}")
    print("STEP 1: Fetching Webpage")
    print(f"{'='*80}\n")
    print(f"URL: {url}")

    try:
        # Set a user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        # Get text
        text = soup.get_text(separator='\n', strip=True)

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = '\n'.join(lines)

        # Limit to reasonable size (first 10000 chars)
        if len(clean_text) > 10000:
            clean_text = clean_text[:10000] + "\n\n[Content truncated...]"

        print(f"✓ Fetched {len(clean_text)} characters")

        return clean_text

    except requests.exceptions.RequestException as e:
        print(f"ERROR fetching webpage: {e}", file=sys.stderr)
        print("Continuing with limited analysis...", file=sys.stderr)
        return f"Failed to fetch content from {url}. Error: {str(e)}"

def extract_key_info(client: anthropic.Anthropic, url: str, content: str) -> Dict[str, Any]:
    """Extract key information about the competitor."""
    print(f"\n{'='*80}")
    print("STEP 2: Extracting Key Information")
    print(f"{'='*80}\n")

    prompt = f"""Analyze this competitor's website and extract key information:

URL: {url}

WEBPAGE CONTENT:
{content}

Extract and provide a JSON response with:
{{
  "company_name": "name",
  "tagline": "their main value proposition",
  "target_audience": "who they serve",
  "key_features": ["feature 1", "feature 2", "feature 3"],
  "pricing_model": "freemium|subscription|one-time|enterprise|unclear",
  "pricing_tiers": ["tier info if visible"],
  "unique_selling_points": ["USP 1", "USP 2"],
  "tech_stack_visible": ["technologies mentioned"],
  "customer_segments": ["segment 1", "segment 2"],
  "positioning": "how they position themselves in market",
  "content_strategy": "blog|docs|tutorials|case-studies|etc",
  "call_to_action": "primary CTA on page"
}}

If information is not available, use "Not visible on page".
Only output valid JSON, no other text."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        info_text = message.content[0].text
        # Extract JSON from potential markdown code blocks
        if "```json" in info_text:
            info_text = info_text.split("```json")[1].split("```")[0].strip()
        elif "```" in info_text:
            info_text = info_text.split("```")[1].split("```")[0].strip()

        info = json.loads(info_text)

        print("Competitor Information:")
        print(json.dumps(info, indent=2))

        return info

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON response: {e}", file=sys.stderr)
        print(f"Raw response: {info_text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR extracting information: {e}", file=sys.stderr)
        sys.exit(1)

def compare_products(client: anthropic.Anthropic, competitor_info: Dict[str, Any], your_product: str) -> str:
    """Compare competitor to your product."""
    print(f"\n{'='*80}")
    print("STEP 3: Product Comparison")
    print(f"{'='*80}\n")

    prompt = f"""Compare this competitor to our product:

COMPETITOR:
{json.dumps(competitor_info, indent=2)}

OUR PRODUCT: {your_product}

Provide a detailed comparison covering:

## Feature Comparison
- Features they have that we don't
- Features we have that they don't
- Features we both have (compare implementation/approach)

## Pricing Comparison
- How their pricing compares to ours
- Value proposition differences
- Which pricing model might be more attractive to customers

## Positioning Comparison
- How they position vs how we position
- Target audience overlap and differences
- Messaging differences

## User Experience
- What they do well in UX/UI
- What we do better
- Opportunities for us to learn from them

Keep it objective and actionable."""

    try:
        print("Generating comparison (streaming)...\n")

        comparison = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                comparison += text

        print("\n")
        return comparison

    except Exception as e:
        print(f"\nERROR comparing products: {e}", file=sys.stderr)
        sys.exit(1)

def generate_swot(client: anthropic.Anthropic, competitor_info: Dict[str, Any], comparison: str, your_product: str) -> str:
    """Generate SWOT analysis."""
    print(f"\n{'='*80}")
    print("STEP 4: SWOT Analysis")
    print(f"{'='*80}\n")

    prompt = f"""Based on this competitive analysis, generate a SWOT analysis for our product ({your_product}):

COMPETITOR INFO:
{json.dumps(competitor_info, indent=2)}

COMPARISON:
{comparison}

Generate a comprehensive SWOT analysis:

## Strengths
What we do better than this competitor (3-5 points)

## Weaknesses
Where we fall short compared to them (3-5 points)

## Opportunities
Market opportunities based on their gaps or our differentiators (3-5 points)

## Threats
Competitive threats they pose or market risks (3-5 points)

For each point, be specific and actionable. Include concrete examples where possible.

Then add:

## Strategic Recommendations
Top 3 immediate actions we should take based on this analysis.

Format clearly with headers and bullet points."""

    try:
        print("Generating SWOT analysis (streaming)...\n")

        swot = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                swot += text

        print("\n")
        return swot

    except Exception as e:
        print(f"\nERROR generating SWOT: {e}", file=sys.stderr)
        sys.exit(1)

def generate_positioning_strategy(client: anthropic.Anthropic, competitor_info: Dict[str, Any], swot: str, your_product: str) -> str:
    """Generate positioning strategy recommendations."""
    print(f"\n{'='*80}")
    print("STEP 5: Positioning Strategy")
    print(f"{'='*80}\n")

    prompt = f"""Based on this competitive intelligence, suggest positioning strategies for {your_product}:

COMPETITOR:
{json.dumps(competitor_info, indent=2)}

SWOT ANALYSIS:
{swot[:2000]}...

Provide:

## Differentiation Strategy
How should we differentiate from this competitor?

## Messaging Recommendations
- Key messages to emphasize
- What to avoid saying
- Unique angles to explore

## Target Market Strategy
- Should we compete head-to-head or find a niche?
- Which customer segments should we focus on?
- Where do we have the strongest competitive advantage?

## Product Development Priorities
Based on this analysis, what features/improvements should be prioritized?

## Marketing & Sales Strategy
- How to position against this competitor in sales conversations
- Marketing channels where we might have an advantage
- Content strategy to highlight our strengths

Keep it strategic and actionable."""

    try:
        print("Generating positioning strategy...\n")

        message = client.messages.create(
            model=MODEL,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        strategy = message.content[0].text
        print(strategy)
        return strategy

    except Exception as e:
        print(f"ERROR generating strategy: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main competitor analysis execution."""
    if len(sys.argv) < 3:
        print("Usage: python competitor_analyzer.py <competitor_url> <your_product_name>")
        print("\nExample:")
        print('  python competitor_analyzer.py "https://competitor.com" "LaunchFast"')
        sys.exit(1)

    competitor_url = sys.argv[1]
    your_product = sys.argv[2]

    print(f"\n{'#'*80}")
    print(f"# COMPETITOR ANALYSIS: {competitor_url}")
    print(f"# YOUR PRODUCT: {your_product}")
    print(f"{'#'*80}")

    # Initialize client
    client = create_client()

    # Execute analysis pipeline
    content = fetch_webpage(competitor_url)
    competitor_info = extract_key_info(client, competitor_url, content)
    comparison = compare_products(client, competitor_info, your_product)
    swot = generate_swot(client, competitor_info, comparison, your_product)
    strategy = generate_positioning_strategy(client, competitor_info, swot, your_product)

    print(f"\n{'#'*80}")
    print("# COMPETITIVE ANALYSIS COMPLETE")
    print(f"{'#'*80}")
    print(f"\nCompetitor: {competitor_info.get('company_name', 'Unknown')}")
    print(f"Analysis complete. Review the detailed findings above.")
    print(f"\nNext steps:")
    print("1. Review the SWOT analysis for strategic insights")
    print("2. Implement positioning strategy recommendations")
    print("3. Prioritize product development based on competitive gaps")

if __name__ == "__main__":
    main()
