#!/bin/bash
# Connection Verification Script

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Checking Backend (FastAPI)..."
if curl -s http://localhost:8000/api/v1/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is reachable at http://localhost:8000/api/v1/health${NC}"
else
    echo -e "${RED}✗ Backend is NOT reachable at http://localhost:8000. Ensure it is running with 'uvicorn src.api.app:app --port 8000'${NC}"
fi

echo "Checking Frontend (Next.js)..."
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓ Frontend is reachable at http://localhost:3000${NC}"
else
    echo -e "${RED}✗ Frontend is NOT reachable at http://localhost:3000. Ensure it is running with 'npm run dev'${NC}"
fi

echo "Testing Mermaid Endpoint (expected 404 if no data, but should not be Connection Refused)..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/trace/task/test-id/visualization/mermaid)
if [ "$HTTP_STATUS" == "404" ] || [ "$HTTP_STATUS" == "200" ]; then
    echo -e "${GREEN}✓ Mermaid endpoint returned $HTTP_STATUS (Connection Successful)${NC}"
elif [ "$HTTP_STATUS" == "000" ]; then
    echo -e "${RED}✗ Mermaid endpoint unreachable (Connection Refused)${NC}"
else
    echo -e "${RED}✗ Mermaid endpoint returned unexpected status: $HTTP_STATUS${NC}"
fi
