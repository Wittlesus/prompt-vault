#!/usr/bin/env node
/**
 * Competitor Analyzer - Competitive Intelligence
 * Takes a competitor URL → extracts key info → compares to your product → outputs SWOT analysis
 *
 * Usage:
 *     node competitor_analyzer.js "https://competitor.com" "Your Product Name"
 *
 * Requirements:
 *     npm install @anthropic-ai/sdk node-fetch cheerio
 *
 * Environment:
 *     ANTHROPIC_API_KEY - Your Anthropic API key
 */

import Anthropic from '@anthropic-ai/sdk';
import fetch from 'node-fetch';
import * as cheerio from 'cheerio';

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
 * Fetch and extract text content from a webpage
 */
async function fetchWebpage(url) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 1: Fetching Webpage');
  console.log('='.repeat(80) + '\n');
  console.log(`URL: ${url}`);

  try {
    // Set a user agent to avoid being blocked
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      },
      timeout: 10000,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const html = await response.text();

    // Parse HTML
    const $ = cheerio.load(html);

    // Remove script and style elements
    $('script, style, nav, footer').remove();

    // Get text
    const text = $('body').text();

    // Clean up excessive whitespace
    const lines = text
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0);
    let cleanText = lines.join('\n');

    // Limit to reasonable size (first 10000 chars)
    if (cleanText.length > 10000) {
      cleanText = cleanText.substring(0, 10000) + '\n\n[Content truncated...]';
    }

    console.log(`✓ Fetched ${cleanText.length} characters`);

    return cleanText;
  } catch (error) {
    console.error('ERROR fetching webpage:', error.message);
    console.error('Continuing with limited analysis...');
    return `Failed to fetch content from ${url}. Error: ${error.message}`;
  }
}

/**
 * Extract key information about the competitor
 */
async function extractKeyInfo(client, url, content) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 2: Extracting Key Information');
  console.log('='.repeat(80) + '\n');

  const prompt = `Analyze this competitor's website and extract key information:

URL: ${url}

WEBPAGE CONTENT:
${content}

Extract and provide a JSON response with:
{
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
}

If information is not available, use "Not visible on page".
Only output valid JSON, no other text.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    });

    let infoText = message.content[0].text;

    // Extract JSON from potential markdown code blocks
    if (infoText.includes('```json')) {
      infoText = infoText.split('```json')[1].split('```')[0].trim();
    } else if (infoText.includes('```')) {
      infoText = infoText.split('```')[1].split('```')[0].trim();
    }

    const info = JSON.parse(infoText);

    console.log('Competitor Information:');
    console.log(JSON.stringify(info, null, 2));

    return info;
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error('ERROR: Invalid JSON response:', error.message);
    } else {
      console.error('ERROR extracting information:', error.message);
    }
    process.exit(1);
  }
}

/**
 * Compare competitor to your product
 */
async function compareProducts(client, competitorInfo, yourProduct) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 3: Product Comparison');
  console.log('='.repeat(80) + '\n');

  const prompt = `Compare this competitor to our product:

COMPETITOR:
${JSON.stringify(competitorInfo, null, 2)}

OUR PRODUCT: ${yourProduct}

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

Keep it objective and actionable.`;

  try {
    console.log('Generating comparison (streaming)...\n');

    let comparison = '';
    const stream = await client.messages.stream({
      model: MODEL,
      max_tokens: 3000,
      messages: [{ role: 'user', content: prompt }],
    });

    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
        process.stdout.write(chunk.delta.text);
        comparison += chunk.delta.text;
      }
    }

    console.log('\n');
    return comparison;
  } catch (error) {
    console.error('\nERROR comparing products:', error.message);
    process.exit(1);
  }
}

/**
 * Generate SWOT analysis
 */
async function generateSWOT(client, competitorInfo, comparison, yourProduct) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 4: SWOT Analysis');
  console.log('='.repeat(80) + '\n');

  const prompt = `Based on this competitive analysis, generate a SWOT analysis for our product (${yourProduct}):

COMPETITOR INFO:
${JSON.stringify(competitorInfo, null, 2)}

COMPARISON:
${comparison}

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

Format clearly with headers and bullet points.`;

  try {
    console.log('Generating SWOT analysis (streaming)...\n');

    let swot = '';
    const stream = await client.messages.stream({
      model: MODEL,
      max_tokens: 3000,
      messages: [{ role: 'user', content: prompt }],
    });

    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
        process.stdout.write(chunk.delta.text);
        swot += chunk.delta.text;
      }
    }

    console.log('\n');
    return swot;
  } catch (error) {
    console.error('\nERROR generating SWOT:', error.message);
    process.exit(1);
  }
}

/**
 * Generate positioning strategy recommendations
 */
async function generatePositioningStrategy(client, competitorInfo, swot, yourProduct) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 5: Positioning Strategy');
  console.log('='.repeat(80) + '\n');

  const prompt = `Based on this competitive intelligence, suggest positioning strategies for ${yourProduct}:

COMPETITOR:
${JSON.stringify(competitorInfo, null, 2)}

SWOT ANALYSIS:
${swot.substring(0, 2000)}...

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

Keep it strategic and actionable.`;

  try {
    console.log('Generating positioning strategy...\n');

    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2500,
      messages: [{ role: 'user', content: prompt }],
    });

    const strategy = message.content[0].text;
    console.log(strategy);
    return strategy;
  } catch (error) {
    console.error('ERROR generating strategy:', error.message);
    process.exit(1);
  }
}

/**
 * Main competitor analysis execution
 */
async function main() {
  if (process.argv.length < 4) {
    console.log('Usage: node competitor_analyzer.js <competitor_url> <your_product_name>');
    console.log('\nExample:');
    console.log('  node competitor_analyzer.js "https://competitor.com" "LaunchFast"');
    process.exit(1);
  }

  const competitorUrl = process.argv[2];
  const yourProduct = process.argv[3];

  console.log('\n' + '#'.repeat(80));
  console.log(`# COMPETITOR ANALYSIS: ${competitorUrl}`);
  console.log(`# YOUR PRODUCT: ${yourProduct}`);
  console.log('#'.repeat(80));

  // Initialize client
  const client = createClient();

  // Execute analysis pipeline
  const content = await fetchWebpage(competitorUrl);
  const competitorInfo = await extractKeyInfo(client, competitorUrl, content);
  const comparison = await compareProducts(client, competitorInfo, yourProduct);
  const swot = await generateSWOT(client, competitorInfo, comparison, yourProduct);
  const strategy = await generatePositioningStrategy(client, competitorInfo, swot, yourProduct);

  console.log('\n' + '#'.repeat(80));
  console.log('# COMPETITIVE ANALYSIS COMPLETE');
  console.log('#'.repeat(80));
  console.log(`\nCompetitor: ${competitorInfo.company_name || 'Unknown'}`);
  console.log('Analysis complete. Review the detailed findings above.');
  console.log('\nNext steps:');
  console.log('1. Review the SWOT analysis for strategic insights');
  console.log('2. Implement positioning strategy recommendations');
  console.log('3. Prioritize product development based on competitive gaps');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
