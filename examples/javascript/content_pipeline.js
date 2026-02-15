#!/usr/bin/env node
/**
 * Content Pipeline - Full Content Generation Workflow
 * Takes a topic → generates outline → writes draft → optimizes for SEO → generates social posts
 *
 * Usage:
 *     node content_pipeline.js "How to build a SaaS in 2026"
 *
 * Requirements:
 *     npm install @anthropic-ai/sdk
 *
 * Environment:
 *     ANTHROPIC_API_KEY - Your Anthropic API key
 */

import Anthropic from '@anthropic-ai/sdk';

// Model to use for all API calls
const MODEL = 'claude-sonnet-4-5-20250929';

/**
 * Create and return an Anthropic client
 */
function createClient() {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error('ERROR: ANTHROPIC_API_KEY environment variable not set');
    console.error('Set it with: export ANTHROPIC_API_KEY=\'your-key-here\'');
    process.exit(1);
  }
  return new Anthropic({ apiKey });
}

/**
 * Step 1: Generate a structured outline for the topic
 */
async function generateOutline(client, topic) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 1: Generating Outline');
  console.log('='.repeat(80) + '\n');

  const prompt = `Create a comprehensive outline for a blog post about: "${topic}"

The outline should:
- Have an engaging title
- Include 5-7 main sections with H2 headings
- Include 2-3 subsections (H3) under each main section
- Include an introduction and conclusion
- Focus on actionable, practical content
- Be optimized for reader engagement

Format as a clean, hierarchical outline with clear numbering.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    });

    const outline = message.content[0].text;
    console.log(outline);
    return outline;
  } catch (error) {
    console.error('ERROR generating outline:', error.message);
    process.exit(1);
  }
}

/**
 * Step 2: Write a full draft based on the outline
 */
async function writeDraft(client, topic, outline) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 2: Writing Full Draft');
  console.log('='.repeat(80) + '\n');

  const prompt = `Write a complete blog post based on this outline:

TOPIC: ${topic}

OUTLINE:
${outline}

Requirements:
- Write in a conversational, engaging tone
- Include specific examples and actionable tips
- Use short paragraphs (2-3 sentences max)
- Include transitions between sections
- Target length: 1500-2000 words
- Use markdown formatting (headers, lists, bold, etc.)
- Make it valuable and practical

Write the complete article now:`;

  try {
    console.log('Generating draft (streaming)...\n');

    let draft = '';
    const stream = await client.messages.stream({
      model: MODEL,
      max_tokens: 4000,
      messages: [{ role: 'user', content: prompt }],
    });

    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
        process.stdout.write(chunk.delta.text);
        draft += chunk.delta.text;
      }
    }

    console.log('\n');
    return draft;
  } catch (error) {
    console.error('\nERROR writing draft:', error.message);
    process.exit(1);
  }
}

/**
 * Step 3: Optimize the content for SEO
 */
async function optimizeSEO(client, topic, draft) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 3: SEO Optimization');
  console.log('='.repeat(80) + '\n');

  const prompt = `Analyze this blog post and provide SEO recommendations:

TOPIC: ${topic}

ARTICLE:
${draft}

Provide:
1. Optimized meta title (60 chars max)
2. Optimized meta description (155 chars max)
3. 5 primary keywords to target
4. 5 secondary keywords (LSI/related terms)
5. Suggested URL slug
6. 3 specific content improvements for better SEO

Format your response clearly with headers for each section.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    });

    const seoRecommendations = message.content[0].text;
    console.log(seoRecommendations);
    return { recommendations: seoRecommendations };
  } catch (error) {
    console.error('ERROR optimizing SEO:', error.message);
    process.exit(1);
  }
}

/**
 * Step 4: Generate social media posts
 */
async function generateSocialPosts(client, topic, draft) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 4: Generating Social Media Posts');
  console.log('='.repeat(80) + '\n');

  const draftExcerpt = draft.substring(0, 1500) + '...';

  const prompt = `Based on this article, create social media posts for distribution:

TOPIC: ${topic}

ARTICLE EXCERPT:
${draftExcerpt}

Generate:
1. Twitter/X thread (5-7 tweets, numbered, engaging hooks)
2. LinkedIn post (professional tone, 150-200 words)
3. Reddit post (title + body, conversational, community-focused)
4. Hacker News title (compelling, HN-style)

Make each post platform-appropriate and engaging. Include relevant hashtags where appropriate.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    });

    const socialPosts = message.content[0].text;
    console.log(socialPosts);
    return socialPosts;
  } catch (error) {
    console.error('ERROR generating social posts:', error.message);
    process.exit(1);
  }
}

/**
 * Main pipeline execution
 */
async function main() {
  if (process.argv.length < 3) {
    console.log('Usage: node content_pipeline.js "Your topic here"');
    console.log('Example: node content_pipeline.js "How to build a SaaS in 2026"');
    process.exit(1);
  }

  const topic = process.argv[2];

  console.log('\n' + '#'.repeat(80));
  console.log(`# CONTENT PIPELINE: ${topic}`);
  console.log('#'.repeat(80));

  // Initialize client
  const client = createClient();

  // Execute pipeline
  const outline = await generateOutline(client, topic);
  const draft = await writeDraft(client, topic, outline);
  const seo = await optimizeSEO(client, topic, draft);
  const social = await generateSocialPosts(client, topic, draft);

  console.log('\n' + '#'.repeat(80));
  console.log('# PIPELINE COMPLETE');
  console.log('#'.repeat(80));
  console.log('\nAll outputs generated successfully!');
  console.log('You can now copy the draft, implement SEO recommendations, and distribute via social media.');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
