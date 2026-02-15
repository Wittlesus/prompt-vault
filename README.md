<p align="center">
  <img src="https://img.shields.io/github/stars/Wittlesus/prompt-vault?style=social" alt="GitHub Stars">
  <img src="https://img.shields.io/github/license/Wittlesus/prompt-vault" alt="License">
  <img src="https://img.shields.io/badge/Built%20with-AI-blueviolet?style=flat-square" alt="Built with AI">
  <img src="https://img.shields.io/badge/Money--Back-30%20Day%20Guarantee-green?style=flat-square" alt="30-Day Money-Back Guarantee">
</p>

<h1 align="center">PromptVault</h1>

<p align="center"><strong>Not prompts. Production-ready AI automation pipelines.</strong></p>
<p align="center">64 expert-crafted prompts + 4 ready-to-run workflow scripts. Copy, add your API key, run. Working AI automation in 60 seconds.</p>

<p align="center">
  <a href="https://buy.stripe.com/3cI6oG5iJ8hA93m4xk08g04"><img src="https://img.shields.io/badge/BUY%20NOW-$19-black?style=for-the-badge&logo=stripe&logoColor=white" alt="Buy Now $19"></a>
</p>

<p align="center"><em>One-time purchase. Not a subscription. Team usage included.</em></p>

---

## Features

- [x] **64 expert-crafted prompts** across 7 categories (not one-liners -- full frameworks)
- [x] **4 ready-to-run workflow scripts** -- Python + JavaScript with CLI interfaces
- [x] **Content Pipeline** -- topic to publishable article with SEO and social posts
- [x] **Code Reviewer** -- automated code review from git diffs (bugs, security, performance)
- [x] **Support Classifier** -- email triage with auto-drafted responses
- [x] **Competitor Analyzer** -- SWOT analysis and positioning strategy
- [x] **Sample data included** -- test every workflow immediately
- [x] **Git integration** -- works with diffs, commits, and branches
- [x] **Streaming support** -- real-time output from AI responses
- [x] **Model-agnostic** -- works with Claude, ChatGPT, Gemini, Llama, Mistral
- [x] **Team usage included** -- share with your entire team
- [x] **Lifetime updates** -- new workflows and prompts added over time

---

## Quick Start (60 Seconds)

```bash
# 1. Install dependencies
pip install anthropic gitpython       # Python workflows
npm install @anthropic-ai/sdk         # JavaScript workflows

# 2. Set your API key
export ANTHROPIC_API_KEY='your-key-here'

# 3. Run your first workflow
python examples/python/content_pipeline.py "How to build a SaaS in 2026"

# Or review your git changes for bugs and security issues
git diff | python examples/python/code_reviewer.py -

# Or classify and respond to support emails
cat support_email.txt | python examples/python/support_classifier.py -
```

That is it. Working AI automation in under 60 seconds.

---

## Why PromptVault?

**The problem with free prompt libraries:** They give you one-liners like "Review my code." You still have to figure out how to integrate them into your workflow.

**PromptVault solves this:** Complete automation pipelines with working code. Copy a script, add your API key, run it.

| Source | What You Get | Price |
|--------|-------------|-------|
| **PromptBase** | Individual prompts for $2-10 each | Pay per prompt |
| **FlowGPT** | Millions of community prompts (unvetted) | Free |
| **PromptVault** | Complete automation pipelines with working code + 64 expert prompts | **$19 one-time** |

---

## What Is Included

### 4 Ready-to-Run Workflows

**Content Pipeline** -- Full content generation automation. One command goes from topic to publishable article with SEO optimization and social media distribution plan.

**Code Reviewer** -- Comprehensive automated code review. Analyzes git diffs for bugs, security issues, and performance problems with structured feedback and severity ratings.

**Support Classifier** -- Automated customer support triage. Classifies emails by category, priority, and sentiment. Drafts professional responses and suggests action items.

**Competitor Analyzer** -- Competitive intelligence automation. Fetches and analyzes competitor websites. Generates feature comparison, SWOT analysis, and positioning strategy.

