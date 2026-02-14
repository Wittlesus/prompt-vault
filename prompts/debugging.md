# Debugging Prompts

A collection of 10 battle-tested prompts for AI-assisted debugging. From cryptic error messages to elusive memory leaks, these prompts help you diagnose and fix issues faster.

---

## 1. Error Message Decoder

**Use Case:** When you encounter a cryptic error message or exception, get a plain-English explanation and actionable fix.

**Prompt:**

```
You are a senior developer who excels at debugging. I'm encountering the following error and need your help understanding and fixing it.

## Error Information
- **Error message**: [PASTE FULL ERROR MESSAGE]
- **When it occurs**: [What action triggers it]
- **Frequency**: [Always / intermittent / only in production]
- **Recent changes**: [What changed recently before this started]

## Context
- **Language/Framework**: [e.g., Node.js 20 with Express 4]
- **Environment**: [development / staging / production]
- **OS**: [e.g., Ubuntu 22.04 in Docker]

## What I Need
1. **Plain English explanation**: What this error actually means (not just restating the message)
2. **Root cause analysis**: The most likely cause given the context
3. **Step-by-step fix**: Exact code or config changes to resolve it
4. **Verification**: How to confirm the fix works
5. **Prevention**: How to prevent this error from recurring

If there are multiple possible causes, rank them by likelihood and provide diagnostic steps to determine which one applies.

Relevant code:
"""
[PASTE THE CODE AROUND THE ERROR LOCATION]
"""
```

**Example Output Snippet:**

```markdown
## Error: `ECONNREFUSED 127.0.0.1:5432`

### Plain English
Your application is trying to connect to a PostgreSQL database on localhost
port 5432, but nothing is listening there. The database server is either
not running, not listening on that port, or your app is looking at the
wrong host.

### Most Likely Cause (Given Docker Context)
You're running the app inside a Docker container. Inside the container,
`localhost` refers to the container itself, NOT your host machine. The
database is running on the host but the app is looking inside the container.

### Fix
```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_HOST=db  # Use the service name, not localhost
    depends_on:
      - db
  db:
    image: postgres:16
    ports:
      - "5432:5432"
```

### Verification
```bash
# From inside the container, verify connectivity:
docker exec -it app_container nc -z db 5432
# Should output: Connection to db 5432 port [tcp/postgresql] succeeded!
```
```

**Tips for Customization:**
- Include the full stack trace, not just the error message
- Mention if the error happens only under load or specific conditions
- Add: "This worked yesterday. The only change was [describe change]"

---

## 2. Stack Trace Interpreter

**Use Case:** Analyze a full stack trace to identify the actual root cause, distinguishing framework noise from your application's error.

**Prompt:**

```
You are a debugging expert analyzing a stack trace. Your job is to cut through the noise and find the real problem.

## Stack Trace
"""
[PASTE THE COMPLETE STACK TRACE HERE]
"""

## Analysis Required:

### 1. Root Cause Identification
- Which line in MY code (not framework/library code) is the actual source of the error?
- Highlight the critical frames and explain why they matter
- Cross out the framework frames and explain what they're doing (so I can ignore them in the future)

### 2. Call Chain Explanation
Trace the execution path in plain English:
```
1. Your code called X in file.js:42
2. Which triggered Y in library.js:100 (framework internals - ignore)
3. Which attempted Z, but failed because...
```

### 3. Variable State Inference
Based on the stack trace and error type, what were the likely values of key variables at the point of failure?

### 4. Fix
- What code change fixes this?
- Are there other places in the codebase that might have the same issue? (pattern to search for)

### 5. Debugging Commands
If I need more information, what debugging commands or breakpoints should I set?
```

**Example Output Snippet:**

```markdown
## Stack Trace Analysis

### Frames That Matter (YOUR code)
```
→ at processPayment (src/services/payment.js:67)     ← ROOT CAUSE
  at handleCheckout (src/controllers/checkout.js:23)   ← Entry point
```

### Frames to Ignore (Framework)
```
  at Layer.handle [as handle_request] (express/lib/router/layer.js:95)
  at next (express/lib/router/route.js:144)
  ... (Express routing internals - just routing the request to your handler)
