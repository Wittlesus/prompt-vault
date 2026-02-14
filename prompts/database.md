# Database Prompts

A collection of 8 battle-tested prompts for database work. From schema design to query optimization, generate production-ready database solutions.

---

## 1. Schema Design Architect

**Use Case:** Design a normalized, performant database schema from business requirements, including tables, relationships, indexes, and constraints.

**Prompt:**

```
You are a database architect designing a schema for a production application. Create a complete, well-normalized database schema.

## Business Requirements
"""
[DESCRIBE: What the application does, key entities, relationships, expected data volume, read/write ratio]
"""

## Design Requirements:
1. **Normalization**: At least 3NF, with strategic denormalization justified
2. **Naming Convention**: snake_case, plural table names, descriptive column names
3. **Primary Keys**: UUID v7 (time-sortable) or auto-increment (specify reasoning)
4. **Foreign Keys**: All relationships explicit with ON DELETE/UPDATE actions
5. **Indexes**: Cover all foreign keys, common query patterns, and unique constraints
6. **Constraints**: NOT NULL where appropriate, CHECK constraints for validation, UNIQUE constraints
7. **Audit Fields**: created_at, updated_at on every table, soft delete where appropriate
8. **Data Types**: Use the most appropriate type (don't store dates as strings, use DECIMAL for money, etc.)

## Deliverables:

### 1. Entity Relationship Description
- List all entities with their purpose
- Describe all relationships (one-to-one, one-to-many, many-to-many)
- Cardinality constraints

### 2. Complete SQL DDL
- CREATE TABLE statements with all columns, types, constraints
- CREATE INDEX statements with justification for each
- Comments on non-obvious design decisions

### 3. Sample Queries
- Show that the schema supports the 5 most common operations
- Include JOIN patterns for relationship traversal

### 4. Migration Scripts
- Version-numbered migration files
- Both UP and DOWN migrations

### 5. Estimated Sizes
- Row size estimate per table
- Table size projection at 1M, 10M, 100M rows
- Index size estimates
```

**Example Output Snippet:**

```sql
-- 001_create_users.sql

-- Users table: Core identity for all account types
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    email_verified_at TIMESTAMPTZ,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    role VARCHAR(20) NOT NULL DEFAULT 'user'
        CHECK (role IN ('user', 'admin', 'moderator')),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'suspended', 'deleted')),
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_users_email UNIQUE (email)
);

-- Index for login lookup (most frequent query)
CREATE INDEX idx_users_email_status ON users(email, status)
    WHERE status = 'active';

-- Index for admin user listing
CREATE INDEX idx_users_created_at ON users(created_at DESC);

COMMENT ON TABLE users IS 'Core user accounts. One row per registered user.';
COMMENT ON COLUMN users.password_hash IS 'bcrypt hash, never store plaintext';
COMMENT ON COLUMN users.status IS 'Soft delete via status=deleted, row preserved for FK integrity';

-- Auto-update updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 002_create_organizations.sql

-- Organizations: Multi-tenant workspace
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    plan VARCHAR(20) NOT NULL DEFAULT 'free'
        CHECK (plan IN ('free', 'pro', 'enterprise')),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_organizations_slug UNIQUE (slug)
);

-- Junction table for many-to-many user<->org membership
CREATE TABLE organization_members (
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL DEFAULT 'member'
        CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (organization_id, user_id)
);

CREATE INDEX idx_org_members_user ON organization_members(user_id);
```

**Tips for Customization:**
- Specify: "We use PostgreSQL 16" or "We must support MySQL 8"
- Add: "Include partitioning strategy for tables expected to exceed 100M rows"
- Mention: "We need multi-tenant isolation (row-level security or schema-per-tenant)"

---

## 2. Query Optimization Expert

**Use Case:** Analyze slow queries, explain execution plans, and rewrite queries for optimal performance.

**Prompt:**

