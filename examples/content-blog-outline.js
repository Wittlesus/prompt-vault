#!/usr/bin/env node
/**
 * Blog Post Outline Generator
 * Generate SEO-optimized blog post outlines with keyword research.
 *
 * Usage:
 *   node content-blog-outline.js "your topic here"
 *
 * Requirements:
 *   npm install @anthropic-ai/sdk
 */

const Anthropic = require('@anthropic-ai/sdk');

async function generateBlogOutline(topic) {
  const client = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  const prompt = `You are an SEO content strategist. Create a comprehensive blog post outline for: "${topic}"

Requirements:
1. SEO-optimized title (under 60 chars, includes primary keyword)
2. Meta description (under 160 chars)
3. Target keywords (primary + 3-5 LSI keywords)
4. Outline structure:
   - Hook (first paragraph premise)
   - 5-7 H2 sections with bullet points
   - Each section should target a search intent
   - Include data/stat callouts where relevant
   - FAQ section (3-5 common questions)
   - CTA direction

Format as markdown. Focus on search intent and topical authority.`;

  const message = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 2048,
    messages: [{ role: 'user', content: prompt }],
  });

  return message.content[0].text;
}

async function main() {
  const topic = process.argv[2];

  if (!topic) {
    console.error('Usage: node content-blog-outline.js "your topic"');
    process.exit(1);
  }

  console.log('Generating blog outline for:', topic);
  console.log('='.repeat(70));

  const outline = await generateBlogOutline(topic);

  console.log(outline);
  console.log('='.repeat(70));
}

main().catch(console.error);