```

### What Happened (Plain English)
1. A POST request hit your `/checkout` endpoint
2. `handleCheckout()` called `processPayment()` with the order data
3. At line 67 of payment.js, `order.paymentMethod.token` was accessed
4. But `order.paymentMethod` is `undefined` - this is a **TypeError**
5. This means the order object arrived without a payment method attached

### Likely Variable State
```javascript
// At payment.js:67, the order object probably looks like:
{
  id: "ord_123",
  items: [...],
  paymentMethod: undefined  // <-- THIS IS THE PROBLEM
  // Expected: { type: "card", token: "tok_..." }
}
```

### Fix
```javascript
// payment.js:67 - Add validation before accessing nested properties
if (!order.paymentMethod?.token) {
  throw new ValidationError('Payment method with token is required');
}
```

### Search for Similar Issues
```bash
# Find other places that access paymentMethod without null checks
grep -rn "paymentMethod\." src/ --include="*.js" | grep -v "paymentMethod?"
```
```

**Tips for Customization:**
- Include the full stack trace (don't truncate)
- Add: "This is a production error affecting 5% of requests"
- Specify: "I'm using TypeScript but the stack trace shows compiled JS"

---

## 3. Performance Profiling Assistant

**Use Case:** Analyze performance data (slow queries, flame graphs, metrics) to identify bottlenecks and optimize.

**Prompt:**

```
You are a performance engineer analyzing application performance data to identify and fix bottlenecks.

## Performance Data
"""
[PASTE: slow query logs, profiler output, flame graph text, response time metrics, or APM screenshots described in text]
"""

## Context
- **What's slow**: [Specific endpoint, page, or operation]
- **How slow**: [Current: Xms, Target: Yms]
- **When it's slow**: [Always / under load / specific conditions]
- **Scale**: [Requests per second, data volume, concurrent users]

## Analysis Required:

### 1. Bottleneck Identification
Rank all bottlenecks by impact:
| Rank | Bottleneck | Time Consumed | % of Total | Fix Difficulty |
|------|-----------|---------------|------------|----------------|

### 2. Root Cause for Top Bottleneck
- What exactly is slow and why?
- Is it CPU-bound, I/O-bound, memory-bound, or network-bound?
- Is it a code issue, data issue, or infrastructure issue?

### 3. Optimization Plan (ordered by impact)
For each optimization:
- **Change**: What to do
- **Expected Improvement**: How much faster
- **Effort**: Hours to implement
- **Risk**: What could go wrong
- **Code**: Actual implementation

### 4. Quick Wins
Things that can be fixed in under 30 minutes for immediate improvement.

### 5. Monitoring
What metrics to add to detect this problem proactively in the future.
```

**Example Output Snippet:**

```markdown
## Bottleneck Analysis: GET /api/dashboard (2,400ms avg)

### Bottleneck Ranking
| Rank | Bottleneck | Time | % | Fix Difficulty |
|------|-----------|------|---|----------------|
| 1 | N+1 query in user stats | 1,800ms | 75% | Easy |
| 2 | Unindexed WHERE clause | 400ms | 17% | Easy |
| 3 | JSON serialization of large response | 150ms | 6% | Medium |
| 4 | Template rendering | 50ms | 2% | Low priority |

### Top Bottleneck: N+1 Query

**Root Cause**: The dashboard loads 50 team members, then for EACH member
runs a separate query to get their stats. That's 51 queries instead of 2.

**Current Code (51 queries):**
```sql
SELECT * FROM team_members WHERE team_id = 42;
-- Then for EACH of the 50 members:
SELECT count(*) FROM tasks WHERE assigned_to = ?;
SELECT sum(hours) FROM time_entries WHERE user_id = ?;
```

**Optimized Code (2 queries):**
```sql
SELECT * FROM team_members WHERE team_id = 42;

SELECT
  assigned_to,
  count(*) as task_count,
  COALESCE(sum(te.hours), 0) as total_hours
FROM tasks t
LEFT JOIN time_entries te ON te.task_id = t.id
WHERE t.assigned_to IN (SELECT id FROM team_members WHERE team_id = 42)
GROUP BY assigned_to;
```

**Expected Improvement**: 2,400ms → 600ms (75% reduction)

### Quick Win: Add Missing Index
```sql
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
-- Expected improvement: 400ms → 20ms for the WHERE clause
```
```

**Tips for Customization:**
- Include `EXPLAIN ANALYZE` output for slow queries
- Add: "We're running on a t3.medium EC2 instance"
- Specify your APM tool: "Here's the Datadog trace for this request"

---

## 4. Memory Leak Detective

**Use Case:** Diagnose memory leaks using heap snapshots, memory growth patterns, or symptoms described in production.

**Prompt:**

```
You are a memory leak specialist. Help me find and fix a memory leak in my application.

## Symptoms
- **Memory growth pattern**: [Linear growth, sudden spikes, sawtooth but trending up]
- **Memory at start**: [e.g., 150MB]
- **Memory after X hours**: [e.g., 2GB after 4 hours]
- **OOM kills**: [Yes/No, how often]
- **GC behavior**: [Frequent full GCs, long GC pauses]

## Environment
- **Language/Runtime**: [Node.js 20 / Python 3.12 / Java 21 / Go 1.22]
- **Framework**: [Express / Django / Spring / etc.]
- **Infrastructure**: [Container memory limit, instances, autoscaling]

## Data (provide any available)
- Heap snapshot diff
- Memory profiler output
- Process metrics over time
- Code that runs in the hot path

## Analysis Required:

### 1. Leak Pattern Identification
Based on the symptoms, what type of memory leak is this most likely?
- Event listener accumulation
- Closure capturing large objects
- Cache without eviction/TTL
- Global state growing unboundedly
- Circular references preventing GC
- Stream/connection not properly closed
- Timer/interval not cleared

### 2. Diagnostic Steps
Exact commands and code to pinpoint the leak:
```javascript
// Heap snapshot comparison technique
// Memory profiling code to add temporarily
// Monitoring code to track object counts
```

### 3. Fix
- Exact code change to fix the leak
- Verification: How to confirm the leak is fixed

### 4. Prevention
- Patterns to follow to prevent future leaks
- Monitoring to add

Relevant code:
"""
[PASTE YOUR CODE, ESPECIALLY: event handlers, caching code, global variables, streaming code, WebSocket handlers]
"""
```

**Example Output Snippet:**

```markdown
## Diagnosis: Event Listener Accumulation

### Pattern Match
Your symptoms (linear growth, ~50MB/hour) are classic for event listener
accumulation. Each WebSocket connection adds listeners that aren't removed
on disconnect.

### The Leak
```javascript
// server.js - Current code
wss.on('connection', (ws) => {
  // This listener is added every connection but NEVER removed
  database.on('change', (change) => {    // ← LEAK
    ws.send(JSON.stringify(change));
  });
});
```

Every new WebSocket connection adds a new `database.on('change')` listener.
When the client disconnects, the WebSocket is garbage collected, but the
database listener keeps a reference to the closure (which holds `ws`).
After 1,000 connections: 1,000 orphaned listeners, each holding a dead
WebSocket object in memory.

### Fix
```javascript
wss.on('connection', (ws) => {
  // Create a named handler so we can remove it
  const changeHandler = (change) => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(change));
    }
  };

  database.on('change', changeHandler);

  // CRITICAL: Clean up on disconnect
  ws.on('close', () => {
    database.removeListener('change', changeHandler);
  });
});
```

### Verification
```javascript
// Add temporary monitoring
setInterval(() => {
  console.log('DB change listeners:', database.listenerCount('change'));
  console.log('Active WS connections:', wss.clients.size);
  console.log('Heap used:', Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + 'MB');
  // Listener count should closely match connection count
}, 60000);
```

### Prevention Checklist
- [ ] Every `.on()` must have a corresponding `.off()` / `.removeListener()`
- [ ] Add `maxListeners` warnings: `database.setMaxListeners(100)`
- [ ] Monitor `process.memoryUsage()` and alert on growth trends
```

