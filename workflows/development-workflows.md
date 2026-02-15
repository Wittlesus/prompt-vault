# Development Workflows - Production-Ready Automation Chains

Complete AI automation systems for software development tasks. Each workflow chains prompts together to produce production-ready code and documentation.

---

## Workflow 1: Code Review Agent (Full PR Analysis)

**What This Automates:** Reviews an entire pull request across all dimensions: bugs, security, performance, style, tests. Generates actionable review comments with file/line references.

**When to Use:** Every PR before merge, especially when team doesn't have senior reviewers available 24/7.

### The Complete Chain

```python
# save as: pr_review_agent.py
import anthropic
import subprocess
import json
from typing import Dict, List

class PRReviewAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def get_pr_diff(self, pr_number: int = None) -> str:
        """Get git diff for PR."""
        if pr_number:
            cmd = f"gh pr diff {pr_number}"
        else:
            cmd = "git diff main...HEAD"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    def step1_categorize_changes(self, diff: str) -> Dict:
        """Analyze diff and categorize changes."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1200,
            system="""You are a tech lead categorizing PR changes.
Analyze the diff and output JSON with:
- change_type: feature/bugfix/refactor/docs/test
- files_changed: array of {file, change_summary, risk_level}
- scope: frontend/backend/database/infrastructure
- estimated_complexity: low/medium/high
- breaking_changes: boolean""",
            messages=[{"role": "user", "content": f"Analyze this diff:\n\n{diff[:8000]}"}]
        )

        return json.loads(response.content[0].text)

    def step2_bug_detection(self, diff: str) -> List[Dict]:
        """Deep scan for bugs."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="""Senior engineer reviewing code for bugs.
Find ALL potential bugs: null refs, off-by-one, race conditions, unhandled errors, etc.
Output JSON array with: file, line_range, severity, description, suggested_fix.""",
            messages=[{"role": "user", "content": f"Review for bugs:\n\n{diff[:12000]}"}]
        )

        return json.loads(response.content[0].text)

    def step3_security_audit(self, diff: str) -> List[Dict]:
        """Security vulnerability scan."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            system="""Application security engineer.
Find security vulnerabilities: injection, XSS, auth bypass, secrets, PII exposure.
Output JSON array with: file, line_range, vulnerability, risk_level, remediation.""",
            messages=[{"role": "user", "content": f"Security audit:\n\n{diff[:12000]}"}]
        )

        return json.loads(response.content[0].text)

    def step4_performance_review(self, diff: str) -> List[Dict]:
        """Performance optimization suggestions."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            system="""Performance engineer reviewing code.
Find: N+1 queries, missing indexes, memory leaks, blocking operations, inefficient algorithms.
Output JSON array with: file, line_range, issue, impact_estimate, optimization.""",
            messages=[{"role": "user", "content": f"Performance review:\n\n{diff[:12000]}"}]
        )

        return json.loads(response.content[0].text)

    def step5_test_coverage_analysis(self, diff: str) -> Dict:
        """Analyze test coverage."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system="""QA engineer reviewing tests.
Output JSON with: has_tests (boolean), test_files (array), coverage_assessment, missing_tests (array of scenarios).""",
            messages=[{"role": "user", "content": f"Analyze test coverage:\n\n{diff[:10000]}"}]
        )

        return json.loads(response.content[0].text)

    def step6_generate_review_comment(self, analysis: Dict) -> str:
        """Generate final review comment."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system="""Tech lead writing PR review comments. Be constructive, specific, and actionable.
Format as Markdown with sections: Summary, Blocking Issues, Suggestions, What Looks Good.""",
            messages=[{"role": "user", "content": f"Write review comment:\n{json.dumps(analysis, indent=2)}"}]
        )

        return response.content[0].text

    def review_pr(self, pr_number: int = None) -> Dict:
        """Complete PR review workflow."""
        print("Fetching PR diff...")
        diff = self.get_pr_diff(pr_number)

        print("Step 1: Categorizing changes...")
        categorization = self.step1_categorize_changes(diff)
        print(f"Change type: {categorization['change_type']}, Complexity: {categorization['estimated_complexity']}")

        print("Step 2: Bug detection...")
        bugs = self.step2_bug_detection(diff)
        print(f"Found {len(bugs)} potential bugs")

        print("Step 3: Security audit...")
        security = self.step3_security_audit(diff)
        print(f"Found {len(security)} security concerns")

        print("Step 4: Performance review...")
        performance = self.step4_performance_review(diff)
        print(f"Found {len(performance)} performance issues")

        print("Step 5: Test coverage analysis...")
        tests = self.step5_test_coverage_analysis(diff)

        analysis = {
            "categorization": categorization,
            "bugs": bugs,
            "security": security,
            "performance": performance,
            "test_coverage": tests
        }

        print("Step 6: Generating review comment...")
        review_comment = self.step6_generate_review_comment(analysis)

        return {
            "analysis": analysis,
            "review_comment": review_comment,
            "verdict": self._determine_verdict(bugs, security)
        }

    def _determine_verdict(self, bugs: List, security: List) -> str:
        """Determine approval status."""
        critical_bugs = [b for b in bugs if b.get('severity') == 'critical']
        high_security = [s for s in security if s.get('risk_level') in ['critical', 'high']]

        if critical_bugs or high_security:
            return "REQUEST_CHANGES"
        elif bugs or security:
            return "APPROVE_WITH_COMMENTS"
        else:
            return "APPROVE"

# Usage
if __name__ == "__main__":
    import os

    agent = PRReviewAgent(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Review current branch vs main
    result = agent.review_pr()

    # Save review
    with open("pr_review.md", "w") as f:
        f.write(f"# PR Review\n\n")
        f.write(f"**Verdict:** {result['verdict']}\n\n")
        f.write(result['review_comment'])

    with open("pr_review_detailed.json", "w") as f:
        json.dump(result['analysis'], f, indent=2)

    print(f"\n{'='*50}")
    print(f"VERDICT: {result['verdict']}")
    print(f"{'='*50}")
```

