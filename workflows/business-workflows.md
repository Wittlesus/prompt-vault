# Business Workflows - Production-Ready Automation Chains

Complete AI automation systems for business intelligence, competitive analysis, and strategic planning. Each workflow produces actionable insights.

---

## Workflow 1: Competitive Intelligence Automation

**What This Automates:** Monitors competitors, analyzes their moves, generates strategic recommendations. Runs weekly to keep you informed.

**When to Use:** When you have 3+ competitors to track but no dedicated market research team.

### The Complete Chain

```python
# save as: competitive_intel.py
import anthropic
import json
from typing import List, Dict
from datetime import datetime

class CompetitiveIntelligence:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_analyze_competitor_updates(self, competitor_data: List[Dict]) -> Dict:
        """Analyze recent competitor activity."""
        updates_text = "\n\n".join([
            f"Competitor: {c['name']}\nRecent updates:\n" + "\n".join(c['updates'])
            for c in competitor_data
        ])

        prompt = f"""Analyze these competitor updates from the past week:

{updates_text}

Output JSON with:
- significant_moves (array: competitor, move, strategic_implication)
- emerging_trends (patterns across competitors)
- threat_level (low/medium/high for each competitor)
- opportunities (gaps we can exploit)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="Product strategist analyzing competitive landscape. Focus on actionable insights.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_feature_gap_analysis(self, our_features: List[str], competitor_analysis: Dict) -> Dict:
        """Identify feature gaps."""
        prompt = f"""Our current features:
{json.dumps(our_features)}

Competitor analysis:
{json.dumps(competitor_analysis)}

Perform gap analysis. Output JSON with:
- features_we_lack (array with: feature, competitor_who_has_it, user_demand_estimate)
- features_we_lead_on (our unique advantages)
- table_stakes (features everyone must have)
- differentiators (features that win deals)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            system="Product manager performing competitive feature analysis.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step3_strategic_recommendations(self, analysis: Dict, gap_analysis: Dict, company_goals: Dict) -> str:
        """Generate strategic recommendations."""
        prompt = f"""Competitive analysis: {json.dumps(analysis)}
Gap analysis: {json.dumps(gap_analysis)}
Company goals: {json.dumps(company_goals)}

Generate strategic recommendations:
1. Immediate actions (this sprint)
2. Short-term strategy (this quarter)
3. Long-term positioning (12 months)
4. Features to prioritize
5. Messaging/positioning adjustments
6. Potential partnerships or acquisitions

Format as executive summary (2 pages max)."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2500,
            system="Strategy consultant writing executive recommendations. Be specific and actionable.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def generate_report(self, competitor_data: List[Dict], our_features: List[str], company_goals: Dict) -> Dict:
        """Complete competitive intelligence workflow."""
        print("Step 1: Analyzing competitor updates...")
        analysis = self.step1_analyze_competitor_updates(competitor_data)
        print(f"Found {len(analysis.get('significant_moves', []))} significant moves")

        print("Step 2: Feature gap analysis...")
        gap_analysis = self.step2_feature_gap_analysis(our_features, analysis)

        print("Step 3: Generating strategic recommendations...")
        recommendations = self.step3_strategic_recommendations(analysis, gap_analysis, company_goals)

        return {
            "generated_date": datetime.now().isoformat(),
            "competitor_analysis": analysis,
            "gap_analysis": gap_analysis,
            "strategic_recommendations": recommendations
        }

# Usage
if __name__ == "__main__":
    import os

    intel = CompetitiveIntelligence(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Sample data (in production, scrape from competitor blogs, changelog pages, etc.)
    competitors = [
        {
            "name": "CompetitorA",
            "updates": [
                "Launched AI-powered search feature",
                "Acquired startup focused on mobile analytics",
                "Announced Series C funding $50M"
            ]
        },
        {
            "name": "CompetitorB",
            "updates": [
                "Released API v3 with GraphQL support",
                "Introduced team collaboration features",
                "Expanded to European market"
            ]
        }
    ]

    our_features = [
        "Kanban boards",
        "Time tracking",
        "REST API",
        "Slack integration"
    ]

    company_goals = {
        "q1_goal": "Increase activation rate from 30% to 40%",
        "annual_goal": "Reach $2M ARR",
        "target_market": "Remote teams 10-100 people"
    }

    report = intel.generate_report(competitors, our_features, company_goals)

    # Save report
    with open(f"competitive_intel_{datetime.now().strftime('%Y%m%d')}.md", "w") as f:
        f.write("# Weekly Competitive Intelligence Report\n\n")
        f.write(f"Generated: {report['generated_date']}\n\n")
        f.write("## Strategic Recommendations\n\n")
        f.write(report['strategic_recommendations'])

    with open(f"competitive_intel_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Competitive intelligence report generated!")
```