**Tips for Customization:**
- Include heap snapshot data if available
- Add: "This only happens in production, not locally"
- Specify: "We use Redis pub/sub for real-time events"

---

## 5. Race Condition Analyzer

**Use Case:** Identify and fix race conditions, deadlocks, and concurrency issues in async or multi-threaded code.

**Prompt:**

```
You are a concurrency expert specializing in race conditions and distributed systems bugs.

Analyze the following code for concurrency issues:

## What to Look For:
1. **Race Conditions**: Two operations that assume sequential execution but can interleave
2. **TOCTOU Bugs**: Time-of-check to time-of-use gaps (check then act, but state changes between)
3. **Lost Updates**: Two concurrent writes where one overwrites the other
4. **Deadlocks**: Circular lock dependencies
5. **Starvation**: One path always wins, another never executes
6. **Double Processing**: Same work done twice due to lack of idempotency
7. **Phantom Reads**: Data changes between two reads in the same operation
8. **Non-Atomic Operations**: Multi-step operations that should be atomic but aren't

## For Each Issue Found:

### 1. The Race Condition
- Describe the exact interleaving of operations that causes the bug
- Use a timeline diagram:
```
Thread A:  read(balance=100) ──────────────── write(balance=50)
Thread B:  ────────── read(balance=100) ── write(balance=70)
Result: balance=70 (Thread A's deduction lost!)
```

### 2. Reproduction Steps
- Conditions needed to trigger this (load, timing, specific order)
- How likely is this in production?

### 3. Fix
- Concrete code change with the synchronization mechanism used
- Explain why this fix is correct

### 4. Testing
- How to write a test that reproduces this race condition

Code to analyze:
"""
[PASTE YOUR CONCURRENT/ASYNC CODE HERE]
"""
```

**Example Output Snippet:**

```markdown
## Race Condition #1: Lost Inventory Update

### The Bug
The `purchaseItem` function reads inventory, checks availability, then writes
the new count. Between the read and write, another request can read the
stale count.

### Timeline
```
Request A:  SELECT stock FROM items WHERE id=1;  (stock=1)
Request B:  ──────── SELECT stock FROM items WHERE id=1;  (stock=1)
Request A:  UPDATE items SET stock=0 WHERE id=1;  ✓ (sold last item)
Request B:  ──────── UPDATE items SET stock=0 WHERE id=1;  ✓ (OVERSOLD!)
Result: 2 orders placed, only 1 item in stock → oversold!
```

### Current Code (Vulnerable)
```javascript
async function purchaseItem(itemId) {
  const item = await db.query('SELECT stock FROM items WHERE id = $1', [itemId]);
  if (item.stock <= 0) throw new Error('Out of stock');  // TOCTOU gap here
  await db.query('UPDATE items SET stock = stock - 1 WHERE id = $1', [itemId]);
  return { success: true };
}
```

### Fix: Atomic Conditional Update
```javascript
async function purchaseItem(itemId) {
  // Single atomic operation: check AND update in one query
  const result = await db.query(
    'UPDATE items SET stock = stock - 1 WHERE id = $1 AND stock > 0 RETURNING *',
    [itemId]
  );
  if (result.rowCount === 0) {
    throw new Error('Out of stock');
  }
  return { success: true };
}
```

### Why This Fix Works
The `UPDATE ... WHERE stock > 0` is atomic at the database level.
PostgreSQL uses row-level locking, so only one transaction can update
the row at a time. If two requests race, one gets the row and the
other sees `rowCount === 0`.

### Test
```javascript
it('should not oversell under concurrent purchases', async () => {
  await db.query('INSERT INTO items (id, stock) VALUES (1, 1)');

  // Fire 10 concurrent purchase attempts
  const results = await Promise.allSettled(
    Array(10).fill(null).map(() => purchaseItem(1))
  );

  const successes = results.filter(r => r.status === 'fulfilled');
  const failures = results.filter(r => r.status === 'rejected');

  expect(successes).toHaveLength(1);   // Only 1 should succeed
  expect(failures).toHaveLength(9);    // Rest should fail

  const item = await db.query('SELECT stock FROM items WHERE id = 1');
  expect(item.rows[0].stock).toBe(0);  // Never negative
});
```
```

**Tips for Customization:**
- Specify: "We use PostgreSQL with SERIALIZABLE isolation level"
- Add: "This is a distributed system with multiple instances behind a load balancer"
- Mention: "We use Redis for distributed locking"

---

## 6. Log Analysis Expert

**Use Case:** Analyze application logs to reconstruct what happened, identify the root cause of an incident, and extract actionable insights.

**Prompt:**

```
You are an SRE expert analyzing production logs during an incident. Help me understand what happened and why.

## Logs
"""
[PASTE LOG ENTRIES HERE - include timestamps, log levels, messages]
"""

## Context
- **Incident**: [Brief description of the issue users reported]
- **Timeline**: [When did it start, when was it noticed, is it ongoing?]
- **Recent Changes**: [Deployments, config changes, infrastructure changes]

## Analysis Required:

### 1. Timeline Reconstruction
Create a chronological narrative of what happened:
```
10:15:00 - Normal operation, processing 200 req/s
10:15:42 - First warning: [description]
10:15:45 - Error rate spiked because [reason]
...
```

### 2. Root Cause
- What was the triggering event?
- What was the root cause vs. the symptoms?
- Why didn't existing monitoring catch it sooner?

### 3. Affected Scope
- What users/services were affected?
- What data might be inconsistent?

### 4. Correlation Patterns
- Are there patterns in the errors (specific user, endpoint, region, time)?
- What do the SUCCESSFUL requests during the incident have in common?

### 5. Log Improvements
- What additional logging would have made this easier to diagnose?
- What log queries should we save for future incidents?

### 6. Remediation
- Immediate fix
- What data needs to be cleaned up
- How to prevent recurrence
```

**Example Output Snippet:**

```markdown
## Timeline Reconstruction

```
14:30:00  [INFO]  Deploy v2.14.3 started (commit abc123)
14:30:45  [INFO]  Deploy v2.14.3 complete, 3/3 pods healthy
14:31:02  [WARN]  Redis connection pool exhausted (0/10 available)
14:31:02  [WARN]  Redis connection pool exhausted (0/10 available)
14:31:03  [ERROR] Session lookup failed: ECONNREFUSED redis:6379
14:31:03  [ERROR] 50 requests returned 503 in last 5 seconds
14:31:10  [WARN]  Health check failed on pod-2 (dependency: redis)
14:31:15  [INFO]  Kubernetes restarting pod-2 (health check failed)
14:31:20  [WARN]  pod-1 and pod-3 absorbing pod-2's traffic → overloaded
14:31:30  [ERROR] Cascading failure: all pods returning 503
```

## Root Cause

The deploy at 14:30 introduced a Redis connection leak. The new code opens
a Redis connection per request but doesn't return it to the pool (missing
`finally { client.release() }` in the new session middleware).

At ~200 req/s, the 10-connection pool was exhausted in 50ms. Once the pool
was empty, all session lookups failed, causing 503 errors. The health check
depends on Redis, so pods started failing health checks and restarting,
creating a cascading failure.

## The Specific Bug
```javascript
// v2.14.3 introduced this in session-middleware.js:
async function getSession(req) {
  const client = await redis.pool.acquire();  // Acquires connection
  const session = await client.get(`sess:${req.cookies.sid}`);
  return JSON.parse(session);
  // BUG: client.release() never called → connection leaked
}
```
```

**Tips for Customization:**
- Include all log levels (DEBUG/INFO/WARN/ERROR), not just errors
- Add: "Here are the corresponding metrics from Datadog/Grafana"
- Mention: "Include logs from multiple services if the issue spans services"

---

## 7. Debugging Strategy Planner

**Use Case:** When you have a vague bug report and don't know where to start, get a systematic plan to narrow down the cause.

**Prompt:**

```
You are a principal engineer known for debugging the toughest production issues. I have a bug that I can't figure out. Help me create a systematic debugging plan.

## The Bug
- **Symptoms**: [What users see / what's wrong]
- **Expected Behavior**: [What should happen]
- **Frequency**: [Always / intermittent / only specific conditions]
- **Environment**: [Dev / staging / production only]
- **Since When**: [Has it always been like this, or did it start at a specific time?]
- **Attempted Fixes**: [What I've already tried]

## Create a Debugging Plan:

### Phase 1: Reproduce
- Exact steps to reproduce the issue reliably
- If intermittent: how to increase reproduction rate
- Minimal reproduction case

### Phase 2: Isolate
- Binary search strategy to narrow the cause:
  - Is it frontend or backend?
  - Is it code, data, or infrastructure?
  - Is it this service or a dependency?
- Specific experiments to run (each eliminates a hypothesis)

### Phase 3: Identify
- What to inspect once the area is narrowed:
  - Specific log queries
  - Debugger breakpoints to set
  - Network requests to inspect
  - Database queries to run

### Phase 4: Verify
- How to confirm the root cause before fixing
- What evidence proves it's THIS cause and not something else

### Phase 5: Fix & Validate
- Fix approach
- How to verify the fix resolves the issue
- How to check for no regressions

For each phase, provide specific commands and code, not just general advice.
```

**Example Output Snippet:**

```markdown
## Debugging Plan: "Users intermittently see stale profile data after updating"

### Phase 1: Reproduce

**Increase reproduction rate:**
```bash
# Hit the update endpoint, then immediately read
for i in {1..100}; do
  curl -X PUT localhost:3000/api/profile -d '{"name":"Test'$i'"}' \
    -H "Authorization: Bearer $TOKEN"
  RESULT=$(curl -s localhost:3000/api/profile -H "Authorization: Bearer $TOKEN")
  EXPECTED="Test$i"
  if [[ "$RESULT" != *"$EXPECTED"* ]]; then
    echo "STALE READ on attempt $i: expected $EXPECTED, got $RESULT"
  fi
done
```

### Phase 2: Isolate

**Experiment 1: Is it the cache?**
```bash
# Bypass cache and read directly from DB
curl localhost:3000/api/profile?_nocache=1 -H "Authorization: Bearer $TOKEN"
```
- If fresh: it's a caching issue → go to "Cache Investigation"
- If stale: it's a database issue → go to "DB Investigation"

**Experiment 2: Which cache layer?**
```bash
# Check Redis directly
redis-cli GET "profile:user_123"
# Check CDN cache
curl -I https://cdn.example.com/api/profile  # Look at Age and Cache-Control headers
```

**Experiment 3: Is it read-replica lag?**
```bash
# Check replication lag
psql -h db-replica -c "SELECT now() - pg_last_xact_replay_timestamp() AS lag;"
# If lag > 0: reads from replica are stale → go to "Replica Lag Fix"
```

### Phase 3: Identify (Cache Investigation)

Most likely cause: Cache invalidation not happening after writes.

```javascript
// Add temporary logging to the update endpoint:
async function updateProfile(userId, data) {
  await db.update('profiles', userId, data);
  console.log(`[DEBUG] DB updated for ${userId} at ${Date.now()}`);

  await cache.delete(`profile:${userId}`);
  console.log(`[DEBUG] Cache invalidated for ${userId} at ${Date.now()}`);

  // Verify: read immediately after invalidation
  const cached = await cache.get(`profile:${userId}`);
  console.log(`[DEBUG] Cache after invalidation: ${cached}`);
  // If this shows data, another process is re-caching stale data
}
```
```

**Tips for Customization:**
- Be as specific as possible about the symptoms
- Include: "I've already checked X and Y, which were normal"
- Add: "The bug only happens between 2-4 PM EST"

---

## 8. Dependency Conflict Resolver

**Use Case:** Debug and resolve package/dependency conflicts, version mismatches, and build failures.

**Prompt:**

```
You are a build systems expert specializing in dependency management and version resolution.

I'm experiencing a dependency conflict. Help me resolve it.

## Error
"""
[PASTE THE FULL BUILD ERROR / DEPENDENCY RESOLUTION ERROR]
"""

## Current Dependency State
"""
[PASTE package.json, requirements.txt, go.mod, Cargo.toml, or equivalent]
"""

## Environment
- **Package Manager**: [npm/yarn/pnpm/pip/cargo/go]
- **Lock File**: [Do you have one? When was it last updated?]
- **Node/Python/Go Version**: [exact version]

## Analysis Required:

### 1. Conflict Explanation
- Which packages conflict and why?
- Dependency tree showing the conflict path:
```
your-app
├── package-a@2.0 requires lib-x@^3.0
└── package-b@1.5 requires lib-x@^2.0  ← CONFLICT
```

### 2. Resolution Options (ranked by safety)
For each option:
- What to change
- Risk level
- Side effects
- Exact commands to run

### 3. Prevention
- How to prevent this from recurring
- Lock file management best practices
- Dependabot/Renovate configuration

Provide the exact commands to resolve this, not just advice.
```

**Example Output Snippet:**

```markdown
## Conflict Explanation

```
your-project
├── @auth/core@2.1.0
│   └── requires jose@^5.0.0
└── next-auth@4.24.0
    └── requires jose@^4.11.0  ← CONFLICT: needs jose 4.x, but auth/core needs 5.x
```

`jose` v4 and v5 have incompatible APIs (v5 dropped `CompactSign` class).
npm can't install both because they have the same module name.

## Resolution Options

### Option 1: Upgrade next-auth (Recommended, Low Risk)
```bash
# next-auth v5 beta uses jose@5.x, resolving the conflict
npm install next-auth@5.0.0-beta.18
```
**Risk**: next-auth v5 has API changes. Check migration guide.
**Side effects**: Auth configuration syntax changes.

### Option 2: Pin jose with overrides (Quick Fix, Medium Risk)
```json
// package.json
{
  "overrides": {
    "jose": "5.2.0"
  }
}
```
```bash
rm -rf node_modules package-lock.json && npm install
```
**Risk**: next-auth@4 may break if it uses jose APIs removed in v5.
**Side effects**: Test all auth flows thoroughly.

### Option 3: Use npm aliases (Advanced, Low Risk)
```json
{
  "dependencies": {
    "jose-v4": "npm:jose@4.15.0",
    "jose-v5": "npm:jose@5.2.0"
  }
}
```
**Risk**: Requires patching import paths. Complex.

### Prevention
```json
// renovate.json - Keep related packages in sync
{
  "packageRules": [
    {
      "groupName": "auth packages",
      "matchPackageNames": ["next-auth", "@auth/core", "jose"]
    }
  ]
}
```
```

**Tips for Customization:**
- Include your full lock file if the error is about version resolution
- Add: "I can't upgrade package X because of [reason]"
- Specify: "We use a monorepo with workspace hoisting"

---

## 9. Environment-Specific Bug Debugger

**Use Case:** Debug issues that appear only in specific environments (production only, Docker only, CI only, specific OS, etc.).

**Prompt:**

```
You are a DevOps debugging expert who specializes in environment-specific issues - bugs that appear in one environment but not another.

## The Problem
- **Works in**: [e.g., local macOS development]
- **Fails in**: [e.g., Docker container in production]
- **Error**: [What happens in the failing environment]
- **Expected**: [What should happen]

## Environment Comparison
Provide any differences you know about:
| Aspect | Working Env | Broken Env |
|--------|-------------|------------|
| OS | macOS 14 | Alpine Linux 3.19 |
| Node Version | 20.10 | 20.11 |
| Memory | 16GB | 512MB |
| File System | APFS | ext4 |
| Network | Direct | Behind NAT/proxy |
| Env Vars | .env file | Kubernetes secrets |
| [add more] | | |

## Analysis Required:

### 1. Common Causes for This Pattern
Based on the "works here, fails there" pattern, rank likely causes:
- File path differences (case sensitivity, path separators)
- Missing system dependencies (native modules, fonts, certificates)
- Environment variable differences
- Memory/resource constraints
- Network/DNS differences
- Permission differences
- Timing differences (faster/slower machine)
- Architecture differences (x86 vs ARM)

### 2. Diagnostic Commands
Exact commands to run in BOTH environments to compare:
```bash
# Run these in both environments and compare output
```

### 3. Fix
- The specific difference causing the issue
- How to make it work consistently in both environments
```

**Example Output Snippet:**

```markdown
## Diagnosis: File Path Case Sensitivity

### The Issue
macOS (APFS) is case-INsensitive: `require('./Utils')` finds `utils.js`
Linux (ext4) is case-SENSITIVE: `require('./Utils')` fails, file is `utils.js`

### Diagnostic
```bash
# In both environments, run:
find /app/src -name "*.js" | sort > /tmp/files.txt

# Check for case mismatches in imports:
grep -rn "require\|import" src/ | grep -i "utils" --color
# Look for: import from './Utils' when file is './utils.js'
```

### Files With Mismatched Cases
```
src/services/auth.js:3:  import { hash } from './Utils';     ← Capital U
src/utils.js                                                  ← lowercase u
```

### Fix
```javascript
// auth.js - line 3
// Before (works on macOS, fails on Linux)
import { hash } from './Utils';

// After (works everywhere)
import { hash } from './utils';
```

### Prevention: Add ESLint Rule
```json
// .eslintrc
{
  "rules": {
    "import/no-unresolved": "error"
  },
  "settings": {
    "import/resolver": {
      "node": {
        "caseSensitive": true  // Enforce case-sensitive imports even on macOS
      }
    }
  }
}
```

### CI Check
```bash
# Add to CI pipeline: detect case-sensitivity issues
git config core.ignoreCase false
git ls-files | sort -f | uniq -di
# Any output = files that differ only in case = problem on Linux
```
```

**Tips for Customization:**
- Fill in the environment comparison table as completely as possible
- Add: "I can SSH into both environments to run diagnostics"
- Include: Dockerfile and docker-compose.yml for container-specific issues

---

## 10. Production Incident Debugger

**Use Case:** You're on call and something is broken in production RIGHT NOW. Get a rapid triage and resolution plan.

**Prompt:**

```
You are an incident commander helping debug a production issue in real-time. I need fast, actionable guidance.

## INCIDENT STATUS
- **Severity**: [P1-Critical / P2-High / P3-Medium]
- **Impact**: [What users are affected, what's broken]
- **Duration**: [How long has it been happening]
- **Trending**: [Getting worse / stable / improving]

## WHAT I KNOW
- **Alerts firing**: [List alerts]
- **Error rate**: [Current vs normal]
- **Recent changes**: [Deploys, config changes, infrastructure changes in last 24h]
- **Logs showing**: [Key error messages]
- **Metrics**: [CPU, memory, latency, error rate, queue depth]

## WHAT I NEED RIGHT NOW

### 1. Triage (2 minutes)
- Is this a code bug, infrastructure issue, or external dependency?
- What's the fastest way to mitigate user impact RIGHT NOW (even before finding root cause)?
  - Rollback deploy?
  - Scale up?
  - Enable feature flag?
  - Failover to backup?

### 2. Diagnosis (10 minutes)
- Top 3 most likely root causes given the symptoms
- For each: one command to confirm or rule out
- Decision tree for rapid diagnosis

### 3. Fix (15 minutes)
- For the most likely cause: exact commands to fix
- Verification: how to confirm it's fixed
- Communication: status update template for stakeholders

### 4. Post-Incident (after resolution)
- What data to preserve for post-mortem
- Quick wins to prevent recurrence

Provide COMMANDS, not concepts. I need to copy-paste and execute immediately.
```

**Example Output Snippet:**

```markdown
## TRIAGE (Do This First - 2 min)

**Fastest mitigation: ROLLBACK** (deploy was 1 hour ago, issue started 1 hour ago)

```bash
# Rollback to previous version immediately
kubectl rollout undo deployment/api-server -n production
kubectl rollout status deployment/api-server -n production --timeout=120s

# Verify: error rate should drop within 60 seconds
kubectl logs -l app=api-server -n production --tail=50 | grep -c "ERROR"
```

If rollback doesn't fix it within 2 minutes, it's not the deploy → continue diagnosis.

## DIAGNOSIS (10 min)

### Hypothesis 1: Database Connection Exhaustion (70% likely)
Symptoms match: 503 errors, increasing latency, recent deploy may have connection leak
```bash
# Check active connections vs limit
kubectl exec -it postgres-0 -n production -- \
  psql -c "SELECT count(*) as active, \
  (SELECT setting FROM pg_settings WHERE name='max_connections') as max \
  FROM pg_stat_activity WHERE state='active';"
# If active > 80% of max → THIS IS IT
```

### Hypothesis 2: OOM Kills (20% likely)
```bash
# Check for recent OOM events
kubectl get events -n production --sort-by='.lastTimestamp' | grep -i "oom\|kill\|evict"

# Check current memory per pod
kubectl top pods -n production -l app=api-server
```

### Hypothesis 3: External Dependency Down (10% likely)
```bash
# Quick check of dependencies from inside the cluster
kubectl exec -it api-server-pod -n production -- \
  curl -sS -o /dev/null -w "%{http_code} %{time_total}s" https://payment-api.stripe.com/v1/health
```

## STATUS UPDATE TEMPLATE
```
[Incident Update - HH:MM UTC]
Impact: [X]% of API requests returning 503 errors
Status: Investigating - deployed rollback, monitoring recovery
ETA: Expect resolution within 15 minutes
Next update: In 10 minutes or when resolved
```
```

**Tips for Customization:**
- Include your actual kubectl context and namespace
- Add: "We use PagerDuty and need to update the incident there"
- Specify: "Our rollback process requires approval from [person]"