### JavaScript Version

```javascript
// save as: prReviewAgent.js
import Anthropic from '@anthropic-ai/sdk';
import { execSync } from 'child_process';
import fs from 'fs/promises';

class PRReviewAgent {
  constructor(apiKey) {
    this.client = new Anthropic({ apiKey });
  }

  getPRDiff(prNumber = null) {
    const cmd = prNumber ? `gh pr diff ${prNumber}` : 'git diff main...HEAD';
    return execSync(cmd, { encoding: 'utf-8' });
  }

  async step1CategorizeChanges(diff) {
    const response = await this.client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1200,
      system: `Tech lead categorizing PR changes. Output JSON with: change_type, files_changed, scope, estimated_complexity, breaking_changes.`,
      messages: [{ role: 'user', content: `Analyze:\n\n${diff.substring(0, 8000)}` }]
    });

    return JSON.parse(response.content[0].text);
  }

  async step2BugDetection(diff) {
    const response = await this.client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 2000,
      system: `Senior engineer finding bugs. Output JSON array with: file, line_range, severity, description, suggested_fix.`,
      messages: [{ role: 'user', content: `Review for bugs:\n\n${diff.substring(0, 12000)}` }]
    });

    return JSON.parse(response.content[0].text);
  }

  async reviewPR(prNumber = null) {
    console.log('Fetching PR diff...');
    const diff = this.getPRDiff(prNumber);

    console.log('Step 1: Categorizing changes...');
    const categorization = await this.step1CategorizeChanges(diff);

    console.log('Step 2: Bug detection...');
    const bugs = await this.step2BugDetection(diff);

    // Steps 3-6 similar to Python version...

    return { categorization, bugs };
  }
}

const agent = new PRReviewAgent(process.env.ANTHROPIC_API_KEY);
const result = await agent.reviewPR();
console.log('Review complete:', result);
```

---

## Workflow 2: Documentation Generator (README + API Docs)

**What This Automates:** Reads your codebase and generates comprehensive README, API documentation, and code comments.

### Complete Script