```
You are a database performance expert. Optimize the following slow query.

## The Slow Query
```sql
[PASTE YOUR SLOW QUERY HERE]
```

## Performance Data
- **Current execution time**: [e.g., 4.5 seconds]
- **Target execution time**: [e.g., under 100ms]
- **Table sizes**: [e.g., orders: 5M rows, users: 500K rows]
- **EXPLAIN ANALYZE output**: (if available)
```
[PASTE EXPLAIN ANALYZE OUTPUT HERE]
```

## Analysis Required:

### 1. Query Plan Interpretation
- Walk through the EXPLAIN output in plain English
- Identify the most expensive operations
- Flag sequential scans on large tables

### 2. Root Cause
Why is this query slow? Common causes to check:
- Missing indexes (sequential scan instead of index scan)
- Poor JOIN order or type
- Unnecessary columns in SELECT (fetching too much data)
- Subquery that should be a JOIN (or vice versa)
- Functions in WHERE clause preventing index usage
- Implicit type casting
- Lock contention
- Stale statistics

### 3. Optimized Query
- Rewritten query with explanation of each change
- Expected performance improvement with reasoning

### 4. Index Recommendations
```sql
CREATE INDEX ... -- with justification for each index
```

### 5. Application-Level Optimizations
- Caching recommendations
- Pagination strategy
- Denormalization trade-offs if query can't be made fast enough

### 6. Before/After Comparison
Show expected EXPLAIN differences after optimization.
```

**Example Output Snippet:**

```markdown
## Query Plan Interpretation

The query is doing a **sequential scan on the orders table (5M rows)** because
the WHERE clause uses `DATE(created_at) = '2025-01-15'` which wraps the column
in a function, preventing the index on `created_at` from being used.

### Current Plan (4.5 seconds)
```
Seq Scan on orders  (cost=0.00..185432.00 rows=5000000)
  Filter: (date(created_at) = '2025-01-15')
  Rows Removed by Filter: 4985000
  -> Hash Join  (cost=...)
```

### Root Cause
1. `DATE(created_at)` prevents index usage (function wrapping)
2. Missing composite index for the JOIN condition
3. `SELECT *` fetches 45 columns when only 5 are needed

### Optimized Query
```sql
-- Before (4.5s): function on column prevents index use
SELECT *
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE DATE(o.created_at) = '2025-01-15'
ORDER BY o.created_at DESC;

-- After (12ms): range scan on native column type
SELECT
  o.id, o.total, o.status, o.created_at,
  u.name, u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.created_at >= '2025-01-15 00:00:00'
  AND o.created_at <  '2025-01-16 00:00:00'
ORDER BY o.created_at DESC
LIMIT 100;
```

### New Index
```sql
-- Covers the WHERE + ORDER BY + commonly selected columns
CREATE INDEX idx_orders_created_at_covering
ON orders(created_at DESC)
INCLUDE (id, total, status, user_id);
```
```

**Tips for Customization:**
- Always include EXPLAIN ANALYZE output if possible
- Specify: "We can't add more indexes due to write throughput requirements"
- Add table DDL: "Here's the current schema and existing indexes"

---

## 3. Migration Script Generator

**Use Case:** Generate safe, reversible database migration scripts for schema changes with zero-downtime deployment.

**Prompt:**

```
You are a database migration expert who writes safe, zero-downtime migration scripts.

## Current Schema
```sql
[PASTE CURRENT TABLE DEFINITIONS]
```

## Desired Change
[DESCRIBE: What needs to change and why]

## Constraints
- **Zero Downtime**: Migrations must not lock tables or break running application
- **Backward Compatible**: Old application code must work during migration
- **Reversible**: Every migration must have a rollback script
- **Migration Tool**: [Prisma Migrate / Knex / Flyway / Alembic / raw SQL]

## Generate:

### 1. Migration Plan
- Ordered list of steps with rationale
- Estimated execution time per step
- Lock analysis (will this lock the table? for how long?)
- Risk assessment per step

### 2. Migration Scripts (multi-step for safety)
Instead of one big migration, break into safe steps:
- Step 1: Add new column (nullable, no default - instant on PostgreSQL)
- Step 2: Backfill data (in batches, not one UPDATE)
- Step 3: Add NOT NULL constraint (after backfill)
- Step 4: Add new index (CONCURRENTLY)
- Step 5: Drop old column (after code deploys)

### 3. Rollback Scripts
- Rollback for each step individually
- Full rollback from any intermediate state

### 4. Validation Queries
- Check migration completed correctly
- Verify data integrity
- Confirm no data loss

### 5. Deployment Coordination
- Which steps can happen before code deploy?
- Which steps require code deploy first?
- What order: migrate first or deploy first?
```

