#!/usr/bin/env python3
"""
Cache Implementation Verification Script

Verifies that all cache components are properly installed and configured.
Run this before deploying the caching layer.
"""

import sys
from pathlib import Path


def check_files_exist():
    """Verify all required files exist."""
    print("Checking file existence...")

    files = [
        # Core implementation
        "src/cache/__init__.py",
        "src/cache/redis_cache.py",
        "src/cache/cache_decorators.py",
        "src/cache/lifecycle.py",
        "src/cache/README.md",

        # Tests
        "tests/unit/test_cache/__init__.py",
        "tests/unit/test_cache/test_redis_cache.py",
        "tests/integration/test_cache_integration.py",

        # Documentation
        "docs/redis-caching-layer.md",
        "docs/cache-quick-start.md",
        "examples/cache_performance_demo.py",

        # Modified files
        "src/core/config.py",
        "src/state/persistence/database_adapter.py",
        "src/memory/memory_manager.py",
        "src/api/app.py",
        "src/api/routes/health.py",
        "config/default.yaml",
    ]

    missing = []
    for file_path in files:
        full_path = Path(file_path)
        if not full_path.exists():
            missing.append(file_path)
            print(f"  ✗ {file_path} - MISSING")
        else:
            print(f"  ✓ {file_path}")

    return len(missing) == 0


def check_imports():
    """Verify all cache modules can be imported."""
    print("\nChecking imports...")

    try:
        from src.cache.redis_cache import RedisCacheManager, cache_manager, CacheMetrics
        print("  ✓ redis_cache module")
    except ImportError as e:
        print(f"  ✗ redis_cache module: {e}")
        return False

    try:
        from src.cache.cache_decorators import cached, cache_invalidate
        print("  ✓ cache_decorators module")
    except ImportError as e:
        print(f"  ✗ cache_decorators module: {e}")
        return False

    try:
        from src.cache.lifecycle import initialize_cache, shutdown_cache
        print("  ✓ lifecycle module")
    except ImportError as e:
        print(f"  ✗ lifecycle module: {e}")
        return False

    try:
        from src.core.config import settings
        assert hasattr(settings, 'cache'), "settings.cache not found"
        assert hasattr(settings.cache, 'enabled'), "settings.cache.enabled not found"
        assert hasattr(settings.cache, 'redis_uri'), "settings.cache.redis_uri not found"
        assert hasattr(settings.cache, 'ttl'), "settings.cache.ttl not found"
        print("  ✓ config.cache settings")
    except (ImportError, AssertionError) as e:
        print(f"  ✗ config.cache settings: {e}")
        return False

    return True


def check_configuration():
    """Verify configuration is correct."""
    print("\nChecking configuration...")

    try:
        from src.core.config import settings

        print(f"  Cache enabled: {settings.cache.enabled}")
        print(f"  Redis URI: {settings.cache.redis_uri}")
        print(f"  TTL settings:")
        for entity, ttl in settings.cache.ttl.items():
            print(f"    - {entity}: {ttl}s")

        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False


def check_integration():
    """Verify integration with existing code."""
    print("\nChecking integration points...")

    try:
        # Check database adapter integration
        from src.state.persistence.database_adapter import DatabaseAdapter
        import inspect

        load_state_source = inspect.getsource(DatabaseAdapter.load_state)
        if 'cache_manager' in load_state_source:
            print("  ✓ DatabaseAdapter.load_state integrated")
        else:
            print("  ✗ DatabaseAdapter.load_state NOT integrated")
            return False

        get_artifacts_source = inspect.getsource(DatabaseAdapter.get_artifacts)
        if 'cache_manager' in get_artifacts_source:
            print("  ✓ DatabaseAdapter.get_artifacts integrated")
        else:
            print("  ✗ DatabaseAdapter.get_artifacts NOT integrated")
            return False

        # Check memory manager integration
        from src.memory.memory_manager import MemoryManager

        get_memory_source = inspect.getsource(MemoryManager.get_user_memory)
        if 'cache_manager' in get_memory_source:
            print("  ✓ MemoryManager.get_user_memory integrated")
        else:
            print("  ✗ MemoryManager.get_user_memory NOT integrated")
            return False

        # Check app.py integration
        from src.api.app import startup_event, shutdown_event

        startup_source = inspect.getsource(startup_event)
        if 'initialize_cache' in startup_source:
            print("  ✓ App startup integrated")
        else:
            print("  ✗ App startup NOT integrated")
            return False

        shutdown_source = inspect.getsource(shutdown_event)
        if 'shutdown_cache' in shutdown_source:
            print("  ✓ App shutdown integrated")
        else:
            print("  ✗ App shutdown NOT integrated")
            return False

        # Check health endpoint
        from src.api.routes.health import router
        routes = [route.path for route in router.routes]
        if '/cache' in routes:
            print("  ✓ Health cache endpoint added")
        else:
            print("  ✗ Health cache endpoint NOT added")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Integration check error: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking dependencies...")

    dependencies = {
        'redis': 'redis',
        'motor': 'motor',
        'pymongo': 'pymongo',
        'fastapi': 'fastapi',
        'pydantic': 'pydantic',
    }

    all_installed = True
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            all_installed = False

    return all_installed


def main():
    """Run all verification checks."""
    print("="*60)
    print("Cache Implementation Verification")
    print("="*60)

    checks = [
        ("Files Exist", check_files_exist),
        ("Imports", check_imports),
        ("Configuration", check_configuration),
        ("Dependencies", check_dependencies),
        ("Integration", check_integration),
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n✗ {check_name} check failed with error: {e}")
            results[check_name] = False

    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)

    all_passed = True
    for check_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n✓ All checks passed! Cache implementation is ready.")
        print("\nNext steps:")
        print("1. Start Redis: redis-server")
        print("2. Run tests: pytest tests/unit/test_cache/ -v")
        print("3. Start app: uvicorn src.api.app:app --reload")
        print("4. Check health: curl http://localhost:8000/api/v1/health/cache")
        return 0
    else:
        print("\n✗ Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
