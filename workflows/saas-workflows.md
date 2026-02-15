# SaaS Workflows - Production-Ready Automation Chains

Complete AI automation systems for SaaS operations. Each workflow includes the full prompt chain, system prompts, API integration code in Python and JavaScript, and expected outputs.

---

## Workflow 1: User Onboarding Email Sequence Generator

**What This Automates:** Analyzes your product features and generates a complete 7-email onboarding sequence with personalization logic based on user behavior.

**When to Use:** When launching a new product or redesigning onboarding. Alternative to hiring a copywriter for $2-5K.

### The Complete Chain

#### Step 1: Product Analysis System Prompt

```python
# System prompt for analyzing product and extracting key value props
PRODUCT_ANALYZER_SYSTEM = """You are a SaaS product marketing expert who analyzes products to identify:
1. Core value proposition (what problem it solves)
2. Key features mapped to user pain points
3. Critical "aha moments" (when users realize the value)
4. Common drop-off points in user journeys
5. Feature adoption sequence (what to learn first, second, third)

Output as structured JSON with clear feature-to-benefit mappings."""

# User provides product description
product_description = """
[Your product description, feature list, and target user persona]
"""
```

#### Step 2: Behavior Segmentation Prompt

```python
BEHAVIOR_SEGMENTATION_SYSTEM = """You are a growth marketing specialist who designs behavioral segmentation.
Given product features, create user segments based on signup behavior and engagement patterns.
Define trigger conditions for each email in the sequence."""

# This receives output from Step 1
segmentation_prompt = f"""
Based on this product analysis:
{step1_output}

Create 3-5 user segments with:
- Segment name and description
- Behavioral triggers (e.g., "Created project but didn't invite team")
- Email sequence modifications for each segment
- Expected conversion metrics
"""
```

#### Step 3: Email Sequence Generator

```python
EMAIL_SEQUENCE_SYSTEM = """You are an email marketing conversion specialist.
Write high-converting onboarding emails with:
- Compelling subject lines (A/B test variants)
- Personalized body copy
- Clear single CTA per email
- Social proof placement
- Specific product education

Format output as ready-to-use HTML email templates with merge tags."""

email_generation_prompt = f"""
Product context: {step1_output}
User segments: {step2_output}

Generate a 7-email onboarding sequence:

Day 0 (immediate): Welcome + quick win
Day 1: Feature spotlight #1 (core value)
Day 3: Feature spotlight #2 (expansion)
Day 5: Social proof + case study
Day 7: Activation push (based on segment)
Day 10: Power user tips
Day 14: Upgrade nudge (if free tier)

For each email provide:
- Subject line (2 variants for A/B testing)
- Preview text
- Body (HTML + plain text)
- CTA button text and link
- Personalization logic (merge tags)
"""
```

### Complete Automation Script (Python)

