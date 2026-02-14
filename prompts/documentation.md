# Documentation Prompts

A collection of 10 battle-tested prompts for generating high-quality documentation. These prompts turn the chore of writing docs into a one-shot copy-paste operation.

---

## 1. README Generator

**Use Case:** Generate a comprehensive, professional README.md for any project, covering all the sections developers expect.

**Prompt:**

```
You are a technical writer creating a world-class README.md for an open-source project.

Based on the following project information, generate a complete README.md with these sections:

1. **Project Title & Badges** (build status, npm version, license, coverage)
2. **One-line Description**: What this project does in one sentence
3. **Key Features**: 5-8 bullet points highlighting what makes this project useful
4. **Quick Start**: Get up and running in under 2 minutes
5. **Installation**: Detailed setup for all supported platforms/package managers
6. **Usage**: 3 practical code examples from simple to advanced
7. **API Reference**: Table of main functions/methods with parameters and return types
8. **Configuration**: All config options with defaults and descriptions
9. **Architecture**: Brief overview of project structure
10. **Contributing**: How to submit issues and PRs
11. **FAQ**: 5 common questions with answers
12. **License**: License type and link

Formatting rules:
- Use clear, concise language (8th grade reading level)
- Include copy-pasteable code blocks with syntax highlighting
- Add a table of contents with anchor links
- Use tables for structured data (config options, API reference)

Project information:
"""
[PASTE: project name, tech stack, purpose, main features, install command, basic usage]
"""
```

**Example Output Snippet:**

```markdown
# SuperCache

> Blazing-fast, type-safe caching for Node.js with automatic invalidation.

[![npm](https://img.shields.io/npm/v/supercache)](https://npmjs.com/supercache)
[![CI](https://github.com/user/supercache/actions/workflows/ci.yml/badge.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]()

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
...

## Quick Start

```bash
npm install supercache
```

```typescript
import { Cache } from 'supercache';

const cache = new Cache({ ttl: '5m' });
await cache.set('user:1', userData);
const user = await cache.get('user:1'); // typed!
```
```

**Tips for Customization:**
- Include your actual package.json for accurate install commands
- Add screenshots or GIFs for visual projects
- Specify tone: "Write for a developer audience" vs "Write for non-technical users"

---

## 2. API Documentation Generator

**Use Case:** Generate complete API documentation from endpoint code, including request/response schemas, auth, and examples.

**Prompt:**

```
You are an API documentation specialist. Generate comprehensive REST API documentation from the following endpoint code.

For EACH endpoint, document:

### Endpoint Header
- **Method & Path**: `GET /api/v1/resource`
- **Description**: What this endpoint does
- **Authentication**: Required auth type (Bearer token, API key, none)
- **Rate Limit**: If applicable

### Request
- **Headers**: Required and optional headers (table format)
- **Path Parameters**: Name, type, description, required/optional
- **Query Parameters**: Name, type, description, default value, constraints
- **Request Body**: Full JSON schema with field descriptions and validation rules

### Response
- **Success Response**: Status code + full JSON example
- **Error Responses**: All possible error codes with example bodies
- **Response Headers**: Any custom headers returned

### Example
- **cURL**: Complete copy-pasteable cURL command
- **JavaScript**: fetch/axios example
- **Python**: requests library example

Use OpenAPI 3.0 terminology and format where possible.

Endpoint code:
"""
[PASTE YOUR ROUTE/CONTROLLER CODE HERE]
"""
```

**Example Output Snippet:**

```markdown
## Create User

`POST /api/v1/users`

Create a new user account.

**Authentication:** Bearer Token (admin role required)

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address |
| `name` | string | Yes | Full name (2-100 chars) |
| `role` | enum | No | `user`, `admin`, `viewer`. Default: `user` |

```json
{
  "email": "jane@example.com",
  "name": "Jane Doe",
  "role": "admin"
}
```

### Response

**201 Created**
```json
{
  "id": "usr_abc123",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "role": "admin",
  "createdAt": "2025-01-15T08:30:00Z"
}
```

### cURL Example
```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","name":"Jane Doe"}'
```
```

**Tips for Customization:**
- Add: "Include webhook documentation for async events"
- Specify: "Generate OpenAPI 3.0 YAML as well"
- Include auth details: "We use JWT tokens with refresh rotation"

---

