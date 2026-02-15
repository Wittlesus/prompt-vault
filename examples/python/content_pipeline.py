#!/usr/bin/env python3
"""
Content Pipeline - Full Content Generation Workflow
Takes a topic → generates outline → writes draft → optimizes for SEO → generates social posts

Usage:
    python content_pipeline.py "How to build a SaaS in 2026"

Requirements:
    pip install anthropic

Environment:
    ANTHROPIC_API_KEY - Your Anthropic API key
"""

import os
import sys
import anthropic
from typing import Dict, Any

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

def generate_outline(client: anthropic.Anthropic, topic: str) -> str:
    """Step 1: Generate a structured outline for the topic."""
    print(f"\n{'='*80}")
    print("STEP 1: Generating Outline")
    print(f"{'='*80}\n")

    prompt = f"""Create a comprehensive outline for a blog post about: "{topic}"

The outline should:
- Have an engaging title
- Include 5-7 main sections with H2 headings
- Include 2-3 subsections (H3) under each main section
- Include an introduction and conclusion
- Focus on actionable, practical content
- Be optimized for reader engagement

Format as a clean, hierarchical outline with clear numbering."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        outline = message.content[0].text
        print(outline)
        return outline

    except Exception as e:
        print(f"ERROR generating outline: {e}", file=sys.stderr)
        sys.exit(1)

def write_draft(client: anthropic.Anthropic, topic: str, outline: str) -> str:
    """Step 2: Write a full draft based on the outline."""
    print(f"\n{'='*80}")
    print("STEP 2: Writing Full Draft")
    print(f"{'='*80}\n")

    prompt = f"""Write a complete blog post based on this outline:

TOPIC: {topic}

OUTLINE:
{outline}

Requirements:
- Write in a conversational, engaging tone
- Include specific examples and actionable tips
- Use short paragraphs (2-3 sentences max)
- Include transitions between sections
- Target length: 1500-2000 words
- Use markdown formatting (headers, lists, bold, etc.)
- Make it valuable and practical

Write the complete article now:"""

    try:
        print("Generating draft (streaming)...\n")

        draft = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                draft += text

        print("\n")
        return draft

    except Exception as e:
        print(f"\nERROR writing draft: {e}", file=sys.stderr)
        sys.exit(1)

def optimize_seo(client: anthropic.Anthropic, topic: str, draft: str) -> Dict[str, str]:
    """Step 3: Optimize the content for SEO."""
    print(f"\n{'='*80}")
    print("STEP 3: SEO Optimization")
    print(f"{'='*80}\n")

    prompt = f"""Analyze this blog post and provide SEO recommendations:

TOPIC: {topic}

ARTICLE:
{draft}

Provide:
1. Optimized meta title (60 chars max)
2. Optimized meta description (155 chars max)
3. 5 primary keywords to target
4. 5 secondary keywords (LSI/related terms)
5. Suggested URL slug
6. 3 specific content improvements for better SEO

Format your response clearly with headers for each section."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        seo_recommendations = message.content[0].text
        print(seo_recommendations)
        return {"recommendations": seo_recommendations}

    except Exception as e:
        print(f"ERROR optimizing SEO: {e}", file=sys.stderr)
        sys.exit(1)

def generate_social_posts(client: anthropic.Anthropic, topic: str, draft: str) -> str:
    """Step 4: Generate social media posts."""
    print(f"\n{'='*80}")
    print("STEP 4: Generating Social Media Posts")
    print(f"{'='*80}\n")

    prompt = f"""Based on this article, create social media posts for distribution:

TOPIC: {topic}

ARTICLE EXCERPT:
{draft[:1500]}...

Generate:
1. Twitter/X thread (5-7 tweets, numbered, engaging hooks)
2. LinkedIn post (professional tone, 150-200 words)
3. Reddit post (title + body, conversational, community-focused)
4. Hacker News title (compelling, HN-style)

Make each post platform-appropriate and engaging. Include relevant hashtags where appropriate."""

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        social_posts = message.content[0].text
        print(social_posts)
        return social_posts

    except Exception as e:
        print(f"ERROR generating social posts: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main pipeline execution."""
    if len(sys.argv) < 2:
        print("Usage: python content_pipeline.py \"Your topic here\"")
        print("Example: python content_pipeline.py \"How to build a SaaS in 2026\"")
        sys.exit(1)

    topic = sys.argv[1]

    print(f"\n{'#'*80}")
    print(f"# CONTENT PIPELINE: {topic}")
    print(f"{'#'*80}")

    # Initialize client
    client = create_client()

    # Execute pipeline
    outline = generate_outline(client, topic)
    draft = write_draft(client, topic, outline)
    seo = optimize_seo(client, topic, draft)
    social = generate_social_posts(client, topic, draft)

    print(f"\n{'#'*80}")
    print("# PIPELINE COMPLETE")
    print(f"{'#'*80}")
    print("\nAll outputs generated successfully!")
    print("You can now copy the draft, implement SEO recommendations, and distribute via social media.")

if __name__ == "__main__":
    main()
