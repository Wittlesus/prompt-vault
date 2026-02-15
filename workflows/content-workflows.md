# Content Workflows - Production-Ready Automation Chains

Complete AI automation systems for content creation. Each workflow chains multiple prompts together to produce publication-ready content.

---

## Workflow 1: Blog Post Production Pipeline

**What This Automates:** Takes a topic idea and produces a complete, SEO-optimized blog post with outline, draft, editing pass, meta tags, and social promotion posts.

**When to Use:** Publishing 2+ blog posts per week. Alternative to hiring a content writer at $0.15-0.50/word.

### The Complete Chain

#### Step 1: Research & Outline System Prompt

```python
RESEARCH_SYSTEM = """You are an SEO content strategist and researcher.
Given a topic, conduct competitive analysis and create a data-driven outline.

Research process:
1. Identify top-ranking content for this topic (simulate SERP analysis)
2. Extract common themes and gaps in existing content
3. Identify unique angle/hook
4. Create detailed outline with H2/H3 structure
5. Suggest internal linking opportunities
6. Recommend target keyword and related keywords

Output as structured JSON."""
```

#### Step 2: Draft Writer System Prompt

```python
DRAFT_WRITER_SYSTEM = """You are an experienced content writer specializing in [INDUSTRY].
Write in a conversational but authoritative tone. Use:
- Short paragraphs (2-4 sentences max)
- Subheadings every 200-300 words
- Bullet points for scannability
- Real examples and data points
- Transition phrases between sections

Avoid: fluff, passive voice, jargon without explanation, unsupported claims."""
```

#### Step 3: Editor System Prompt

```python
EDITOR_SYSTEM = """You are a senior content editor known for tightening prose and catching mistakes.

Edit for:
1. Clarity: Remove unnecessary words, simplify complex sentences
2. Accuracy: Flag unsupported claims that need citations
3. Flow: Ensure smooth transitions between sections
4. Engagement: Add questions, examples, or analogies where dry
5. SEO: Ensure target keyword appears naturally in H1, first paragraph, H2s
6. Call-to-action: Strengthen the CTA at the end

Track changes in a structured format showing before/after."""
```

#### Step 4: Meta Content Generator

```python
META_SYSTEM = """You are an SEO specialist writing meta tags and social content.

Generate:
1. Meta title (under 60 chars, includes target keyword)
2. Meta description (under 160 chars, compelling, includes keyword)
3. OpenGraph title and description (can differ from meta)
4. Featured image suggestion (describe what visual would work)
5. Tweet (280 chars)
6. LinkedIn post (longer format, professional)
7. Email newsletter blurb (2-3 sentences)"""
```

### Complete Automation Script (Python)