## 3. JSDoc / TSDoc Comment Generator

**Use Case:** Generate thorough inline documentation comments for functions, classes, and modules.

**Prompt:**

```
You are a documentation expert generating JSDoc (or TSDoc) comments for production TypeScript/JavaScript code.

For each function, class, method, and exported constant in the following code, generate comprehensive documentation comments:

### For Functions/Methods:
- `@description` - What the function does and when to use it
- `@param` - Every parameter with type and description
- `@returns` - Return type and what it represents
- `@throws` - Every error type the function can throw and when
- `@example` - At least one usage example with expected output
- `@since` - Version when introduced (use "1.0.0" as default)
- `@see` - Related functions or external references

### For Classes:
- Class-level description of purpose and responsibilities
- `@example` of instantiation and basic usage

### For Types/Interfaces:
- Description of what the type represents
- Each property documented with description and constraints

### Rules:
- Be specific, not generic ("Validates email format using RFC 5322 regex" NOT "Validates the input")
- Document edge cases and gotchas
- Include param constraints ("Must be positive integer", "Max 100 chars")
- Use complete sentences

Return the FULL original code with documentation comments added above each item.

Code to document:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```typescript
/**
 * Calculates the compound interest for a given principal amount over time.
 *
 * Uses the standard compound interest formula: A = P(1 + r/n)^(nt)
 * Results are rounded to 2 decimal places for currency representation.
 *
 * @param principal - The initial investment amount in dollars. Must be positive.
 * @param annualRate - Annual interest rate as a decimal (e.g., 0.05 for 5%). Must be between 0 and 1.
 * @param compoundsPerYear - Number of times interest compounds per year. Typically 1, 4, 12, or 365.
 * @param years - Investment duration in years. Must be positive integer.
 * @returns The final amount including principal and earned interest, rounded to 2 decimal places.
 * @throws {RangeError} If principal or years is negative or zero.
 * @throws {TypeError} If any parameter is not a finite number.
 *
 * @example
 * // Calculate 5% annual interest compounded monthly for 10 years on $1000
 * const result = calculateCompoundInterest(1000, 0.05, 12, 10);
 * console.log(result); // 1647.01
 *
 * @since 1.0.0
 * @see {@link calculateSimpleInterest} for non-compounding calculation
 */
