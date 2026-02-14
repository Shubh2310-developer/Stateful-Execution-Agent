#!/bin/bash
echo "Checking system health..."

# Check API endpoint
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health)

if [ "$response" == "200" ]; then
    echo "API is Healthy"
else
    echo "API Health Check FAILED with status $response"
    exit 1
fi
