# AI Workflow Examples

This directory contains **ready-to-run code examples** that demonstrate practical AI workflows using the Anthropic Claude API. Each example is a complete, production-ready script that solves a real-world problem.

## Quick Start

### Prerequisites

1. **Get an API Key**
   - Sign up at [console.anthropic.com](https://console.anthropic.com)
   - Create an API key
   - Set it as an environment variable:
     ```bash
     export ANTHROPIC_API_KEY='your-api-key-here'
     ```

2. **Install Dependencies**

   **For Python examples:**
   ```bash
   pip install anthropic requests beautifulsoup4
   ```

   **For JavaScript examples:**
   ```bash
   npm install @anthropic-ai/sdk node-fetch cheerio
   ```

### Running the Examples

**Python:**
```bash
python python/content_pipeline.py "How to build a SaaS in 2026"
```

**JavaScript:**
```bash
node javascript/content_pipeline.js "How to build a SaaS in 2026"
```

**CLI Wrappers:**
```bash
chmod +x cli/*.sh
./cli/content-pipeline.sh "How to build a SaaS in 2026"
```

## Available Workflows

### 1. Content Pipeline
**File:** `content_pipeline.py` | `content_pipeline.js` | `cli/content-pipeline.sh`

**What it does:**
- Generates a comprehensive content outline
- Writes a full 1500-2000 word draft
- Provides SEO optimization recommendations
- Creates social media posts for distribution

**Use cases:**
- Blog post generation
- Marketing content creation
- Content marketing automation
- SEO-optimized article writing

**Example:**
```bash
python python/content_pipeline.py "10 Tips for Remote Teams"
```

**Output:**
- Structured outline with 5-7 sections
- Full article in markdown format
- Meta title, description, and keywords
- Twitter thread, LinkedIn post, Reddit post, HN title

---

### 2. Support Classifier
**File:** `support_classifier.py` | `support_classifier.js` | `cli/support-classifier.sh`

**What it does:**
- Classifies support emails by category and priority
- Analyzes customer sentiment
- Drafts professional responses
- Suggests internal action items

**Use cases:**
- Customer support automation
- Email triage and routing
- Response template generation
- Support ticket prioritization

**Example:**
```bash
# From file
python python/support_classifier.py customer_email.txt

# From stdin
cat email.txt | python python/support_classifier.py -
```

**Output:**
- Category: bug/feature/question/billing/etc
- Priority: critical/high/medium/low
- Sentiment analysis
- Draft response email
- Internal action recommendations

---

### 3. Code Reviewer
**File:** `code_reviewer.py` | `code_reviewer.js` | `cli/code-reviewer.sh`

**What it does:**
- Analyzes git diffs for potential bugs
- Reviews security vulnerabilities
- Identifies performance issues
- Provides structured feedback

**Use cases:**
- Automated code review
- Pre-merge PR analysis
- Security audits
- Performance optimization

**Example:**
```bash
# From git diff
git diff main...feature-branch | python python/code_reviewer.py -

# From file
python python/code_reviewer.py changes.diff
```

**Output:**
- Diff summary (files changed, complexity, risk)
- Bug detection with severity ratings
- Security vulnerability analysis
- Performance recommendations
- Overall approval status

---

### 4. Competitor Analyzer
**File:** `competitor_analyzer.py` | `competitor_analyzer.js` | `cli/competitor-analyzer.sh`

**What it does:**
- Fetches and analyzes competitor websites
- Extracts key product information
- Compares features and pricing
- Generates SWOT analysis and positioning strategy

**Use cases:**
- Competitive intelligence
- Market research
- Product positioning
- Strategic planning

**Example:**
```bash
python python/competitor_analyzer.py "https://vercel.com" "LaunchFast"
```

**Output:**
- Competitor information (features, pricing, positioning)
- Feature-by-feature comparison
- SWOT analysis
- Strategic recommendations
- Positioning strategy

---

## Project Structure

```
examples/
├── README.md                    # This file
├── python/                      # Python implementations
│   ├── content_pipeline.py
│   ├── support_classifier.py
│   ├── code_reviewer.py
│   └── competitor_analyzer.py
├── javascript/                  # JavaScript implementations
│   ├── content_pipeline.js
│   ├── support_classifier.js
│   ├── code_reviewer.js
│   └── competitor_analyzer.js
└── cli/                        # Shell script wrappers
    ├── content-pipeline.sh
    ├── support-classifier.sh
    ├── code-reviewer.sh
    └── competitor-analyzer.sh
```

## Usage Patterns

### Piping with stdin

Many examples support reading from stdin using `-`:

```bash
# Support classifier
cat support_email.txt | python python/support_classifier.py -

# Code reviewer
git diff | python python/code_reviewer.py -
git diff main...feature | python python/code_reviewer.py -
```

### Streaming output

Examples that generate long-form content use streaming for immediate feedback:

```python
# Python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```javascript
// JavaScript
const stream = await client.messages.stream(...);
for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta') {
        process.stdout.write(chunk.delta.text);
    }
}
```

### Error handling

All examples include comprehensive error handling:

- API key validation
- Input validation
- Network error handling
- JSON parsing with fallbacks
- Graceful degradation

## Customization Guide

### Modifying prompts

Each script has clearly marked prompt sections. To customize:

1. Find the prompt in the function (e.g., `generate_outline`)
2. Modify the instructions to match your needs
3. Adjust `max_tokens` if needed for longer/shorter outputs

Example:
```python
prompt = f"""Create a comprehensive outline for a blog post about: "{topic}"

The outline should:
- Have an engaging title
- Include 5-7 main sections  # Change this to 3-4 for shorter posts
- Include 2-3 subsections
...
```

### Changing the model

All examples use `claude-sonnet-4-5-20250929` by default. To use a different model:

```python
# Change this constant at the top of the file
MODEL = "claude-opus-4-6"  # For maximum quality
MODEL = "claude-sonnet-4-5-20250929"  # For balanced performance (default)
```

### Adjusting output formats

Examples output in different formats:
- **Markdown**: Content pipeline, code reviewer
- **JSON**: Support classifier (classification step), code reviewer (analysis step)
- **Plain text**: Most responses

To change output format, modify the prompt's format instructions:

```python
prompt = """...
Format as JSON:
{
  "field": "value"
}
"""
```

### Adding new workflows

To create a new workflow:

1. Copy an existing example as a template
2. Modify the prompts for your use case
3. Adjust the pipeline steps (add/remove as needed)
4. Update error handling for your specific inputs
5. Add to this README

## Tips for Best Results

### 1. Provide sufficient context

The more context you give, the better the results:

**Bad:**
```bash
python content_pipeline.py "SaaS"
```

**Good:**
```bash
python content_pipeline.py "How to build a profitable SaaS in 2026: A technical founder's guide"
```

### 2. Use appropriate models

- **Claude Sonnet**: Fast, cost-effective, great for most tasks
- **Claude Opus**: Maximum quality for critical tasks
- **Claude Haiku**: Fastest for simple classification tasks (not used in examples)

### 3. Chain workflows together

Combine multiple examples for powerful automation:

```bash
# 1. Generate content
python content_pipeline.py "Topic" > article.md

# 2. Review the generated code examples
git diff | python code_reviewer.py -

# 3. Analyze competitors
python competitor_analyzer.py "https://competitor.com" "YourProduct"
```

### 4. Adjust max_tokens based on needs

- Outlines: 1000-2000 tokens
- Full articles: 3000-4000 tokens
- Code reviews: 2000-3000 tokens per section
- Classifications: 500-1000 tokens

### 5. Handle rate limits

If you hit rate limits:
- Add delays between requests: `time.sleep(1)`
- Use exponential backoff for retries
- Batch requests where possible

## Common Issues & Solutions

### Issue: "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
export ANTHROPIC_API_KEY='your-key-here'

# To persist across sessions (add to ~/.bashrc or ~/.zshrc):
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "Module not found: anthropic"

**Solution:**
```bash
pip install anthropic

# Or for JavaScript:
npm install @anthropic-ai/sdk
```

### Issue: Rate limit errors

**Solution:**
The Anthropic API has rate limits. If you hit them:
- Wait a few seconds and retry
- Reduce the frequency of requests
- Upgrade your API tier at console.anthropic.com

### Issue: Output is truncated

**Solution:**
Increase `max_tokens` in the script:
```python
max_tokens=4000  # Increase from 2000
```

### Issue: JSON parsing errors

**Solution:**
The examples handle this automatically by extracting JSON from markdown code blocks. If you still have issues:
- Check the raw API response
- Ensure prompt says "Only output valid JSON"
- Add more explicit format instructions

## Cost Estimates

Based on Anthropic's pricing (as of Feb 2026):

| Workflow | Tokens (avg) | Cost per run |
|----------|--------------|--------------|
| Content Pipeline | ~15,000 | ~$0.05 |
| Support Classifier | ~5,000 | ~$0.02 |
| Code Reviewer | ~10,000 | ~$0.03 |
| Competitor Analyzer | ~12,000 | ~$0.04 |

*Costs are approximate and based on Sonnet 4.5 pricing. Actual costs depend on input size and output length.*

## Advanced Usage

### Batch processing

Process multiple items in a loop:

```bash
# Classify multiple support emails
for email in emails/*.txt; do
    python python/support_classifier.py "$email" >> results.txt
done

# Review multiple PRs
for pr in {123..130}; do
    gh pr diff $pr | python python/code_reviewer.py - > reviews/pr-$pr.txt
done
```

### Integration with CI/CD

Use code reviewer in GitHub Actions:

```yaml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Get diff
        run: git diff origin/main...HEAD > changes.diff
      - name: Review code
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python examples/python/code_reviewer.py changes.diff
```

### Building on these examples

These examples are starting points. Common extensions:

1. **Save outputs to files** instead of stdout
2. **Add configuration files** for custom prompts
3. **Build web interfaces** with Flask/Express
4. **Create Slack bots** that use these workflows
5. **Add databases** to track history and analytics
6. **Implement caching** to reduce API costs

## Model Information

All examples use **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`):

- **Context window**: 200k tokens
- **Output**: Up to 8k tokens
- **Strengths**: Code, analysis, structured output
- **Speed**: Fast (2-3 seconds for most requests)
- **Cost**: $3/million input tokens, $15/million output tokens

For more details, see [Anthropic's documentation](https://docs.anthropic.com).

## Support & Feedback

These examples are part of **PromptVault** - an AI Workflow Library for developers.

- **Issues**: Open a GitHub issue if something doesn't work
- **Questions**: Check the [main README](../README.md) or prompt library
- **Improvements**: PRs welcome for new workflows or optimizations

## License

These examples are included with your PromptVault purchase. You may:
- ✓ Use them in personal and commercial projects
- ✓ Modify them for your needs
- ✓ Share them with your team
- ✗ Redistribute or resell them

---

**Built with Claude API** | [Get PromptVault](https://buy.stripe.com/3cI6oG5iJ8hA93m4xk08g04) | More tools at [github.com/Wittlesus](https://github.com/Wittlesus)