function calculateCompoundInterest(
  principal: number,
  annualRate: number,
  compoundsPerYear: number,
  years: number
): number {
```

**Tips for Customization:**
- Specify: "Use Python docstrings (Google style)" for Python projects
- Add: "Include `@deprecated` tags for functions being phased out"
- For libraries: "Include `@public` or `@internal` visibility tags"

---

## 4. Changelog Entry Writer

**Use Case:** Generate well-structured changelog entries from git diffs, commit messages, or PR descriptions.

**Prompt:**

```
You are a technical writer maintaining a changelog following the Keep a Changelog (keepachangelog.com) format.

Based on the following changes, generate changelog entries organized by:

### Categories:
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

### Rules:
- Write from the USER's perspective, not the developer's
- Start each entry with a verb (Add, Fix, Change, Remove, Improve)
- Include issue/PR references where available
- Be specific about what changed and why it matters
- Group related changes together
- Order by importance within each category

### Format:
```
## [X.Y.Z] - YYYY-MM-DD

### Added
- Add dark mode support for all dashboard pages (#234)

### Fixed
- Fix crash when uploading files larger than 10MB (#456)
```

Changes to document:
"""
[PASTE: git log, commit messages, PR descriptions, or diff summaries]
"""
```

**Example Output Snippet:**

```markdown
## [2.3.0] - 2025-01-15

### Added
- Add bulk export functionality for reports in CSV and PDF formats (#892)
- Add keyboard shortcuts for common actions (Ctrl+S to save, Ctrl+K to search) (#901)
- Add webhook notifications for failed payment events (#887)

### Changed
- Improve search performance by 3x with new indexing strategy (#895)
- Update user avatar component to support WebP format (#903)

### Fixed
- Fix race condition causing duplicate email notifications (#889)
- Fix incorrect timezone display for users in UTC+ zones (#891)
- Fix memory leak in real-time dashboard when left open for 24+ hours (#894)

### Security
- Upgrade `jsonwebtoken` from 8.5.1 to 9.0.0 to fix CVE-2022-23529 (#900)
```

**Tips for Customization:**
- Provide your git log: `git log --oneline v2.2.0..HEAD`
- Specify semver: "Determine if this is a MAJOR, MINOR, or PATCH release"
- Add audience: "This changelog is read by non-technical customers"

---

## 5. Architecture Documentation

**Use Case:** Generate architecture decision records (ADRs) and system design documentation from code structure.

**Prompt:**

```
You are a solutions architect creating architecture documentation for a development team.

Based on the following system information, generate comprehensive architecture documentation:

## 1. System Overview
- High-level description of what the system does
- System context diagram description (external systems, users, data flows)
- Key architectural decisions and rationale

## 2. Component Architecture
- List all major components/services
- For each component: purpose, technology, ownership
- Component interaction diagram description (who calls whom)

## 3. Data Architecture
- Data stores used (databases, caches, queues, object storage)
- Data flow between components
- Data ownership and boundaries
- Data retention and backup policies

## 4. Infrastructure
- Deployment topology (cloud provider, regions, AZs)
- Scaling strategy (horizontal vs vertical, auto-scaling triggers)
- CI/CD pipeline overview

## 5. Cross-Cutting Concerns
- Authentication & Authorization flow
- Logging, monitoring, and alerting strategy
- Error handling patterns
- Caching strategy

## 6. Architecture Decision Records (ADRs)
For the 3 most significant architectural decisions, write an ADR:
- **Title**: Short decision description
- **Status**: Accepted/Proposed/Deprecated
- **Context**: What problem we faced
- **Decision**: What we chose and why
- **Consequences**: Tradeoffs and implications

System information:
"""
[PASTE: tech stack, folder structure, infrastructure details, team context]
"""
```

**Example Output Snippet:**

```markdown
# System Architecture: OrderFlow

## System Overview

OrderFlow is an event-driven e-commerce order management system processing
~50,000 orders/day across 3 geographic regions. It handles the complete order
lifecycle from cart checkout through fulfillment and returns.

## ADR-001: Event-Driven Architecture over Request-Response

**Status:** Accepted (2024-06-15)

**Context:** Our monolithic order processing system couldn't scale beyond
20K orders/day. Synchronous processing meant a slow payment gateway would
block the entire order pipeline.

**Decision:** Adopt event-driven architecture using Apache Kafka as the
event backbone. Each domain (payments, inventory, shipping) becomes an
independent consumer.

**Consequences:**
- (+) Each service scales independently
- (+) Payment gateway latency doesn't block order confirmation
- (-) Increased operational complexity (Kafka cluster management)
- (-) Eventual consistency requires idempotent consumers
- (-) Debugging distributed transactions is harder (adopted correlation IDs)
```

**Tips for Customization:**
- Include your folder structure output: `tree -L 2`
- Add: "We are migrating from monolith to microservices"
- Specify audience: "This document is for new engineers during onboarding"

---

## 6. Onboarding Guide Generator

**Use Case:** Create a step-by-step onboarding guide for new developers joining a project.

**Prompt:**

```
You are creating a developer onboarding guide that takes a new team member from zero to productive in their first week.

Based on the following project information, create a comprehensive onboarding document:

## Day 1: Environment Setup
- Prerequisites checklist (OS, tools, accounts needed)
- Step-by-step local development setup with exact commands
- How to verify everything is working (smoke test)
- Common setup problems and solutions (troubleshooting FAQ)

## Day 2: Codebase Tour
- Project structure walkthrough (what lives where)
- Key files every developer should know about
- Architecture overview (keep it simple, link to detailed docs)
- Data flow for the most common user action (trace a request end-to-end)

## Day 3: Development Workflow
- Branch naming convention
- How to create and submit a PR
- Code review process and expectations
- CI/CD pipeline: what runs and what it checks
- How to deploy to staging vs production

## Day 4: Key Concepts & Domain Knowledge
- Glossary of domain terms the team uses
- Business context: what problem does this solve?
- Key integrations with external services
- Common gotchas and tribal knowledge

## Day 5: First Task
- Suggested starter tasks (good first issues)
- Who to ask for help and how (Slack channels, office hours)
- Useful bookmarks and dashboards
- 30/60/90 day expectations

Write in a warm, encouraging tone. Include exact commands (not "install the dependencies" but "npm install"). Assume the reader is a competent developer who is simply new to THIS project.

Project information:
"""
[PASTE: tech stack, repo URL, team tools (Slack, Jira, etc.), development process]
"""
```

**Example Output Snippet:**

```markdown
# Welcome to the Acme Platform Team! 🎉

## Day 1: Getting Your Environment Ready

### Prerequisites Checklist
- [ ] macOS 13+ or Ubuntu 22.04+ (Windows users: use WSL2)
- [ ] Node.js 20.x (`nvm install 20`)
- [ ] Docker Desktop 4.x+
- [ ] GitHub account added to `acme-platform` org (ask @sarah in #eng-onboarding)
- [ ] 1Password vault access for development secrets

### Local Setup (15 minutes)

```bash
# 1. Clone the repo
git clone git@github.com:acme/platform.git
cd platform

# 2. Copy environment variables
cp .env.example .env.local
# Ask in #eng-onboarding for the DATABASE_URL and API_KEY values

# 3. Start infrastructure (Postgres, Redis, LocalStack)
docker compose up -d

# 4. Install dependencies and run migrations
npm install
npm run db:migrate
npm run db:seed

# 5. Start the dev server
npm run dev
# Open http://localhost:3000 - you should see the login page
```

### "It's Not Working" Troubleshooting
| Symptom | Fix |
|---------|-----|
| `ECONNREFUSED :5432` | Docker isn't running. Start Docker Desktop first. |
| `Module not found` | Delete `node_modules` and run `npm install` again |
| Blank page at localhost | Check browser console. Usually a missing `.env.local` variable |
```

**Tips for Customization:**
- Include your actual .env.example variables
- Add: "Include a section on our on-call rotation and incident response"
- Specify: "We use pnpm, not npm"

---

## 7. Code Comment Explainer

**Use Case:** Add clear explanatory comments to complex, algorithmic, or legacy code that is hard to understand.

**Prompt:**

```
You are a senior developer adding explanatory comments to complex code to make it understandable for mid-level developers.

Review the following code and add comments that explain:

1. **Purpose**: What does this block of code accomplish? (at the top)
2. **Why, Not What**: Explain WHY decisions were made, not what the code literally does
   - Bad: `// increment i` (obvious from the code)
   - Good: `// Skip the header row which contains column names, not data`
3. **Algorithm Explanation**: For complex algorithms, explain the approach in plain English
4. **Business Logic**: Explain business rules that aren't obvious from the code
5. **Gotchas**: Mark non-obvious behavior, workarounds, or things that look wrong but are intentional
6. **Performance Notes**: Why a particular approach was chosen for performance reasons
7. **TODO/FIXME**: Flag areas that need improvement with specific descriptions

### Rules:
- Don't state the obvious (no `// returns the result` before a return statement)
- Use `//` for single-line, `/** */` for function-level documentation
- Keep comments concise (1-2 lines max per comment)
- Mark workarounds with `// WORKAROUND:` and link to the issue
- Mark temporary code with `// TODO:` and a description of the proper fix

Return the complete code with comments added.

Code to comment:
"""
[PASTE YOUR COMPLEX OR LEGACY CODE HERE]
"""
```

**Example Output Snippet:**

```javascript
/**
 * Distributes inventory across warehouses using a weighted round-robin
 * algorithm that accounts for warehouse capacity and shipping zones.
 */
function distributeInventory(items, warehouses) {
  // Sort warehouses by available capacity (descending) so we fill
  // the most available warehouse first, preventing overflow situations
  const sorted = warehouses.sort((a, b) => b.capacity - a.capacity);

  // WORKAROUND: The Midwest warehouse API reports capacity 2x higher
  // than actual. Halve it until they fix their reporting (JIRA-4521)
  sorted.forEach(w => {
    if (w.region === 'midwest') w.capacity = Math.floor(w.capacity / 2);
  });

  // Use modular arithmetic to cycle through warehouses. This ensures
  // even distribution even when item count isn't divisible by warehouse count.
  for (let i = 0; i < items.length; i++) {
    const warehouseIndex = i % sorted.length;
    // ...
  }
}
```

**Tips for Customization:**
- Specify: "This is legacy code from 2018 with no original authors available"
- Add: "Focus on the business logic - our new team members struggle with domain concepts"
- Include context: "This implements the Raft consensus algorithm"

---

## 8. Inline Tutorial / Walkthrough

**Use Case:** Generate a step-by-step tutorial that walks through a feature implementation, suitable for a blog post or internal wiki.

**Prompt:**

```
You are a technical educator creating a step-by-step tutorial that teaches developers how to build a feature from scratch.

Based on the following completed implementation, reverse-engineer a tutorial that:

### Structure:
1. **Introduction** (2-3 paragraphs)
   - What we're building and why
   - What the reader will learn
   - Prerequisites (knowledge, tools, accounts needed)

2. **Step-by-Step Implementation** (5-10 steps)
   For each step:
   - What we're doing and why
   - The complete code for this step (not diffs - full files as they should look)
   - Explanation of key decisions
   - Common mistakes to avoid at this step
   - How to verify this step works (expected output)

3. **Testing** (1-2 steps)
   - How to write tests for what we built
   - Complete test code

4. **Conclusion**
   - Recap what we built
   - Possible extensions and next steps
   - Links to further reading

### Writing Rules:
- Write like you're pair programming with the reader
- Every code block should be complete and runnable (no `...` or `// rest of code`)
- Explain the "why" before the "how"
- Include expected terminal output after commands
- Call out potential confusion points proactively

Implementation code:
"""
[PASTE YOUR COMPLETED FEATURE CODE HERE]
"""
```

**Example Output Snippet:**

```markdown
# Building Real-Time Notifications with WebSockets

In this tutorial, we'll add real-time notifications to our Express app using
Socket.IO. By the end, users will see notifications pop up instantly without
refreshing the page.

**What you'll learn:**
- Setting up Socket.IO with an existing Express server
- Authenticating WebSocket connections with JWT
- Broadcasting events to specific users
- Handling reconnection gracefully

**Prerequisites:** Node.js 18+, existing Express app with JWT auth

## Step 1: Install Dependencies

```bash
npm install socket.io socket.io-client
```

## Step 2: Initialize Socket.IO Alongside Express

We need to attach Socket.IO to the same HTTP server that Express uses.
The key insight: Express and Socket.IO share the same port but handle
different protocols (HTTP vs WebSocket).

```javascript
// server.js
const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');

const app = express();
const httpServer = createServer(app);  // wrap Express in raw HTTP server
const io = new Server(httpServer, {
  cors: { origin: "http://localhost:3000" }
});

// IMPORTANT: use httpServer.listen(), not app.listen()
// app.listen() creates its own HTTP server that Socket.IO doesn't know about
httpServer.listen(4000, () => console.log('Server on :4000'));
```

**Verify it works:**
```
$ node server.js
Server on :4000
```
```

**Tips for Customization:**
- Specify: "Write for intermediate developers familiar with React but new to WebSockets"
- Add: "Include a troubleshooting section at the end"
- Mention: "This will be published on our engineering blog"

---

## 9. Migration Guide Writer

**Use Case:** Generate upgrade/migration guides when changing major versions, frameworks, or APIs.

**Prompt:**

```
You are a developer experience writer creating a migration guide that helps developers upgrade safely and confidently.

Based on the following changes between versions, create a migration guide:

### Structure:

## Overview
- What's changing and why
- Timeline (when does the old version reach EOL?)
- Estimated migration effort (small/medium/large)

## Breaking Changes
For EACH breaking change:
1. **What Changed**: Precise description
2. **Before (Old)**: Code example of the old way
3. **After (New)**: Code example of the new way
4. **Automated Fix**: Codemod or find-replace command if available
5. **Manual Steps**: If automation isn't possible, exact steps to fix

## Deprecation Warnings
- What's deprecated but still working
- When it will be removed
- How to migrate proactively

## New Features
- What's new and why you should adopt it
- Quick examples of new APIs

## Step-by-Step Migration
1. Preparation checklist
2. Ordered list of changes to make (dependency order matters!)
3. How to test after each step
4. Rollback plan if something goes wrong

## FAQ
- Common questions and concerns about the migration

### Rules:
- Show COMPLETE before/after code examples (not partial snippets)
- Include grep/find commands to locate all instances that need changing
- Test commands to verify migration success at each step

Version changes:
"""
[PASTE: changelog, breaking changes list, old API vs new API]
"""
```

**Example Output Snippet:**

```markdown
# Migration Guide: v3.x to v4.0

## Overview
v4.0 replaces the callback-based API with async/await and drops Node.js 16 support.
**Estimated effort**: 2-4 hours for most projects.

## Breaking Change #1: Async API

**What Changed**: All database methods now return Promises instead of accepting callbacks.

**Find affected code:**
```bash
grep -rn "\.find(\|\.save(\|\.delete(" src/ --include="*.js" | grep "callback\|function\|=>"
```

**Before (v3):**
```javascript
db.find({ id: 1 }, function(err, result) {
  if (err) return handleError(err);
  console.log(result);
});
```

**After (v4):**
```javascript
try {
  const result = await db.find({ id: 1 });
  console.log(result);
} catch (err) {
  handleError(err);
}
```

**Automated Fix:**
```bash
npx our-codemod callback-to-async src/
```
```

**Tips for Customization:**
- Include your actual old and new API signatures
- Add: "Include a section on database migration scripts"
- Specify: "Our users are on versions ranging from 2.x to 3.x"

---

## 10. Runbook / Operations Guide

**Use Case:** Generate runbooks for common operational tasks, incident response, and maintenance procedures.

**Prompt:**

```
You are an SRE writing operational runbooks for a production system. These runbooks will be used by on-call engineers at 3am, so they must be crystal clear and actionable.

Based on the following system information, generate runbooks for common operational scenarios:

### Runbook Format (for each scenario):

## [Scenario Name]

**Severity**: P1/P2/P3/P4
**Time to Resolve**: Estimated
**Escalation**: Who to contact if this doesn't work

### Symptoms
- What alerts fire
- What the user sees
- What dashboards show

### Diagnosis
1. Step-by-step commands to identify the root cause
2. Include exact commands with expected output
3. Decision tree: "If you see X, go to Step A. If you see Y, go to Step B."

### Resolution
1. Step-by-step fix with exact commands
2. How to verify the fix worked
3. How to communicate status to stakeholders

### Prevention
- What to do after the incident to prevent recurrence
- Post-incident review template

### Generate Runbooks For:
1. **Service Down**: Application returns 5xx errors
2. **Database Connection Pool Exhausted**: DB connections maxed out
3. **High Memory Usage**: Service approaching OOM kill
4. **Deployment Rollback**: New release causing issues
5. **Data Inconsistency**: Mismatch between systems detected

System information:
"""
[PASTE: tech stack, infrastructure, monitoring tools, deployment process]
"""
```

**Example Output Snippet:**

```markdown
## Runbook: Database Connection Pool Exhausted

**Severity**: P2
**Time to Resolve**: 15-30 minutes
**Escalation**: @db-team in #incidents if not resolved in 15 min

### Symptoms
- Alert: `PostgresConnectionPoolExhausted` in PagerDuty
- Users see: Slow page loads, then 503 errors
- Dashboard: Grafana "DB Connections" panel shows 100% utilization

### Diagnosis

```bash
# 1. Check current connection count
psql -h db-primary -U readonly -c \
  "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"
# Expected: Should be < 100. If 100+, pool is exhausted.

# 2. Find long-running queries hogging connections
psql -h db-primary -U readonly -c \
  "SELECT pid, now() - pg_stat_activity.query_start AS duration, query
   FROM pg_stat_activity
   WHERE state = 'active' AND now() - query_start > interval '30 seconds'
   ORDER BY duration DESC LIMIT 10;"

# 3. Check if it's a specific service causing the issue
psql -h db-primary -U readonly -c \
  "SELECT application_name, count(*)
   FROM pg_stat_activity
   GROUP BY application_name ORDER BY count DESC;"
```

### Resolution

**If long-running queries are the cause:**
```bash
# Kill the offending queries (get PIDs from diagnosis step 2)
psql -h db-primary -U admin -c "SELECT pg_terminate_backend(PID);"
```

**If a specific service is leaking connections:**
```bash
# Restart the leaking service
kubectl rollout restart deployment/ORDER_SERVICE -n production
```

**Verify fix:**
```bash
# Connections should drop within 30 seconds
watch -n 5 'psql -h db-primary -U readonly -c \
  "SELECT count(*) FROM pg_stat_activity;"'
```
```

**Tips for Customization:**
- Include your actual monitoring tool commands (Datadog, Grafana, CloudWatch)
- Add: "Include Slack message templates for status updates"
- Specify: "We use Kubernetes on AWS EKS"
