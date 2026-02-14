# DevOps Prompts

A collection of 8 battle-tested prompts for DevOps tasks. From Dockerfiles to CI/CD pipelines, generate production-grade infrastructure configurations.

---

## 1. Dockerfile Generator

**Use Case:** Generate optimized, secure, production-ready Dockerfiles for any application stack.

**Prompt:**

```
You are a Docker expert creating a production-grade Dockerfile. Generate an optimized, secure Dockerfile for the following application.

## Application Details
- **Language/Runtime**: [e.g., Node.js 20, Python 3.12, Go 1.22, Java 21]
- **Framework**: [e.g., Next.js, Django, Spring Boot]
- **Build Command**: [e.g., npm run build]
- **Start Command**: [e.g., node server.js]
- **Port**: [e.g., 3000]
- **Dependencies**: [System packages needed, e.g., sharp needs libvips]
- **Environment**: [Needs env vars at build time? Runtime only?]

## Requirements (implement ALL of these):

### Security
- Use non-root user
- Use specific image tags (not :latest)
- Don't store secrets in the image
- Minimize installed packages (no curl/wget in prod unless needed)
- Use COPY instead of ADD
- Set read-only filesystem where possible

### Performance
- Multi-stage build (separate builder and runner stages)
- Optimize layer caching (copy package files before source code)
- Use .dockerignore (generate this too)
- Minimize final image size (use slim/alpine base where possible)
- Pin dependency versions in the image

### Production Readiness
- Health check instruction
- Proper signal handling (PID 1 problem)
- Labels for metadata (maintainer, version, description)
- Configurable via environment variables
- Graceful shutdown support

Generate:
1. The Dockerfile
2. The .dockerignore file
3. A docker-compose.yml for local development
4. Build and run commands
```

**Example Output Snippet:**

```dockerfile
# ===== Stage 1: Dependencies =====
FROM node:20.11-slim AS deps
WORKDIR /app

# Copy only package files first (better layer caching)
COPY package.json package-lock.json ./
RUN npm ci --only=production && \
    # Cache prod deps separately for multi-stage
    cp -R node_modules /prod_deps && \
    # Install all deps (including devDependencies for build)
    npm ci

# ===== Stage 2: Builder =====
FROM node:20.11-slim AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# ===== Stage 3: Production Runner =====
FROM node:20.11-slim AS runner

LABEL maintainer="team@example.com"
LABEL version="1.0.0"

# Security: run as non-root
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 appuser

WORKDIR /app

# Copy only production deps and built output
COPY --from=deps --chown=appuser:appgroup /prod_deps/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/package.json ./

USER appuser
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

# Use dumb-init to handle PID 1 correctly
RUN apt-get update && apt-get install -y dumb-init && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["dumb-init", "--"]

CMD ["node", "dist/server.js"]
```

**Tips for Customization:**
- Specify: "We need GPU support (NVIDIA CUDA base image)"
- Add: "Include a development stage with hot reloading"
- Mention: "Final image must be under 200MB"

---

## 2. CI/CD Pipeline Generator

**Use Case:** Generate complete CI/CD pipeline configurations for GitHub Actions, GitLab CI, or other platforms.

**Prompt:**

```
You are a CI/CD expert creating a production-grade pipeline. Generate a complete CI/CD pipeline for the following project.

## Project Details
- **CI Platform**: [GitHub Actions / GitLab CI / CircleCI / Jenkins]
- **Language**: [e.g., TypeScript/Node.js]
- **Test Framework**: [e.g., Jest]
- **Linting**: [e.g., ESLint + Prettier]
- **Deployment Target**: [e.g., AWS ECS, Kubernetes, Vercel, Heroku]
- **Docker**: [Yes/No]
- **Database**: [Needed for integration tests?]
- **Monorepo**: [Yes/No, tool: Turborepo/Nx/Lerna?]

## Pipeline Stages Required:

### 1. Validation (on every PR)
- Lint code
- Type check
- Run unit tests with coverage report
- Run integration tests (with test database)
- Check for dependency vulnerabilities
- Build to verify no build errors
- Comment coverage report on PR

### 2. Build (on merge to main)
- Build Docker image
- Tag with git SHA and branch
- Push to container registry
- Cache build layers

### 3. Deploy to Staging (automatic on main)
- Deploy to staging environment
- Run smoke tests against staging
- Notify team on Slack

### 4. Deploy to Production (manual approval)
- Blue/green or canary deployment
- Run smoke tests
- Monitor error rate for 5 minutes
- Auto-rollback if error rate > threshold
- Notify team on success/failure

### Additional Requirements:
- Reusable workflows / job templates
- Secret management (not hardcoded)
- Caching strategy for dependencies
- Branch protection rules recommendations
- Concurrent workflow handling (cancel outdated runs)
```