```python
# save as: docs_generator.py
import anthropic
import os
import json
from pathlib import Path
from typing import List, Dict

class DocumentationGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def scan_codebase(self, root_dir: str) -> Dict:
        """Scan codebase structure."""
        structure = {
            "entry_points": [],
            "core_modules": [],
            "api_routes": [],
            "config_files": []
        }

        # Find entry points
        for pattern in ["main.py", "index.js", "app.py", "server.js"]:
            matches = list(Path(root_dir).rglob(pattern))
            if matches:
                structure["entry_points"].extend([str(m) for m in matches])

        # Find API routes
        for pattern in ["*routes*.py", "*routes*.js", "*api*.py", "*controller*.js"]:
            matches = list(Path(root_dir).rglob(pattern))
            structure["api_routes"].extend([str(m) for m in matches[:10]])

        return structure

    def step1_analyze_codebase(self, files: List[str]) -> Dict:
        """Understand what the codebase does."""
        code_samples = []
        for f in files[:5]:  # First 5 files
            try:
                with open(f, 'r') as file:
                    code_samples.append(f"File: {f}\n{file.read()[:2000]}")
            except:
                pass

        prompt = f"""Analyze this codebase:

{chr(10).join(code_samples)}

Output JSON with:
- project_type (web_app/cli_tool/library/api/other)
- tech_stack (array)
- main_features (array of features)
- target_users (who uses this)
- architecture_pattern (MVC/microservices/serverless/etc)"""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1200,
            system="Senior developer analyzing codebases. Identify patterns and purpose.",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def step2_generate_readme(self, analysis: Dict, package_name: str) -> str:
        """Generate README.md."""
        prompt = f"""Project: {package_name}
Analysis: {json.dumps(analysis, indent=2)}

Generate comprehensive README.md with:
- Project title and tagline
- What it does (2-3 sentences)
- Key features (bulleted)
- Installation
- Quick start / Usage
- API reference (if applicable)
- Configuration
- Contributing
- License

Use clear examples. Write for developers who've never seen this project."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2500,
            system="Technical writer creating README files. Clear, practical, example-driven.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def step3_generate_api_docs(self, api_files: List[str]) -> str:
        """Generate API documentation."""
        api_code = []
        for f in api_files[:5]:
            try:
                with open(f, 'r') as file:
                    api_code.append(f"File: {f}\n{file.read()}")
            except:
                pass

        if not api_code:
            return "No API routes found."

        prompt = f"""API route files:

{chr(10).join(api_code)}

Generate API documentation with:
- Endpoint list with HTTP method and path
- Request parameters (path, query, body)
- Response format and status codes
- Example requests using curl
- Authentication requirements

Format as Markdown."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=3000,
            system="API documentation specialist. Write clear, complete API docs with examples.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def step4_add_code_comments(self, file_path: str) -> str:
        """Add docstrings/comments to code."""
        with open(file_path, 'r') as f:
            code = f.read()

        prompt = f"""Add comprehensive comments/docstrings to this code:

{code}

For each function/class:
- Purpose
- Parameters with types
- Return value
- Example usage (if non-trivial)

Return the fully commented code."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            system="Senior developer adding documentation. Write helpful, concise comments.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def generate(self, root_dir: str, package_name: str) -> Dict:
        """Complete documentation workflow."""
        print("Scanning codebase...")
        structure = self.scan_codebase(root_dir)

        print("Step 1: Analyzing codebase...")
        analysis = self.step1_analyze_codebase(
            structure["entry_points"] + structure["core_modules"]
        )
        print(f"Project type: {analysis['project_type']}")

        print("Step 2: Generating README...")
        readme = self.step2_generate_readme(analysis, package_name)

        print("Step 3: Generating API docs...")
        api_docs = self.step3_generate_api_docs(structure["api_routes"])

        return {
            "analysis": analysis,
            "readme": readme,
            "api_docs": api_docs
        }

# Usage
if __name__ == "__main__":
    import os

    generator = DocumentationGenerator(api_key=os.environ["ANTHROPIC_API_KEY"])

    result = generator.generate(
        root_dir="./my-project",
        package_name="MyAwesomeProject"
    )

    # Save README
    with open("README.md", "w") as f:
        f.write(result["readme"])

    # Save API docs
    with open("API_DOCS.md", "w") as f:
        f.write(result["api_docs"])

    print("Documentation generated!")
```

---

## Workflow 3: Test Suite Generator

**What This Automates:** Analyzes your code and generates comprehensive unit tests, integration tests, and edge case tests.

### Complete Script

