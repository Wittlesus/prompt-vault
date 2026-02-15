# PromptVault - AI Workflow Automation Library

> **Production-ready AI automation systems.** Not prompts—complete multi-step workflows with Python and JavaScript code.

## The Problem with Free Prompt Libraries

Free libraries like FlowGPT, PromptHero, and awesome-chatgpt-prompts give you millions of one-shot prompts like:
- "Review my code for bugs"
- "Write unit tests"
- "Analyze this market"

**But they don't give you automation.** You still have to:
- Manually copy-paste prompts
- Chain multiple prompts together yourself
- Parse and format the output
- Integrate with your tools (git, APIs, databases)

## How PromptVault Is Different

We give you **complete automation workflows** with:

1. **Multi-step prompt chains** - Output from prompt 1 automatically feeds into prompt 2
2. **System prompts for each step** - Not just user prompts, but role definitions and output formats
3. **Ready-to-run Python and JavaScript code** - Copy, add API key, run
4. **API integration examples** - Anthropic, OpenAI, streaming, error handling
5. **Expected output formats** - Know exactly what you'll get
6. **When to use vs. alternatives** - Cost comparisons and use case guidance

## Pricing

**$19 — One-time purchase. Not a subscription.**

[**Buy Now**](https://buy.stripe.com/3cI6oG5iJ8hA93m4xk08g04)

**What you get:**
- 15+ complete automation workflows across 4 categories
- Full Python and JavaScript implementation code
- System prompts + user prompts + chaining logic
- Works with Claude API (adaptable to OpenAI, Gemini, etc.)
- Team usage included
- Lifetime updates

**Save $119:** Get this + 6 other products in the [Complete Bundle for $99](https://buy.stripe.com/5kQeVceTj0P8enGe7U08g06)

## Quick Start (5 minutes)

```bash
# 1. Install SDK
pip install anthropic  # or: npm install @anthropic-ai/sdk

# 2. Set API key
export ANTHROPIC_API_KEY=sk-ant-xxxxx

# 3. Copy a workflow script (e.g., PR Review Agent)
# Save from workflows/development-workflows.md as pr_review.py

# 4. Run it
python pr_review.py

# Output: Complete PR review in pr_review.md + detailed analysis in JSON
```

That's it. From copy-paste to working automation in 5 minutes.

## Workflow Categories

### [SaaS Workflows](workflows/saas-workflows.md)

**1. User Onboarding Email Sequence Generator**
- Step 1: Analyze product features → Extract value props
- Step 2: Segment users → Define behavioral triggers
- Step 3: Generate emails → 7-email sequence with A/B variants
- **Replaces:** Email copywriter ($2-5K per sequence)
- **Cost:** $19 + ~$50-100/month API costs

**2. Support Ticket Auto-Categorization & Routing**
- Step 1: Categorize ticket → Extract urgency, sentiment, PII
- Step 2: Search KB → Find relevant articles
- Step 3: Draft response → Empathetic, solution-focused
- Step 4: Route to team → Engineering/billing/support
- **Replaces:** Support ops hire ($60-80K/year)

**3. Feature Request Analysis & Prioritization**
- Step 1: Deduplicate → Group similar requests
- Step 2: RICE scoring → Reach, Impact, Confidence, Effort
- Step 3: Generate PRD → Outline for top feature
- **Replaces:** Product analyst time (4-8 hours → 5 minutes)

**4. Changelog Generation from Git Commits**
- Step 1: Fetch commits → Parse git log
- Step 2: Categorize → New/improved/fixed
- Step 3: Generate release notes → Blog + in-app + email + tweet
- **Replaces:** Manual changelog writing (1-2 hours per release)

---

### [Content Workflows](workflows/content-workflows.md)

**1. Blog Post Production Pipeline**
- Step 1: Research & outline → Competitive analysis, SEO keywords
- Step 2: Write draft → Conversational, data-driven, 1500+ words
- Step 3: Edit → Tighten prose, optimize SEO
- Step 4: Meta content → Title tags, social posts
- **Replaces:** Content writer ($150-500 per 1500-word post)
- **Cost:** ~$1-3 per post in API costs

**2. Newsletter Content Generator**
- Step 1: Curate content → Pick best 5-7 items
- Step 2: Write commentary → 2-3 paragraphs per item
- Step 3: Format → HTML email + plain text + web archive
- **Replaces:** Newsletter writer ($500-2K/month)

**3. Landing Page Copy Generator**
- Step 1: Value prop analysis → Extract emotional hooks
- Step 2: Write sections → Hero, features, pricing, FAQ, CTA
- Step 3: A/B variants → 2 headline options, 2 CTA variants
- **Replaces:** Copywriter ($1-3K for landing page)

---

### [Development Workflows](workflows/development-workflows.md)

**1. Code Review Agent (Full PR Analysis)**
- Step 1: Categorize changes → Feature/bugfix/refactor
- Step 2: Bug detection → Null refs, off-by-one, race conditions
- Step 3: Security audit → Injection, XSS, secrets exposure
- Step 4: Performance review → N+1 queries, memory leaks
- Step 5: Test coverage → Missing tests, edge cases
- Step 6: Generate review → Markdown PR comment
- **Time saved:** 30-60 min manual review → 2-3 min automated

**2. Documentation Generator (README + API Docs)**
- Step 1: Scan codebase → Find entry points, routes, configs
- Step 2: Analyze → Understand project type, tech stack
- Step 3: Generate README → Installation, usage, examples
- Step 4: Generate API docs → Endpoints, parameters, responses
- **Time saved:** 2-4 hours → 5 minutes

**3. Test Suite Generator**
- Step 1: Analyze code → Identify functions, edge cases, integration points
- Step 2: Generate unit tests → Happy path, edge cases, error handling
- Step 3: Generate integration tests → API/DB/external service tests
- **Coverage:** Comprehensive test suite in minutes

**4. Bug Triage & Root Cause Analysis**
- Step 1: Categorize error → Type, severity, affected component
- Step 2: Root cause analysis → Why it failed, contributing factors
- Step 3: Suggest fix → Working code solution
- **Time saved:** Hours of debugging → Minutes

---

### [Business Workflows](workflows/business-workflows.md)

**1. Competitive Intelligence Automation**
- Step 1: Analyze competitor updates → Significant moves, trends
- Step 2: Feature gap analysis → What we lack, what we lead on
- Step 3: Strategic recommendations → Immediate + short-term + long-term
- **Replaces:** Market research firm ($15-50K per report)
- **Frequency:** Run weekly for $5-10 in API costs

**2. Customer Interview Synthesizer**
- Step 1: Extract quotes → Key insights from each interview
- Step 2: Identify themes → Patterns across 10+ interviews
- Step 3: Generate insights → Research report with recommendations
- **Replaces:** UX researcher ($150-300/hour for synthesis)

**3. Pricing Strategy Analyzer**
- Step 1: Analyze costs → Unit economics, LTV, minimum viable price
- Step 2: Competitive pricing → Market analysis, positioning gaps
- Step 3: Segment analysis → Willingness to pay by customer type
- Step 4: Recommend pricing → Tiers, metric, anchoring, testing plan
- **Replaces:** Pricing consultant ($10-30K for strategy)

**4. Market Research Report Generator**
- Step 1: Market overview → Key players, trends, barriers
- Step 2: TAM/SAM/SOM → Market sizing with methodology
- Step 3: Opportunity analysis → Where to compete, differentiate
- **Replaces:** Market research consultant ($15-50K)

---

## Complete Code Examples

Every workflow includes:

### Python Implementation
```python
# save as: pr_review_agent.py
import anthropic
import subprocess
import json
from typing import Dict, List

class PRReviewAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_categorize_changes(self, diff: str) -> Dict:
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1200,
            system="""Tech lead categorizing PR changes.
Output JSON with: change_type, files_changed, scope, complexity.""",
            messages=[{"role": "user", "content": f"Analyze:\n{diff}"}]
        )
        return json.loads(response.content[0].text)

    # ... steps 2-6 ...

    def review_pr(self) -> Dict:
        diff = subprocess.run("git diff main...HEAD", shell=True,
                             capture_output=True, text=True).stdout

        analysis = self.step1_categorize_changes(diff)
        bugs = self.step2_bug_detection(diff)
        security = self.step3_security_audit(diff)
        # ... complete workflow ...

        return {"analysis": analysis, "bugs": bugs, "security": security}

# Usage
if __name__ == "__main__":
    import os
    agent = PRReviewAgent(api_key=os.environ["ANTHROPIC_API_KEY"])
    result = agent.review_pr()
    print(json.dumps(result, indent=2))
```

### JavaScript Implementation
```javascript
// save as: prReviewAgent.js
import Anthropic from '@anthropic-ai/sdk';
import { execSync } from 'child_process';

class PRReviewAgent {
  constructor(apiKey) {
    this.client = new Anthropic({ apiKey });
  }

  async step1CategorizeChanges(diff) {
    const response = await this.client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1200,
      system: 'Tech lead categorizing PR changes. Output JSON.',
      messages: [{ role: 'user', content: `Analyze:\n${diff}` }]
    });
    return JSON.parse(response.content[0].text);
  }

  // ... steps 2-6 ...

  async reviewPR() {
    const diff = execSync('git diff main...HEAD', { encoding: 'utf-8' });
    const analysis = await this.step1CategorizeChanges(diff);
    // ... complete workflow ...
    return { analysis };
  }
}

// Usage
const agent = new PRReviewAgent(process.env.ANTHROPIC_API_KEY);
const result = await agent.reviewPR();
console.log(JSON.stringify(result, null, 2));
```

---

## ROI Calculator

| Task | Manual Cost | PromptVault Cost | Time Saved |
|------|-------------|------------------|------------|
| **Blog post (1500 words)** | $150-500 (writer) | $1-3 (API) | 3-5 hours → 10 min |
| **Code review per PR** | 30-60 min (eng time) | 2-3 min + $0.50 API | 27-57 min |
| **Support ticket triage** | $60K/year (ops hire) | $19 + $100/mo API | Automated |
| **Market research report** | $15-50K (consultant) | $19 + $5-10 (API) | Weeks → Hours |
| **Onboarding email sequence** | $2-5K (copywriter) | $19 + $50-100 (API) | 2 weeks → 1 hour |

**Break-even:** If you publish 1 blog post, review 5 PRs, or analyze 1 market, you've paid for PromptVault.

---

## When to Use This vs. Alternatives

| Use PromptVault When... | Hire Humans When... |
|-------------------------|---------------------|
| Budget <$10K for the task | Budget >$50K (complex strategy) |
| Need results in days/hours | Can wait weeks/months |
| Technical/analytical work | Highly creative/storytelling work |
| Team <20 people | Team >100 (can build internal tools) |
| Iteration speed matters | One-time critical decision |

---

## Adapting to Other AI Models

All examples use Anthropic Claude, but you can easily swap providers:

### OpenAI (GPT-4)
```python
from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
)
```

### Google Gemini
```python
import google.generativeai as genai
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt)
```

---

## FAQ

**Q: How is this different from FlowGPT, PromptBase, or awesome-chatgpt-prompts?**
A: Those give you individual prompts. PromptVault gives you complete automation workflows with:
- Multi-step chains (prompt 1 output feeds prompt 2)
- Production-ready code in Python and JavaScript
- System prompts + user prompts + error handling
- API integration patterns

**Q: Do I need coding experience?**
A: Basic Python or JavaScript helps, but the scripts are simple and well-commented. If you can run `python script.py`, you can use these. Customization requires light coding.

**Q: Which AI model should I use?**
A: Workflows are written for Claude but work with any API-compatible LLM. Recommendations:
- **Claude Opus 4.6** - Best quality for code review, strategy ($0.50-2 per run)
- **Claude Sonnet 4.5** - Faster, cheaper for categorization ($0.10-0.50 per run)
- **GPT-4 Turbo** - Alternative for content/business ($0.30-1.50 per run)

**Q: Can I customize these?**
A: Absolutely. Every script is designed to be modified. Change prompts, add steps, adjust models, integrate with your tools.

**Q: Can my team use this?**
A: Yes, single purchase covers your entire team.

**Q: What's included in "lifetime updates"?**
A: New workflows, improved prompts, new model support, integration patterns. All free.

---

## File Structure

```
prompt-vault/
  README.md                         # This file
  CLAUDE.md                         # Project context
  GUMROAD_LISTING.md               # Sales copy

  workflows/                        # Complete automation workflows
    saas-workflows.md              # Onboarding, support, features, changelog
    content-workflows.md           # Blog, newsletter, landing pages
    development-workflows.md       # Code review, docs, tests, bug triage
    business-workflows.md          # Competitive intel, interviews, pricing, market research

  prompts/                          # Original 64 expert prompts (still included)
    code-review.md
    documentation.md
    testing.md
    debugging.md
    devops.md
    database.md
    product.md
```

---

## More Developer Tools

| Product | Description | Price |
|---------|-------------|-------|
| [LaunchFast SaaS Starter](https://github.com/Wittlesus/launchfast-starter) | Next.js 16 boilerplate with auth, payments, AI | $79 |
| [SEO Blog Engine](https://github.com/Wittlesus/seo-blog-engine) | CLI for generating SEO blog posts | $29 |
| [Indie Hacker Toolkit](https://github.com/Wittlesus/indie-hacker-toolkit) | Planning templates for solo founders | $19 |
| [CursorRules Pro](https://github.com/Wittlesus/cursorrules-pro) | .cursorrules for 8 popular stacks | $14 |
| [Complete Bundle](https://buy.stripe.com/5kQeVceTj0P8enGe7U08g06) | All products above | $99 |

---

## License

Personal and team use permitted. Redistribution or resale is not permitted.

---

**The transformation:** From "a collection of prompts" to "production-ready AI automation systems."

Free libraries give you fishing hooks. We give you fishing boats with autopilot.