```python
# save as: onboarding_email_generator.py
import anthropic
import json
import os

class OnboardingEmailGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_analyze_product(self, product_description: str) -> dict:
        """Analyze product and extract key features and value props."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="""You are a SaaS product marketing expert who analyzes products to identify:
1. Core value proposition (what problem it solves)
2. Key features mapped to user pain points
3. Critical "aha moments" (when users realize the value)
4. Common drop-off points in user journeys
5. Feature adoption sequence (what to learn first, second, third)

Output as structured JSON.""",
            messages=[{
                "role": "user",
                "content": f"Analyze this product:\n\n{product_description}"
            }]
        )

        return json.loads(response.content[0].text)

    def step2_create_segments(self, product_analysis: dict) -> dict:
        """Create behavioral user segments."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            system="""You are a growth marketing specialist who designs behavioral segmentation.
Create user segments based on signup behavior and engagement patterns.
Output as JSON with trigger conditions.""",
            messages=[{
                "role": "user",
                "content": f"""Based on this product analysis:
{json.dumps(product_analysis, indent=2)}

Create 3-5 user segments with behavioral triggers and email modifications."""
            }]
        )

        return json.loads(response.content[0].text)

    def step3_generate_emails(self, product_analysis: dict, segments: dict) -> list:
        """Generate the complete email sequence."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            system="""You are an email marketing conversion specialist.
Write high-converting onboarding emails with compelling copy and clear CTAs.
Format as JSON array of email objects.""",
            messages=[{
                "role": "user",
                "content": f"""Product: {json.dumps(product_analysis, indent=2)}
Segments: {json.dumps(segments, indent=2)}

Generate a 7-email onboarding sequence with:
- Day 0: Welcome + quick win
- Day 1: Feature spotlight #1
- Day 3: Feature spotlight #2
- Day 5: Social proof
- Day 7: Activation push
- Day 10: Power tips
- Day 14: Upgrade nudge

For each: subject (2 variants), preview, HTML body, CTA, merge tags."""
            }]
        )

        return json.loads(response.content[0].text)

    def generate_complete_sequence(self, product_description: str) -> dict:
        """Run the complete workflow."""
        print("Step 1: Analyzing product...")
        product_analysis = self.step1_analyze_product(product_description)

        print("Step 2: Creating user segments...")
        segments = self.step2_create_segments(product_analysis)

        print("Step 3: Generating email sequence...")
        emails = self.step3_generate_emails(product_analysis, segments)

        return {
            "product_analysis": product_analysis,
            "segments": segments,
            "email_sequence": emails
        }

# Usage
if __name__ == "__main__":
    generator = OnboardingEmailGenerator(api_key=os.environ["ANTHROPIC_API_KEY"])

    product_desc = """
    ProjectHub is a project management tool for remote teams.
    Features: Kanban boards, time tracking, video standups, async updates.
    Target: 5-50 person remote-first companies.
    Pain point: Too many meetings, lack of async communication.
    """

    result = generator.generate_complete_sequence(product_desc)

    # Save to file
    with open("onboarding_emails.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"Generated {len(result['email_sequence'])} emails!")
```

### JavaScript/Node.js Version

```javascript
// save as: onboardingEmailGenerator.js
import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs/promises';

class OnboardingEmailGenerator {
  constructor(apiKey) {
    this.client = new Anthropic({ apiKey });
  }

  async step1AnalyzeProduct(productDescription) {
    const response = await this.client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 2000,
      system: `You are a SaaS product marketing expert who analyzes products to identify:
1. Core value proposition
2. Key features mapped to user pain points
3. Critical "aha moments"
4. Common drop-off points
5. Feature adoption sequence

Output as structured JSON.`,
      messages: [{
        role: 'user',
        content: `Analyze this product:\n\n${productDescription}`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async step2CreateSegments(productAnalysis) {
    const response = await this.client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1500,
      system: `You are a growth marketing specialist.
Create behavioral user segments with trigger conditions.
Output as JSON.`,
      messages: [{
        role: 'user',
        content: `Based on:\n${JSON.stringify(productAnalysis, null, 2)}\n\nCreate 3-5 segments.`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async step3GenerateEmails(productAnalysis, segments) {
    const response = await this.client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 4000,
      system: `Email marketing conversion specialist.
Write high-converting onboarding emails. Output as JSON array.`,
      messages: [{
        role: 'user',
        content: `Product: ${JSON.stringify(productAnalysis, null, 2)}
Segments: ${JSON.stringify(segments, null, 2)}

Generate 7-email sequence (Day 0, 1, 3, 5, 7, 10, 14) with subject variants, HTML, CTAs.`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async generateCompleteSequence(productDescription) {
    console.log('Step 1: Analyzing product...');
    const productAnalysis = await this.step1AnalyzeProduct(productDescription);

    console.log('Step 2: Creating segments...');
    const segments = await this.step2CreateSegments(productAnalysis);

    console.log('Step 3: Generating emails...');
    const emails = await this.step3GenerateEmails(productAnalysis, segments);

    return { productAnalysis, segments, emailSequence: emails };
  }
}

// Usage
const generator = new OnboardingEmailGenerator(process.env.ANTHROPIC_API_KEY);

const productDesc = `
ProjectHub is a project management tool for remote teams.
Features: Kanban boards, time tracking, video standups, async updates.
Target: 5-50 person remote-first companies.
Pain point: Too many meetings, lack of async communication.
`;

const result = await generator.generateCompleteSequence(productDesc);
await fs.writeFile('onboarding_emails.json', JSON.stringify(result, null, 2));
console.log(`Generated ${result.emailSequence.length} emails!`);
```

### Expected Output Structure

