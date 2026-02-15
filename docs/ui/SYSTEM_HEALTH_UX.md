# Antigravity System Health UX

Beyond task execution, operators need to monitor the underlying infrastructure. This document defines the UX patterns for system health and observability.

## 1. The Infrastructure Pulse
- **Global Status Bar**: A minimalist indicator in the header showing the health of core services (API, DB, LLM Provider, Cache).
- **Service Status Indicators**:
  - `Operational` (Emerald)
  - `Degraded` (Amber)
  - `Outage` (Red)

## 2. LLM Provider Visibility (Groq/Anthropic)
- **Rate Limit Gauges**: Real-time visualization of current token usage against provider limits.
- **Provider Latency**: A line chart showing the time-to-first-token (TTFT) for LLM responses.
- **Fallback Status**: Indicator if the system has automatically switched to a backup model due to provider issues.

## 3. Database & Cache Health
- **Connection Pools**: Gauge showing active vs. total connections for MongoDB and Redis.
- **Persistence Latency**: Tracking how long it takes to save state versions (critical for the "Stateful" promise).
- **Cache Hit Rate**: A percentage visualization of how often Redis is successfully serving cached data.

## 4. Error Logging Hub
- **System Logs**: A specialized high-density view for raw application logs (separate from the agent's Decision Trace).
- **Alert Stream**: A real-time feed of infrastructure-level alerts (e.g., "Memory usage exceeding 80%").
- **Filtering**: Filter logs by service name, error level (INFO/WARN/ERROR), and trace ID.

## 5. Proactive Health Checks
- **Health Check Report**: A one-click "Deep Audit" that runs a suite of connectivity and latency tests and produces a report.
- **Auto-remediation Toasts**: Notify the user when the system automatically fixes a health issue (e.g., "Reconnected to MongoDB after temporary drop").