### Expected Output

```json
{
  "competitor_analysis": {
    "significant_moves": [
      {
        "competitor": "CompetitorA",
        "move": "AI-powered search",
        "strategic_implication": "Raising user expectations for search quality. Table stakes in 6 months."
      }
    ],
    "threat_level": {
      "CompetitorA": "high",
      "CompetitorB": "medium"
    }
  },
  "gap_analysis": {
    "features_we_lack": [
      {
        "feature": "AI search",
        "competitor": "CompetitorA",
        "user_demand": "high"
      }
    ]
  },
  "strategic_recommendations": "## Immediate Actions\n1. Prototype AI search (2 week sprint)..."
}
```

---

## Workflow 2: Customer Interview Synthesizer

**What This Automates:** Analyzes transcripts from 10+ customer interviews, extracts themes, identifies pain points, generates product insights.

**When to Use:** After user research sprints. Alternative to hiring a UX researcher to synthesize findings.

### Complete Script

```python
# save as: interview_synthesizer.py
import anthropic
import json
from typing import List, Dict
from collections import defaultdict

class InterviewSynthesizer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_extract_quotes(self, transcript: str, participant_id: str) -> List[Dict]:
        """Extract key quotes from single interview."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1200,
            system="""UX researcher extracting insights from interviews.
Output JSON array with: quote (verbatim), theme (category), sentiment (positive/negative/neutral), pain_point (boolean).""",
            messages=[{"role": "user", "content": f"Participant {participant_id}:\n{transcript}"}]
        )

        quotes = json.loads(response.content[0].text)
        for q in quotes:
            q['participant'] = participant_id
        return quotes

    def step2_identify_themes(self, all_quotes: List[Dict]) -> Dict:
        """Cluster quotes into themes."""
        quotes_by_theme = defaultdict(list)
        for q in all_quotes:
            quotes_by_theme[q['theme']].append(q)

        prompt = f"""All quotes from interviews:
{json.dumps(all_quotes, indent=2)}

Identify major themes. Output JSON with:
- themes (array with: name, frequency, severity, representative_quotes)
- top_pain_points (array ranked by urgency)
- positive_feedback (what users love)
- feature_requests (specific asks)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="UX researcher identifying patterns across interviews.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step3_generate_insights(self, themes: Dict, product_context: Dict) -> str:
        """Generate actionable product insights."""
        prompt = f"""Interview themes: {json.dumps(themes)}
Product context: {json.dumps(product_context)}

Write research synthesis report with:
1. Executive Summary (key findings in 3 bullets)
2. Major Themes (with evidence)
3. Top 5 Pain Points (ranked by urgency)
4. Recommended Actions (specific product/design changes)
5. Quotes (illustrative examples)

Format as Markdown for stakeholder presentation."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2500,
            system="UX researcher writing research reports. Be specific, evidence-based, actionable.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def synthesize(self, transcripts: List[Dict], product_context: Dict) -> Dict:
        """Complete synthesis workflow."""
        print("Step 1: Extracting quotes from all interviews...")
        all_quotes = []
        for t in transcripts:
            quotes = self.step1_extract_quotes(t['transcript'], t['participant_id'])
            all_quotes.extend(quotes)
        print(f"Extracted {len(all_quotes)} quotes from {len(transcripts)} interviews")

        print("Step 2: Identifying themes...")
        themes = self.step2_identify_themes(all_quotes)
        print(f"Identified {len(themes.get('themes', []))} major themes")

        print("Step 3: Generating insights report...")
        report = self.step3_generate_insights(themes, product_context)

        return {
            "quotes": all_quotes,
            "themes": themes,
            "report": report
        }

# Usage
if __name__ == "__main__":
    import os

    synthesizer = InterviewSynthesizer(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Sample transcripts (in production, these come from Otter.ai, Zoom, etc.)
    transcripts = [
        {
            "participant_id": "P001",
            "transcript": "The onboarding was confusing. I didn't understand where to start. I almost gave up..."
        },
        {
            "participant_id": "P002",
            "transcript": "I love the Slack integration. It saves me so much time. But the mobile app is slow..."
        }
        # ... more interviews
    ]

    product_ctx = {
        "product": "ProjectHub",
        "target_users": "Remote teams",
        "current_focus": "Improving activation rate"
    }

    result = synthesizer.synthesize(transcripts, product_ctx)

    # Save report
    with open("user_research_synthesis.md", "w") as f:
        f.write(result['report'])

    with open("user_research_data.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Research synthesis complete!")
```