**Example Output Snippet:**

```sql
-- Migration Plan: Rename `users.name` to `users.display_name`
-- This is a multi-step zero-downtime migration
-- Total estimated time: ~15 minutes for 500K rows

-- ============================================
-- STEP 1: Add new column (instant, no lock)
-- Run BEFORE code deploy
-- ============================================
-- UP
ALTER TABLE users ADD COLUMN display_name VARCHAR(100);

-- DOWN
ALTER TABLE users DROP COLUMN IF EXISTS display_name;

-- ============================================
-- STEP 2: Backfill in batches (no lock)
-- Run BEFORE code deploy
-- ============================================
-- UP (run in application code or script, not as a single transaction)
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET display_name = name
    WHERE display_name IS NULL
      AND id IN (
        SELECT id FROM users WHERE display_name IS NULL LIMIT batch_size
      );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    RAISE NOTICE 'Updated % rows', rows_updated;
    EXIT WHEN rows_updated = 0;

    -- Brief pause to reduce load
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;

-- DOWN
UPDATE users SET display_name = NULL;

-- ============================================
-- STEP 3: Deploy code that reads/writes BOTH columns
-- Application writes to BOTH `name` and `display_name`
-- Application reads from `display_name` with fallback to `name`
-- ============================================

-- ============================================
-- STEP 4: Add NOT NULL constraint (after backfill confirmed)
-- ============================================
-- UP
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
ALTER TABLE users ALTER COLUMN display_name SET DEFAULT '';

-- DOWN
ALTER TABLE users ALTER COLUMN display_name DROP NOT NULL;
ALTER TABLE users ALTER COLUMN display_name DROP DEFAULT;

-- ============================================
-- STEP 5: Drop old column (AFTER code no longer reads `name`)
-- Run AFTER code deploy that removes all `name` references
-- ============================================
-- UP
ALTER TABLE users DROP COLUMN name;

-- DOWN (best effort - data from backfill)
ALTER TABLE users ADD COLUMN name VARCHAR(100);
UPDATE users SET name = display_name;

-- ============================================
-- VALIDATION QUERIES
-- ============================================
-- Verify no NULLs remain
SELECT count(*) FROM users WHERE display_name IS NULL;  -- Should be 0

-- Verify data integrity
SELECT count(*) FROM users WHERE display_name = '' AND name IS NOT NULL;  -- Should be 0

-- Verify row count unchanged
SELECT count(*) FROM users;  -- Should match pre-migration count
```

**Tips for Customization:**
- Specify: "We use PostgreSQL so ALTER TABLE ADD COLUMN is instant when nullable"
- Add: "Our table has 50M rows, so backfill must be batched"
- Mention: "We have read replicas with 5-second lag"

---

## 4. Data Modeling Advisor

**Use Case:** Choose the right data model (relational, document, graph, time-series) for your use case and design it properly.

**Prompt:**

```
You are a data modeling expert who helps teams choose and design the right data model for their use case.

## Use Case
"""
[DESCRIBE: What data you're storing, how it's queried, read/write patterns, relationships, scale requirements]
"""

## Analysis Required:

### 1. Data Model Evaluation
Compare these approaches for YOUR specific use case:

| Approach | Pros | Cons | Best When |
|----------|------|------|-----------|
| Relational (PostgreSQL) | | | |
| Document (MongoDB) | | | |
| Graph (Neo4j) | | | |
| Key-Value (Redis/DynamoDB) | | | |
| Time-Series (TimescaleDB) | | | |
| Wide-Column (Cassandra) | | | |

### 2. Recommended Model
- Which model fits best and why
- What are the trade-offs you're accepting
- Hybrid approach if applicable (e.g., PostgreSQL + Redis cache)

### 3. Schema Design
- Complete schema in the recommended model
- Partitioning/sharding strategy if needed
- Index design for query patterns

### 4. Query Patterns
- Show how the top 10 most common operations look in this model
- Performance characteristics for each query

### 5. Growth Plan
- How does this scale from 1K to 1M to 1B records?
- At what point do you need to change strategies?
- Estimated costs at each scale point

### 6. Anti-Patterns to Avoid
- What NOT to do with this data model
- Common mistakes teams make
```

