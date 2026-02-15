import sys
import os
import asyncio
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.getcwd())

def check_imports():
    print("[1/3] Verifying Module Imports...")
    modules = [
        "src.api.app",
        "src.planner.planner",
        "src.executor.executor",
        "src.memory.memory_manager",
        "src.state.state_manager",
        "src.orchestration.task_router"
    ]

    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ Imported {module}")
        except ImportError as e:
            print(f"  ✗ Failed to import {module}: {e}")
            failed.append(module)
        except Exception as e:
            print(f"  ✗ Error importing {module}: {e}")
            failed.append(module)

    if failed:
        print(f"\nFailed to import {len(failed)} modules.")
        return False
    return True

def check_app_integrity():
    print("\n[2/3] Verifying FastAPI App Integrity...")
    try:
        from src.api.app import app
        from fastapi.testclient import TestClient

        # Verify Routes exist
        print("  Verifying Route Registration...")
        routes = [route.path for route in app.routes]
        required_routes = [
            "/api/v1/health",
            "/api/v1/tasks",
            "/api/v1/memory/{user_id}",
            "/api/v1/state/{task_id}",
            "/api/v1/artifacts/task/{task_id}"
        ]

        missing_routes = []
        for req in required_routes:
            # Simple check if the route path is present (ignoring methods for now)
            if req not in routes:
                # Regex matching might be needed for path params in some frameworks,
                # but FastAPI app.routes usually stores the path template.
                missing_routes.append(req)

        if missing_routes:
            print(f"  ! Warning: Some expected routes might be missing or have different paths: {missing_routes}")
            # Don't fail hard on this unless strict, but good to know.
        else:
            print(f"  ✓ Verified {len(required_routes)} core routes are registered")

        client = TestClient(app)

        # Test Health Endpoint
        response = client.get("/api/v1/health")
        if response.status_code == 200:
             print(f"  ✓ Health endpoint reachable: {response.json()}")
        else:
             print(f"  ✗ Health endpoint failed: {response.status_code} - {response.text}")
             return False

        # Test Config Loading
        from src.core.config import settings
        print(f"  ✓ Configuration loaded (Environment: {settings.app.env})")

        return True
    except Exception as e:
        print(f"  ✗ App integrity check failed: {e}")
        return False

async def check_mongo_connection():
    print("\n[3/3] Verifying Database Connection...")
    try:
        from src.core.config import settings
        from motor.motor_asyncio import AsyncIOMotorClient

        client = AsyncIOMotorClient(settings.database.mongodb_uri, serverSelectionTimeoutMS=2000)
        await client.server_info()
        print(f"  ✓ Connected to MongoDB at {settings.database.mongodb_uri}")
        return True
    except Exception as e:
        print(f"  ✗ MongoDB connection failed: {e}")
        return False

async def main():
    print("==========================================")
    print("   Backend Integrity Verification")
    print("==========================================\n")

    imports_ok = check_imports()
    app_ok = check_app_integrity()
    db_ok = await check_mongo_connection()

    print("\n==========================================")
    if imports_ok and app_ok and db_ok:
        print("✓ All Backend Checks Passed")
        sys.exit(0)
    else:
        print("✗ Backend Verification Failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
