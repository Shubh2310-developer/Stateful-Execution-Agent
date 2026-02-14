# Stateful Execution Agent

**Autonomous goal-driven AI knowledge worker with persistent state, memory, and transparent decision-making.**

---

## 🚀 Overview

The **Stateful Execution Agent** is a production-grade autonomous AI system designed to operate as a persistent knowledge worker. Unlike standard conversational interfaces, this system transforms high-level goals into structured, executable plans, maintains state across interactions, and utilizes a multi-layer memory system to learn and adapt over time.

Built on the **Groq** LLM platform and **FastAPI**, it is engineered for reliability, observability, and scalability.

## ✨ Key Features

- **Goal-Driven Planning**: Decomposes complex user goals into atomic, executable steps with dependency mapping.
- **Stateful Execution**: Maintains persistent task state, allowing for session resumption and robust error recovery.
- **Multi-Layer Memory**:
  - **Short-Term**: Task-scoped context and working variables.
  - **Long-Term**: Learns user preferences, domain knowledge, and historical patterns.
- **Decision Traceability**: Append-only event stream logging every reasoning point, tool invocation, and validation outcome.
- **Modular Tooling**: Integrated registry for document generation, data analysis, web search, and PDF processing.
- **Production Observability**: Grafana dashboards, Prometheus metrics, and comprehensive health monitoring.

## 🏗️ Architecture

The system follows a modular architecture with a clear separation of concerns:

- **Orchestrator**: Manages the task lifecycle, routing, and validation.
- **Planner**: Transforms goals into structured JSON plans.
- **Executor**: Runs individual steps using specialized tools.
- **Reviewer**: Performs quality assurance against success criteria.
- **State/Memory**: Handles persistence and contextual awareness.

For detailed architecture diagrams and design specifications, see [docs/architecture/system-overview.md](docs/architecture/system-overview.md).

## 🛠️ Quick Start

### Prerequisites
- Python 3.10+
- MongoDB (State persistence)
- Redis (Caching)
- Groq API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/stateful-execution-agent.git
   cd stateful-execution-agent
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Start the API server**:
   ```bash
   uvicorn src.api.app:app --reload
   ```

## ⚙️ Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | API key for Groq LLM services | - |
| `MODEL_NAME` | Primary LLM model identifier | `mixtral-8x7b-32768` |
| `MONGODB_URL` | Connection string for MongoDB Atlas | - |
| `REDIS_HOST` | Hostname for Redis cache | `localhost` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka brokers for trace logging | `localhost:9092` |

## 📂 Project Structure

```text
stateful-execution-agent/
├── src/
│   ├── api/            # FastAPI application & routes
│   ├── core/           # Shared types & configuration
│   ├── executor/       # Step execution & tool orchestration
│   ├── llm/            # Groq client & prompt building
│   ├── memory/         # Short-term & long-term memory systems
│   ├── orchestration/  # Task lifecycle management
│   ├── planner/        # Goal decomposition & step generation
│   ├── reviewer/       # Quality assurance & validation
│   ├── state/          # Persistence & versioning
│   ├── tools/          # Specialized tool registry
│   └── trace/          # Decision logging & analytics
├── docs/               # Comprehensive documentation
├── tests/              # Unit, integration & performance tests
├── infrastructure/     # Terraform & Kubernetes configs
└── monitoring/         # Grafana & Prometheus dashboards
```

## 📖 Documentation

- [Getting Started Guide](docs/guides/getting-started.md)
- [API Reference](docs/api/endpoints.md)
- [Architecture Deep Dive](docs/architecture/ROADMAP.md)
- [Deployment Guide](docs/guides/deployment.md)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
