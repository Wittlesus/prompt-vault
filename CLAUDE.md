# PromptVault

## Overview
AI Workflow Library for developers: 64 production-ready prompts + 4 complete automation workflows with ready-to-run code (Python + JavaScript). Sold at $19.

## Tech Stack
- **Prompts:** Markdown files (no framework, no dependencies)
- **Workflows:** Python 3 + Node.js with Anthropic SDK
- **Distribution:** Git repo / digital download

## Key Commands
- No build or dev commands -- this is a content product
- Preview markdown with any editor or `npx markserv .` for local preview

## Project Structure
- `prompts/` -- All 64 prompts organized by category (7 files)
  - `code-review.md` -- 10 code review prompts
  - `documentation.md` -- 10 documentation prompts
  - `testing.md` -- 10 testing prompts
  - `debugging.md` -- 10 debugging prompts
  - `devops.md` -- 8 DevOps prompts
  - `database.md` -- 8 database prompts
  - `product.md` -- 8 product development prompts
- `examples/` -- Ready-to-run workflow automation (NEW)
  - `python/` -- 4 Python workflows using Anthropic SDK
  - `javascript/` -- 4 JavaScript workflows using Anthropic SDK
  - `cli/` -- Shell script wrappers for easy CLI usage
  - `README.md` -- Complete workflow documentation
- `README.md` -- Product documentation and usage guide
- `GUMROAD_LISTING.md` -- Sales copy and listing details

## Key Files
- `prompts/*.md` -- The actual prompt library (7 category files, 64 prompts total)
- `examples/python/*.py` -- 4 production-ready Python workflows (content_pipeline, support_classifier, code_reviewer, competitor_analyzer)
- `examples/javascript/*.js` -- Same 4 workflows in JavaScript
- `examples/cli/*.sh` -- Shell wrappers for CLI usage
- `examples/README.md` -- Complete workflow documentation with setup, usage, customization
- `README.md` -- Product overview and usage instructions

## Stripe Integration
- Payment link: `buy.stripe.com/3cI6oG5iJ8hA93m4xk08g04` ($19)
- No runtime Stripe integration (digital product, one-time purchase)

## Notes
- Each prompt follows a consistent structure: title, use case, prompt text, example output, customization tips
- Prompts are model-agnostic (Claude, ChatGPT, Gemini, etc.)
- **NEW:** Examples directory contains production-ready code using Anthropic Claude API (claude-sonnet-4-5-20250929)
- All workflows support streaming output, error handling, stdin/file input
- Each workflow is a complete pipeline (e.g., content_pipeline: outline → draft → SEO → social posts)
- Single purchase covers entire team usage
- Repo: github.com/Wittlesus/prompt-vault
