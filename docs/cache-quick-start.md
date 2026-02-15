# Redis Caching - Quick Start Guide

## Setup (5 minutes)

### 1. Install Redis

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# macOS
brew install redis

# Docker
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

### 2. Verify Redis is Running

```bash
redis-cli ping
# Expected output: PONG
```

### 3. Update Configuration (Optional)

The default configuration works out of the box. To customize:

```yaml
# config/default.yaml
cache:
  enabled: true
  redis_uri: "redis://localhost:6379/0"
  ttl:
    task_state: 300      # 5 minutes
    user_memory: 600     # 10 minutes
    task_artifacts: 300  # 5 minutes
```

### 4. Start Application

Use the master script to start the system with all infrastructure checks:

```bash
./scripts/master_verify_and_start.sh
```

Alternatively, to start just the backend manually:

```bash
# The cache will automatically initialize on startup
uvicorn src.api.app:app --reload
```

You should see in the logs:
```
INFO: Initializing Redis cache...
INFO: Redis cache initialized successfully: redis://localhost:6379/0
```

## Verify It's Working

### Check Cache Health

```bash
curl http://localhost:8000/api/v1/health/cache
```

Expected response:
```json
{
  "enabled": true,
  "initialized": true,
  "metrics": {
    "hit_rate": 0.0,
    "hits": 0,
    "misses": 0,
    "errors": 0,
    "avg_time_cached_ms": 0.0,
    "avg_time_uncached_ms": 0.0
  }
}
```

### Monitor Cache in Real-Time

```bash
# Watch Redis statistics
watch -n 1 'redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses"'

# Monitor cache keys
watch -n 1 'redis-cli KEYS "*" | wc -l'

# See actual cache keys
redis-cli KEYS "*"
```

### Test Cache Performance

```bash
# Create a task (this will be cached after first load)
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "goal": {
      "request": "Test task",
      "success_criteria": ["Complete test"]
    }
  }'

# Get task state multiple times (should be faster after first request)
time curl http://localhost:8000/api/v1/state/{task_id}  # First: ~50ms
time curl http://localhost:8000/api/v1/state/{task_id}  # Cached: ~5ms
time curl http://localhost:8000/api/v1/state/{task_id}  # Cached: ~5ms

# Check cache metrics
curl http://localhost:8000/api/v1/health/cache
# You should see hits > 0 and hit_rate > 0
```

## Common Operations

### Disable Cache (for debugging)

```yaml
# config/default.yaml
cache:
  enabled: false
```

Or via environment variable:
```bash
export AGENT_CACHE__ENABLED=false
uvicorn src.api.app:app --reload
```

### Clear All Cache

```bash
redis-cli FLUSHDB
```

### Clear Specific Cache

```bash
# Clear all task state cache
redis-cli KEYS "task:state:*" | xargs redis-cli DEL

# Clear specific task
redis-cli DEL "task:state:your-task-id"

# Clear all user memory cache
redis-cli KEYS "user:memory:*" | xargs redis-cli DEL
```

### View Cached Data

```bash
# Get cache entry
redis-cli GET "task:state:your-task-id"

# See TTL
redis-cli TTL "task:state:your-task-id"

# See all keys with pattern
redis-cli KEYS "task:*"
```

## Troubleshooting

### "Redis cache is disabled in configuration"

**Solution**: Enable cache in config or check Redis connection.

```bash
# Test Redis connection
redis-cli ping

# Check config
cat config/default.yaml | grep -A 6 "cache:"
```

### "Failed to initialize Redis cache: Connection refused"

**Solution**: Redis is not running.

```bash
# Start Redis
sudo systemctl start redis

# Or with Docker
docker start redis
```

### Cache not invalidating

**Solution**: Check that cache invalidation is being called.

```bash
# Check logs for invalidation messages
grep "Invalidated cache" logs/app.log

# Verify cache keys are being deleted
redis-cli MONITOR | grep DEL
```

### Low hit rate

**Solution**: Increase TTL or check access patterns.

```yaml
cache:
  ttl:
    task_state: 600      # Increase to 10 minutes
    user_memory: 1200    # Increase to 20 minutes
```

## Performance Tips

1. **Monitor Hit Rate**: Aim for 70-80% hit rate
2. **Tune TTL**: Balance freshness vs performance
3. **Use Connection Pooling**: Default 20 connections is usually sufficient
4. **Redis Memory**: Allocate 1-2GB for moderate workloads
5. **Enable Persistence**: Use AOF for production

## Next Steps

- Read full documentation: `docs/redis-caching-layer.md`
- Run tests: `pytest tests/unit/test_cache/ -v`
- Monitor metrics: Check `/api/v1/health/cache` regularly
- Tune configuration based on your workload

## Support

If you encounter issues:

1. Check Redis logs: `sudo journalctl -u redis -f`
2. Check application logs: `tail -f logs/app.log`
3. Verify configuration: `python -c "from src.core.config import settings; print(settings.cache)"`