```json
{
  "product_analysis": {
    "value_proposition": "Replace synchronous meetings with async updates",
    "aha_moments": [
      "First async standup video recorded and watched by team",
      "Full week with zero status meetings"
    ],
    "feature_sequence": ["kanban_board", "async_updates", "video_standups", "time_tracking"]
  },
  "segments": [
    {
      "name": "Solo Explorer",
      "trigger": "Signed up but hasn't invited team",
      "email_modifications": "Emphasize team invite CTA in day 1-3 emails"
    }
  ],
  "email_sequence": [
    {
      "day": 0,
      "subject_a": "Welcome to ProjectHub - Your first async standup in 60 seconds",
      "subject_b": "You're in! Let's eliminate your next status meeting",
      "preview": "Record your first update in under a minute...",
      "html_body": "<html>...</html>",
      "cta": "Record Your First Update",
      "merge_tags": ["{{first_name}}", "{{company_name}}"]
    }
  ]
}
```

### Integration with Email Service Providers

```python
# Integration with SendGrid, Mailchimp, or Customer.io
def upload_to_sendgrid(email_sequence: list, api_key: str):
    """Upload generated emails to SendGrid automation."""
    import sendgrid
    from sendgrid.helpers.mail import Mail

    sg = sendgrid.SendGridAPIClient(api_key=api_key)

    for idx, email in enumerate(email_sequence):
        # Create automation template
        template_data = {
            "name": f"Onboarding Day {email['day']}",
            "subject": email["subject_a"],  # Use A variant as default
            "html_content": email["html_body"],
            "generation": "dynamic"
        }
        # Upload via SendGrid API
        response = sg.client.templates.post(request_body=template_data)
        print(f"Created template {email['day']}: {response.status_code}")
```

---

## Workflow 2: Support Ticket Auto-Categorization & Routing

**What This Automates:** Reads incoming support tickets, categorizes by urgency/type, extracts key info, and routes to the right team with a drafted response.

**When to Use:** When support volume exceeds 50 tickets/day. Alternative to hiring a support ops person.

### The Complete Chain

#### Step 1: Ticket Analysis System Prompt

```python
TICKET_ANALYZER_SYSTEM = """You are a customer support operations specialist.
Analyze support tickets to extract:
1. Issue category (bug, feature request, billing, how-to, integration, other)
2. Urgency (critical/high/medium/low)
3. Product area affected
4. Customer sentiment (angry, frustrated, neutral, happy)
5. Whether ticket contains PII or sensitive data

Output as structured JSON."""
```

#### Step 2: Knowledge Base Search Prompt

```python
KB_SEARCH_SYSTEM = """You are a support agent with access to the knowledge base.
Given a categorized ticket, search for relevant help articles and past solutions.
Return the top 3 most relevant resources with confidence scores."""
```

#### Step 3: Response Drafter Prompt

```python
RESPONSE_DRAFTER_SYSTEM = """You are a senior customer support agent known for empathetic, clear responses.
Draft a response that:
- Acknowledges the customer's frustration
- Provides a solution or next steps
- Includes links to relevant help docs
- Sets clear expectations (timeline, escalation)
- Maintains brand voice: friendly but professional

Never promise what engineering can't deliver. Always verify before claiming a bug is fixed."""
```

### Complete Automation Script

