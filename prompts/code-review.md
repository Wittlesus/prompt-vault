# Code Review Prompts

A collection of 10 battle-tested prompts for automated code review. Paste these into Claude or ChatGPT along with your code to get instant, thorough reviews.

---

## 1. Bug Detection Sweep

**Use Case:** Scan code for logical errors, off-by-one mistakes, null reference risks, race conditions, and other common bugs before they reach production.

**Prompt:**

```
You are an expert software engineer performing a meticulous code review focused exclusively on bug detection.

Analyze the following code and identify ALL potential bugs, including but not limited to:
- Logical errors and off-by-one mistakes
- Null/undefined reference risks
- Race conditions and concurrency issues
- Unhandled edge cases (empty inputs, boundary values, overflow)
- Incorrect type assumptions or coercions
- Resource leaks (unclosed connections, file handles, streams)
- Incorrect error handling that swallows or misroutes exceptions

For each bug found, provide:
1. **Location**: File name and line number (or code snippet)
2. **Severity**: Critical / High / Medium / Low
3. **Description**: What the bug is and under what conditions it triggers
4. **Fix**: A concrete code fix

If no bugs are found, say so explicitly rather than inventing issues.

Code to review:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
### Bug #1
- **Location**: `userService.js`, line 42
- **Severity**: Critical
- **Description**: `user.profile.email` is accessed without checking if `user.profile`
  exists. When a user has no profile (new OAuth signups), this throws a TypeError
  crashing the request handler.
- **Fix**:
  ```js
  const email = user.profile?.email ?? user.email;
  ```

### Bug #2
- **Location**: `orderProcessor.js`, line 118
- **Severity**: High
- **Description**: The for-loop uses `i <= items.length` instead of `i < items.length`,
  causing an off-by-one error that reads `undefined` on the last iteration.
- **Fix**: Change `i <= items.length` to `i < items.length`.
```

**Tips for Customization:**
- Add your project's common pitfalls (e.g., "We use Prisma, so watch for missing `await` on queries")
- Specify the language/framework for more targeted analysis
- Append "Focus especially on [async/await patterns | state mutations | API boundary validation]" to narrow scope

---

## 2. Security Vulnerability Audit

**Use Case:** Identify security flaws such as injection attacks, authentication bypasses, data exposure, and insecure configurations.

**Prompt:**

```
You are a senior application security engineer conducting a security audit of the following code.

Analyze it for ALL security vulnerabilities, referencing the OWASP Top 10 where applicable:
- SQL injection, NoSQL injection, command injection, XSS
- Broken authentication or authorization logic
- Sensitive data exposure (hardcoded secrets, PII in logs, unencrypted storage)
- Insecure deserialization
- Missing input validation or sanitization
- CSRF vulnerabilities
- Insecure direct object references (IDOR)
- Security misconfigurations
- Missing rate limiting on sensitive endpoints
- Improper cryptographic usage

For each vulnerability:
1. **Vulnerability**: Name and CWE ID if applicable
2. **Location**: Where in the code
3. **Risk Level**: Critical / High / Medium / Low
4. **Attack Scenario**: How an attacker could exploit this
5. **Remediation**: Specific code changes to fix it

Code to audit:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
### Vulnerability #1: SQL Injection (CWE-89)
- **Location**: `db/queries.js`, line 23
- **Risk Level**: Critical
- **Attack Scenario**: The `searchTerm` parameter is concatenated directly into the SQL
  query string. An attacker can submit `'; DROP TABLE users; --` as the search term
  to destroy the users table.
- **Remediation**:
  ```js
  // Before (vulnerable)
  const query = `SELECT * FROM products WHERE name = '${searchTerm}'`;

  // After (parameterized)
  const query = `SELECT * FROM products WHERE name = $1`;
  const result = await pool.query(query, [searchTerm]);
  ```
```

**Tips for Customization:**
- Specify your tech stack (e.g., "This is a Node.js Express app with PostgreSQL")
- Mention compliance requirements: "We must comply with SOC 2 / HIPAA / PCI-DSS"
- Add: "Also check for secrets that should be in environment variables"

---

## 3. Performance Optimization Review

**Use Case:** Find performance bottlenecks, memory-inefficient patterns, unnecessary computations, and opportunities for optimization.

**Prompt:**

```
You are a performance engineering specialist reviewing code for optimization opportunities.

Analyze the following code for performance issues including:
- Unnecessary re-renders or re-computations
- N+1 query problems and unoptimized database access patterns
- Memory leaks and excessive memory allocation
- Missing caching opportunities
- Blocking operations that should be async
- Inefficient data structures or algorithm choices
- Redundant API calls or network requests
- Large bundle size contributors (frontend)
- Missing pagination or unbounded data fetching

