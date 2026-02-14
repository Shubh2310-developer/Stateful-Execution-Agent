# Technology Stack

**Analysis Date:** 2026-02-14

## Languages

**Primary:**
- Python 3.10+ - Used throughout the entire codebase for core logic, API, and orchestration.

**Secondary:**
- Shell/Bash - Used in `scripts/` for deployment, setup, and maintenance.
- YAML/JSON - Used for configuration in `config/` and data schemas in `data/schemas/`.
- SQL - Used for database migrations and queries (PostgreSQL).

## Runtime

**Environment:**
- Python 3.10+
- CUDA 13.0 compatible for NVIDIA GeForce RTX 4050 support.

**Package Manager:**
- pip - Managed via `requirements.txt`.
- Lockfile: missing (only `requirements.txt` present).

## Frameworks

**Core:**
- FastAPI 0.109.2 - Web framework for the API layer in `src/api/`.
- Celery 5.3.6 - Distributed task queue for background processing.
- Pydantic 2.6.1 - Data validation and settings management.

**Testing:**
- Pytest 7.x - Testing framework located in `tests/`.
- Locust 2.22.0 - Load testing framework in `tests/performance/`.

**Build/Dev:**
- Docker - Containerization via `Dockerfile` and `docker-compose.yml`.
- Terraform - Infrastructure as Code in `infrastructure/terraform/`.
- Kubernetes/Helm - Orchestration in `infrastructure/kubernetes/`.

## Key Dependencies

**Critical:**
- groq 0.4.2 - SDK for interacting with Groq LLM services in `src/llm/`.
- torch 2.1.2+cu118 - Deep learning framework with CUDA support.
- sentence-transformers 2.3.1 - Used for generating vector embeddings in `src/memory/`.
- faiss-gpu 1.7.2 - GPU-accelerated similarity search for memory retrieval.

**Infrastructure:**
- motor 3.3.2 - Async MongoDB driver for state persistence.
- asyncpg 0.29.0 - Async PostgreSQL driver for data storage.
- redis 5.0.1 - Caching and session management.
- aiokafka 0.10.0 - Async Kafka client for trace logging in `src/trace/`.

## Configuration

**Environment:**
- Managed via `src/core/config.py` using `pydantic-settings`.
- Loads from `.env` file and system environment variables.

**Build:**
- `pyproject.toml` - Project metadata.
- `requirements.txt` - Dependency list.
- `docker-compose.yml` - Local development environment orchestration.

## Platform Requirements

**Development:**
- Python 3.10+
- NVIDIA Driver 580.119.02 or newer for CUDA 13.0 support.
- MongoDB, PostgreSQL, Redis, Kafka, and MinIO services.

**Production:**
- Kubernetes (EKS/GKE/Custom) or Docker Swarm.
- S3-compatible object storage.
- Managed database services (MongoDB Atlas, AWS RDS).

---

*Stack analysis: 2026-02-14*