```python
# save as: blog_post_pipeline.py
import anthropic
import json
import os
from typing import Dict, List

class BlogPostPipeline:
    def __init__(self, api_key: str, brand_voice: str = "professional but approachable"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.brand_voice = brand_voice

    def step1_research_and_outline(self, topic: str, target_audience: str, seo_keywords: List[str] = None) -> Dict:
        """Research topic and create detailed outline."""
        prompt = f"""Topic: {topic}
Target audience: {target_audience}
SEO keywords: {', '.join(seo_keywords) if seo_keywords else 'None specified'}

Research this topic and create a comprehensive outline."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="""SEO content strategist. Research topics and create outlines.
Output JSON with: unique_angle, target_keyword, related_keywords, outline (array of sections with h2/h3), competitor_gaps, internal_links.""",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_write_draft(self, outline: Dict, word_count: int = 1500) -> str:
        """Write the full blog post draft."""
        prompt = f"""Using this outline:
{json.dumps(outline, indent=2)}

Write a {word_count}-word blog post. Target keyword: {outline.get('target_keyword')}
Brand voice: {self.brand_voice}

Include:
- Engaging introduction with a hook
- Each section from the outline, fully developed
- Real examples and data where possible
- Strong conclusion with clear CTA"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            system="""Experienced content writer. Write conversational, data-driven blog posts.
Use short paragraphs, subheadings, bullet points. Avoid fluff.""",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def step3_edit_draft(self, draft: str, target_keyword: str) -> Dict:
        """Edit for clarity, flow, and SEO."""
        prompt = f"""Original draft:
{draft}

Target keyword: {target_keyword}

Edit this draft. Return JSON with:
- edited_version (full text)
- changes_made (array of {section, before, after, reason})
- seo_score (1-10 with feedback)
- readability_score (1-10 with feedback)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4500,
            system="""Senior content editor. Tighten prose, improve flow, optimize for SEO.
Flag unsupported claims. Strengthen CTAs.""",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step4_generate_meta_and_social(self, final_post: str, target_keyword: str) -> Dict:
        """Generate all meta tags and social promotion content."""
        prompt = f"""Blog post:
{final_post[:1500]}... [truncated]

Target keyword: {target_keyword}

Generate all meta tags and social posts."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system="""SEO specialist. Write compelling meta tags and social posts.
Output JSON with: meta_title, meta_description, og_title, og_description, tweet, linkedin_post, email_blurb, featured_image_suggestion.""",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def generate_complete_post(self, topic: str, target_audience: str, word_count: int = 1500, seo_keywords: List[str] = None) -> Dict:
        """Run the complete pipeline."""
        print("Step 1: Research and outlining...")
        outline = self.step1_research_and_outline(topic, target_audience, seo_keywords)
        print(f"Outline complete. Unique angle: {outline.get('unique_angle')}")

        print("Step 2: Writing draft...")
        draft = self.step2_write_draft(outline, word_count)
        print(f"Draft complete. {len(draft.split())} words.")

        print("Step 3: Editing...")
        edited = self.step3_edit_draft(draft, outline.get('target_keyword'))
        print(f"Editing complete. Made {len(edited.get('changes_made', []))} improvements.")

        print("Step 4: Generating meta content and social posts...")
        meta = self.step4_generate_meta_and_social(edited['edited_version'], outline.get('target_keyword'))

        return {
            "outline": outline,
            "draft": draft,
            "edited_post": edited['edited_version'],
            "edit_log": edited.get('changes_made', []),
            "seo_score": edited.get('seo_score'),
            "meta_content": meta,
            "word_count": len(edited['edited_version'].split())
        }

# Usage
if __name__ == "__main__":
    pipeline = BlogPostPipeline(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        brand_voice="friendly and practical, like a senior developer explaining to a junior"
    )

    result = pipeline.generate_complete_post(
        topic="How to reduce API response time in Node.js",
        target_audience="Backend developers with 1-3 years experience",
        word_count=1800,
        seo_keywords=["node.js performance", "API optimization", "reduce latency"]
    )

    # Save to Markdown file
    with open("blog_post.md", "w") as f:
        f.write(f"# {result['meta_content']['meta_title']}\n\n")
        f.write(f"**Meta Description:** {result['meta_content']['meta_description']}\n\n")
        f.write("---\n\n")
        f.write(result['edited_post'])

    # Save meta content
    with open("blog_meta.json", "w") as f:
        json.dump(result['meta_content'], f, indent=2)

    print(f"\nBlog post generated!")
    print(f"Word count: {result['word_count']}")
    print(f"SEO score: {result['seo_score']}/10")
```

### JavaScript/Node.js Version

```javascript
// save as: blogPostPipeline.js
import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs/promises';

class BlogPostPipeline {
  constructor(apiKey, brandVoice = 'professional but approachable') {
    this.client = new Anthropic({ apiKey });
    this.brandVoice = brandVoice;
  }

  async step1ResearchAndOutline(topic, targetAudience, seoKeywords = []) {
    const response = await this.client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 2000,
      system: `SEO content strategist. Research topics and create outlines.
Output JSON with: unique_angle, target_keyword, related_keywords, outline, competitor_gaps, internal_links.`,
      messages: [{
        role: 'user',
        content: `Topic: ${topic}\nAudience: ${targetAudience}\nKeywords: ${seoKeywords.join(', ')}\n\nResearch and outline.`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async step2WriteDraft(outline, wordCount = 1500) {
    const response = await this.client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 4000,
      system: `Experienced content writer. Write conversational, data-driven posts.
