# PromptVault Examples

Ready-to-run AI automation workflows across 4 categories.

## Quick Start (60 seconds)

1. **Install dependencies:**
   ```bash
   pip install anthropic gitpython  # Python examples
   npm install @anthropic-ai/sdk    # JavaScript examples
   ```

2. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY='your-key-here'
   ```

3. **Run an example:**
   ```bash
   # Generate blog outline
   node content-blog-outline.js "Best React frameworks 2026"

   # Review your staged git changes
   python dev-code-review-automation.py

   # Generate onboarding email
   python saas-onboarding-email.py --user-data data/user-sample.json

   # Prioritize feature backlog
   python business-feature-prioritization.py --features data/features-sample.json
   ```

That's it. Working AI automation in under 60 seconds.

## Available Workflows

### SaaS Workflows
- **saas-onboarding-email.py** - Generate personalized onboarding emails based on user signup data

### Content Workflows
- **content-blog-outline.js** - SEO-optimized blog post outlines with keyword research

### Development Workflows
- **dev-code-review-automation.py** - Automated code review on git diffs (pre-commit checks)

### Business Workflows
- **business-feature-prioritization.py** - RICE scoring and prioritization for feature requests

## Example Data

The `data/` directory contains sample JSON files for testing:
- `user-sample.json` - Sample user signup data
- `features-sample.json` - Sample feature requests with product context

## Customization

Each script is designed to be modified:
- Change the prompts to match your brand voice
- Add streaming support for real-time output
- Pipe output to other tools (Notion API, Linear, email services)
- Chain multiple workflows together

## Requirements

**Python workflows:**
```bash
pip install anthropic gitpython
```

**JavaScript workflows:**
```bash
npm install @anthropic-ai/sdk
```

**API Key:**
Get your Anthropic API key at https://console.anthropic.com/

## What Makes These Different

These aren't just prompts. They're complete automation pipelines:
- CLI interfaces with argument parsing
- File I/O and data handling
- Git integration (for dev workflows)
- Error handling
- Formatted output

Copy the script. Add your API key. Run it. That's the PromptVault difference.
