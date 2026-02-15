#!/usr/bin/env node
/**
 * Code Reviewer - Automated Code Review
 * Takes a git diff → reviews for bugs, security, performance → outputs structured feedback
 *
 * Usage:
 *     node code_reviewer.js path/to/file.diff
 *     git diff | node code_reviewer.js -
 *     git diff main...feature-branch | node code_reviewer.js -
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
 * Read diff content from file or stdin
 */
async function readDiff(source) {
  try {
    let diffContent;

    if (source === '-') {
      // Read from stdin
      const chunks = [];
      for await (const chunk of process.stdin) {
        chunks.push(chunk);
      }
      diffContent = Buffer.concat(chunks).toString('utf-8');
    } else {
      // Read from file
      diffContent = fs.readFileSync(source, 'utf-8');
    }

    if (!diffContent.trim()) {
      console.error('ERROR: Diff content is empty');
      process.exit(1);
    }

    return diffContent;
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.error(`ERROR: File not found: ${source}`);
    } else {
      console.error(`ERROR reading diff: ${error.message}`);
    }
    process.exit(1);
  }
}

/**
 * Analyze the diff and provide a summary
 */
async function analyzeDiff(client, diffContent) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 1: Diff Analysis');
  console.log('='.repeat(80) + '\n');

  const prompt = `Analyze this git diff and provide a structured summary:

DIFF:
${diffContent}

Provide a JSON response with:
{
  "files_changed": number,
  "lines_added": number,
  "lines_removed": number,
  "languages": ["list", "of", "languages"],
  "change_type": "feature|bugfix|refactor|docs|test|config|other",
  "complexity": "low|medium|high",
  "risk_level": "low|medium|high",
  "summary": "one-sentence description of changes",
  "files": [
    {"path": "file.js", "change_summary": "what changed in this file"}
  ]
}

Only output valid JSON, no other text.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    });

    let analysisText = message.content[0].text;

    // Extract JSON from potential markdown code blocks
    if (analysisText.includes('```json')) {
      analysisText = analysisText.split('```json')[1].split('```')[0].trim();
    } else if (analysisText.includes('```')) {
      analysisText = analysisText.split('```')[1].split('```')[0].trim();
    }

    const analysis = JSON.parse(analysisText);

    console.log('Diff Summary:');
    console.log(JSON.stringify(analysis, null, 2));

    return analysis;
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error('ERROR: Invalid JSON response:', error.message);
    } else {
      console.error('ERROR analyzing diff:', error.message);
    }
    process.exit(1);
  }
}

/**
 * Review the code for potential bugs
 */
async function reviewBugs(client, diffContent) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 2: Bug Detection');
  console.log('='.repeat(80) + '\n');

  const prompt = `Review this code diff for potential bugs:

DIFF:
${diffContent}

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

Format clearly with headers and bullet points.`;

  try {
    console.log('Analyzing for bugs...\n');

    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 3000,
      messages: [{ role: 'user', content: prompt }],
    });

    const bugs = message.content[0].text;
    console.log(bugs);
    return bugs;
  } catch (error) {
    console.error('ERROR reviewing bugs:', error.message);
    process.exit(1);
  }
}

/**
 * Review the code for security issues
 */
async function reviewSecurity(client, diffContent) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 3: Security Analysis');
  console.log('='.repeat(80) + '\n');

  const prompt = `Review this code diff for security vulnerabilities:

DIFF:
${diffContent}

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

Format clearly with headers and bullet points.`;

  try {
    console.log('Analyzing for security issues...\n');

    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 3000,
      messages: [{ role: 'user', content: prompt }],
    });

    const security = message.content[0].text;
    console.log(security);
    return security;
  } catch (error) {
    console.error('ERROR reviewing security:', error.message);
    process.exit(1);
  }
}

/**
 * Review the code for performance issues
 */
async function reviewPerformance(client, diffContent) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 4: Performance Review');
  console.log('='.repeat(80) + '\n');

  const prompt = `Review this code diff for performance issues:

DIFF:
${diffContent}

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

Format clearly with headers and bullet points.`;

  try {
    console.log('Analyzing for performance issues...\n');

    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 3000,
      messages: [{ role: 'user', content: prompt }],
    });

    const performance = message.content[0].text;
    console.log(performance);
    return performance;
  } catch (error) {
    console.error('ERROR reviewing performance:', error.message);
    process.exit(1);
  }
}

/**
 * Generate final review summary and recommendation
 */
async function generateSummary(client, analysis, bugs, security, performance) {
  console.log('\n' + '='.repeat(80));
  console.log('STEP 5: Review Summary');
  console.log('='.repeat(80) + '\n');

  const prompt = `Based on this code review, provide a final summary and recommendation:

DIFF ANALYSIS:
${JSON.stringify(analysis, null, 2)}

BUGS FOUND:
${bugs.substring(0, 1000)}...

SECURITY ISSUES:
${security.substring(0, 1000)}...

PERFORMANCE ISSUES:
${performance.substring(0, 1000)}...

Provide:
1. **Overall Assessment**: APPROVED | APPROVED_WITH_COMMENTS | CHANGES_REQUESTED | BLOCKED
2. **Summary**: 2-3 sentence overview of the changes and review
3. **Critical Issues**: List any blocking issues (if any)
4. **Recommendations**: Top 3 actions before merging (if any)
5. **Positive Notes**: What was done well in this PR

Keep it concise and actionable.`;

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 1500,
      messages: [{ role: 'user', content: prompt }],
    });

    const summary = message.content[0].text;
    console.log(summary);
    return summary;
  } catch (error) {
    console.error('ERROR generating summary:', error.message);
    process.exit(1);
  }
}

/**
 * Main code review execution
 */
async function main() {
  if (process.argv.length < 3) {
    console.log('Usage: node code_reviewer.js <diff_file>');
    console.log('       node code_reviewer.js -    (read from stdin)');
    console.log('\nExamples:');
    console.log('  git diff | node code_reviewer.js -');
    console.log('  git diff main...feature | node code_reviewer.js -');
    console.log('  node code_reviewer.js changes.diff');
    process.exit(1);
  }

  const source = process.argv[2];

  console.log('\n' + '#'.repeat(80));
  console.log('# AUTOMATED CODE REVIEW');
  console.log('#'.repeat(80));

  // Initialize client
  const client = createClient();

  // Read diff
  const diffContent = await readDiff(source);

  console.log(`\nDiff size: ${diffContent.length} characters`);

  // Execute review pipeline
  const analysis = await analyzeDiff(client, diffContent);
  const bugs = await reviewBugs(client, diffContent);
  const security = await reviewSecurity(client, diffContent);
  const performance = await reviewPerformance(client, diffContent);
  const summary = await generateSummary(client, analysis, bugs, security, performance);

  console.log('\n' + '#'.repeat(80));
  console.log('# CODE REVIEW COMPLETE');
  console.log('#'.repeat(80));
  console.log(`\nRisk Level: ${analysis.risk_level.toUpperCase()}`);
  console.log(`Complexity: ${analysis.complexity.toUpperCase()}`);
  console.log('\nReview complete. See detailed findings above.');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