---

## Workflow 3: Pricing Strategy Analyzer

**What This Automates:** Analyzes your costs, competitor pricing, and customer segments to recommend optimal pricing tiers.

### Complete Script

```python
# save as: pricing_analyzer.py
import anthropic
import json
from typing import Dict, List

class PricingAnalyzer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_analyze_costs(self, cost_breakdown: Dict) -> Dict:
        """Analyze unit economics."""
        prompt = f"""Cost breakdown per customer:
{json.dumps(cost_breakdown, indent=2)}

Calculate and output JSON with:
- cogs_per_customer (total cost of goods sold)
- ltv_estimate (based on churn and subscription length)
- minimum_viable_price (to cover costs + 20% margin)
- ideal_price_range (for 40-60% gross margin)"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=800,
            system="SaaS financial analyst. Calculate unit economics.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_competitive_pricing_analysis(self, competitor_pricing: List[Dict]) -> Dict:
        """Analyze market pricing."""
        prompt = f"""Competitor pricing:
{json.dumps(competitor_pricing, indent=2)}

Output JSON with:
- price_ranges (by tier: free/starter/pro/enterprise)
- value_metric (what they charge for: seats/usage/features)
- positioning_gaps (underserved price points)
- anchor_pricing (highest prices setting market expectations)"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system="Pricing strategist analyzing competitive pricing.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step3_segment_analysis(self, customer_segments: List[Dict]) -> Dict:
        """Willingness to pay by segment."""
        prompt = f"""Customer segments:
{json.dumps(customer_segments, indent=2)}

For each segment, estimate:
- willingness_to_pay (price range)
- price_sensitivity (high/medium/low)
- preferred_pricing_model (per-seat/usage-based/flat)
- deal_breakers (what would cause them not to buy)

Output JSON."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1200,
            system="Pricing economist analyzing customer segments.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step4_recommend_pricing(self, costs: Dict, competitive: Dict, segments: Dict, business_goals: Dict) -> str:
        """Generate pricing recommendation."""
        prompt = f"""Unit economics: {json.dumps(costs)}
Competitive analysis: {json.dumps(competitive)}
Customer segments: {json.dumps(segments)}
Business goals: {json.dumps(business_goals)}

Recommend complete pricing strategy:

1. Pricing Tiers
   - How many tiers (3-4 recommended)
   - Price point for each
   - Feature allocation per tier
   - Target segment per tier

2. Pricing Metric
   - Per-seat vs usage-based vs flat
   - Rationale

3. Anchoring Strategy
   - Which tier should be "most popular"
   - How to present pricing page

4. Discounting Policy
   - Annual vs monthly
   - Volume discounts
   - Non-profit/education

5. Testing Plan
   - A/B test structure
   - What to measure
   - When to iterate

Format as Markdown."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2500,
            system="Pricing consultant creating pricing strategies. Be specific with numbers.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def analyze(self, cost_breakdown: Dict, competitor_pricing: List[Dict], customer_segments: List[Dict], business_goals: Dict) -> Dict:
        """Complete pricing analysis."""
        print("Step 1: Analyzing costs...")
        costs = self.step1_analyze_costs(cost_breakdown)
        print(f"Minimum viable price: ${costs['minimum_viable_price']}")

        print("Step 2: Competitive pricing analysis...")
        competitive = self.step2_competitive_pricing_analysis(competitor_pricing)

        print("Step 3: Customer segment analysis...")
        segments = self.step3_segment_analysis(customer_segments)

        print("Step 4: Generating pricing recommendation...")
        recommendation = self.step4_recommend_pricing(costs, competitive, segments, business_goals)

        return {
            "unit_economics": costs,
            "competitive_analysis": competitive,
            "segment_analysis": segments,
            "pricing_recommendation": recommendation
        }

# Usage
if __name__ == "__main__":
    import os

    analyzer = PricingAnalyzer(api_key=os.environ["ANTHROPIC_API_KEY"])

    costs = {
        "cloud_hosting_per_customer_per_month": 5,
        "ai_api_costs_per_customer_per_month": 3,
        "support_cost_per_customer_per_month": 2,
        "average_customer_lifetime_months": 18
    }

    competitors = [
        {"name": "CompetitorA", "tiers": [{"name": "Free", "price": 0}, {"name": "Pro", "price": 29}, {"name": "Team", "price": 99}]},
        {"name": "CompetitorB", "tiers": [{"name": "Starter", "price": 19}, {"name": "Business", "price": 79}]}
    ]

    segments = [
        {"segment": "Solo freelancers", "size": 10000, "characteristics": "Price sensitive, need basic features"},
        {"segment": "Small teams (5-20)", "size": 3000, "characteristics": "Value collaboration, willing to pay for quality"}
    ]

    goals = {
        "revenue_target": "$100K MRR in 12 months",
        "preferred_customer": "Small teams",
        "positioning": "Premium but accessible"
    }

    result = analyzer.analyze(costs, competitors, segments, goals)

    with open("pricing_strategy.md", "w") as f:
        f.write(result['pricing_recommendation'])

    print("Pricing analysis complete!")
```