```python
# save as: support_ticket_automation.py
import anthropic
import json
import os
from typing import Dict, List

class SupportTicketAutomation:
    def __init__(self, api_key: str, knowledge_base: List[Dict] = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.kb = knowledge_base or []

    def step1_analyze_ticket(self, ticket_text: str, customer_context: Dict) -> Dict:
        """Categorize and extract metadata from ticket."""
        prompt = f"""Ticket from {customer_context.get('email')}:
Plan: {customer_context.get('plan', 'Free')}
Account age: {customer_context.get('account_age_days')} days

Ticket content:
{ticket_text}

Analyze and return JSON."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=800,
            system="""Analyze support tickets. Extract: category, urgency, product_area,
sentiment, has_pii (boolean). Output as JSON.""",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_search_knowledge_base(self, ticket_analysis: Dict) -> List[Dict]:
        """Search KB for relevant articles."""
        # In production, this would query your actual KB (Zendesk, Notion, etc.)
        # Here we use Claude to simulate semantic search
        kb_context = "\n".join([
            f"Article {i+1}: {art['title']} - {art['summary']}"
            for i, art in enumerate(self.kb[:20])  # Top 20 articles
        ])

        prompt = f"""Ticket analysis: {json.dumps(ticket_analysis)}

Knowledge base:
{kb_context}

Return top 3 most relevant articles as JSON array with: article_id, title, relevance_score (0-1)"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            system="You are a semantic search engine for support content.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step3_draft_response(
        self,
        ticket_text: str,
        analysis: Dict,
        kb_articles: List[Dict],
        customer_context: Dict
    ) -> Dict:
        """Draft a complete support response."""
        prompt = f"""Customer: {customer_context.get('name')} ({customer_context.get('email')})
Plan: {customer_context.get('plan')}
Sentiment: {analysis.get('sentiment')}
Category: {analysis.get('category')}

Their message:
{ticket_text}

Relevant help articles:
{json.dumps(kb_articles, indent=2)}

Draft a response that solves their issue. Include:
- Empathetic opening
- Clear solution or next steps
- Links to articles
- Timeline expectations

Output as JSON with: subject, body_text, body_html, suggested_tags, escalate_to_engineering (boolean)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1200,
            system="""Senior support agent. Write empathetic, solution-focused responses.
Never over-promise. Set clear expectations. Brand voice: friendly but professional.""",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def process_ticket(self, ticket_text: str, customer_context: Dict) -> Dict:
        """Complete automation workflow."""
        print("Step 1: Analyzing ticket...")
        analysis = self.step1_analyze_ticket(ticket_text, customer_context)

        print(f"Category: {analysis['category']}, Urgency: {analysis['urgency']}")

        print("Step 2: Searching knowledge base...")
        kb_articles = self.step2_search_knowledge_base(analysis)

        print("Step 3: Drafting response...")
        response_draft = self.step3_draft_response(
            ticket_text, analysis, kb_articles, customer_context
        )

        return {
            "analysis": analysis,
            "recommended_articles": kb_articles,
            "draft_response": response_draft,
            "routing": self._determine_routing(analysis)
        }

    def _determine_routing(self, analysis: Dict) -> Dict:
        """Determine which team should handle this ticket."""
        urgency = analysis.get('urgency')
        category = analysis.get('category')

        if urgency == 'critical':
            return {"team": "engineering", "sla_hours": 2}
        elif category == 'billing':
            return {"team": "billing", "sla_hours": 4}
        elif category == 'bug':
            return {"team": "engineering", "sla_hours": 24}
        else:
            return {"team": "support", "sla_hours": 12}

# Usage
if __name__ == "__main__":
    # Sample knowledge base
    kb = [
        {"id": 1, "title": "How to reset password", "summary": "Guide for password reset flow"},
        {"id": 2, "title": "Integrating with Slack", "summary": "Step-by-step Slack integration"},
        {"id": 3, "title": "Billing FAQ", "summary": "Common billing questions answered"}
    ]

    automation = SupportTicketAutomation(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        knowledge_base=kb
    )

    ticket = """Subject: Can't connect Slack integration - getting 403 error

I've tried following the docs but when I click 'Connect Slack' I get a 403 Forbidden error.
This is blocking my entire team from using the product. We're on the Pro plan and this
is extremely frustrating. Please help ASAP!"""

    customer = {
        "name": "Sarah Chen",
        "email": "sarah@acmecorp.com",
        "plan": "Pro",
        "account_age_days": 12
    }

    result = automation.process_ticket(ticket, customer)

    print("\n" + "="*50)
    print("AUTOMATION RESULT")
    print("="*50)
    print(f"Category: {result['analysis']['category']}")
    print(f"Urgency: {result['analysis']['urgency']}")
    print(f"Route to: {result['routing']['team']} (SLA: {result['routing']['sla_hours']}h)")
    print(f"\nDraft response:\n{result['draft_response']['body_text']}")
```

### Expected Output

```json
{
  "analysis": {
    "category": "integration",
    "urgency": "high",
    "product_area": "slack_integration",
    "sentiment": "frustrated",
    "has_pii": false
  },
  "recommended_articles": [
    {
      "article_id": 2,
      "title": "Integrating with Slack",
      "relevance_score": 0.95
    }
  ],
  "draft_response": {
    "subject": "Re: Slack integration 403 error - investigating now",
    "body_text": "Hi Sarah,\n\nI'm sorry you're running into this 403 error...",
    "escalate_to_engineering": true
  },
  "routing": {
    "team": "engineering",
    "sla_hours": 2
  }
}
```