For each issue found:
1. **Issue**: Brief description
2. **Impact**: Estimated performance impact (e.g., "Adds ~200ms per request at 1000 records")
3. **Current Code**: The problematic code snippet
4. **Optimized Code**: The improved version
5. **Explanation**: Why the optimization works

Also provide an overall performance score from 1-10 and a prioritized list of improvements.

Code to review:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
**Overall Performance Score: 5/10**

### Issue #1: N+1 Query in User Listing
- **Impact**: At 500 users, this generates 501 database queries instead of 2.
  Adds ~3 seconds to page load.
- **Current Code**:
  ```js
  const users = await User.findAll();
  for (const user of users) {
    user.orders = await Order.findAll({ where: { userId: user.id } });
  }
  ```
- **Optimized Code**:
  ```js
  const users = await User.findAll({
    include: [{ model: Order }]
  });
  ```
- **Explanation**: Eager loading fetches all users and their orders in 2 queries
  using a JOIN, eliminating the N+1 problem.
```

**Tips for Customization:**
- Specify expected scale: "This endpoint handles ~10,000 requests/minute"
- Mention your infrastructure: "Running on AWS Lambda with 256MB memory"
- Add frontend context: "This is a React component that re-renders on every keystroke"

---

## 4. Refactoring Suggestions

**Use Case:** Identify code that could be restructured for better readability, maintainability, and adherence to design principles.

**Prompt:**

```
You are a senior software architect reviewing code for refactoring opportunities. Your goal is to improve code quality without changing behavior.