---

## Workflow 4: Market Research Report Generator

**What This Automates:** Researches a market, identifies opportunities, sizes the market, and generates a comprehensive market research report.

### Complete Script

```python
# save as: market_research.py
import anthropic
import json
from typing import Dict, List

class MarketResearcher:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_market_overview(self, market_description: str) -> Dict:
        """Generate market overview."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            system="""Market research analyst. Output JSON with:
- market_definition
- key_players (array of companies)
- market_trends (array)
- growth_drivers
- barriers_to_entry""",
            messages=[{"role": "user", "content": f"Research this market: {market_description}"}]
        )

        return json.loads(response.content[0].text)

    def step2_tam_sam_som(self, market_overview: Dict, product_description: str) -> Dict:
        """Calculate TAM/SAM/SOM."""
        prompt = f"""Market: {json.dumps(market_overview)}
Our product: {product_description}

Calculate TAM/SAM/SOM (Total/Serviceable/Obtainable Market).
Output JSON with estimates and methodology."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1000,
            system="Market sizing analyst. Show your work.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step3_opportunity_analysis(self, market_data: Dict) -> str:
        """Identify opportunities."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="Strategy consultant identifying market opportunities.",
            messages=[{"role": "user", "content": f"Find opportunities in: {json.dumps(market_data)}"}]
        )

        return response.content[0].text

    def generate_report(self, market_description: str, product_description: str) -> Dict:
        """Complete research workflow."""
        print("Step 1: Market overview...")
        overview = self.step1_market_overview(market_description)

        print("Step 2: Market sizing...")
        sizing = self.step2_tam_sam_som(overview, product_description)

        print("Step 3: Opportunity analysis...")
        opportunities = self.step3_opportunity_analysis({**overview, **sizing})

        return {
            "overview": overview,
            "market_sizing": sizing,
            "opportunities": opportunities
        }

# Usage
researcher = MarketResearcher(api_key=os.environ["ANTHROPIC_API_KEY"])
result = researcher.generate_report(
    "AI-powered customer support automation",
    "Chatbot that handles tier-1 support tickets"
)
print(json.dumps(result, indent=2))
```

---

## When to Use Business Workflows vs. Consultants

| Use Workflows When... | Hire Consultants When... |
|---|---|
| Budget <$10K for research | Budget >$50K (McKinsey-level depth) |
| Need quick directional insights (days) | Need court-ready reports (months) |
| Internal decision-making | Board presentations, investor decks |
| Iterative hypothesis testing | One-time strategic pivot |

**Cost comparison:**
- Market research firm: $15-50K per report
- UX research consultant: $150-300/hour
- Pricing consultant: $10-30K for strategy
- This workflow library: $19 + API costs ($50-200/month)
