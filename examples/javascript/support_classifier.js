#!/usr/bin/env node
/**
 * Support Email Classifier - Automated Support Triage
 * Takes a support email → categorizes → drafts response → suggests priority
 *
 * Usage:
 *     node support_classifier.js path/to/email.txt
 *     cat email.txt | node support_classifier.js -
 *
 * Requirements:
 *     npm install @anthropic-ai/sdk
 *
 * Environment:
 *     ANTHROPIC_API_KEY - Your Anthropic API key
 */

import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs';

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
 * Read email content from file or stdin
 */
async function readEmail(source) {
  try {
    let emailContent;

    if (source === '-') {
      // Read from stdin
      const chunks = [];
      for await (const chunk of process.stdin) {
        chunks.push(chunk);
      }
      emailContent = Buffer.concat(chunks).toString('utf-8');
    } else {
      // Read from file
      emailContent = fs.readFileSync(source, 'utf-8');
    }

    if (!emailContent.trim()) {
      console.error('ERROR: Email content is empty');
      process.exit(1);
    }

    return emailContent;
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.error(`ERROR: File not found: ${source}`);
    } else {
      console.error(`ERROR reading email: ${error.message}`);
    }
    process.exit(1);
  }
}

/**
 * Classify the support email into categories
 */
async function classifyEmail(client, emailContent) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 1: Email Classification');
  console.log('='.repeat(80) + '\n');

  const prompt = `Analyze this support email and classify it:

EMAIL CONTENT:
${emailContent}

Provide a JSON response with the following structure:
{
  "category": "bug|feature|question|billing|account|technical|other",
  "subcategory": "more specific classification",
  "priority": "critical|high|medium|low",
  "sentiment": "frustrated|neutral|positive",
  "product_area": "which part of the product this relates to",
  "requires_technical_team": true/false,
  "estimated_resolution_time": "immediate|< 1 hour|< 1 day|< 1 week|requires investigation",
  "key_points": ["list", "of", "main", "points"],
  "customer_request": "concise summary of what they want"
}

Only output valid JSON, no other text.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }],
    });

    let classificationText = message.content[0].text;

    // Extract JSON from potential markdown code blocks
    if (classificationText.includes('```json')) {
      classificationText = classificationText.split('```json')[1].split('```')[0].trim();
    } else if (classificationText.includes('```')) {
      classificationText = classificationText.split('```')[1].split('```')[0].trim();
    }

    const classification = JSON.parse(classificationText);

    console.log('Classification Results:');
    console.log(JSON.stringify(classification, null, 2));

    return classification;
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error('ERROR: Invalid JSON response:', error.message);
    } else {
      console.error('ERROR classifying email:', error.message);
    }
    process.exit(1);
  }
}

/**
 * Draft an appropriate response based on classification
 */
async function draftResponse(client, emailContent, classification) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 2: Drafting Response');
  console.log('='.repeat(80) + '\n');

  const prompt = `Draft a professional support response to this email:

ORIGINAL EMAIL:
${emailContent}

CLASSIFICATION:
- Category: ${classification.category}
- Priority: ${classification.priority}
- Sentiment: ${classification.sentiment}
- Customer Request: ${classification.customer_request}

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

Write the response email now:`;

  try {
    console.log('Generating response (streaming)...\n');

    let response = '';
    const stream = await client.messages.stream({
      model: MODEL,
      max_tokens: 1500,
      messages: [{ role: 'user', content: prompt }],
    });

    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
        process.stdout.write(chunk.delta.text);
        response += chunk.delta.text;
      }
    }

    console.log('\n');
    return response;
  } catch (error) {
    console.error('\nERROR drafting response:', error.message);
    process.exit(1);
  }
}

/**
 * Suggest internal actions and priority
 */
async function suggestActions(client, classification) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 3: Internal Action Items');
  console.log('='.repeat(80) + '\n');

  const prompt = `Based on this support ticket classification, suggest internal actions:

CLASSIFICATION:
${JSON.stringify(classification, null, 2)}

Provide:
1. **Recommended Assignment**: Which team/person should handle this
2. **Priority Justification**: Why this priority level is appropriate
3. **Action Items**: Specific steps the assigned person should take
4. **Follow-up Timeline**: When to check back with the customer
5. **Related Issues**: Potential connections to other tickets or known issues
6. **Escalation Triggers**: What would require escalating this ticket

Keep it concise and actionable.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }],
    });

    const actions = message.content[0].text;
    console.log(actions);
    return actions;
  } catch (error) {
    console.error('ERROR generating action items:', error.message);
    process.exit(1);
  }
}

/**
 * Main classifier execution
 */
async function main() {
  if (process.argv.length < 3) {
    console.log('Usage: node support_classifier.js <email_file>');
    console.log('       node support_classifier.js -    (read from stdin)');
    console.log('\nExamples:');
    console.log('  node support_classifier.js customer_email.txt');
    console.log('  cat email.txt | node support_classifier.js -');
    process.exit(1);
  }

  const source = process.argv[2];

  console.log('\n' + '#'.repeat(80));
  console.log('# SUPPORT EMAIL CLASSIFIER');
  console.log('#'.repeat(80));

  // Initialize client
  const client = createClient();

  // Read email
  const emailContent = await readEmail(source);

  console.log('\nOriginal Email:');
  console.log('-'.repeat(80));
  const preview = emailContent.substring(0, 500);
  console.log(preview + (emailContent.length > 500 ? '...' : ''));
  console.log('-'.repeat(80));

  // Execute classification pipeline
  const classification = await classifyEmail(client, emailContent);
  const response = await draftResponse(client, emailContent, classification);
  const actions = await suggestActions(client, classification);

  console.log('\n' + '#'.repeat(80));
  console.log('# CLASSIFICATION COMPLETE');
  console.log('#'.repeat(80));
  console.log(`\nCategory: ${classification.category.toUpperCase()}`);
  console.log(`Priority: ${classification.priority.toUpperCase()}`);
  console.log(`Sentiment: ${classification.sentiment}`);
  console.log('\nDraft response and action items generated above.');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