---

## Workflow 3: Feature Request Analysis & Prioritization

**What This Automates:** Aggregates feature requests from multiple sources, deduplicates, extracts themes, and generates a RICE-scored prioritization report.

**When to Use:** When you have 50+ feature requests scattered across email, support tickets, and feedback tools.

### Complete Script

```python
# save as: feature_request_analyzer.py
import anthropic
import json
from collections import defaultdict
from typing import List, Dict

class FeatureRequestAnalyzer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_deduplicate_and_cluster(self, requests: List[Dict]) -> Dict:
        """Group similar feature requests."""
        requests_text = "\n\n".join([
            f"Request {i+1} (from {r['source']}): {r['text']}"
            for i, r in enumerate(requests)
        ])

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="""You are a product analyst who identifies patterns in feature requests.
Group similar requests together, extract the core user need, and identify request themes.
Output as JSON with: clusters (array), each containing: theme, core_need, request_ids (array), user_count.""",
            messages=[{"role": "user", "content": f"Analyze these requests:\n{requests_text}"}]
        )

        return json.loads(response.content[0].text)

    def step2_rice_scoring(self, clusters: Dict, product_context: Dict) -> List[Dict]:
        """Apply RICE framework to each cluster."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="""You are a product strategist applying RICE scoring.
For each feature cluster, estimate:
- Reach: users affected per quarter
- Impact: 0.25/0.5/1/2/3 (minimal to massive)
- Confidence: 50/80/100%
- Effort: person-weeks

Calculate RICE score: (Reach * Impact * Confidence) / Effort
Output as JSON array sorted by RICE score descending.""",
            messages=[{"role": "user", "content": f"""Product context:
{json.dumps(product_context, indent=2)}

Feature clusters:
{json.dumps(clusters, indent=2)}

Score each cluster using RICE framework."""}]
        )

        return json.loads(response.content[0].text)

    def step3_generate_prd_outline(self, top_feature: Dict) -> str:
        """Generate PRD outline for the top-scoring feature."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            system="""Product manager writing PRD outlines. Include: problem statement,
proposed solution, success metrics, user stories, technical considerations.""",
            messages=[{"role": "user", "content": f"Create PRD outline for:\n{json.dumps(top_feature)}"}]
        )

        return response.content[0].text

    def analyze(self, requests: List[Dict], product_context: Dict) -> Dict:
        """Run complete analysis."""
        print("Step 1: Clustering requests...")
        clusters = self.step1_deduplicate_and_cluster(requests)
        print(f"Found {len(clusters['clusters'])} unique feature themes")

        print("Step 2: RICE scoring...")
        scored = self.step2_rice_scoring(clusters, product_context)

        print("Step 3: Generating PRD outline for top feature...")
        prd = self.step3_generate_prd_outline(scored[0])

        return {
            "clusters": clusters,
            "prioritized_features": scored,
            "top_feature_prd": prd
        }

# Usage
if __name__ == "__main__":
    analyzer = FeatureRequestAnalyzer(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Sample feature requests from various sources
    requests = [
        {"source": "support_ticket", "text": "Can we export reports to PDF?"},
        {"source": "email", "text": "Would love PDF export for our reports"},
        {"source": "in_app_survey", "text": "Need dark mode please!"},
        {"source": "sales_call", "text": "Customers asking for team workspaces"},
        {"source": "support_ticket", "text": "Can multiple people collaborate in real-time?"},
    ]

    product_ctx = {
        "active_users": 50000,
        "team_size": 8,
        "current_quarter_goal": "Improve retention from 78% to 85%"
    }

    result = analyzer.analyze(requests, product_ctx)
    print(json.dumps(result, indent=2))
```

---

## Workflow 4: Changelog Generation from Git Commits

**What This Automates:** Reads git commits, groups by feature/fix/improvement, generates user-facing release notes in multiple formats (blog, in-app, email, social).

**When to Use:** Every release cycle instead of manually writing release notes.

### Complete Script