```python
# save as: test_generator.py
import anthropic
import os
from typing import Dict, List

class TestGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_analyze_code_for_testing(self, code: str, file_path: str) -> Dict:
        """Identify what needs testing."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            system="""QA engineer analyzing code for testing needs.
Output JSON with:
- functions_to_test (array with: name, complexity, critical_path)
- edge_cases (array of scenarios)
- integration_points (external services, DB, API calls)
- test_framework_recommendation (jest/pytest/etc based on code)""",
            messages=[{"role": "user", "content": f"File: {file_path}\n\n{code}"}]
        )

        return json.loads(response.content[0].text)

    def step2_generate_unit_tests(self, code: str, analysis: Dict, framework: str) -> str:
        """Generate unit tests."""
        prompt = f"""Code to test:
{code}

Analysis: {json.dumps(analysis)}

Generate comprehensive unit tests using {framework}:
- Test each function's happy path
- Test edge cases
- Test error handling
- Use descriptive test names
- Include setup/teardown if needed
- Mock external dependencies

Return complete test file ready to run."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=3500,
            system=f"Expert {framework} test writer. Write thorough, maintainable tests.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def step3_generate_integration_tests(self, code: str, analysis: Dict, framework: str) -> str:
        """Generate integration tests."""
        if not analysis.get('integration_points'):
            return "# No integration points found"

        prompt = f"""Code: {code}

Integration points: {json.dumps(analysis['integration_points'])}

Generate integration tests for:
- API endpoint tests (full request/response cycle)
- Database interaction tests
- External service integration

Use {framework}. Include test fixtures and cleanup."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2500,
            system=f"{framework} integration test specialist. Test real interactions.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def generate(self, file_path: str) -> Dict:
        """Complete test generation workflow."""
        print(f"Reading {file_path}...")
        with open(file_path, 'r') as f:
            code = f.read()

        print("Step 1: Analyzing code for testing needs...")
        analysis = self.step1_analyze_code_for_testing(code, file_path)
        framework = analysis['test_framework_recommendation']
        print(f"Test framework: {framework}")

        print("Step 2: Generating unit tests...")
        unit_tests = self.step2_generate_unit_tests(code, analysis, framework)

        print("Step 3: Generating integration tests...")
        integration_tests = self.step3_generate_integration_tests(code, analysis, framework)

        return {
            "analysis": analysis,
            "unit_tests": unit_tests,
            "integration_tests": integration_tests,
            "framework": framework
        }

# Usage
if __name__ == "__main__":
    generator = TestGenerator(api_key=os.environ["ANTHROPIC_API_KEY"])

    result = generator.generate(file_path="./src/api/users.js")

    # Save tests
    ext = "test.js" if "jest" in result["framework"].lower() else "test.py"
    with open(f"users.{ext}", "w") as f:
        f.write(result["unit_tests"])

    with open(f"users.integration.{ext}", "w") as f:
        f.write(result["integration_tests"])

    print(f"Tests generated! Framework: {result['framework']}")
```

---

## Workflow 4: Bug Triage & Root Cause Analysis

**What This Automates:** Analyzes error logs, stack traces, and code context to diagnose bugs and suggest fixes.

### Complete Script

```python
# save as: bug_triage.py
import anthropic
import json
from typing import Dict

class BugTriageAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def step1_categorize_error(self, error_log: str) -> Dict:
        """Categorize the error."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=800,
            system="""Senior engineer triaging bugs. Categorize errors.
Output JSON with: error_type, severity, affected_component, likely_cause, urgency.""",
            messages=[{"role": "user", "content": f"Categorize this error:\n{error_log}"}]
        )

        return json.loads(response.content[0].text)

    def step2_root_cause_analysis(self, error_log: str, code_context: str) -> Dict:
        """Find root cause."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            system="""Debugging specialist. Perform root cause analysis.
Output JSON with: root_cause, contributing_factors, reproduction_steps, similar_issues.""",
            messages=[{"role": "user", "content": f"Error:\n{error_log}\n\nCode:\n{code_context}"}]
        )

        return json.loads(response.content[0].text)

    def step3_suggest_fix(self, analysis: Dict, code_context: str) -> str:
        """Generate fix."""
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1200,
            system="""Senior developer suggesting bug fixes. Provide working code fixes.""",
            messages=[{"role": "user", "content": f"Analysis: {json.dumps(analysis)}\n\nCode:\n{code_context}\n\nSuggest fix."}]
        )

        return response.content[0].text

    def triage(self, error_log: str, code_context: str = "") -> Dict:
        """Complete triage workflow."""
        print("Step 1: Categorizing error...")
        category = self.step1_categorize_error(error_log)
        print(f"Error type: {category['error_type']}, Severity: {category['severity']}")

        print("Step 2: Root cause analysis...")
        rca = self.step2_root_cause_analysis(error_log, code_context)

        print("Step 3: Suggesting fix...")
        fix = self.step3_suggest_fix(rca, code_context)

        return {
            "category": category,
            "root_cause": rca,
            "suggested_fix": fix
        }

# Usage
error = """
TypeError: Cannot read property 'email' of undefined
  at getUserEmail (src/utils/user.js:42:18)
  at processRequest (src/api/auth.js:67:22)
"""

code = """
function getUserEmail(user) {
  return user.profile.email;  // Line 42
}
"""

agent = BugTriageAgent(api_key=os.environ["ANTHROPIC_API_KEY"])
result = agent.triage(error, code)
print(json.dumps(result, indent=2))
```

---

## When to Use Development Workflows vs. Manual Review

| Use Workflows When... | Manual Review When... |
|---|---|
| No senior engineers available 24/7 | Complex architectural decisions |
| Team <10 engineers (everyone's stretched thin) | Security-critical components |
| Fast iteration cycles (multiple PRs/day) | First implementation of critical algorithm |
| Learning/onboarding junior devs | Customer-facing code with brand implications |

**Time savings:**
- Manual PR review: 30-60 minutes
- Automated review: 2-3 minutes
- Manual documentation: 2-4 hours
- Automated docs: 5 minutes
