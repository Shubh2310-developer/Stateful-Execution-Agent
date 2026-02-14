# Deployment Guide

The Stateful Execution Agent is designed to be containerized and deployed using modern orchestration tools.

## Docker Deployment

The project includes a `Dockerfile` and `docker-compose.yml` for easy multi-container deployment.

### Local Infrastructure with Docker Compose

To start all required infrastructure (MongoDB, PostgreSQL, Redis, MinIO, Kafka) and the monitoring stack:

```bash
docker compose up -d
```

### Building the Application Image

```bash
docker build -t stateful-agent:latest .
```

## Kubernetes Deployment

Configuration files for Kubernetes are located in `infrastructure/kubernetes/`.

1.  **Apply the base manifests:**
    ```bash
    kubectl apply -f infrastructure/kubernetes/base/
    ```

2.  **Using Helm:**
    ```bash
    helm install stateful-agent ./infrastructure/kubernetes/helm/stateful-agent
    ```

## Production Considerations

### Security
- Change the `SECRET_KEY` in `.env`.
- Use a dedicated service account for S3/MinIO.
- Ensure MongoDB and PostgreSQL are not exposed publicly.
- Implement proper JWT validation in `src/api/dependencies/auth.py`.

### Scalability
- The API is stateless and can be scaled horizontally.
- For long-running tasks, consider moving execution to background workers using the `src/orchestration/workflow_engine.py` with a task queue like Celery.

### Monitoring
- Prometheus metrics are available at `/metrics` (if instrumented).
- Grafana dashboards are provided in `monitoring/grafana/dashboards/`.