**Example Output Snippet:**

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel outdated PR runs

permissions:
  contents: read
  pull-requests: write  # For coverage comments

jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage --ci
      - uses: davelosert/vitest-coverage-report-action@v2
        if: github.event_name == 'pull_request'

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
```

**Tips for Customization:**
- Specify: "We use a monorepo with 5 packages"
- Add: "Include Terraform plan/apply stages for infrastructure"
- Mention: "We need HIPAA-compliant audit logging in the pipeline"

---

## 3. Infrastructure as Code Generator

**Use Case:** Generate Terraform, CloudFormation, or Pulumi configurations for cloud infrastructure.

**Prompt:**

```
You are an infrastructure engineer creating IaC (Infrastructure as Code) configurations.

## Infrastructure Requirements
- **Cloud Provider**: [AWS / GCP / Azure]
- **IaC Tool**: [Terraform / CloudFormation / Pulumi / CDK]
- **Application Type**: [Web app / API / Microservices / Static site / ML workload]
- **Expected Scale**: [Requests/sec, data volume, concurrent users]
- **Budget Constraint**: [Monthly budget target]

## Components Needed:
1. **Compute**: [ECS/EKS/Lambda/EC2 + sizing]
2. **Database**: [RDS/DynamoDB/ElastiCache + sizing]
3. **Storage**: [S3 buckets, EBS volumes]
4. **Networking**: [VPC, subnets, load balancer, CDN]
5. **Security**: [IAM roles, security groups, WAF, secrets manager]
6. **Monitoring**: [CloudWatch, alarms, dashboards]
7. **DNS**: [Route53, certificates]

## Requirements:
- Use modules for reusability
- Implement least-privilege IAM
- Enable encryption at rest and in transit
- Multi-AZ for high availability
- Auto-scaling with defined min/max
- Tagging strategy for cost allocation
- Separate environments (dev/staging/prod) using workspaces or variables
- State management (remote backend with locking)
- Output important values (endpoints, ARNs)

Generate the complete IaC configuration with:
1. Main configuration files
2. Variables file with descriptions and defaults
3. Outputs file
4. tfvars examples for each environment
5. Backend configuration
6. README with architecture diagram (text-based)
```

**Example Output Snippet:**

```hcl
# modules/api/main.tf

resource "aws_ecs_cluster" "main" {
  name = "${var.project}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = local.common_tags
}

resource "aws_ecs_service" "api" {
  name            = "${var.project}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"

  deployment_circuit_breaker {
    enable   = true
    rollback = true  # Auto-rollback on failed deployment
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = var.api_port
  }

  tags = local.common_tags
}

