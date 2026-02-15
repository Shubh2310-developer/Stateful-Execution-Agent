#!/bin/bash
set -e

# ==============================================================================
# STATEFUL EXECUTION AGENT - MASTER VERIFICATION & STARTUP SCRIPT
# ==============================================================================

# Add current directory to PYTHONPATH so python scripts can find 'src'
export PYTHONPATH=$PYTHONPATH:.

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

LOG_DIR="logs"
mkdir -p $LOG_DIR

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}   Stateful Execution Agent - System Orchestration${NC}"
echo -e "${GREEN}==================================================${NC}"

# ------------------------------------------------------------------------------
# 1. INFRASTRUCTURE CHECK
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[1/5] Checking Infrastructure...${NC}"

# Check Python Environment
if [[ -z "$VIRTUAL_ENV" && -z "$CONDA_DEFAULT_ENV" ]]; then
    echo -e "${YELLOW}! Warning: No virtual environment detected.${NC}"
    echo "  Recommended: 'conda activate stateful-execution-agent' or 'source venv/bin/activate'"
else
    echo -e "${GREEN}✓ Environment active: $(basename ${VIRTUAL_ENV:-$CONDA_DEFAULT_ENV})${NC}"
fi

# Function to check if a port is open
check_port() {
    python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1); result = s.connect_ex(('localhost', $1)); exit(result)"
}

# Function to start docker services
start_docker_services() {
    if command -v docker-compose &> /dev/null; then
        echo "  Attempting to start infrastructure via Docker Compose..."
        docker-compose up -d mongodb redis
    elif command -v docker &> /dev/null; then
        echo "  Attempting to start infrastructure via Docker Compose (plugin)..."
        docker compose up -d mongodb redis
    else
        echo -e "${RED}  ! Docker not found. Cannot auto-start infrastructure.${NC}"
        return 1
    fi
}

# Check MongoDB (Port 27017)
if check_port 27017; then
    echo -e "${GREEN}✓ MongoDB is running (Port 27017)${NC}"
else
    echo -e "${YELLOW}MongoDB is NOT running. Attempting to start...${NC}"
    if ! start_docker_services; then
         # Fallback to local if docker failed
         { sudo systemctl start mongod || sudo service mongodb start; } || echo -e "${RED}  ! Failed to start MongoDB locally.${NC}"
    fi

    # Wait for startup
    echo "  Waiting for MongoDB to be ready..."
    sleep 5
    if check_port 27017; then
        echo -e "${GREEN}✓ MongoDB started successfully${NC}"
    else
        echo -e "${RED}✗ MongoDB failed to start. Please check 'docker-compose logs' or system logs.${NC}"
        exit 1
    fi
fi

# Check Redis (Port 6379)
if check_port 6379; then
    echo -e "${GREEN}✓ Redis is running (Port 6379)${NC}"
else
    echo -e "${YELLOW}Redis is NOT running. Attempting to start...${NC}"
    # Docker services usually start together, but ensure it's up
    if ! start_docker_services; then
         { sudo systemctl start redis-server || redis-server --daemonize yes; } || echo -e "${RED}  ! Failed to start Redis locally.${NC}"
    fi

    # Wait for startup
    sleep 2
    if check_port 6379; then
        echo -e "${GREEN}✓ Redis started successfully${NC}"
    else
        echo -e "${RED}✗ Redis failed to start.${NC}"
        exit 1
    fi
fi

# ------------------------------------------------------------------------------
# 2. BACKEND INTEGRITY & SETUP
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[2/5] Verifying Backend Integrity...${NC}"

# Run the python verification script
if python3 scripts/verify_backend_integrity.py; then
    echo -e "${GREEN}✓ Backend modules and database connection verified${NC}"
else
    echo -e "${RED}✗ Backend verification failed. Check logs/backend_verify.log${NC}"
    exit 1
fi

echo -e "\n${YELLOW}[3/5] Seeding Database...${NC}"
python3 scripts/setup/seed_data.py

# ------------------------------------------------------------------------------
# 3. STARTING SERVICES
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[4/5] Starting Services...${NC}"

# Start Backend
echo "  Starting FastAPI Backend (Port 8000)..."
if pgrep -f "uvicorn src.api.app:app" > /dev/null; then
    echo -e "${YELLOW}  ! Backend already running. Killing old process...${NC}"
    pkill -f "uvicorn src.api.app:app"
    sleep 2
fi

nohup uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload > $LOG_DIR/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

# Wait for Backend to be ready
echo "  Waiting for backend health check..."
MAX_RETRIES=30
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/api/v1/health > /dev/null; then
        echo -e "${GREEN}✓ Backend is healthy!${NC}"
        break
    fi
    sleep 1
    COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}✗ Backend failed to start within 30 seconds. Check logs/backend.log${NC}"
    cat $LOG_DIR/backend.log
    exit 1
fi

# Start Frontend
echo "  Starting Next.js Frontend (Port 3000)..."
if [ ! -d "node_modules" ] && [ -f "package.json" ]; then
    echo "  Installing frontend dependencies..."
    npm install > $LOG_DIR/npm_install.log 2>&1
fi

if pgrep -f "next dev" > /dev/null; then
    echo -e "${YELLOW}  ! Frontend already running. Killing old process...${NC}"
    pkill -f "next dev"
    sleep 2
fi

nohup npm run dev > $LOG_DIR/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

# ------------------------------------------------------------------------------
# 4. SYSTEM SIMULATION CHECK
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[5/5] Running End-to-End Simulation...${NC}"
# Run the simulation script to verify the chain works
if python3 scripts/simulate_frontend_flow.py; then
    echo -e "${GREEN}✓ End-to-End Simulation successful!${NC}"
else
    echo -e "${RED}✗ Simulation failed. Check the output above.${NC}"
    # We don't exit here, we still want to leave the servers running for the user
fi

# ------------------------------------------------------------------------------
# 5. READY
# ------------------------------------------------------------------------------
echo -e "\n${GREEN}==================================================${NC}"
echo -e "${GREEN}   SYSTEM FULLY OPERATIONAL${NC}"
echo -e "${GREEN}==================================================${NC}"
echo -e "  Backend API:   http://localhost:8000/api/v1/docs"
echo -e "  Frontend UI:   http://localhost:3000"
echo -e "  Logs:          $LOG_DIR/backend.log, $LOG_DIR/frontend.log"
echo -e ""
echo -e "To stop all services, run: pkill -f 'uvicorn|next'"