Short paragraphs, subheadings, bullets. Avoid fluff.`,
      messages: [{
        role: 'user',
        content: `Outline: ${JSON.stringify(outline, null, 2)}\n\nWrite ${wordCount}-word post. Voice: ${this.brandVoice}`
      }]
    });

    return response.content[0].text;
  }

  async step3EditDraft(draft, targetKeyword) {
    const response = await this.client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 4500,
      system: `Senior content editor. Tighten prose, improve flow, optimize SEO.
Return JSON with: edited_version, changes_made, seo_score, readability_score.`,
      messages: [{
        role: 'user',
        content: `Draft:\n${draft}\n\nKeyword: ${targetKeyword}\n\nEdit and return JSON.`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async step4GenerateMetaAndSocial(finalPost, targetKeyword) {
    const response = await this.client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1000,
      system: `SEO specialist. Write meta tags and social posts.
Output JSON with: meta_title, meta_description, og_title, og_description, tweet, linkedin_post, email_blurb, featured_image_suggestion.`,
      messages: [{
        role: 'user',
        content: `Post: ${finalPost.substring(0, 1500)}...\n\nKeyword: ${targetKeyword}\n\nGenerate meta content.`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async generateCompletePost(topic, targetAudience, wordCount = 1500, seoKeywords = []) {
    console.log('Step 1: Research and outlining...');
    const outline = await this.step1ResearchAndOutline(topic, targetAudience, seoKeywords);
    console.log(`Outline complete. Angle: ${outline.unique_angle}`);

    console.log('Step 2: Writing draft...');
    const draft = await this.step2WriteDraft(outline, wordCount);
    console.log(`Draft complete. ${draft.split(' ').length} words.`);

    console.log('Step 3: Editing...');
    const edited = await this.step3EditDraft(draft, outline.target_keyword);
    console.log(`Editing complete. ${edited.changes_made?.length || 0} improvements.`);

    console.log('Step 4: Generating meta content...');
    const meta = await this.step4GenerateMetaAndSocial(edited.edited_version, outline.target_keyword);

    return {
      outline,
      draft,
      editedPost: edited.edited_version,
      editLog: edited.changes_made,
      seoScore: edited.seo_score,
      metaContent: meta,
      wordCount: edited.edited_version.split(' ').length
    };
  }
}

// Usage
const pipeline = new BlogPostPipeline(process.env.ANTHROPIC_API_KEY);

const result = await pipeline.generateCompletePost(
  'How to reduce API response time in Node.js',
  'Backend developers with 1-3 years experience',
  1800,
  ['node.js performance', 'API optimization', 'reduce latency']
);

// Save to file
const markdown = `# ${result.metaContent.meta_title}\n\n**Meta Description:** ${result.metaContent.meta_description}\n\n---\n\n${result.editedPost}`;
await fs.writeFile('blog_post.md', markdown);
await fs.writeFile('blog_meta.json', JSON.stringify(result.metaContent, null, 2));

