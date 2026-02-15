# PromptVault — AI Workflow Library for Developers

> **Not prompts. Production-ready AI automation pipelines.**

Free prompt libraries give you one-shot prompts. PromptVault gives you complete automation chains with ready-to-run code.

## Pricing

**$19 — One-time purchase. Not a subscription.**

[**Buy Now**](https://buy.stripe.com/3cI6oG5iJ8hA93m4xk08g04)

What you get:
- 64 expert-crafted prompts across 7 categories
- 4+ ready-to-run workflow automation scripts (Python + JavaScript)
- Sample data and CLI tools you can use today
- Works with Claude, ChatGPT, Gemini, and any AI model
- Team usage included (share with your entire team)
- Lifetime updates as new workflows and prompts are added

**Save $119:** Get this + 6 other products in the [Complete Bundle for $99](https://buy.stripe.com/5kQeVceTj0P8enGe7U08g06)

## Why PromptVault?

**The problem with free prompt libraries:** They give you clever one-liners like "Review my code" or "Write tests." You still have to figure out how to integrate them into your workflow.

**PromptVault solves this:** Complete automation pipelines with working code. Copy a script, add your API key, run it. Working AI automation in 60 seconds.

### What You Actually Get

| What | Description |
|------|-------------|
| **64 Expert Prompts** | Comprehensive frameworks (not one-liners) for code review, testing, debugging, docs, DevOps, database, and product work |
| **Workflow Automation Scripts** | Ready-to-run Python and JavaScript code with CLI interfaces |
| **Sample Data** | Example JSON files so you can test immediately |
| **Integration Patterns** | Git hooks, streaming output, API chaining, file I/O |

### Comparison

| Source | What You Get | Price |
|--------|-------------|-------|
| **PromptBase** | Individual prompts for $2-10 each | Pay per prompt |
| **FlowGPT** | Browse millions of community prompts | Free (unvetted quality) |
| **PromptVault** | Complete automation pipelines with working code + 64 expert prompts | $19 one-time |

## Quick Start (60 seconds)

**1. Install dependencies:**
```bash
pip install anthropic gitpython  # Python workflows
npm install @anthropic-ai/sdk    # JavaScript workflows
```

**2. Set your API key:**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

**3. Run your first workflow:**
```bash
# Generate SEO blog outline
node examples/content-blog-outline.js "Best React frameworks 2026"

# Or review your git changes before committing
python examples/dev-code-review-automation.py
```

That's it. Working AI automation in under 60 seconds.

See [examples/README.md](examples/README.md) for all available workflows.

## What's Included

### Ready-to-Run Workflows

**SaaS Workflows**
- Generate personalized onboarding emails from user signup data
- Automate customer support response templates
- Create product tour scripts based on user behavior

**Content Workflows**
- SEO blog post outlines with keyword research
- Social media content batching
- Email newsletter generation from content feed

**Development Workflows**
- Automated code review on git diffs (pre-commit checks)
- Test generation from function signatures
- Documentation generation from code comments

**Business Workflows**
- RICE scoring for feature prioritization
- Competitive analysis from product URLs
- User interview script generation

### 64 Expert Prompts

All prompts are organized into 7 categories. Each prompt is a comprehensive framework (not a one-liner) with:
- Detailed instructions and role setting
- Structured output format specification
- Example output snippets
- Customization tips for your tech stack

| Category | Prompts | Use Cases |
|----------|---------|-----------|
| [Code Review](prompts/code-review.md) | 10 | Bug detection, security audits, performance reviews, refactoring suggestions, naming conventions, error handling, API design, style checks, dependency audits, pre-merge reviews |
| [Documentation](prompts/documentation.md) | 10 | README generation, API docs, JSDoc/TSDoc, changelogs, architecture docs, onboarding guides, code comments, tutorials, migration guides, runbooks |
| [Testing](prompts/testing.md) | 10 | Unit tests, integration tests, edge case identification, test data factories, test plans, snapshot tests, mocks & stubs, property-based tests, E2E tests, regression identification |
| [Debugging](prompts/debugging.md) | 10 | Error decoding, stack trace analysis, performance profiling, memory leak detection, race conditions, log analysis, debugging strategy, dependency conflicts, environment bugs, production incidents |
| [DevOps](prompts/devops.md) | 8 | Dockerfiles, CI/CD pipelines, infrastructure as code, monitoring & alerting, Kubernetes manifests, Nginx configuration, database backups, incident response |
| [Database](prompts/database.md) | 8 | Schema design, query optimization, migration scripts, data modeling, ORM queries, performance diagnostics, seed data, security hardening |
| [Product](prompts/product.md) | 8 | User stories, PRDs, competitive analysis, feature prioritization, release notes, user interviews, A/B test design, metrics dashboards |

## How to Use

### Option 1: Run the Automation Scripts

The fastest way to get value. The `examples/` directory contains ready-to-run workflows:

```bash
# Review your staged changes before committing
python examples/dev-code-review-automation.py

# Generate feature prioritization with RICE scores
python examples/business-feature-prioritization.py --features data/features.json

# Create personalized onboarding emails
python examples/saas-onboarding-email.py --user-data data/user.json
```

See [examples/README.md](examples/README.md) for full documentation.

### Option 2: Use the Prompts Directly

Browse the `prompts/` directory, copy the prompt you need, and paste it into Claude or ChatGPT.

Each prompt includes:
- **Use Case:** When and why to use it
- **Full Prompt:** The complete text to copy-paste
- **Example Output:** What good results look like
- **Customization Tips:** How to adapt for your stack

### Option 3: Chain Workflows Together

Build multi-step automation by piping output between scripts:

```bash
# Generate code → Review code → Generate tests
your-code-gen-tool | python examples/dev-code-review-automation.py | python examples/test-generator.py
```

## Features That Matter

**CLI interfaces.** Every workflow script has argument parsing, help text, and error handling. Just run it.

**Streaming support.** Modify any script to stream output in real-time (examples included).

**Git integration.** Development workflows integrate with git diffs, commits, and branches.

**Sample data included.** Test every workflow immediately with provided JSON files.

**Customizable prompts.** Every prompt and script is designed to be modified for your brand voice, tech stack, and workflow.

**Model-agnostic.** Works with Claude, ChatGPT, Gemini, Llama, Mistral, or any instruction-following LLM.

## Who Is This For?

- **Software engineers** who want AI automation that runs on its own, not prompts they have to babysit
- **Solo developers** who need to automate code review, documentation, and QA without hiring
- **Tech leads** who want team-wide AI workflows (not everyone crafting their own prompts)
- **Freelancers** who need to deliver faster without sacrificing quality
- **Engineering managers** building AI-augmented development practices

## Who Is This NOT For?

- People who have never used AI coding assistants (start with free tiers first)
- Teams that already have mature internal AI automation
- Anyone looking for prompt injection attacks or jailbreaks (this is for building, not breaking)

## FAQ

**Q: How is this different from free prompt libraries?**
A: Free libraries give you prompts. PromptVault gives you automation. Working Python and JavaScript code with CLI interfaces, file I/O, git integration, and error handling. Copy the script, add your API key, run it. That's the difference.

**Q: Will these scripts work with [specific AI model]?**
A: Yes. The example scripts use Claude (Anthropic API), but you can swap in OpenAI, Google, or any other provider. The prompts themselves are model-agnostic and work with any instruction-following LLM.

**Q: Can I modify the scripts and prompts?**
A: Absolutely. That's the point. Every script is designed to be customized. Change the prompts, add streaming, pipe to other tools, integrate with your stack. Make them your own.

**Q: Do I need to know Python or JavaScript?**
A: Basic familiarity helps, but the scripts are simple and well-commented. If you can run `python script.py`, you can use these. Customization requires light coding.

**Q: Can I share these with my team?**
A: Yes. A single purchase covers your entire team. Share in your wiki, Notion, GitHub, or wherever your team works.

**Q: How often is this updated?**
A: New workflows and prompts are added as AI capabilities evolve. All purchasers receive lifetime updates at no additional cost.

**Q: What if I'm not satisfied?**
A: If the workflows don't save you time in the first week, email for a full refund. No questions asked.

## Example Use Cases

**Pre-commit code review:** Run `dev-code-review-automation.py` as a git pre-commit hook. Catch bugs before they reach CI.

**Content batching:** Generate 10 blog outlines on Monday, schedule all week's content in one session.

**Onboarding automation:** Trigger `saas-onboarding-email.py` from your signup webhook. Personalized emails without writing a word.

**Feature backlog grooming:** Run `business-feature-prioritization.py` before sprint planning. Let AI do the RICE scoring math.

**Documentation debt:** Point the doc generator at your codebase. Generate READMEs for every package.

## File Structure

```
prompt-vault/
  README.md              # You are here
  GUMROAD_LISTING.md     # Sales copy and listing details
  prompts/               # 64 expert prompts across 7 categories
    code-review.md
    documentation.md
    testing.md
    debugging.md
    devops.md
    database.md
    product.md
  examples/              # Ready-to-run workflow automation scripts
    README.md            # Workflow documentation
    saas-onboarding-email.py
    content-blog-outline.js
    dev-code-review-automation.py
    business-feature-prioritization.py
    data/                # Sample data for testing
      user-sample.json
      features-sample.json
```

## More Developer Tools

| Product | Description | Price |
|---------|-------------|-------|
| [LaunchFast SaaS Starter](https://github.com/Wittlesus/launchfast-starter) | Next.js 16 boilerplate with auth, payments, AI, email | $79 |
| [SEO Blog Engine](https://github.com/Wittlesus/seo-blog-engine) | CLI for generating SEO blog posts | $29 |
| [Indie Hacker Toolkit](https://github.com/Wittlesus/indie-hacker-toolkit) | 5 planning templates for solo founders | $19 |
| [CursorRules Pro](https://github.com/Wittlesus/cursorrules-pro) | .cursorrules for 8 popular stacks | $14 |
| [Complete Bundle](https://buy.stripe.com/5kQeVceTj0P8enGe7U08g06) | All products above | $99 |

## License

Personal and team use permitted. Redistribution or resale is not permitted.

---

**The key sell:** Copy a script, add your API key, run it. Working AI automation in 60 seconds.

Not prompts you have to manually run. Automation that runs itself.