# Auto-scaling
resource "aws_appautoscaling_target" "api" {
  max_capacity       = var.api_max_count
  min_capacity       = var.api_min_count
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "api_cpu" {
  name               = "${var.project}-api-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.api.resource_id
  scalable_dimension = aws_appautoscaling_target.api.scalable_dimension
  service_namespace  = aws_appautoscaling_target.api.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

**Tips for Customization:**
- Specify: "We need to be SOC 2 compliant"
- Add: "Include a bastion host for database access"
- Mention: "We have an existing VPC (vpc-abc123) to deploy into"

---

## 4. Monitoring & Alerting Setup

**Use Case:** Generate monitoring dashboards, alerting rules, and SLO definitions for production services.

**Prompt:**

```
You are an observability engineer setting up comprehensive monitoring for a production service.

## Service Details
- **Service Name**: [e.g., payment-api]
- **Type**: [REST API / gRPC / Worker / Cron job]
- **SLA**: [e.g., 99.9% uptime, p99 latency < 500ms]
- **Tech Stack**: [e.g., Node.js on Kubernetes]
- **Dependencies**: [Database, cache, external APIs, message queue]
- **Monitoring Tool**: [Datadog / Grafana+Prometheus / CloudWatch / New Relic]

## Generate:

### 1. Key Metrics to Track (Golden Signals)
- **Latency**: Request duration at p50, p95, p99
- **Traffic**: Requests per second by endpoint and status code
- **Errors**: Error rate, error types, error by endpoint
- **Saturation**: CPU, memory, connections, queue depth

### 2. SLO Definitions
- Availability SLO with error budget
- Latency SLO with burn rate alerts
- SLI formulas (what exactly counts as "good")

### 3. Alert Rules
For each alert:
- **Metric**: What to measure
- **Condition**: Threshold and duration
- **Severity**: P1-P4
- **Runbook Link**: What to do when it fires
- **Notification**: Who gets paged

Categories:
- Service health alerts (down, degraded)
- Performance alerts (latency, throughput)
- Resource alerts (CPU, memory, disk, connections)
- Business alerts (failed payments, signup drops)
- Dependency alerts (database slow, external API down)

### 4. Dashboard Layout
- Overview dashboard (single pane of glass)
- Per-service detail dashboard
- Infrastructure dashboard
- Business metrics dashboard

Provide the actual configuration in your monitoring tool's format.
```

**Example Output Snippet:**

```yaml
# prometheus-rules.yml
groups:
  - name: payment-api.rules
    rules:
      # SLO: 99.9% availability (43.8 min downtime/month budget)
      - alert: PaymentAPIHighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{service="payment-api",code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="payment-api"}[5m]))
          ) > 0.001
        for: 5m
        labels:
          severity: critical
          team: payments
        annotations:
          summary: "Payment API error rate above SLO ({{ $value | humanizePercentage }})"
          runbook: "https://wiki.internal/runbooks/payment-api-errors"
          dashboard: "https://grafana.internal/d/payment-api"

      # SLO: p99 latency < 500ms
      - alert: PaymentAPIHighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="payment-api"}[5m])) by (le)
          ) > 0.5
        for: 10m
        labels:
          severity: warning
          team: payments
        annotations:
          summary: "Payment API p99 latency {{ $value }}s (SLO: 0.5s)"

      # Resource: Database connection pool near exhaustion
      - alert: PaymentAPIDBConnectionPoolLow
        expr: |
          db_pool_available_connections{service="payment-api"}
          / db_pool_max_connections{service="payment-api"}
          < 0.2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "DB connection pool below 20% available"

# Grafana Dashboard JSON
# grafana-dashboard.json
{
  "dashboard": {
    "title": "Payment API - Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [{
          "expr": "sum(rate(http_requests_total{service='payment-api'}[1m])) by (code)"
        }]
      },
      {
        "title": "Error Budget Remaining",
        "type": "gauge",
        "targets": [{
          "expr": "1 - (sum(increase(http_requests_total{service='payment-api',code=~'5..'}[30d])) / sum(increase(http_requests_total{service='payment-api'}[30d])))"
        }],
        "thresholds": [
          { "value": 0, "color": "red" },
          { "value": 0.5, "color": "yellow" },
          { "value": 0.9, "color": "green" }
        ]
      }
    ]
  }
}
```

**Tips for Customization:**
- Specify: "We use PagerDuty for on-call and Slack for non-critical alerts"
- Add: "Include business metrics: revenue per minute, successful checkouts"
- Mention: "We need compliance-specific monitoring (access logs, data access)"

---

## 5. Kubernetes Manifest Generator

**Use Case:** Generate production-ready Kubernetes manifests including deployments, services, ingress, HPA, and more.

**Prompt:**

```
You are a Kubernetes platform engineer creating production-ready manifests.

## Application Details
- **Application Name**: [e.g., user-api]
- **Container Image**: [e.g., registry.example.com/user-api]
- **Port**: [e.g., 8080]
- **Resources**: [CPU/memory requirements estimated]
- **Replicas**: [Min/Max for autoscaling]
- **Dependencies**: [Database, Redis, other services]
- **Config**: [Environment variables, config files, secrets needed]

## Generate Kubernetes Manifests For:

### 1. Deployment
- Rolling update strategy with maxSurge/maxUnavailable
- Resource requests AND limits
- Liveness, readiness, and startup probes
- Pod disruption budget
- Pod anti-affinity (spread across nodes)
- Security context (non-root, read-only filesystem)
- Graceful shutdown (preStop hook + terminationGracePeriodSeconds)

### 2. Service
- ClusterIP for internal, LoadBalancer or Ingress for external
- Named ports
- Session affinity if needed

### 3. Ingress
- TLS termination
- Rate limiting annotations
- CORS headers
- Path-based routing

### 4. Horizontal Pod Autoscaler
- CPU and memory based scaling
- Custom metrics if applicable
- Scale-down stabilization

### 5. ConfigMap & Secrets
- Non-sensitive config in ConfigMap
- Sensitive data in Secrets (with External Secrets Operator or SOPS)
- Environment-specific overlays

### 6. Network Policy
- Restrict ingress/egress to required services only

### 7. Service Account
- With minimal RBAC

Use Kustomize overlays for environment management (base + overlays/dev, staging, prod).
```

**Example Output Snippet:**

```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-api
  labels:
    app: user-api
    app.kubernetes.io/name: user-api
    app.kubernetes.io/version: "1.0.0"
spec:
  replicas: 2
  revisionHistoryLimit: 5
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime deploys
  selector:
    matchLabels:
      app: user-api
  template:
    metadata:
      labels:
        app: user-api
    spec:
      serviceAccountName: user-api
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      terminationGracePeriodSeconds: 30
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: user-api
                topologyKey: kubernetes.io/hostname
      containers:
        - name: user-api
          image: registry.example.com/user-api:latest  # Overridden per env
          ports:
            - name: http
              containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
          envFrom:
            - configMapRef:
                name: user-api-config
            - secretRef:
                name: user-api-secrets
          startupProbe:
            httpGet:
              path: /health/startup
              port: http
            failureThreshold: 30
            periodSeconds: 2
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            periodSeconds: 30
            failureThreshold: 3
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]  # Allow LB to drain
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

**Tips for Customization:**
- Specify: "We use Istio service mesh for traffic management"
- Add: "Include PodMonitor/ServiceMonitor for Prometheus scraping"
- Mention: "We need init containers for database migrations"

---

## 6. Nginx / Reverse Proxy Configuration

**Use Case:** Generate production-grade Nginx, Caddy, or Traefik configurations for reverse proxying, SSL, caching, and rate limiting.

**Prompt:**

```
You are a web infrastructure expert creating a production Nginx configuration.

## Requirements
- **Proxy Target**: [e.g., Node.js app on port 3000]
- **Domain**: [e.g., api.example.com]
- **SSL**: [Let's Encrypt / custom cert / Cloudflare]
- **Features Needed**:
  - [ ] Reverse proxy with WebSocket support
  - [ ] SSL termination with A+ rating
  - [ ] HTTP/2 enabled
  - [ ] Rate limiting per IP
  - [ ] Request size limits
  - [ ] CORS headers
  - [ ] Security headers (CSP, HSTS, X-Frame-Options)
  - [ ] Gzip/Brotli compression
  - [ ] Static file caching
  - [ ] Health check endpoint
  - [ ] Access and error logging (structured JSON)
  - [ ] IP allowlist/blocklist
  - [ ] Redirect HTTP to HTTPS
  - [ ] Custom error pages

Generate:
1. nginx.conf (main config)
2. conf.d/api.conf (site config)
3. SSL configuration
4. Rate limiting configuration
5. Security headers snippet
6. Docker Compose setup for Nginx + Certbot
7. Testing commands to verify the config
```

**Example Output Snippet:**

```nginx
# /etc/nginx/conf.d/api.conf

# Rate limiting zones
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

# Upstream with keepalive connections
upstream api_backend {
    server app:3000;
    keepalive 32;
    keepalive_timeout 60s;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.example.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # SSL Configuration (A+ on SSL Labs)
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "0" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rate limiting
    limit_req zone=api_limit burst=50 nodelay;
    limit_conn conn_limit 50;

    # Stricter rate limit for auth endpoints
    location /api/auth/ {
        limit_req zone=auth_limit burst=10 nodelay;
        proxy_pass http://api_backend;
        include /etc/nginx/proxy_params;
    }

    # API proxy
    location /api/ {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;

        client_max_body_size 10m;
    }

    # Health check (no rate limit, no logging)
    location /health {
        access_log off;
        proxy_pass http://api_backend;
    }
}
```

**Tips for Customization:**
- Specify: "We use Cloudflare in front so trust their IPs for X-Forwarded-For"
- Add: "Include caching for GraphQL GET requests"
- Mention: "We need to serve a React SPA from the same domain"

---

## 7. Database Backup & Recovery Script

**Use Case:** Generate automated database backup, rotation, and recovery scripts with monitoring.

**Prompt:**

```
You are a database reliability engineer creating backup and recovery automation.

## Database Details
- **Database**: [PostgreSQL 16 / MySQL 8 / MongoDB 7]
- **Size**: [e.g., 50GB]
- **Growth Rate**: [e.g., 1GB/month]
- **RPO**: [Recovery Point Objective - max acceptable data loss, e.g., 1 hour]
- **RTO**: [Recovery Time Objective - max acceptable downtime, e.g., 30 minutes]
- **Storage**: [S3 / GCS / Azure Blob / local]
- **Environment**: [Docker / Kubernetes / VM]

## Generate:

### 1. Backup Script
- Full backup (daily at low-traffic time)
- Incremental/WAL backup (continuous)
- Compression and encryption before upload
- Parallel dump for large databases
- Progress logging

### 2. Rotation Policy
- Keep last 7 daily backups
- Keep last 4 weekly backups
- Keep last 12 monthly backups
- Automatic cleanup of expired backups

### 3. Recovery Script
- Full restore from any backup
- Point-in-time recovery (PITR)
- Restore to a different host (for testing)
- Estimated recovery time display

### 4. Verification
- Automated restore testing (weekly, to a test instance)
- Backup integrity verification (checksum)
- Alert if backup fails or is older than RPO

### 5. Monitoring
- Backup success/failure alerts
- Backup size trending
- Time-since-last-backup metric
- Recovery test results

Provide complete, runnable scripts (bash) with error handling.
```

**Example Output Snippet:**

```bash
#!/usr/bin/env bash
# backup-postgres.sh - Automated PostgreSQL backup with encryption and S3 upload
set -euo pipefail

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-production}"
DB_USER="${DB_USER:-backup_user}"
S3_BUCKET="${S3_BUCKET:-company-db-backups}"
ENCRYPTION_KEY_FILE="/etc/backup/encryption.key"
RETENTION_DAYS=7
RETENTION_WEEKS=4
RETENTION_MONTHS=12

# Derived variables
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DAY_OF_WEEK=$(date +%u)
DAY_OF_MONTH=$(date +%d)
BACKUP_FILE="pg_${DB_NAME}_${TIMESTAMP}.sql.gz.enc"
LOG_FILE="/var/log/backups/pg_backup_${TIMESTAMP}.log"

log() { echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"; }

# Start backup
log "Starting backup of ${DB_NAME}..."

# Create compressed, encrypted backup
pg_dump \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --format=custom \
  --compress=9 \
  --jobs=4 \
  --verbose \
  2>> "$LOG_FILE" | \
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -pass file:"$ENCRYPTION_KEY_FILE" \
  -out "/tmp/${BACKUP_FILE}"

BACKUP_SIZE=$(du -h "/tmp/${BACKUP_FILE}" | cut -f1)
log "Backup complete: ${BACKUP_SIZE}"

# Upload to S3 with appropriate retention tag
RETENTION_TAG="daily"
if [ "$DAY_OF_WEEK" = "7" ]; then RETENTION_TAG="weekly"; fi
if [ "$DAY_OF_MONTH" = "01" ]; then RETENTION_TAG="monthly"; fi

aws s3 cp "/tmp/${BACKUP_FILE}" \
  "s3://${S3_BUCKET}/${RETENTION_TAG}/${BACKUP_FILE}" \
  --storage-class STANDARD_IA \
  --metadata "retention=${RETENTION_TAG},db=${DB_NAME},size=${BACKUP_SIZE}"

log "Uploaded to s3://${S3_BUCKET}/${RETENTION_TAG}/${BACKUP_FILE}"

# Verify upload
aws s3api head-object \
  --bucket "$S3_BUCKET" \
  --key "${RETENTION_TAG}/${BACKUP_FILE}" > /dev/null 2>&1 || {
  log "ERROR: Upload verification failed!"
  exit 1
}

# Cleanup local temp file
rm -f "/tmp/${BACKUP_FILE}"

# Push success metric
curl -s -X POST "http://pushgateway:9091/metrics/job/pg_backup" \
  --data-binary @- <<METRICS
pg_backup_last_success_timestamp $(date +%s)
pg_backup_size_bytes $(stat -f%z "/tmp/${BACKUP_FILE}" 2>/dev/null || echo 0)
pg_backup_duration_seconds $SECONDS
METRICS

log "Backup complete in ${SECONDS}s"
```

**Tips for Customization:**
- Specify: "We need cross-region replication for disaster recovery"
- Add: "Include a Kubernetes CronJob manifest for scheduling"
- Mention: "Backups must be HIPAA compliant (encrypted, access logged)"

---

## 8. Incident Response Automation

**Use Case:** Generate automated incident response scripts, runbooks, and communication templates.

**Prompt:**

```
You are an SRE building incident response automation. Create a comprehensive incident response toolkit.

## Team Details
- **Team Size**: [e.g., 5 engineers on rotation]
- **Communication**: [Slack / Teams / PagerDuty]
- **Infrastructure**: [AWS / GCP / Azure / Kubernetes]
- **Services**: [List critical services and their dependencies]
- **SLA**: [e.g., 99.9% uptime, 15-min response for P1]

## Generate:

### 1. Incident Response Script
Automated first-responder script that:
- Gathers system state (pods, metrics, recent deploys, logs)
- Creates incident channel in Slack
- Pages the right team based on affected service
- Posts initial situation report
- Starts a timeline log

### 2. Diagnostic Toolkit
Scripts for common incident patterns:
- `diagnose-high-latency.sh`
- `diagnose-high-error-rate.sh`
- `diagnose-out-of-memory.sh`
- `diagnose-database-issues.sh`

Each script should:
- Run in under 30 seconds
- Output a summary of findings
- Suggest next actions based on results

### 3. Communication Templates
- Initial incident notification
- Hourly status updates
- Resolution notification
- Post-incident summary (for stakeholders)

### 4. Rollback Automation
- One-command rollback for the last deploy
- Database migration rollback
- Feature flag emergency disable

### 5. Post-Incident
- Automated post-mortem document creation
- Timeline extraction from Slack messages
- Action item tracking template
```

**Example Output Snippet:**

```bash
#!/usr/bin/env bash
# incident-response.sh - Automated first-responder toolkit
set -euo pipefail

NAMESPACE="${1:-production}"
SEVERITY="${2:-P2}"
DESCRIPTION="${3:-Automated incident detection}"

echo "========================================="
echo "  INCIDENT RESPONSE - $(date -Iseconds)"
echo "  Severity: ${SEVERITY}"
echo "========================================="

# 1. Quick system snapshot
echo -e "\n--- POD STATUS ---"
kubectl get pods -n "$NAMESPACE" --sort-by='.status.startTime' | \
  grep -E "Error|CrashLoop|Pending|0/" || echo "All pods healthy"

echo -e "\n--- RECENT EVENTS (last 15 min) ---"
kubectl get events -n "$NAMESPACE" \
  --sort-by='.lastTimestamp' \
  --field-selector type=Warning \
  | tail -20

echo -e "\n--- RECENT DEPLOYS (last 2 hours) ---"
kubectl rollout history deployment -n "$NAMESPACE" | tail -10

echo -e "\n--- RESOURCE USAGE ---"
kubectl top pods -n "$NAMESPACE" --sort-by=cpu | head -10

echo -e "\n--- ERROR LOG SAMPLE (last 5 min) ---"
kubectl logs -l app -n "$NAMESPACE" --since=5m --tail=50 | \
  grep -i "error\|fatal\|panic" | tail -20

# 2. Create Slack incident channel
INCIDENT_ID="inc-$(date +%Y%m%d)-$(openssl rand -hex 3)"
CHANNEL_NAME="${INCIDENT_ID}"

CHANNEL_ID=$(curl -s -X POST "https://slack.com/api/conversations.create" \
  -H "Authorization: Bearer ${SLACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"${CHANNEL_NAME}\"}" | jq -r '.channel.id')

# 3. Post initial situation report
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "channel": "${CHANNEL_ID}",
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "Incident ${INCIDENT_ID} - ${SEVERITY}"}
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*Description:* ${DESCRIPTION}\n*Status:* Investigating\n*Commander:* $(whoami)\n*Started:* $(date -Iseconds)"}
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*Quick Actions:*\n:rewind: \`kubectl rollout undo deployment/api -n ${NAMESPACE}\`\n:mag: \`kubectl logs -l app=api -n ${NAMESPACE} --since=10m\`"}
    }
  ]
}
EOF

echo -e "\n✓ Incident channel created: #${CHANNEL_NAME}"
echo "✓ Situation report posted"
echo "✓ Run 'diagnose-${SEVERITY}.sh' for detailed analysis"
```

**Tips for Customization:**
- Specify: "We use OpsGenie instead of PagerDuty"
- Add: "Include Terraform state lock check for infrastructure incidents"
- Mention: "We need to notify customers via StatusPage.io automatically"