All workflows available in **Python**, **JavaScript**, and **CLI wrappers**.

### 64 Expert Prompts

| Category | Prompts | Covers |
|----------|---------|--------|
| [Code Review](prompts/code-review.md) | 10 | Bug detection, security audits, performance, refactoring, API design |
| [Documentation](prompts/documentation.md) | 10 | READMEs, API docs, changelogs, architecture docs, tutorials |
| [Testing](prompts/testing.md) | 10 | Unit tests, integration tests, edge cases, mocks, E2E |
| [Debugging](prompts/debugging.md) | 10 | Error decoding, stack traces, memory leaks, race conditions |
| [DevOps](prompts/devops.md) | 8 | Dockerfiles, CI/CD, Kubernetes, Nginx, incident response |
| [Database](prompts/database.md) | 8 | Schema design, query optimization, migrations, security |
| [Product](prompts/product.md) | 8 | User stories, PRDs, feature prioritization, A/B tests |

Each prompt includes: detailed instructions, structured output format, example output, and customization tips.

---

## Example Use Cases

- **Pre-commit code review:** Run `code_reviewer.py` as a git hook. Catch bugs before CI.
- **Content batching:** Generate 10 blog outlines on Monday, schedule the entire week.
- **Onboarding automation:** Trigger support classifier from your signup webhook.
- **Feature backlog grooming:** Let AI do RICE scoring before sprint planning.
- **Documentation debt:** Point the doc generator at your codebase. Generate READMEs for every package.

---

## Who Is This For?

- **Software engineers** who want AI automation that runs on its own
- **Solo developers** who need to automate code review, docs, and QA without hiring
- **Tech leads** who want team-wide AI workflows (not everyone crafting their own prompts)
- **Freelancers** who need to deliver faster without sacrificing quality

---

## Pricing

<p align="center">
  <a href="https://buy.stripe.com/3cI6oG5iJ8hA93m4xk08g04"><img src="https://img.shields.io/badge/BUY%20NOW-$19-black?style=for-the-badge&logo=stripe&logoColor=white" alt="Buy Now $19"></a>
</p>

**$19 -- One-time purchase. Team usage included.**

**What you get:**
- 64 expert-crafted prompts across 7 categories
- 4 ready-to-run workflow automation scripts (Python + JavaScript)
- Sample data and CLI tools
- Works with Claude, ChatGPT, Gemini, and any AI model
- Share with your entire team
- Lifetime updates

> **30-day money-back guarantee.** If the workflows do not save you time in the first week, get a full refund. No questions asked.

### Save $119

Get PromptVault + 6 other developer products in the [**Complete Bundle for $99**](https://buy.stripe.com/5kQeVceTj0P8enGe7U08g06).

---

## File Structure

```
prompt-vault/
  prompts/               # 64 expert prompts across 7 categories
    code-review.md
    documentation.md
    testing.md
    debugging.md
    devops.md
    database.md
    product.md
  examples/              # Ready-to-run workflow automation
    python/              # Python implementations
    javascript/          # JavaScript implementations
    cli/                 # Shell script wrappers
    README.md            # Workflow documentation
```

---

## More Developer Tools

| Product | Description | Price |
|---------|-------------|-------|
| [LaunchFast SaaS Starter](https://github.com/Wittlesus/launchfast-starter) | Next.js 16 boilerplate with auth, payments, AI, email | $79 |
| [SEO Blog Engine](https://github.com/Wittlesus/seo-blog-engine) | CLI for generating SEO-optimized blog posts | $29 |
| [Indie Hacker Toolkit](https://github.com/Wittlesus/indie-hacker-toolkit) | 8 planning templates for solo founders | $19 |
| [CursorRules Pro](https://github.com/Wittlesus/cursorrules-pro) | AI coding configs for Cursor, Claude Code, Windsurf, Copilot | $14 |
| [**Complete Bundle**](https://buy.stripe.com/5kQeVceTj0P8enGe7U08g06) | **All products above** | **$99** |

---

## License

Personal and team use permitted. Redistribution or resale is not permitted.
