# Product Development Prompts

A collection of 8 battle-tested prompts for product development tasks. From user stories to competitive analysis, accelerate your product thinking with AI.

---

## 1. User Story Writer

**Use Case:** Transform vague feature ideas into well-structured user stories with acceptance criteria, edge cases, and technical notes.

**Prompt:**

```
You are a senior product manager who writes exceptionally clear user stories that both designers and engineers love.

Transform the following feature idea into complete user stories:

## Feature Idea
"""
[DESCRIBE THE FEATURE IN PLAIN LANGUAGE]
"""

## For Each User Story, Provide:

### Story Format
**As a** [specific user persona],
**I want** [concrete action],
**So that** [measurable business/user value].

### Acceptance Criteria (Gherkin format)
```
GIVEN [precondition]
WHEN [action]
THEN [expected result]
AND [additional outcomes]
```

### Edge Cases & Error States
- What happens when [unusual scenario]?
- What if the user [unexpected action]?
- What about [accessibility, offline, slow network]?

### Design Notes
- Key UI considerations
- Mobile vs desktop behavior differences
- Loading, empty, and error states

### Technical Notes
- API endpoints implied
- Data model changes needed
- Third-party integrations
- Performance considerations

### Out of Scope (explicitly)
- What this story does NOT include
- What's being deferred to future iterations

### Story Points Estimate
- Complexity: [1-13 Fibonacci scale]
- Justification for the estimate

## Rules:
- One story = one deployable unit of work
- Break large features into 3-7 stories that can be shipped independently
- Each story should deliverable value to users on its own
- Acceptance criteria must be testable (a QA engineer can verify pass/fail)
- Include the "sad path" (error handling) not just the "happy path"
```

**Example Output Snippet:**

```markdown
## User Story 1: Basic Search

**As a** registered user,
**I want** to search products by name or description,
**So that** I can quickly find what I'm looking for without browsing categories.

### Acceptance Criteria

```gherkin
Scenario: Basic keyword search
  GIVEN I am on any page of the application
  WHEN I type "wireless headphones" in the search bar and press Enter
  THEN I see a results page with products matching "wireless headphones"
  AND results are sorted by relevance (best match first)
  AND each result shows: product image, name, price, and average rating
  AND I see the total number of results (e.g., "42 results for 'wireless headphones'")

Scenario: No results found
  GIVEN I search for "xyznonexistent123"
  WHEN the results page loads
  THEN I see a friendly "No products found" message
  AND I see 3-5 suggested alternative searches
  AND I see a "Browse Categories" CTA

Scenario: Empty search
  GIVEN I click the search button without typing anything
  THEN the search bar is focused with a prompt "What are you looking for?"
  AND I see recent searches and popular searches below the bar
```

### Edge Cases
- Search with special characters (`"wireless" headphones`, `O'Brien`)
- Very long search queries (300+ characters) - truncate at 200
- Search while results are still loading from previous search
- Mobile: search triggers on "Go" keyboard button

### Technical Notes
- API: `GET /api/search?q=wireless+headphones&page=1&limit=20`
- Consider Elasticsearch or Algolia for full-text search
- Debounce search input by 300ms for typeahead
- Cache popular search results (TTL: 5 minutes)

