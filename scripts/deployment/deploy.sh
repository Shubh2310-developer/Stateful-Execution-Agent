#!/bin/bash
echo "Starting deployment sequence..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Build and start containers
docker compose up -d --build

echo "Deployment complete. Checking health..."
./scripts/deployment/health_check.sh