Analyze the following code and suggest refactoring improvements based on:
- SOLID principles violations
- DRY (Don't Repeat Yourself) violations
- Overly complex functions (high cyclomatic complexity)
- Poor separation of concerns
- Missing abstraction opportunities
- God classes or functions doing too much
- Deep nesting that could be flattened
- Magic numbers and hardcoded values
- Poor naming that obscures intent
- Opportunities to use well-known design patterns

For each suggestion:
1. **What to Refactor**: Describe the current problem
2. **Why**: Which principle or practice it violates
3. **Before**: The current code
4. **After**: The refactored code
5. **Benefits**: Concrete improvements (testability, readability, etc.)

Prioritize suggestions by impact. Only suggest refactoring that provides clear value - avoid over-engineering.

Code to review:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
### Refactoring #1: Extract Validation Logic
- **What to Refactor**: The `createOrder` function (87 lines) mixes validation,
  business logic, and persistence.
- **Why**: Violates Single Responsibility Principle. Impossible to unit test
  validation without hitting the database.
- **Before**:
  ```js
  async function createOrder(data) {
    if (!data.items || data.items.length === 0) throw new Error('...');
    if (data.total < 0) throw new Error('...');
    // ... 20 more validation lines ...
    // ... business logic ...
    // ... database save ...
  }
  ```
- **After**:
  ```js
  function validateOrder(data) { /* pure validation */ }
  function calculateOrderTotals(items) { /* pure business logic */ }
  async function persistOrder(order) { /* database only */ }
  async function createOrder(data) {
    validateOrder(data);
    const order = calculateOrderTotals(data.items);
    return persistOrder(order);
  }
  ```
- **Benefits**: Each function is independently testable. Validation can be
  reused for order updates. Business logic has no side effects.
```

**Tips for Customization:**
- Specify your team's coding standards or style guide
- Mention: "We prefer functional programming patterns" or "We use OOP with dependency injection"
- Add: "Prioritize refactoring that improves testability"

---

## 5. Naming Convention Review

**Use Case:** Audit variable, function, class, and file names for clarity, consistency, and adherence to language conventions.

**Prompt:**

```
You are a code readability expert reviewing naming conventions. Good names are the best documentation.

Review all names in the following code:
- Variables, constants, and parameters
- Functions and methods
- Classes, interfaces, and types
- Files and modules
- Database tables and columns (if applicable)

Check for:
1. **Clarity**: Does the name communicate what it holds or does?
2. **Consistency**: Do similar concepts use similar naming patterns?
3. **Convention**: Does it follow language-specific conventions (camelCase, snake_case, PascalCase)?
4. **Length**: Is it appropriately sized (not too terse, not too verbose)?
5. **Accuracy**: Does the name match what the code actually does?
6. **Boolean naming**: Do booleans use is/has/should/can prefixes?
7. **Function naming**: Do functions start with verbs (get, set, create, validate, etc.)?
8. **Abbreviations**: Are abbreviations standard and understood?

For each naming issue:
| Current Name | Suggested Name | Reason |
|---|---|---|

Also note any names that are exemplary and worth keeping.

Code to review:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
### Naming Issues Found

| Current Name | Suggested Name | Reason |
|---|---|---|
| `d` | `deliveryDate` | Single-letter names obscure intent |
| `processData()` | `validateAndSaveUserProfile()` | Too vague - what data? what processing? |
| `flag` | `isEligibleForDiscount` | "flag" says nothing about what it represents |
| `temp` | `unsortedItems` | Describes actual content rather than being a throwaway name |
| `handleClick()` | `submitPaymentForm()` | Name should describe the action, not the trigger |
| `data2` | `normalizedResponse` | Numbered suffixes indicate missing semantic meaning |

### Exemplary Names (Keep These)
- `calculateShippingCost()` - Clear verb + noun, self-documenting
- `isAuthenticated` - Proper boolean prefix
- `MAX_RETRY_ATTEMPTS` - Standard constant naming
```

**Tips for Customization:**
- Specify your language: "Use Python PEP 8 conventions" or "Follow Go naming idioms"
- Reference your team's glossary: "We call them 'tenants' not 'organizations'"
- Add: "We use a domain-driven design ubiquitous language: [list key domain terms]"

---

## 6. Error Handling Audit

**Use Case:** Review code for proper error handling, ensuring errors are caught, logged, and communicated correctly without leaking sensitive info.

**Prompt:**

```
You are a reliability engineer reviewing error handling patterns in production code.

Audit the following code for error handling completeness and correctness:

1. **Missing Error Handling**: Operations that can fail but have no try/catch or error callback
2. **Swallowed Errors**: Catch blocks that silently ignore errors
3. **Incorrect Error Types**: Using generic Error instead of specific error classes
4. **Missing Finally/Cleanup**: Resources that aren't cleaned up when errors occur
5. **Error Message Quality**: Are messages actionable? Do they include context?
6. **Error Propagation**: Are errors properly propagated up the call stack?
7. **User-Facing Errors**: Do error responses leak internal details (stack traces, DB schema, file paths)?
8. **Logging**: Are errors logged with sufficient context for debugging?
9. **Retry Logic**: Are transient failures (network, DB) retried appropriately?
10. **Graceful Degradation**: Does the system degrade gracefully or crash entirely?

For each issue:
1. **Problem**: What's wrong
2. **Risk**: What happens in production if this isn't fixed
3. **Fix**: Concrete code solution

Provide a summary error handling score (1-10) and the top 3 priorities.

Code to audit:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
**Error Handling Score: 4/10**

### Issue #1: Swallowed Database Error
- **Problem**: Line 34 catches the database connection error but only logs to
  console. The function returns `undefined` instead of propagating the failure.
- **Risk**: Silent data loss. Users think their data was saved, but it wasn't.
  No alerts fire because the request returns 200 OK.
- **Fix**:
  ```js
  // Before
  try {
    await db.save(record);
  } catch (e) {
    console.log(e);
  }

  // After
  try {
    await db.save(record);
  } catch (error) {
    logger.error('Failed to save user record', {
      userId: record.userId,
      error: error.message,
      stack: error.stack
    });
    throw new DatabaseError('Failed to save record', { cause: error });
  }
  ```
```

**Tips for Customization:**
- Specify your error tracking tool: "We use Sentry for error monitoring"
- Mention your error response format: "We return RFC 7807 Problem Details JSON"
- Add: "Check that all HTTP 5xx responses trigger PagerDuty alerts"

---

## 7. API Design Review

**Use Case:** Review REST/GraphQL API endpoints for consistency, correctness, and adherence to best practices.

**Prompt:**

```
You are an API design expert reviewing endpoint implementations for correctness and best practices.

Review the following API code for:

1. **HTTP Method Correctness**: GET for reads, POST for creation, PUT/PATCH for updates, DELETE for removal
2. **Status Code Accuracy**: 200, 201, 204, 400, 401, 403, 404, 409, 422, 500 used correctly
3. **Request Validation**: All inputs validated before processing
4. **Response Format Consistency**: Consistent JSON shape across all endpoints
5. **Pagination**: List endpoints paginated with proper metadata
6. **Filtering/Sorting**: Query parameter patterns are consistent
7. **Error Responses**: Structured error bodies with codes, messages, and details
8. **Idempotency**: PUT/DELETE operations are idempotent, POST uses idempotency keys where needed
9. **Versioning**: API versioning strategy is clear
10. **HATEOAS/Links**: Related resources are discoverable (if applicable)

For each issue:
1. **Endpoint**: `METHOD /path`
2. **Issue**: What's wrong
3. **Best Practice**: What it should be
4. **Fix**: Code or spec change

Also flag any inconsistencies between endpoints.

Code to review:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
### Issue #1: Incorrect Status Code on Creation
- **Endpoint**: `POST /api/users`
- **Issue**: Returns `200 OK` when creating a new user.
- **Best Practice**: Return `201 Created` with a `Location` header pointing
  to the new resource.
- **Fix**:
  ```js
  // Before
  res.json(newUser);

  // After
  res.status(201)
     .header('Location', `/api/users/${newUser.id}`)
     .json(newUser);
  ```

### Issue #2: Missing Pagination on List Endpoint
- **Endpoint**: `GET /api/orders`
- **Issue**: Returns all orders with no pagination. At 50K orders, this will
  timeout and consume excessive memory.
- **Best Practice**: Default pagination with limit/offset or cursor-based pagination.
- **Fix**: Add `?page=1&per_page=25` with response envelope:
  ```json
  {
    "data": [...],
    "meta": { "page": 1, "per_page": 25, "total": 50000, "total_pages": 2000 }
  }
  ```
```

**Tips for Customization:**
- Specify your API style: "We follow JSON:API spec" or "We use GraphQL"
- Mention auth: "All endpoints require Bearer token except /auth/*"
- Add: "We need OpenAPI 3.0 compliance"

---

## 8. Code Style & Consistency Check

**Use Case:** Ensure code follows consistent formatting, structure, and idioms across the codebase.

**Prompt:**

```
You are a code quality gatekeeper reviewing a pull request for style and consistency.

Check the following code against these criteria:

1. **Formatting**: Consistent indentation, bracket placement, line length
2. **Import Organization**: Grouped and ordered logically (stdlib, external, internal)
3. **Function Organization**: Public before private, logical grouping
4. **Comment Quality**: Comments explain "why" not "what", no stale comments
5. **Dead Code**: Unreachable code, unused imports, commented-out blocks
6. **Consistent Patterns**: Similar operations done the same way throughout
7. **Language Idioms**: Uses idiomatic patterns for the language
8. **Type Usage**: Consistent use of type annotations (if applicable)
9. **Magic Values**: Hardcoded strings/numbers that should be constants
10. **File Length**: Files that are too long and should be split

Format your review as a PR comment with inline suggestions:

For each issue:
- **File:Line**: Location
- **Category**: Which criteria above
- **Suggestion**: Specific change with code example

End with a summary: "Approve", "Request Changes", or "Approve with Nits".

Code to review:
"""
[PASTE YOUR CODE HERE]
"""
```

**Example Output Snippet:**

```
**Decision: Request Changes** (3 blocking issues, 5 nits)

### Blocking

**src/utils.js:12** - Dead Code
```js
// Remove commented-out experimental feature (3 months old per git blame)
// function experimentalSort(arr) { ... }  // 40 lines of dead code
```

**src/api/handler.js:5** - Inconsistent Pattern
```js
// Lines 5-20 use callbacks, but lines 25-80 use async/await.
// Standardize on async/await throughout:
// Before
db.query(sql, (err, result) => { ... });
// After
const result = await db.query(sql);
```

### Nits (Non-Blocking)

**src/models/user.js:1** - Import Organization
```js
// Before: mixed order
import { validateEmail } from '../utils';
import express from 'express';
import { User } from './schema';

// After: external, then internal
import express from 'express';
import { User } from './schema';
import { validateEmail } from '../utils';
```
```

**Tips for Customization:**
- Reference your linter config: "We use ESLint with Airbnb config"
- Specify: "We use Prettier with 100-char line width and single quotes"
- Add team conventions: "We put React hooks at the top of components"

---

## 9. Dependency & Import Review

**Use Case:** Audit dependencies for security risks, unnecessary bloat, circular imports, and version issues.

**Prompt:**

```
You are a supply chain security and dependency management expert.

Review the following code and its dependencies for:

1. **Unused Dependencies**: Imports that are declared but never used
2. **Circular Dependencies**: Module A imports B which imports A
3. **Heavy Dependencies**: Large packages used for simple tasks that could be replaced with native code or lighter alternatives
4. **Deprecated Packages**: Dependencies that are no longer maintained
5. **Version Conflicts**: Multiple versions of the same package
6. **Security Advisories**: Known vulnerabilities in the dependency versions
7. **License Compatibility**: Licenses that conflict with your project's license
8. **Missing Peer Dependencies**: Required peer deps not installed
9. **Barrel File Performance**: Index files that re-export everything causing tree-shaking issues
10. **Dynamic Imports**: Opportunities to lazy-load heavy dependencies

Provide:
1. A dependency health scorecard
2. Specific removal/replacement recommendations
3. A prioritized action list

Files to review:
"""
[PASTE package.json, import statements, and/or requirements.txt HERE]
"""
```

**Example Output Snippet:**

```
### Dependency Health Scorecard

| Dependency | Version | Status | Action |
|---|---|---|---|
| `moment` | 2.29.4 | Deprecated | Replace with `dayjs` (2KB vs 67KB) |
| `lodash` | 4.17.21 | Heavy | Replace `_.get` with optional chaining |
| `left-pad` | 1.3.0 | Unnecessary | Use `String.prototype.padStart()` |
| `express` | 4.18.2 | Healthy | Keep, but plan v5 migration |
| `event-stream` | 3.3.4 | COMPROMISED | Remove immediately (npm advisory) |

### Priority Actions
1. **URGENT**: Remove `event-stream` - known supply chain attack vector
2. **HIGH**: Replace `moment` with `dayjs` - saves 65KB from bundle
3. **MEDIUM**: Tree-shake lodash - import `lodash/get` instead of `lodash`
```

**Tips for Customization:**
- Include your package.json or requirements.txt
- Specify: "We need all dependencies to be MIT or Apache-2.0 licensed"
- Add: "Our bundle budget is 200KB gzipped"

---

## 10. Pre-Merge Comprehensive Review

**Use Case:** Final gate review before merging a PR. Covers correctness, style, tests, docs, and deployment readiness.

**Prompt:**

```
You are a senior tech lead performing a final pre-merge review. This is the last check before code goes to production.

Review this pull request holistically across all dimensions:

## Correctness
- Does the code do what the PR description says?
- Are there logical errors or unhandled scenarios?
- Will it break existing functionality?

## Testing
- Are there sufficient tests? What's missing?
- Do tests cover edge cases and error paths?
- Are tests deterministic (no flakiness)?

## Security
- Any new attack surfaces introduced?
- Inputs validated? Outputs sanitized?
- Authentication/authorization correct?

## Performance
- Any new N+1 queries, unbounded loops, or memory issues?
- Will this scale to 10x current load?

## Maintainability
- Is the code self-documenting?
- Are there sufficient comments for complex logic?
- Future developers can understand this in 6 months?

## Deployment
- Database migrations backward-compatible?
- Feature flags needed?
- Rollback plan clear?
- Monitoring/alerts in place for new functionality?

## Documentation
- README updated if needed?
- API docs updated?
- Changelog entry added?

Provide your verdict:
- **APPROVE**: Ready to merge
- **REQUEST CHANGES**: Must fix [list] before merge
- **NEEDS DISCUSSION**: Architectural concerns to discuss with team

PR Description: [PASTE PR DESCRIPTION]

Code changes:
"""
[PASTE YOUR CODE DIFF OR CHANGED FILES HERE]
"""
```

**Example Output Snippet:**

```
## Verdict: REQUEST CHANGES

### Must Fix Before Merge

1. **Missing Migration Rollback**: The `ALTER TABLE ADD COLUMN` migration at
   `db/migrations/20240115.sql` has no `DOWN` migration. If we need to rollback,
   we'll have a schema mismatch.

2. **No Test for Empty Cart**: The new `checkout()` function has no test for
   when the cart is empty. This will throw an unhandled division-by-zero when
   calculating average item price.

3. **Leaked PII in Logs**: Line 45 logs the full `user` object which includes
   `ssn` and `dateOfBirth`. Use the `sanitizeForLogging(user)` util instead.

### Suggestions (Non-Blocking)
- Consider adding a feature flag for the new payment flow so we can disable
  it without a rollback
- The new `calculateTax` function would benefit from a JSDoc comment
  explaining the tax jurisdiction logic

### What Looks Good
- Clean separation of the payment gateway adapter (easy to swap providers)
- Comprehensive happy-path tests
- Proper use of database transactions for the multi-table write
```

**Tips for Customization:**
- Paste the actual PR description for context
- Specify deployment process: "We deploy via Kubernetes with blue-green strategy"
- Add: "We have a 99.9% SLA so pay extra attention to failure modes"
- Include: "Check backward compatibility - we have mobile clients on version N-2"
