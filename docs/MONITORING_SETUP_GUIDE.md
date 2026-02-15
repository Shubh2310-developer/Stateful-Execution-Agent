# Monitoring Setup Guide - Stateful Execution Agent

## 🎯 Quick Start

### Automated Setup
```bash
# Run the automated monitoring setup
./scripts/setup_monitoring.sh
```

### Manual Setup
If you prefer manual setup, follow the detailed instructions below.

## 📊 Monitoring Stack

### Components
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization dashboards  
- **MongoDB Exporter**: Database metrics
- **Redis Exporter**: Cache metrics
- **Node Exporter**: System metrics

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Agent API      │───▶│   Prometheus    │───▶│    Grafana      │
│  (Port 8000)    │    │   (Port 9090)   │    │   (Port 3000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       ▲                       ▲
        ▼                       │                       │
┌─────────────────┐             │              ┌─────────────────┐
│    MongoDB      │────────────▶│              │     Alerts      │
│  (Port 27017)   │   Exporter   │              │   & Notifications│
└─────────────────┘  (Port 9216) │              └─────────────────┘
        │                       │
        ▼                       │
┌─────────────────┐             │
│     Redis       │────────────▶│
│  (Port 6379)    │   Exporter   │
└─────────────────┘  (Port 9121) │
                                │
┌─────────────────┐             │
│  System Metrics │────────────▶│
│   Node Exporter │             │
│  (Port 9100)    │             │
└─────────────────┘             │
```

## 🚀 Getting Started

### 1. Start Monitoring Stack
```bash
# Navigate to project root
cd /path/to/stateful-execution-agent

# Make setup script executable
chmod +x scripts/setup_monitoring.sh

# Run setup
./scripts/setup_monitoring.sh
```

### 2. Access Dashboards
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

### 3. Import Dashboard
1. Login to Grafana with `admin/admin`
2. Navigate to **Dashboards → Import**
3. Upload `monitoring/grafana/dashboards/agent_performance.json`

## 📈 Key Metrics Tracked

### Performance Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Task Success Rate | Percentage of successful tasks | <90% |
| API Response Time | 95th percentile response time | >10s |
| Planner Success Rate | Planning phase success rate | <95% |
| Tool Execution Rate | Tool success rate by type | <95% |

### Resource Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Memory Usage | Process memory consumption | >1GB |
| CPU Usage | Process CPU utilization | >80% |
| Database Connections | MongoDB active connections | >100 |
| Cache Hit Rate | Redis cache effectiveness | <80% |

### Business Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Daily LLM Cost | Total LLM API costs | >$20 |
| Token Usage | LLM tokens consumed | >80% of limit |
| Tasks per Hour | System throughput | <50/hour |

## 🚨 Alerting Configuration

### Alert Rules Location
- **File**: `monitoring/alerts/agent_alerts.yml`
- **Reload**: Prometheus auto-reloads every 15 seconds

### Critical Alerts
1. **High Task Failure Rate** (>10%)
2. **API Response Time High** (>10s)  
3. **Database Connection Lost**
4. **Daily Cost Exceeded** (>$20)

### Warning Alerts
1. **LLM Token Limit Approaching** (>80%)
2. **Planner Failure Rate** (>5%)
3. **Tool Execution Failures**
4. **Cache Connection Lost**

## 🔧 Customization

### Adding New Metrics
1. **Instrument Code**: Add metrics in your application
```python
from prometheus_client import Counter, Histogram

task_counter = Counter('tasks_created_total', 'Total tasks created')
response_time = Histogram('request_duration_seconds', 'Request duration')
```

2. **Update Dashboard**: Add new panels to Grafana dashboard
3. **Configure Alerts**: Add alert rules to `agent_alerts.yml`

### Custom Dashboards
Create additional dashboards for specific use cases:
- **Cost Analysis**: Track LLM spending patterns
- **User Behavior**: Monitor task patterns by user
- **Performance Debugging**: Deep-dive into slow operations

## 🐛 Troubleshooting

### Common Issues

#### Prometheus Not Scraping
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify agent metrics endpoint
curl -H "X-API-KEY: dev-api-key-12345" http://localhost:8000/metrics
```

#### Grafana Dashboard Empty
1. Check Prometheus data source configuration
2. Verify time range (use "Last 1 hour")
3. Check metric names match your instrumentation

#### Exporter Connection Issues
```bash
# Test MongoDB connection
docker logs mongodb-exporter

# Test Redis connection  
docker logs redis-exporter

# Check if services are accessible
curl http://localhost:9216/metrics  # MongoDB
curl http://localhost:9121/metrics  # Redis
```

### Debug Commands
```bash
# Check all monitoring containers
docker ps | grep -E "(prometheus|grafana|exporter)"

# View logs
docker logs prometheus
docker logs grafana
docker logs mongodb-exporter

# Restart monitoring stack
docker restart prometheus grafana mongodb-exporter redis-exporter
```

## 📊 Dashboard Panels Explained

### 1. Task Success Rate
- **Type**: Stat panel with thresholds
- **Query**: `rate(tasks_completed_total[5m]) / rate(tasks_created_total[5m]) * 100`
- **Thresholds**: Red <70%, Yellow 70-90%, Green >90%

### 2. Task Status Distribution  
- **Type**: Pie chart
- **Query**: `tasks_by_status`
- **Purpose**: Visual breakdown of task states

### 3. API Response Times
- **Type**: Time series
- **Queries**: 50th and 95th percentile response times
- **Purpose**: Track performance trends

### 4. LLM Token Usage
- **Type**: Time series with limit line
- **Purpose**: Monitor token consumption vs daily limits

### 5. Tool Success Rates
- **Type**: Bar gauge  
- **Purpose**: Identify problematic tools

### 6. Error Rates by Component
- **Type**: Time series
- **Purpose**: Isolate failure sources

## 🔮 Advanced Monitoring

### Custom Metrics Integration
```python
# Example: Custom business metrics
from prometheus_client import Gauge

user_satisfaction = Gauge('user_satisfaction_score', 'User satisfaction rating')
task_complexity = Histogram('task_complexity_score', 'Task complexity assessment')
```

### Log Aggregation (Future Enhancement)
- **ELK Stack**: Elasticsearch + Logstash + Kibana
- **Loki**: Grafana's log aggregation system
- **Structured Logging**: JSON formatted logs for better parsing

### Distributed Tracing (Future Enhancement)
- **Jaeger**: Request tracing across microservices
- **Zipkin**: Alternative tracing solution
- **OpenTelemetry**: Industry standard for observability

## 📋 Maintenance

### Daily Tasks
- [ ] Check dashboard for alerts
- [ ] Review error rate trends  
- [ ] Monitor cost metrics

### Weekly Tasks
- [ ] Review performance trends
- [ ] Update alert thresholds if needed
- [ ] Clean up old metrics data

### Monthly Tasks
- [ ] Dashboard optimization
- [ ] Alert rule refinement
- [ ] Capacity planning review

---

**Last Updated**: 2026-02-15  
**Version**: 1.0  
**Maintainer**: Development Team