console.log(`\nBlog post generated! ${result.wordCount} words, SEO score: ${result.seoScore}/10`);
```

### Expected Output Structure

```json
{
  "outline": {
    "unique_angle": "Focus on Node.js-specific optimizations most tutorials miss",
    "target_keyword": "node.js API performance",
    "related_keywords": ["reduce latency", "optimize endpoints", "API speed"],
    "outline": [
      {
        "h2": "Why Node.js APIs slow down (and it's not what you think)",
        "h3": ["The event loop bottleneck", "Synchronous operations", "Database query patterns"]
      },
      {
        "h2": "5 high-impact optimizations",
        "h3": ["Streaming responses", "Connection pooling", "Caching strategies"]
      }
    ]
  },
  "meta_content": {
    "meta_title": "How to Reduce Node.js API Response Time by 70% (5 Proven Techniques)",
    "meta_description": "Speed up your Node.js APIs with these 5 battle-tested optimization techniques. Reduce latency, improve throughput, and handle more requests.",
    "tweet": "Cut your Node.js API response time by 70% with these 5 techniques:\n\n1. Stream responses\n2. Pool connections\n3. Cache strategically\n4. Async everything\n5. Monitor continuously\n\nFull guide:",
    "linkedin_post": "After profiling hundreds of Node.js APIs, I've noticed the same patterns...",
    "featured_image_suggestion": "Split screen: slow API response (red, 2000ms) vs optimized (green, 300ms)"
  }
}
```

---

## Workflow 2: Newsletter Content Generator

**What This Automates:** Curates content from multiple sources, writes commentary, generates newsletter in multiple formats (HTML email, plain text, web archive).

**When to Use:** Publishing weekly/monthly newsletters.

### Complete Script

```python
# save as: newsletter_generator.py
import anthropic
import json
from typing import List, Dict

class NewsletterGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_curate_content(self, content_sources: List[Dict], theme: str = None) -> Dict:
        """Analyze sources and curate top items."""
        sources_text = "\n\n".join([
            f"Source {i+1} ({s['type']}): {s['title']}\n{s.get('summary', '')}"
            for i, s in enumerate(content_sources)
        ])

        prompt = f"""Theme: {theme or 'General industry news'}

Content sources:
{sources_text}

Curate the best 5-7 items for a newsletter. For each:
- Why it's relevant to our audience
- Key takeaway
- Suggested commentary angle (hot take, tutorial, case study)

Output as JSON array."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            system="Content curator with expertise in newsletter writing. Pick signal over noise.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_write_commentary(self, curated_items: List[Dict], brand_voice: str) -> List[Dict]:
        """Write commentary for each curated item."""
        items_with_commentary = []

        for item in curated_items:
            prompt = f"""Item: {item['title']}
Key takeaway: {item['key_takeaway']}
Angle: {item['commentary_angle']}

Write 2-3 paragraph commentary in this voice: {brand_voice}

Include:
- Your perspective or hot take
- Why readers should care
- Practical next step or question to consider"""

            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=500,
                system="Newsletter writer with a distinctive voice. Write opinionated but balanced commentary.",
                messages=[{"role": "user", "content": prompt}]
            )

            items_with_commentary.append({
                **item,
                "commentary": response.content[0].text
            })

        return items_with_commentary

    def step3_format_newsletter(self, items: List[Dict], intro: str, outro: str) -> Dict:
        """Format as HTML email and plain text."""
        prompt = f"""Intro: {intro}
Outro: {outro}

Items:
{json.dumps(items, indent=2)}

Format as:
1. HTML email (responsive, mobile-friendly)
2. Plain text version
3. Web archive version (full HTML page)

Output as JSON with: html_email, plain_text, web_archive."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=3000,
            system="Email template designer. Create clean, readable newsletter formats.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def generate(self, sources: List[Dict], theme: str, intro: str, outro: str, brand_voice: str) -> Dict:
        """Complete workflow."""
        print("Step 1: Curating content...")
        curated = self.step1_curate_content(sources, theme)
        print(f"Curated {len(curated)} items")

        print("Step 2: Writing commentary...")
        with_commentary = self.step2_write_commentary(curated, brand_voice)

        print("Step 3: Formatting newsletter...")
        formatted = self.step3_format_newsletter(with_commentary, intro, outro)

        return {
            "curated_items": curated,
            "formatted": formatted
        }

# Usage
if __name__ == "__main__":
    generator = NewsletterGenerator(api_key=os.environ["ANTHROPIC_API_KEY"])

    sources = [
        {"type": "article", "title": "React 19 Released", "summary": "New features..."},
        {"type": "tutorial", "title": "Building with Next.js 16", "summary": "Step by step..."},
        {"type": "announcement", "title": "Vercel Edge Functions", "summary": "New runtime..."}
    ]

    result = generator.generate(
        sources=sources,
        theme="Web development and React ecosystem",
        intro="Happy Monday! Here's what caught my attention this week:",
        outro="What are you building this week? Hit reply and let me know!",
        brand_voice="Experienced developer sharing lessons learned, slightly opinionated but helpful"
    )

    # Save HTML email
    with open("newsletter.html", "w") as f:
        f.write(result["formatted"]["html_email"])

    print("Newsletter generated!")
