#!/bin/bash
# Quick setup script for Phase 9.5 Redis Caching Layer

set -e

echo "=========================================="
echo "Phase 9.5: Redis Caching Layer Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check if Redis is installed
echo -e "${YELLOW}[Step 1/5]${NC} Checking Redis installation..."
if command -v redis-cli &> /dev/null; then
    echo -e "${GREEN}✓${NC} Redis CLI found"

    # Check if Redis is running
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✓${NC} Redis is running"
    else
        echo -e "${RED}✗${NC} Redis is not running"
        echo ""
        echo "Please start Redis:"
        echo "  - Docker: docker run -d -p 6379:6379 redis:7-alpine"
        echo "  - System: sudo systemctl start redis"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Redis not found"
    echo ""
    echo "Please install Redis:"
    echo "  - Docker: docker run -d -p 6379:6379 --name redis-cache redis:7-alpine"
    echo "  - Ubuntu: sudo apt-get install redis-server"
    echo "  - macOS: brew install redis"
    exit 1
fi

# Step 2: Check Python dependencies
echo ""
echo -e "${YELLOW}[Step 2/5]${NC} Checking Python dependencies..."
if python -c "import redis" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} redis package installed"
else
    echo -e "${YELLOW}!${NC} Installing redis package..."
    pip install redis==5.0.1 hiredis==2.3.2
    echo -e "${GREEN}✓${NC} Dependencies installed"
fi

# Step 3: Verify configuration
echo ""
echo -e "${YELLOW}[Step 3/5]${NC} Verifying configuration..."
if grep -q "cache:" config/default.yaml; then
    echo -e "${GREEN}✓${NC} Cache configuration found in config/default.yaml"
else
    echo -e "${RED}✗${NC} Cache configuration missing"
    echo "Please check config/default.yaml"
    exit 1
fi

# Step 4: Verify implementation files
echo ""
echo -e "${YELLOW}[Step 4/5]${NC} Verifying implementation files..."
REQUIRED_FILES=(
    "src/cache/__init__.py"
    "src/cache/redis_cache.py"
    "src/cache/cache_decorators.py"
    "src/cache/lifecycle.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} Missing: $file"
        exit 1
    fi
done

# Step 5: Run basic health check
echo ""
echo -e "${YELLOW}[Step 5/5]${NC} Testing Redis connection..."
if redis-cli SET test_key "Phase 9.5 works!" &> /dev/null; then
    RESULT=$(redis-cli GET test_key)
    if [ "$RESULT" == "Phase 9.5 works!" ]; then
        echo -e "${GREEN}✓${NC} Redis read/write test successful"
        redis-cli DEL test_key &> /dev/null
    else
        echo -e "${RED}✗${NC} Redis read test failed"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Redis write test failed"
    exit 1
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start the API server:"
echo "     uvicorn src.api.app:app --reload"
echo ""
echo "  2. Verify cache is working:"
echo "     curl http://localhost:8000/api/v1/health/cache"
echo ""
echo "  3. Run performance demo:"
echo "     python examples/cache_performance_demo.py"
echo ""
echo "  4. Run tests:"
echo "     pytest tests/unit/test_cache/ -v"
echo ""
echo "Documentation:"
echo "  - Quick Start: docs/cache-quick-start.md"
echo "  - Setup Guide: PHASE_9.5_SETUP_GUIDE.md"
echo "  - Full Docs: docs/redis-caching-layer.md"
echo ""