### Out of Scope
- Autocomplete/typeahead suggestions (Story #2)
- Filters and faceted search (Story #3)
- Voice search (v2)

### Story Points: 5
Justification: Search UI is straightforward, but backend search infrastructure
(Elasticsearch setup, indexing pipeline) adds complexity.
```

**Tips for Customization:**
- Add your personas: "Our users are: Developer Dan, Manager Maria, Admin Alex"
- Specify: "Include localization requirements (we support 12 languages)"
- Add: "We follow WCAG 2.1 AA accessibility standards"

---

## 2. PRD (Product Requirements Document) Creator

**Use Case:** Generate a comprehensive Product Requirements Document from a feature concept, ready for design and engineering review.

**Prompt:**

```
You are a senior product manager at a top tech company writing a PRD that will align designers, engineers, and stakeholders.

Create a complete PRD for the following feature:

## Feature Concept
"""
[DESCRIBE: What, why, for whom, and roughly how]
"""

## PRD Structure:

### 1. Overview
- **Problem Statement**: What user/business problem does this solve? (Use data if available)
- **Proposed Solution**: One-paragraph summary of what we're building
- **Success Metrics**: 3-5 measurable KPIs with targets
- **Target Users**: Specific personas with their pain points

### 2. Goals & Non-Goals
| Goals (What we ARE doing) | Non-Goals (What we are NOT doing) |
|---------------------------|-----------------------------------|

### 3. User Research Summary
- Key findings from user interviews/surveys (real or hypothesized)
- User quotes that illustrate the problem
- Current workarounds users employ

### 4. Detailed Requirements
Group by user workflow:

**Flow 1: [Name]**
| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| R1 | ... | Must have | |
| R2 | ... | Should have | |
| R3 | ... | Nice to have | |

### 5. User Experience
- Key screens/states described in detail
- Interaction patterns and transitions
- Error handling and edge cases
- Accessibility requirements

### 6. Technical Considerations
- Architecture implications
- API contracts (high-level)
- Data model changes
- Third-party dependencies
- Performance requirements (latency, throughput)
- Security implications

### 7. Launch Plan
- **Phase 1 (MVP)**: Minimum to validate the hypothesis
- **Phase 2**: Full feature based on Phase 1 learnings
- **Phase 3**: Scale and optimize
- Feature flag strategy
- Rollout plan (% of users)

### 8. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|

### 9. Open Questions
- Decisions that need stakeholder input
- Technical unknowns that need spikes

### 10. Timeline
- Design: X weeks
- Engineering: Y weeks
- QA: Z weeks
- Launch target: [date]
```

**Example Output Snippet:**

```markdown
# PRD: Team Workspace Collaboration

**Author**: [PM Name] | **Status**: Draft | **Last Updated**: 2025-01-15

## 1. Overview

### Problem Statement
Currently, 67% of our users (based on Q4 survey, n=2,400) report that sharing
work with teammates requires leaving our platform (copying to Slack, email, or
Google Docs). This leads to:
- 23% of shared items becoming stale within 24 hours
- Users spending 15 min/day on manual cross-platform sharing
- Teams having no single source of truth for project decisions

### Proposed Solution
Add real-time collaborative workspaces where team members can share, comment on,
and jointly edit documents within our platform. Think "Google Docs meets project
management."

### Success Metrics
| Metric | Current | Target (3 months post-launch) |
|--------|---------|-------------------------------|
| Items shared per user per week | 2.1 (external tools) | 8+ (in-platform) |
| Time spent on cross-platform sharing | 15 min/day | <3 min/day |
| Team feature adoption | N/A | 40% of teams with 3+ members |
| NPS for collaboration | 22 | 45+ |
| User retention (teams using workspaces) | 78% (baseline) | 90%+ |

### 2. Goals & Non-Goals

| Goals | Non-Goals |
|-------|-----------|
| Real-time collaborative editing | Full-featured document editor (not competing with Google Docs) |
| Team activity feed and notifications | Video/voice calling |
| Permission-based sharing (view/edit/admin) | Public sharing outside organization |
| Works on mobile (view + comment) | Mobile editing (Phase 2) |
```

**Tips for Customization:**
- Include real user research data if available
- Specify: "This PRD needs to be approved by VP of Engineering and VP of Product"
- Add: "Include competitive analysis section comparing our approach to [competitors]"

---

## 3. Competitive Analysis Framework

**Use Case:** Generate a structured competitive analysis comparing your product to competitors across features, pricing, positioning, and strategy.

**Prompt:**

```
You are a product strategist conducting a thorough competitive analysis.

## Our Product
"""
[DESCRIBE: What you build, for whom, key differentiators, pricing]
"""

## Competitors to Analyze
"""
[LIST: 3-5 competitors with brief descriptions]
"""

## Analysis Framework:

### 1. Feature Comparison Matrix
| Feature | Our Product | Competitor A | Competitor B | Competitor C |
|---------|-------------|-------------|-------------|-------------|
| [Feature 1] | Score (1-5) + notes | Score + notes | Score + notes | Score + notes |
Score: 1=Not available, 2=Basic, 3=Adequate, 4=Good, 5=Best in class

### 2. Positioning Map
Describe where each product sits on two key axes:
- X-axis: [e.g., Simplicity ←→ Power]
- Y-axis: [e.g., Individual ←→ Enterprise]

### 3. Pricing Analysis
| | Our Product | Competitor A | Competitor B |
|---|---|---|---|
| Free tier | | | |
| Entry price | | | |
| Enterprise price | | | |
| Pricing model | | | |
| Value for money | | | |

### 4. SWOT for Each Competitor
- Strengths (what they do better than us)
- Weaknesses (where they fall short)
- Opportunities (gaps we can exploit)
- Threats (what could hurt us)

### 5. Go-to-Market Comparison
- Target audience differences
- Marketing channels used
- Sales motion (self-serve vs sales-led)
- Content strategy
- Community/ecosystem

### 6. Strategic Recommendations
- Where to compete head-on
- Where to differentiate
- Where to concede
- Features to prioritize based on competitive gaps
- Positioning adjustments

### 7. Monitoring Plan
- Key competitor moves to watch for
- Metrics to track quarterly
- Review cadence
```

**Example Output Snippet:**

```markdown
## Feature Comparison: Project Management Tools

| Feature | Acme (Us) | Linear | Jira | Asana |
|---------|-----------|--------|------|-------|
| Issue tracking | 4 - Solid basics | 5 - Best UX | 5 - Most powerful | 4 - Good |
| Sprint planning | 3 - Basic boards | 5 - Cycles are excellent | 5 - Gold standard | 2 - Limited |
| Roadmapping | 2 - Manual only | 4 - Built-in | 3 - Via Advanced Roadmaps ($$) | 4 - Timeline view |
| Git integration | 5 - Deep integration | 5 - Excellent | 4 - Good | 2 - Basic |
| API/Extensibility | 4 - REST + webhooks | 4 - GraphQL | 5 - Marketplace ecosystem | 3 - Limited API |
| Ease of setup | 5 - <5 min | 5 - <5 min | 2 - Days for enterprise | 4 - ~15 min |
| Mobile app | 2 - View only | 3 - Basic editing | 3 - Functional | 4 - Full featured |
| Pricing (per user) | $8/mo | $10/mo | $7.75/mo (Standard) | $10.99/mo |

## Strategic Recommendations

### Compete Head-On (our strengths)
- **Git integration**: We're already best-in-class. Double down with GitLab/Bitbucket.
- **Setup simplicity**: Our 5-minute setup is a key sales driver. Never compromise it.

### Differentiate (unique territory)
- **Developer experience**: Neither Asana nor Jira feels like a dev tool. Linear does,
  but we can beat them with deeper CI/CD integration.
- **AI-powered triage**: None of the competitors auto-categorize and prioritize bugs.
  This is a blue-ocean feature.

### Concede (not worth fighting)
- **Enterprise admin features**: Jira's 20 years of enterprise tooling can't be matched
  in 6 months. Focus on <500 person companies.
- **Marketing project management**: Asana owns this. Not our target user.
```

**Tips for Customization:**
- Include links to competitor websites for accurate pricing
- Add: "Include analysis of their recent product launches (last 6 months)"
- Specify: "Focus on the developer tools market segment"

---

## 4. Feature Prioritization Framework

**Use Case:** Apply structured prioritization frameworks (RICE, MoSCoW, ICE, etc.) to a backlog of feature ideas.

**Prompt:**

```
You are a product strategy expert who helps teams prioritize ruthlessly and ship the right things.

## Current Product Context
"""
[DESCRIBE: Product stage, company goals this quarter, team size, key metrics to move]
"""

## Features to Prioritize
"""
[LIST: 10-20 feature ideas with brief descriptions]
"""

## Apply These Frameworks:

### 1. RICE Scoring
For each feature:
- **Reach**: How many users affected per quarter? (# of users)
- **Impact**: How much will it move the key metric? (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
- **Confidence**: How sure are we about the estimates? (100%/80%/50%)
- **Effort**: Person-weeks to build (including design, eng, QA)
- **RICE Score**: (Reach * Impact * Confidence) / Effort

### 2. Value vs Effort Matrix
Plot each feature on:
- X-axis: Effort (weeks)
- Y-axis: Value (composite of user value + business value)
Categorize into: Quick Wins, Big Bets, Fill-Ins, Money Pits

### 3. MoSCoW Classification
- **Must Have**: Ship will fail without this
- **Should Have**: Important but not a showstopper
- **Could Have**: Nice to have if time permits
- **Won't Have**: Explicitly not doing this iteration

### 4. Strategic Alignment
For each feature, score against company priorities:
| Feature | Revenue | Retention | Acquisition | Tech Debt | Total |
| Weight: | 30% | 30% | 25% | 15% | 100% |

### 5. Final Recommendation
- **Build Now** (this sprint/quarter): Top 3-5 features with rationale
- **Build Next** (next quarter): 3-5 features to start planning
- **Revisit Later**: Features that aren't worth the investment right now
- **Kill**: Features to explicitly remove from the backlog
```

**Example Output Snippet:**

```markdown
## RICE Scoring Results

| # | Feature | Reach | Impact | Confidence | Effort | RICE | Rank |
|---|---------|-------|--------|------------|--------|------|------|
| 1 | Search improvements | 50,000 | 2 | 80% | 3 wks | 26,667 | 1 |
| 2 | Dark mode | 30,000 | 0.5 | 100% | 2 wks | 7,500 | 4 |
| 3 | Team workspaces | 10,000 | 3 | 50% | 8 wks | 1,875 | 6 |
| 4 | Export to PDF | 40,000 | 1 | 80% | 1 wk | 32,000 | Highest! |
| 5 | AI auto-categorize | 20,000 | 2 | 50% | 4 wks | 5,000 | 5 |
| 6 | Mobile app v2 | 25,000 | 2 | 80% | 12 wks | 3,333 | 7 |

## Value vs Effort Matrix

```
High Value │ 🎯 Big Bets          │ ⚡ Quick Wins
           │ Team Workspaces      │ PDF Export
           │ Mobile App v2        │ Search Improvements
           │                      │ AI Auto-categorize
           ├──────────────────────┼──────────────────────
Low Value  │ 💰 Money Pits        │ 📝 Fill-Ins
           │ Custom Themes        │ Dark Mode
           │ Desktop App          │ Keyboard Shortcuts
           │ (avoid these)        │ (do if time permits)
           └──────────────────────┴──────────────────────
             High Effort            Low Effort
```

## Final Recommendation

### Build Now (Q1)
1. **PDF Export** (RICE: 32K) - Highest RICE score, lowest effort. Many users
   requesting this, and it blocks enterprise deals.
2. **Search Improvements** (RICE: 27K) - Direct impact on core product
   experience. Current search has 15% "no results" rate.
3. **AI Auto-categorize** (RICE: 5K) - Unique differentiator. Even at 50%
   confidence, the competitive advantage justifies the bet.

### Kill
- **Custom Themes** - Only 2% of users requested. High effort, no business impact.
- **Desktop App** - Web app covers 98% of use cases. Maintaining another
  platform isn't worth it at our stage.
```

**Tips for Customization:**
- Include real user request data: "Export to PDF has 340 upvotes on our feedback board"
- Add: "We need to consider technical dependencies (Feature X requires Feature Y first)"
- Specify: "Our company OKR is to improve retention from 78% to 85% this quarter"

---

## 5. Release Notes Writer

**Use Case:** Transform engineering changelogs and PR descriptions into user-friendly release notes that customers actually want to read.

**Prompt:**

```
You are a product marketer who writes release notes that users actually read and get excited about.

## Raw Input (engineering changelog)
"""
[PASTE: git log, PR titles/descriptions, or internal changelog]
"""

## Generate Release Notes In These Formats:

### 1. Full Release Notes (Blog/Docs)
For each significant change:
- **User-friendly headline** (benefit, not technical description)
  - Bad: "Implement WebSocket reconnection logic"
  - Good: "Real-time updates now reconnect automatically if your connection drops"
- **Why it matters**: 1-2 sentences from the user's perspective
- **How to use it**: Brief instructions or link to docs
- **Screenshot/GIF placeholder**: Describe what visual would help

### 2. Short Changelog (In-App)
- 5-7 bullet points, each under 15 words
- Lead with the most exciting change
- Group: New, Improved, Fixed

### 3. Social Media Post
- Twitter/X version (280 chars)
- LinkedIn version (longer, more professional)

### 4. Email Announcement
- Subject line (A/B test two options)
- Preview text
- Body with the top 3 changes
- CTA button text and link

## Rules:
- Write for USERS, not developers
- Focus on benefits, not implementation
- Use active voice ("You can now..." not "It is now possible to...")
- Don't mention internal refactoring or tech debt fixes unless they improve UX
- Include version number and date
- Group changes: New Features, Improvements, Bug Fixes
```

**Example Output Snippet:**

```markdown
# Release Notes: v3.5 - January 2025

## What's New

### Find anything in seconds with Smart Search
We completely rebuilt search from the ground up. Type any keyword and get
instant results across all your projects, documents, and comments. Search
now understands typos (searching "mananger" still finds "manager") and
supports filters like `type:document author:jane`.
→ [See search tips](https://docs.example.com/search)

### Export your reports to PDF with one click
The most-requested feature of 2024 is here! Click the export button on any
report to download a beautifully formatted PDF, complete with your charts
and branding. Perfect for sharing with stakeholders who aren't on the platform.
→ Available on Pro and Enterprise plans

## Improvements

### Faster dashboard loading (2x speed improvement)
Your dashboard now loads in under 1 second, even with hundreds of items.
We know you stare at this page every morning - now you can stare at it
with your coffee still hot.

## Bug Fixes
- Fixed an issue where notification preferences would reset after logging out
- Fixed rare crash when pasting images in comments on Safari
- Fixed timezone display for users in India (IST was showing as GMT+5 instead of GMT+5:30)

---

## Short Changelog (In-App)

**New**
- Smart Search: find anything across all projects instantly
- PDF Export for all reports and dashboards

**Improved**
- Dashboard loads 2x faster
- Search understands typos and filters

**Fixed**
- Notification preferences no longer reset on logout
- Correct timezone display for IST users
```

**Tips for Customization:**
- Include screenshots or describe what visuals to create
- Specify: "Our audience is non-technical small business owners"
- Add: "Include a migration note for breaking API changes"

---

## 6. User Interview Script Generator

**Use Case:** Create structured interview scripts for user research, complete with questions, probes, and analysis framework.

**Prompt:**

```
You are a UX researcher designing a user interview to deeply understand user needs, pain points, and behaviors.

## Research Goal
"""
[WHAT DO YOU WANT TO LEARN? e.g., "Understand why users abandon the checkout flow"]
"""

## Target Participants
"""
[WHO TO INTERVIEW: e.g., "Users who started checkout but didn't complete in the last 30 days"]
"""

## Generate:

### 1. Interview Guide

**Introduction Script** (2 minutes)
- Greeting, rapport building
- Explain purpose (without biasing)
- Get consent for recording
- Set expectations for timing

**Warm-Up Questions** (5 minutes)
- Background questions to understand context
- Open-ended, non-threatening

**Core Questions** (25 minutes)
For each question:
- **Main Question**: Open-ended, non-leading
- **Follow-Up Probes**: 2-3 deeper questions based on possible responses
- **Things to Watch For**: Body language, hesitation, emotion indicators
- **Anti-Pattern**: What NOT to ask (leading, biased, closed)

**Behavioral Questions** (10 minutes)
- "Walk me through the last time you..." format
- Focus on actual behavior, not hypothetical

**Closing** (5 minutes)
- "Is there anything I should have asked but didn't?"
- Thank participant, explain next steps

### 2. Screener Survey
- 5-7 questions to qualify participants
- Disqualification criteria

### 3. Analysis Framework
- How to code responses
- Theme template
- Affinity diagram structure

## Rules for Questions:
- Never ask "Would you use feature X?" (people can't predict future behavior)
- Never ask "How much would you pay?" (use Van Westendorp instead)
- Ask about past behavior, not future intentions
- Use the "5 Whys" technique for probing
- Avoid "Do you like...?" (yes/no = useless data)
```

**Example Output Snippet:**

```markdown
# User Interview Guide: Checkout Abandonment

## Introduction (2 min)

"Hi [name], thanks so much for taking the time to chat today. I'm [your name],
and I work on making our shopping experience better. I'm not testing you -
there are no right or wrong answers. I'm genuinely curious about your
experience, and honest feedback (even criticism) is incredibly valuable.

Would it be okay if I record this conversation? It's just so I can focus on
listening rather than taking notes. The recording stays within our research
team.

This should take about 40 minutes. Do you have any questions before we start?"

## Warm-Up (5 min)

1. **Tell me a bit about yourself. What do you do for work?**
   - *Purpose: Build rapport, understand context*

2. **How do you typically shop online? Do you tend to browse or go in knowing what you want?**
   - *Purpose: Understand shopping archetype*

## Core Questions (25 min)

### Q1: "Walk me through your most recent experience shopping on our site."
**Follow-up probes:**
- "What were you looking for that day?"
- "You mentioned you added items to your cart - what happened next?"
- "At what point did you decide to stop? What was going through your mind?"

**Watch for:**
- Where in the story do they slow down or show frustration?
- Do they mention comparing with other sites?
- Do they mention price, trust, or confusion?

**DON'T ask:** "Was the checkout process confusing?" (leading)
**DO ask:** "Tell me about the checkout experience. What stood out to you?"

### Q2: "You mentioned [specific friction point]. Can you tell me more about that?"
**5 Whys probe pattern:**
1. "Why did that make you hesitate?"
2. "What were you expecting to see instead?"
3. "Has that happened on other sites? How did they handle it?"
4. "If you could have changed that moment, what would have helped?"
5. "On a scale of annoying to deal-breaker, where does that fall?"

### Q3: "Did you end up purchasing that item somewhere else?"
**Follow-up probes:**
- "What made you choose that other option?"
- "What did they do differently?"
- "Would anything have kept you on our site?"

**Watch for:**
- Competitor mentions (note which ones)
- Price comparison behavior
- Trust signals they mention
```

**Tips for Customization:**
- Specify: "We're testing a new prototype - include task-based usability questions"
- Add: "Include a section for card sorting exercise"
- Mention: "Interviews are remote via Zoom (adjust for screen sharing instructions)"

---

## 7. A/B Test Design

**Use Case:** Design statistically valid A/B tests with proper hypotheses, metrics, sample sizes, and analysis plans.

**Prompt:**

```
You are a growth data scientist designing a rigorous A/B test.

## What We Want to Test
"""
[DESCRIBE: The change you want to test and why you think it will work]
"""

## Current State
- **Current metric value**: [e.g., 3.2% conversion rate]
- **Daily traffic**: [e.g., 10,000 visitors to this page]
- **Current design/flow**: [Describe what exists today]

## Design the A/B Test:

### 1. Hypothesis
- **Null Hypothesis (H0)**: [The change has no effect on the metric]
- **Alternative Hypothesis (H1)**: [The change improves the metric by X%]
- **Rationale**: Why we believe H1 based on evidence/research

### 2. Metrics
- **Primary metric**: The ONE metric that determines success/failure
- **Secondary metrics**: Other metrics to monitor (2-3 max)
- **Guardrail metrics**: Metrics that must NOT degrade (e.g., revenue, page load time)

### 3. Test Design
- **Variants**: Control (A) and Treatment(s) (B, C)
- **Traffic split**: Percentage per variant
- **Targeting**: Who is included/excluded
- **Randomization unit**: User-level, session-level, or page-level

### 4. Statistical Plan
- **Significance level (alpha)**: 0.05 (standard)
- **Statistical power**: 0.80 (standard)
- **Minimum Detectable Effect (MDE)**: Smallest meaningful improvement
- **Required sample size per variant**: Calculated
- **Estimated test duration**: Based on traffic and sample size
- **Analysis method**: Frequentist (z-test) or Bayesian

### 5. Implementation
- Feature flag configuration
- Tracking events to instrument
- Data pipeline verification checklist

### 6. Analysis Plan (written BEFORE starting the test)
- When to check results (not daily!)
- How to handle significance with multiple comparisons
- What to do if results are inconclusive
- Segmentation analysis to run post-test

### 7. Risks & Mitigations
- Novelty effect (new thing gets clicks just because it's new)
- Sample ratio mismatch (verify equal split)
- Seasonality concerns
- Interference with other running tests
```

**Example Output Snippet:**

```markdown
# A/B Test: Simplified Checkout Flow

## 1. Hypothesis

**H0**: Reducing checkout from 4 steps to 2 steps has no effect on
conversion rate.

**H1**: Reducing checkout from 4 steps to 2 steps increases conversion
rate by at least 10% relative (from 3.2% to 3.52%).

**Rationale**: Heatmap data shows 31% of users drop off between step 2
(shipping) and step 3 (payment). User interviews revealed "it felt like
it would never end." Competitor analysis shows Shopify's one-page checkout
converts 12% better than multi-page in published studies.

## 2. Metrics

| Type | Metric | Current Value | Target |
|------|--------|---------------|--------|
| Primary | Checkout completion rate | 3.2% | 3.52%+ |
| Secondary | Average order value | $67 | No decrease |
| Secondary | Time to complete checkout | 4.2 min | Decrease |
| Guardrail | Error rate during checkout | 0.8% | No increase |
| Guardrail | Payment failure rate | 2.1% | No increase |

## 4. Statistical Plan

```
Significance level (α): 0.05 (two-tailed)
Statistical power (1-β): 0.80
Baseline conversion: 3.2%
Minimum Detectable Effect: 10% relative (0.32 percentage points)
Required sample size: 38,400 per variant
Total needed: 76,800 visitors to checkout
Daily checkout visitors: ~5,000
Estimated duration: 16 days (round up to 3 full weeks for weekly patterns)
```

**Decision Framework:**
- If p < 0.05 AND practical significance (effect > 5%): **Ship it**
- If p < 0.05 BUT effect < 5%: **Discuss** - is the complexity worth it?
- If p > 0.05 after full sample: **No effect** - don't ship, investigate why
- If guardrail metrics degrade by >10%: **Stop test immediately**
```

**Tips for Customization:**
- Include your actual traffic numbers for precise duration estimates
- Specify: "We use LaunchDarkly for feature flags and Amplitude for analytics"
- Add: "We need to account for our 2-week purchase decision cycle"

---

## 8. Product Metrics Dashboard Designer

**Use Case:** Define the key metrics, KPIs, and dashboard layout for monitoring product health and growth.

**Prompt:**

```
You are a product analytics expert designing a metrics framework and dashboard for a product team.

## Product Details
"""
[DESCRIBE: Product type, stage, business model, key user actions]
"""

## Design:

### 1. Metrics Framework (North Star + Supporting)

**North Star Metric**: The ONE metric that best captures the value your product delivers
- Definition (precise, no ambiguity)
- Why this metric (not revenue, not DAU - WHY this one)
- Leading indicators that predict changes in the North Star

**Input Metrics** (levers that drive the North Star):
| Category | Metric | Definition | Owner |
|----------|--------|------------|-------|
| Acquisition | | | |
| Activation | | | |
| Engagement | | | |
| Retention | | | |
| Revenue | | | |

### 2. Dashboard Layout

**Executive Dashboard** (for leadership - glanceable)
- 4-6 key metrics with sparklines
- MoM and YoY comparisons
- Traffic light status (green/yellow/red)

**Product Dashboard** (for PM - daily monitoring)
- Funnel visualization (acquisition → activation → retention)
- Cohort retention curves
- Feature adoption rates
- User segmentation breakdown

**Growth Dashboard** (for growth team)
- Experiment results summary
- Channel-level acquisition metrics
- Conversion funnel with drop-off %

### 3. Alert Rules
For each metric:
- What threshold triggers an alert
- Who gets notified
- How to investigate

### 4. Reporting Cadence
- Daily: What to check
- Weekly: What to review in team meeting
- Monthly: What to present to leadership
- Quarterly: What to include in business review

### 5. Data Requirements
- Events to track (with properties)
- User properties to capture
- SQL queries for key metrics
```

**Example Output Snippet:**

```markdown
# Product Metrics Framework: SaaS Project Management Tool

## North Star Metric

**Weekly Active Projects** = Number of projects with at least 3 actions
(task created, status changed, or comment added) by at least 2 team
members in the last 7 days.

**Why this metric**: It captures:
- Users are engaged (not just logging in)
- Teams are collaborating (not just individuals)
- Value delivery (active projects = problems being solved)
- Better than DAU (a user logging in to check one thing isn't "active")
- Better than revenue (revenue lags behavior by months)

## Input Metrics

| Category | Metric | Definition | Target |
|----------|--------|------------|--------|
| Acquisition | Weekly signups | New accounts created | 500/week |
| Activation | Day-7 activation | % of signups who create a project + invite 1 teammate within 7 days | 35% |
| Engagement | Actions per user/week | Task creates + updates + comments per active user | 25+ |
| Retention | Week-8 retention | % of activated users still active 8 weeks later | 60% |
| Revenue | MRR | Monthly recurring revenue | $150K |
| Revenue | Net Revenue Retention | Revenue from existing customers (expansion - churn) | 110%+ |

## Dashboard: Executive View

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Weekly Active   │ New Signups     │  MRR            │ NPS Score       │
│ Projects: 8,421 │ This week: 523  │ $142,500        │ 47              │
│ ▲ 12% MoM      │ ▲ 8% MoM       │ ▲ 5% MoM       │ ▲ 3 pts MoM    │
│ 🟢 On track    │ 🟢 On track    │ 🟡 Below target │ 🟢 On track    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  Activation Funnel (last 30 days)                                       │
│  Signup: 2,100 → Create Project: 840 (40%) → Invite Team: 630 (30%)   │
│  → Day-7 Active: 525 (25%) → Day-30 Active: 315 (15%)                 │
│  ⚠️ Biggest drop: Create Project → Invite Team (25% drop)              │
└──────────────────────────────────────────────────────────────────────────┘
```

## Alert Rules

| Metric | Yellow Alert | Red Alert | Action |
|--------|-------------|-----------|--------|
| Weekly Active Projects | -10% WoW | -20% WoW | Investigate feature changes, outages |
| Signup rate | -15% WoW | -30% WoW | Check marketing spend, landing page, sign-up flow |
| Error rate | >1% | >5% | Page engineering on-call |
| Day-7 activation | <30% | <25% | Review onboarding flow, run user interviews |
```

**Tips for Customization:**
- Specify your analytics tool: "We use Mixpanel for product analytics and Looker for dashboards"
- Add: "Include retention cohort analysis methodology"
- Mention: "We're a B2B SaaS so include account-level metrics, not just user-level"
