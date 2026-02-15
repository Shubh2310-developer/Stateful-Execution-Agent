#!/bin/bash

# Monitoring Setup Script for Stateful Execution Agent
# This script sets up Prometheus, Grafana, and exporters for comprehensive monitoring

set -e

echo "🚀 Setting up monitoring for Stateful Execution Agent..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker ps >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

print_status "Docker is running"

# Create monitoring network if it doesn't exist
if ! docker network ls | grep -q monitoring; then
    docker network create monitoring
    print_status "Created monitoring network"
else
    print_status "Monitoring network already exists"
fi

# Start Prometheus
echo "🔍 Starting Prometheus..."
docker run -d \
    --name prometheus \
    --network monitoring \
    -p 9090:9090 \
    -v $(pwd)/monitoring/prometheus:/etc/prometheus \
    prom/prometheus:latest \
    --config.file=/etc/prometheus/agent_metrics.yml \
    --storage.tsdb.path=/prometheus \
    --web.console.libraries=/usr/share/prometheus/console_libraries \
    --web.console.templates=/usr/share/prometheus/consoles \
    --web.enable-lifecycle \
    2>/dev/null && print_status "Prometheus started" || print_warning "Prometheus may already be running"

# Start Grafana
echo "📊 Starting Grafana..."
docker run -d \
    --name grafana \
    --network monitoring \
    -p 3000:3000 \
    -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
    -v grafana-storage:/var/lib/grafana \
    -v $(pwd)/monitoring/grafana/dashboards:/var/lib/grafana/dashboards \
    grafana/grafana:latest \
    2>/dev/null && print_status "Grafana started" || print_warning "Grafana may already be running"

# Start MongoDB Exporter
echo "🗄️  Starting MongoDB Exporter..."
docker run -d \
    --name mongodb-exporter \
    --network monitoring \
    -p 9216:9216 \
    percona/mongodb_exporter:latest \
    --mongodb.uri=mongodb://host.docker.internal:27017 \
    2>/dev/null && print_status "MongoDB Exporter started" || print_warning "MongoDB Exporter may already be running"

# Start Redis Exporter
echo "💾 Starting Redis Exporter..."
docker run -d \
    --name redis-exporter \
    --network monitoring \
    -p 9121:9121 \
    oliver006/redis_exporter:latest \
    --redis.addr=redis://host.docker.internal:6379 \
    2>/dev/null && print_status "Redis Exporter started" || print_warning "Redis Exporter may already be running"

# Start Node Exporter (for system metrics)
echo "🖥️  Starting Node Exporter..."
docker run -d \
    --name node-exporter \
    --network monitoring \
    -p 9100:9100 \
    -v /proc:/host/proc:ro \
    -v /sys:/host/sys:ro \
    -v /:/rootfs:ro \
    --pid=host \
    prom/node-exporter:latest \
    --path.procfs=/host/proc \
    --path.sysfs=/host/sys \
    --collector.filesystem.mount-points-exclude="^/(sys|proc|dev|host|etc)($$|/)" \
    2>/dev/null && print_status "Node Exporter started" || print_warning "Node Exporter may already be running"

# Wait for services to start
echo "⏳ Waiting for services to start up..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check Prometheus
if curl -s http://localhost:9090/-/healthy >/dev/null 2>&1; then
    print_status "Prometheus is healthy"
else
    print_warning "Prometheus health check failed"
fi

# Check Grafana
if curl -s http://localhost:3000/api/health >/dev/null 2>&1; then
    print_status "Grafana is healthy"
else
    print_warning "Grafana health check failed"
fi

# Check exporters
for port in 9216 9121 9100; do
    if curl -s http://localhost:$port/metrics >/dev/null 2>&1; then
        print_status "Exporter on port $port is responding"
    else
        print_warning "Exporter on port $port is not responding"
    fi
done

echo ""
echo "🎉 Monitoring setup complete!"
echo ""
echo "📈 Access your monitoring tools:"
echo "   • Prometheus: http://localhost:9090"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "📊 Import the dashboard:"
echo "   1. Login to Grafana (admin/admin)"
echo "   2. Go to Dashboards > Import"
echo "   3. Upload monitoring/grafana/dashboards/agent_performance.json"
echo ""
echo "🚨 Alerts configuration:"
echo "   • Alert rules are in monitoring/alerts/agent_alerts.yml"
echo "   • Configure notification channels in Grafana"
echo ""

# Create a status file
echo "$(date): Monitoring setup completed" > monitoring/setup_status.txt
print_status "Setup status logged to monitoring/setup_status.txt"