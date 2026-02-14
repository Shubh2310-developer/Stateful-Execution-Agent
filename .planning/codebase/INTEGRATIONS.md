# External Integrations

**Analysis Date:** 2026-02-14

## APIs & External Services

**LLM Provider:**
- Groq - Used for generating agent responses and planning.
  - SDK/Client: `groq`
  - Auth: `GROQ_API_KEY` (env var)
  - Implementation: `src/llm/groq_client.py`

**Search:**
- Elasticsearch - Used for advanced search capabilities.
  - SDK/Client: `elasticsearch`

## Data Storage

**Databases:**
- MongoDB - Primary store for task state and persistence.
  - Connection: `MONGODB_URL`
  - Client: `motor` (Async)
  - Implementation: `src/state/persistence/database_adapter.py`
- PostgreSQL - Used for structured data storage and migrations.
  - Connection: `POSTGRES_SERVER`, `POSTGRES_USER`, etc.
  - Client: `asyncpg`

**File Storage:**
- AWS S3 / MinIO - Object storage for task artifacts.
  - SDK/Client: `boto3`, `minio`
  - Implementation: `src/storage/s3_adapter.py`

**Caching:**
- Redis - Used for caching and potentially as a Celery broker.
  - Service: Redis 5.0.1
  - Client: `redis-py`

## Authentication & Identity

**Auth Provider:**
- Custom JWT Authentication
  - Implementation: `src/api/middleware/authentication.py` and `src/api/dependencies/auth.py`
  - SDK/Client: `pyjwt`, `python-jose`

## Monitoring & Observability

**Error Tracking:**
- Loguru - Used for structured logging.
  - Implementation: `src/utils/logger.py`

**Logs:**
- Apache Kafka - Used for streaming agent decision traces.
  - Implementation: `src/trace/trace_logger.py`
  - Topic: `agent-decision-trace`

**Metrics:**
- Prometheus & Grafana - Used for system and task metrics.
  - Implementation: `monitoring/prometheus/`, `monitoring/grafana/`

## CI/CD & Deployment

**Hosting:**
- Kubernetes - Deployment manifests in `infrastructure/kubernetes/`.
- Terraform - Cloud resource provisioning in `infrastructure/terraform/`.

**CI Pipeline:**
- Not explicitly detected (no `.github/workflows` or similar visible in top-level `ls -R`).

## Environment Configuration

**Required env vars:**
- `GROQ_API_KEY`
- `MONGODB_URL`
- `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `S3_ACCESS_KEY` / `S3_SECRET_KEY`

**Secrets location:**
- Managed via environment variables and Kubernetes secrets (`infrastructure/kubernetes/base/secrets.yaml`).

## Webhooks & Callbacks

**Incoming:**
- Webhook endpoints defined in `docs/api/webhooks.md`.

**Outgoing:**
- Not explicitly detected in core logic, but mentioned in documentation.

---

*Integration audit: 2026-02-14*
