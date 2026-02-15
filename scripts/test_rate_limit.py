
import asyncio
import httpx
import time
import os

# Configuration
BASE_URL = "http://localhost:8001"
API_KEY = "dev-api-key-12345" # Default from ui/lib/api.ts. Adjust if needed.
# Ensure we map endpoints that are actually rate limited
ENDPOINTS = [
    "/api/v1/health",
]
REQUESTS_TO_MAKE = 100 # Increased to test higher limits if needed, but 50 is fine for connectivitycheck
REQUESTS_TO_MAKE = 50
CONCURRENCY = 5

async def make_request(client, endpoint, i):
    try:
        start = time.time()
        headers = {'X-API-KEY': API_KEY}
        response = await client.get(endpoint, headers=headers)
        duration = time.time() - start
        
        status = response.status_code
        print(f"Req {i}: {endpoint} -> {status} ({duration:.3f}s)")
        return status
    except Exception as e:
        print(f"Req {i}: {endpoint} -> Error: {e}")
        return 0

async def main():
    print(f"Testing rate limits on {BASE_URL}...")
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        # First verify server is up
        try:
            await client.get("/docs", headers={'X-API-KEY': API_KEY})
            print("Server is reachable.")
        except Exception:
            print("Server is NOT reachable on port 8001. Trying 8000...")
            client.base_url = "http://localhost:8000"
            try:
                await client.get("/docs", headers={'X-API-KEY': API_KEY})
                print("Server is reachable on 8000.")
            except:
                print("Server is not reachable.")
                return

        tasks = []
        for i in range(REQUESTS_TO_MAKE):
            endpoint = ENDPOINTS[i % len(ENDPOINTS)]
            tasks.append(make_request(client, endpoint, i))
            if len(tasks) >= CONCURRENCY:
                 await asyncio.gather(*tasks)
                 tasks = []
        
        if tasks:
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