**Example Output Snippet:**

```markdown
## Recommendation: PostgreSQL with JSONB + TimescaleDB Extension

### Rationale
Your IoT sensor data has:
- Fixed metadata (device_id, location, type) → relational
- Variable sensor readings (different devices report different fields) → JSONB
- Time-series queries (aggregate by hour/day/month) → TimescaleDB hypertable
- 100M+ rows/month → needs partitioning

### Schema Design
```sql
-- Relational: Device metadata (queried by attributes)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    serial_number VARCHAR(50) NOT NULL UNIQUE,
    device_type VARCHAR(30) NOT NULL,
    location GEOGRAPHY(POINT, 4326),  -- PostGIS for geo queries
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Time-series: Sensor readings (hypertable for time-series optimization)
CREATE TABLE sensor_readings (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL REFERENCES devices(id),
    reading_type VARCHAR(30) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- Convert to hypertable (TimescaleDB)
SELECT create_hypertable('sensor_readings', 'time',
    chunk_time_interval => INTERVAL '1 day');

-- Compressed chunks older than 7 days (10x storage savings)
ALTER TABLE sensor_readings SET (
    timescaledb.compress,
    timescaledb.compress_orderby = 'time DESC',
    timescaledb.compress_segmentby = 'device_id'
);

SELECT add_compression_policy('sensor_readings', INTERVAL '7 days');

-- Continuous aggregate for dashboard queries
CREATE MATERIALIZED VIEW hourly_averages
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    device_id,
    reading_type,
    avg(value) as avg_value,
    min(value) as min_value,
    max(value) as max_value,
    count(*) as sample_count
FROM sensor_readings
GROUP BY bucket, device_id, reading_type;
```

### Scale Projections
| Scale | Storage | Query (1-day avg) | Monthly Cost |
|-------|---------|-------------------|--------------|
| 1M rows/mo | 2 GB | <50ms | $20 |
| 100M rows/mo | 40 GB (compressed from 200GB) | <100ms | $150 |
| 1B rows/mo | 400 GB (compressed from 2TB) | <200ms (with continuous aggs) | $800 |
```

**Tips for Customization:**
- Describe your read vs write ratio: "90% reads, 10% writes"
- Add: "We need to support full-text search across 10M documents"
- Specify: "Our team has experience with PostgreSQL but not MongoDB"

---

## 5. Query Builder & ORM Helper

**Use Case:** Translate business requirements into optimized ORM queries (Prisma, Sequelize, SQLAlchemy, etc.) or raw SQL.

**Prompt:**

```
You are an ORM expert who translates business requirements into efficient database queries.

## ORM/Query Builder
[Prisma / Sequelize / TypeORM / SQLAlchemy / Knex / Drizzle / raw SQL]

## Schema
"""
[PASTE YOUR SCHEMA / MODEL DEFINITIONS]
"""

## Queries Needed
For each of the following business requirements, generate:

1. **The ORM query** (idiomatic, using the ORM's best practices)
2. **The raw SQL it generates** (for review)
3. **Performance notes** (will this be efficient? any N+1 risks?)
4. **Edge cases** (what happens with empty results, null values, etc.)

Business requirements:
"""
[LIST YOUR QUERY REQUIREMENTS, e.g.:
- "Find all active users who placed an order in the last 30 days, with their order count and total spent"
- "Get the top 10 products by revenue this month with their categories"
- "Find users who signed up but never placed an order (churn risk)"
]
"""

## Additional Requirements:
- Use eager loading to prevent N+1 queries
- Include proper TypeScript types for results
- Handle pagination with cursor-based approach for large datasets
- Include transaction usage where operations must be atomic
```

**Example Output Snippet:**

```typescript
// Requirement: "Find active users with orders in last 30 days,
// including order count and total spent"

// ===== Prisma Query =====
const activeSpenders = await prisma.user.findMany({
  where: {
    status: 'active',
    orders: {
      some: {
        createdAt: {
          gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        },
      },
    },
  },
  select: {
    id: true,
    email: true,
    name: true,
    _count: {
      select: { orders: true },
    },
    orders: {
      where: {
        createdAt: {
          gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        },
      },
      select: {
        total: true,
      },
    },
  },
  orderBy: {
    orders: {
      _count: 'desc',
    },
  },
  take: 100,
});

// Post-process to calculate total spent (Prisma can't aggregate in select)
const result = activeSpenders.map(user => ({
  id: user.id,
  email: user.email,
  name: user.name,
  orderCount: user._count.orders,
  totalSpent: user.orders.reduce((sum, o) => sum + o.total, 0),
}));

// ===== Generated SQL =====
/*
SELECT u.id, u.email, u.name,
  COUNT(o.id) as order_count,
  SUM(o.total) as total_spent
FROM users u
INNER JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
  AND o.created_at >= NOW() - INTERVAL '30 days'
GROUP BY u.id, u.email, u.name
ORDER BY order_count DESC
LIMIT 100;
*/

// ===== Performance Notes =====
// - This generates 2 queries (one for users, one for orders) due to Prisma's
//   query engine. For better performance on large datasets, use raw SQL:
const rawResult = await prisma.$queryRaw<ActiveSpender[]>`
  SELECT u.id, u.email, u.name,
    COUNT(o.id)::int as "orderCount",
    COALESCE(SUM(o.total), 0)::decimal as "totalSpent"
  FROM users u
  INNER JOIN orders o ON o.user_id = u.id
  WHERE u.status = 'active'
    AND o.created_at >= NOW() - INTERVAL '30 days'
  GROUP BY u.id, u.email, u.name
  ORDER BY "orderCount" DESC
  LIMIT 100;
`;

// ===== Edge Cases =====
// - Users with 0 orders in window: excluded by INNER JOIN (correct for this use case)
// - Users with NULL total on orders: COALESCE handles this
// - New users with 1000+ orders: LIMIT prevents unbounded result
```

**Tips for Customization:**
- Include your actual Prisma schema or model definitions
- Specify: "We need cursor-based pagination for infinite scroll"
- Add: "Include proper error handling for constraint violations"

---

## 6. Database Performance Diagnostic

**Use Case:** Diagnose why your database is slow with a systematic investigation of common issues.

**Prompt:**

```
You are a DBA performing a performance diagnostic on a slow database. Guide me through a systematic investigation.

## Symptoms
- **Database**: [PostgreSQL 16 / MySQL 8 / etc.]
- **Problem**: [Slow queries / high CPU / connection exhaustion / disk full / replication lag]
- **Since When**: [When did it start?]
- **Impact**: [What's affected? Response times? Error rates?]
- **Scale**: [DB size, connections, queries/sec]

## Generate a Diagnostic Runbook:

### Step 1: Quick Health Check
Provide exact queries to run for:
- Active connections vs max
- Long-running queries
- Lock contention
- Replication status
- Cache hit ratio
- Table bloat
- Index usage statistics

### Step 2: Identify Top Offenders
- Top 10 slowest queries (from pg_stat_statements or slow query log)
- Top 10 tables by sequential scans (missing indexes)
- Top 10 most accessed tables (hot spots)
- Unused indexes (wasting write performance)

### Step 3: Resource Analysis
- CPU: What's consuming it? (query complexity, insufficient indexes)
- Memory: shared_buffers hit ratio, work_mem usage
- Disk I/O: Read vs write ratio, random vs sequential
- Connections: Pool saturation, idle connections

### Step 4: Recommendations
Prioritized list of actions with expected improvement.

Provide all diagnostic queries ready to copy-paste.
```

**Example Output Snippet:**

```sql
-- ============================================
-- STEP 1: QUICK HEALTH CHECK
-- Run all of these immediately
-- ============================================

-- 1.1 Connection Status
SELECT
    count(*) FILTER (WHERE state = 'active') as active,
    count(*) FILTER (WHERE state = 'idle') as idle,
    count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_txn,
    count(*) as total,
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max
FROM pg_stat_activity;
-- RED FLAG: idle_in_txn > 0 (these hold locks!)
-- RED FLAG: total > 80% of max

-- 1.2 Long-Running Queries (over 30 seconds)
SELECT
    pid,
    now() - query_start as duration,
    state,
    left(query, 100) as query_preview,
    wait_event_type,
    wait_event
FROM pg_stat_activity
WHERE state != 'idle'
  AND query_start < now() - interval '30 seconds'
ORDER BY duration DESC;
-- ACTION: Consider killing queries running > 5 minutes

-- 1.3 Lock Contention
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.query AS blocked_query,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.query AS blocking_query,
    now() - blocked_activity.query_start AS blocked_duration
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_stat_activity blocked_activity ON blocked_locks.pid = blocked_activity.pid
JOIN pg_stat_activity blocking_activity ON blocking_locks.pid = blocking_activity.pid
WHERE NOT blocked_locks.granted;

-- 1.4 Cache Hit Ratio (should be > 99%)
SELECT
    schemaname, tablename,
    heap_blks_hit * 100.0 / NULLIF(heap_blks_hit + heap_blks_read, 0) as cache_hit_pct,
    heap_blks_read as disk_reads,
    heap_blks_hit as cache_hits
FROM pg_statio_user_tables
ORDER BY heap_blks_read DESC
LIMIT 10;
-- RED FLAG: Any table below 95% = needs more shared_buffers or is too big for RAM

-- ============================================
-- STEP 2: TOP OFFENDERS
-- ============================================

-- 2.1 Slowest Queries (requires pg_stat_statements extension)
SELECT
    left(query, 80) as query,
    calls,
    round(mean_exec_time::numeric, 2) as avg_ms,
    round(total_exec_time::numeric, 2) as total_ms,
    rows as avg_rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- 2.2 Tables Needing Indexes (high sequential scans)
SELECT
    schemaname, tablename,
    seq_scan as sequential_scans,
    idx_scan as index_scans,
    n_live_tup as row_count,
    CASE WHEN seq_scan > 0
      THEN round(100.0 * idx_scan / (seq_scan + idx_scan), 1)
      ELSE 100
    END as index_usage_pct
FROM pg_stat_user_tables
WHERE n_live_tup > 10000  -- Only tables with meaningful data
ORDER BY seq_scan DESC
LIMIT 10;
-- RED FLAG: Large tables with low index_usage_pct need index analysis
```

**Tips for Customization:**
- Specify your database version and hosting (RDS, self-managed, etc.)
- Add: "Include connection pooler diagnostics (PgBouncer)"
- Mention: "We have read replicas and need replication lag metrics"

---

## 7. Seed Data & Test Fixture Generator

**Use Case:** Generate realistic, consistent seed data for development, testing, and demo environments.

**Prompt:**

```
You are a data engineer creating seed data for development and testing environments.

## Schema
```sql
[PASTE YOUR TABLE DEFINITIONS]
```

## Requirements:
1. **Realistic Data**: Use realistic names, emails, dates, addresses (not "test1", "foo@bar")
2. **Relationship Integrity**: All foreign keys valid, junction tables populated correctly
3. **Edge Cases Included**: Mix of normal and edge-case data:
   - Users with 0 orders, 1 order, and 100+ orders
   - Orders in all statuses (pending, paid, shipped, cancelled, refunded)
   - Products with 0 stock, low stock, and high stock
   - Data spanning multiple years for time-based queries
4. **Deterministic**: Same seed produces same data (use seeded random)
5. **Scalable**: Easy to generate N records (not just fixed 10 rows)
6. **Demo-Ready**: Enough data to make dashboards and reports look realistic

## Generate:

### 1. SQL Seed Script
- Insert statements in correct dependency order
- Transaction-wrapped for atomicity
- ON CONFLICT handling for re-runnability

### 2. Seed Script (code)
- Node.js/Python script using faker for large datasets
- Configurable: `SEED_USERS=1000 SEED_ORDERS=50000 node seed.js`
- Progress reporting for large seeds

### 3. Named Fixtures
Create specific named records for testing:
- `admin_user`: Admin with full permissions
- `new_user`: Just signed up, no orders
- `whale_customer`: Premium user with 500+ orders
- `suspended_user`: Account suspended, should be blocked
- `expired_trial`: Trial ended yesterday
```

**Example Output Snippet:**

```sql
-- seed.sql - Development seed data
-- Run with: psql -d myapp_dev -f seed.sql

BEGIN;

-- Clean existing seed data (preserve structure)
TRUNCATE users, orders, order_items, products, categories RESTART IDENTITY CASCADE;

-- ============================================
-- CATEGORIES
-- ============================================
INSERT INTO categories (id, name, slug) VALUES
  ('cat_electronics', 'Electronics', 'electronics'),
  ('cat_clothing', 'Clothing', 'clothing'),
  ('cat_books', 'Books', 'books'),
  ('cat_home', 'Home & Garden', 'home-garden');

-- ============================================
-- PRODUCTS (mix of stock levels)
-- ============================================
INSERT INTO products (id, name, price, stock, category_id) VALUES
  -- Normal stock
  ('prod_laptop', 'ProBook Laptop 15"', 1299.99, 150, 'cat_electronics'),
  ('prod_headphones', 'NoiseFree Pro Headphones', 89.99, 500, 'cat_electronics'),
  ('prod_tshirt', 'Classic Cotton Tee', 24.99, 2000, 'cat_clothing'),
  -- Low stock (triggers "almost gone" alerts)
  ('prod_watch', 'SmartTime Watch Ultra', 399.99, 3, 'cat_electronics'),
  -- Zero stock (out of stock scenarios)
  ('prod_rare_book', 'First Edition: The Pragmatic Programmer', 199.99, 0, 'cat_books'),
  -- High-priced (tests decimal handling)
  ('prod_sofa', 'Artisan Leather Sofa', 3499.50, 12, 'cat_home');

-- ============================================
-- NAMED TEST USERS
-- ============================================

-- Admin user (password: "admin123" bcrypt-hashed)
INSERT INTO users (id, email, name, role, status, password_hash) VALUES
  ('usr_admin', 'admin@example.com', 'Alice Admin',
   'admin', 'active',
   '$2b$10$xJwK1YQkZMkZvYqE5FJNZ.T8YGojIDaA8rK3m8y9.8XwKjVFO');

-- New user (just signed up, no orders yet)
INSERT INTO users (id, email, name, role, status, created_at) VALUES
  ('usr_new', 'newbie@example.com', 'Nina Newuser',
   'user', 'active', NOW() - INTERVAL '1 hour');

-- Whale customer (high-value, many orders)
INSERT INTO users (id, email, name, role, status, created_at) VALUES
  ('usr_whale', 'whale@bigcorp.com', 'Walter Whale',
   'user', 'active', NOW() - INTERVAL '2 years');

-- Suspended user (should be blocked from actions)
INSERT INTO users (id, email, name, role, status) VALUES
  ('usr_suspended', 'suspended@example.com', 'Sam Suspended',
   'user', 'suspended');

-- Expired trial user
INSERT INTO users (id, email, name, role, status, trial_ends_at) VALUES
  ('usr_expired_trial', 'trial@example.com', 'Tina Trial',
   'user', 'active', NOW() - INTERVAL '1 day');

COMMIT;
```

**Tips for Customization:**
- Specify: "Generate 100K orders across 2 years for realistic reporting"
- Add: "Include data for all timezones (test TZ handling)"
- Mention: "Include unicode names and addresses for i18n testing"

---

## 8. Database Security Hardening

**Use Case:** Audit and harden database security, including access control, encryption, and compliance requirements.

**Prompt:**

```
You are a database security expert performing a security hardening audit.

## Current Setup
- **Database**: [PostgreSQL 16 / MySQL 8 / etc.]
- **Hosting**: [RDS / Cloud SQL / self-managed / Docker]
- **Application Access**: [How does the app connect? Connection string, IAM, etc.]
- **Team Access**: [Who has direct DB access? How do they connect?]
- **Compliance**: [SOC 2 / HIPAA / PCI-DSS / GDPR / none]

## Audit & Harden:

### 1. Authentication & Access Control
- Review all database users and their privileges
- Implement least-privilege access (separate users for app, migrations, read-only, admin)
- Password policy and rotation
- Connection encryption (TLS required)

### 2. Network Security
- Who can reach the database? (security groups, network ACLs)
- Is the database on a public subnet? (it shouldn't be)
- VPN or bastion host for developer access
- Connection pooling security

### 3. Data Encryption
- Encryption at rest (disk-level or column-level)
- Encryption in transit (TLS version and cipher suites)
- Application-level encryption for PII
- Key management strategy

### 4. Auditing & Monitoring
- Query logging (who ran what, when)
- Connection logging
- Failed auth attempt alerts
- Privilege escalation alerts
- Data access audit trail

### 5. Backup Security
- Are backups encrypted?
- Who has access to backups?
- Backup integrity verification

### 6. SQL Injection Prevention
- Parameterized query audit
- WAF rules for common injection patterns
- Input validation at application layer

Provide:
- Exact SQL commands to implement each hardening measure
- Configuration file changes
- Monitoring queries to detect security issues
```

**Example Output Snippet:**

```sql
-- ============================================
-- 1. LEAST-PRIVILEGE USER SETUP
-- ============================================

-- Application user: can only CRUD on application tables
CREATE ROLE app_user WITH LOGIN PASSWORD 'use-secrets-manager';
GRANT CONNECT ON DATABASE myapp TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
-- DENY: Cannot DROP tables, ALTER schema, or access pg_stat_statements
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Migration user: can alter schema (used only during deploys)
CREATE ROLE migration_user WITH LOGIN PASSWORD 'use-secrets-manager';
GRANT ALL PRIVILEGES ON DATABASE myapp TO migration_user;
-- This user should only be used in CI/CD pipeline, never by the running app

-- Read-only user: for analytics, dashboards, support team
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'use-secrets-manager';
GRANT CONNECT ON DATABASE myapp TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

-- REVOKE dangerous permissions from all non-admin users
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON pg_stat_statements FROM app_user, readonly_user;

-- ============================================
-- 2. ENFORCE TLS CONNECTIONS
-- ============================================
-- In postgresql.conf:
-- ssl = on
-- ssl_min_protocol_version = 'TLSv1.2'
-- ssl_cert_file = '/path/to/server.crt'
-- ssl_key_file = '/path/to/server.key'

-- In pg_hba.conf: Require SSL for all remote connections
-- hostssl all all 0.0.0.0/0 scram-sha-256
-- hostssl all all ::/0 scram-sha-256
-- (Remove any "host" lines that allow unencrypted connections)

-- ============================================
-- 3. ROW-LEVEL SECURITY (multi-tenant isolation)
-- ============================================
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
-- App must SET app.current_tenant = 'tenant-uuid' on each connection

-- ============================================
-- MONITORING: Detect Suspicious Activity
-- ============================================

-- Find users with excessive privileges
SELECT r.rolname, r.rolsuper, r.rolcreatedb, r.rolcreaterole
FROM pg_roles r
WHERE r.rolsuper = true OR r.rolcreatedb = true
ORDER BY r.rolname;
-- Only the RDS master user should have superuser. Alert on any others.

-- Detect failed login attempts (check pg_log)
-- grep "FATAL.*password authentication failed" /var/log/postgresql/*.log | \
--   awk '{print $NF}' | sort | uniq -c | sort -rn
```

**Tips for Customization:**
- Specify your compliance requirements for exact controls needed
- Add: "We need to encrypt SSN and credit card columns at the application level"
- Mention: "We use AWS RDS, so include RDS-specific security features (IAM auth, Security Groups)"