```python
# save as: changelog_generator.py
import anthropic
import subprocess
import json
from typing import List, Dict

class ChangelogGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def get_commits_since_tag(self, since_tag: str = None) -> List[str]:
        """Fetch git commits since last tag."""
        if since_tag:
            cmd = f"git log {since_tag}..HEAD --pretty=format:'%s|||%b|||%an'"
        else:
            # Last 50 commits if no tag
            cmd = "git log -50 --pretty=format:'%s|||%b|||%an'"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        commits = result.stdout.strip().split('\n')

        return [c for c in commits if c]  # Filter empty

    def step1_categorize_commits(self, commits: List[str]) -> Dict:
        """Categorize commits into user-facing changes."""
        commits_text = "\n".join([f"{i+1}. {c}" for i, c in enumerate(commits)])

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            system="""You are a technical writer converting git commits to user-facing features.

Categorize into:
- new_features: New functionality users can access
- improvements: Enhancements to existing features
- bug_fixes: Resolved issues
- skip: Internal refactoring, dependency updates, etc. (not user-facing)

For each user-facing change, write a user-friendly headline (benefit, not technical detail).
Output as JSON.""",
            messages=[{"role": "user", "content": f"Categorize these commits:\n{commits_text}"}]
        )

        return json.loads(response.content[0].text)

    def step2_generate_release_notes(self, categorized: Dict, version: str) -> Dict:
        """Generate release notes in multiple formats."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2500,
            system="""You are a product marketer writing release notes.
Create:
1. Blog post format (Markdown, detailed, with examples)
2. In-app changelog (5-7 bullets, under 15 words each)
3. Email announcement (subject line, body, CTA)
4. Tweet (280 chars, highlights top feature)

Focus on user benefits, not implementation. Use active voice.""",
            messages=[{"role": "user", "content": f"""Version {version} changes:
{json.dumps(categorized, indent=2)}

Generate all 4 formats. Output as JSON."""}]
        )

        return json.loads(response.content[0].text)

    def generate(self, since_tag: str = None, version: str = "1.0.0") -> Dict:
        """Complete changelog generation."""
        print(f"Fetching commits since {since_tag or 'last 50'}...")
        commits = self.get_commits_since_tag(since_tag)
        print(f"Found {len(commits)} commits")

        print("Step 1: Categorizing commits...")
        categorized = self.step1_categorize_commits(commits)

        print("Step 2: Generating release notes...")
        release_notes = self.step2_generate_release_notes(categorized, version)

        return {
            "version": version,
            "raw_commits": len(commits),
            "categorized_changes": categorized,
            "release_notes": release_notes
        }

# Usage
if __name__ == "__main__":
    generator = ChangelogGenerator(api_key=os.environ["ANTHROPIC_API_KEY"])

    result = generator.generate(since_tag="v2.1.0", version="v2.2.0")

    # Save blog post
    with open("CHANGELOG.md", "w") as f:
        f.write(result["release_notes"]["blog_post"])

    # Save for email
    with open("release_email.json", "w") as f:
        json.dump(result["release_notes"]["email"], f, indent=2)

    print("Release notes generated!")
```

### Expected Output

```json
{
  "version": "v2.2.0",
  "release_notes": {
    "blog_post": "# Release Notes: v2.2.0\n\n## What's New\n\n### Find anything instantly with Smart Search\n...",
    "in_app_changelog": [
      "Smart Search now understands typos and filters",
      "PDF export for all reports",
      "Dashboard loads 2x faster"
    ],
    "email": {
      "subject": "New in v2.2: Smart Search + PDF Export",
      "body": "...",
      "cta": "See What's New"
    },
    "tweet": "v2.2 is live! Smart Search (with typo tolerance), PDF export, and 2x faster dashboards. Ship it."
  }
}
```

---

## When to Use SaaS Workflows vs. Alternatives

| Use This Library When... | Use Alternatives When... |
|---|---|
| You have <100K users (automation ROI isn't huge yet) | You have >500K users (build custom ML models) |
| Your team is <20 people (no dedicated ops roles) | You have dedicated support ops, growth, and marketing teams |
| You ship weekly/biweekly (need fast turnaround) | You ship quarterly (can hire contractors per release) |
| You're bootstrapped (cash-conscious) | You're series B+ (hire full teams) |

**Cost comparison:**
- Onboarding copywriter: $2-5K per sequence
- Support ops hire: $60-80K/year
- This workflow library: $19 one-time + $50-200/month API costs