```

---

## Workflow 3: Landing Page Copy Generator

**What This Automates:** Takes product features and generates complete landing page copy (hero, features, pricing, FAQ, CTA) with A/B test variants.

**When to Use:** Launching new products or redesigning landing pages.

### Complete Script

```python
# save as: landing_page_generator.py
import anthropic
import json
from typing import Dict, List

class LandingPageGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_value_prop_analysis(self, product_info: Dict) -> Dict:
        """Extract core value propositions."""
        prompt = f"""Product: {product_info['name']}
Description: {product_info['description']}
Target audience: {product_info['target_audience']}
Key features: {json.dumps(product_info['features'])}

Analyze and return JSON with:
- primary_value_prop (one sentence, emotional benefit)
- secondary_value_props (3-5 supporting points)
- unique_mechanism (what makes this different)
- before_after_states (current pain vs future state)
- objections (3 common objections and rebuttals)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1200,
            system="Conversion copywriter specializing in SaaS landing pages. Find the emotional hook.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_write_sections(self, value_props: Dict, product_info: Dict) -> Dict:
        """Write all landing page sections."""
        prompt = f"""Value propositions: {json.dumps(value_props, indent=2)}
Product info: {json.dumps(product_info, indent=2)}

Write landing page sections:

1. Hero (above the fold)
   - Headline (A/B variants)
   - Subheadline
   - CTA button text (2 variants)
   - Hero image description

2. Social Proof
   - Testimonial structure (3 quotes)
   - Logo bar text
   - Stats/metrics callout

3. Features (3 sections)
   - Benefit-focused headline
   - Supporting copy
   - Visual suggestion

4. Pricing
   - Plan names
   - Feature bullets
   - CTA copy

5. FAQ (5 questions)
   - Question and answer pairs

6. Final CTA
   - Headline
   - Subtext
   - Button text

Output as JSON."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=3500,
            system="Landing page copywriter. Write benefit-focused, conversion-optimized copy. No fluff.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def generate(self, product_info: Dict) -> Dict:
        """Complete workflow."""
        print("Step 1: Analyzing value propositions...")
        value_props = self.step1_value_prop_analysis(product_info)

        print("Step 2: Writing landing page sections...")
        sections = self.step2_write_sections(value_props, product_info)

        return {
            "value_propositions": value_props,
            "sections": sections
        }

# Usage
if __name__ == "__main__":
    generator = LandingPageGenerator(api_key=os.environ["ANTHROPIC_API_KEY"])

    product = {
        "name": "DevMetrics",
        "description": "Engineering analytics dashboard that shows real productivity, not just activity",
        "target_audience": "Engineering managers at 10-100 person startups",
        "features": [
            "DORA metrics automated from Git/Jira",
            "PR cycle time breakdown",
            "Focus time vs meeting time",
            "Sprint velocity trends"
        ],
        "pricing": {"starter": "$49/mo", "team": "$199/mo"}
    }

    result = generator.generate(product)

    with open("landing_page_copy.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Landing page copy generated!")
```

---

## When to Use Content Workflows vs. Alternatives

| Use This Library When... | Use Alternatives When... |
|---|---|
| Publishing <20 posts/month | Publishing 100+ posts/month (hire full-time writers) |
| Budget <$2K/month for content | Budget >$10K/month (hire agency) |
| Need fast turnaround (same-day) | Can wait 1-2 weeks per piece |
| Technical or niche topics (AI writes better than cheap writers) | Highly creative or storytelling-heavy (hire humans) |

**Cost comparison:**
- Freelance writer: $150-500 per 1500-word post
- Content agency: $2K-5K/month minimum
- This workflow: $19 one-time + $20-100/month API costs
