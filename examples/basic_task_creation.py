import asyncio
import httpx
import json

async def main():
    base_url = "http://localhost:8000/api/v1"

    # 1. Create a new task
    print("--- Creating Task ---")
    task_data = {
        "user_id": "usr_demo_123",
        "goal": "Research the latest trends in autonomous agents and summarize them in a brief report.",
        "execution_mode": "autonomous"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/tasks/create", json=task_data)
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return

        task = response.json()
        task_id = task.get("task_id")
        print(f"Task created: {task_id}")
        print(f"Initial Status: {task.get('status')}")

        # 2. Poll for status
        print("\n--- Polling Status ---")
        for _ in range(5):
            status_response = await client.get(f"{base_url}/tasks/{task_id}/status")
            status_data = status_response.json()
            print(f"Status: {status_data.get('status')} | Progress: {status_data.get('progress', {}).get('percentage')}%")

            if status_data.get("status") in ["completed", "failed"]:
                break
            await asyncio.sleep(2)

        # 3. List artifacts
        print("\n--- Listing Artifacts ---")
        artifacts_response = await client.get(f"{base_url}/artifacts/task/{task_id}")
        artifacts = artifacts_response.json()
        print(f"Produced {len(artifacts)} artifacts.")
        for art in artifacts:
            print(f"- {art.get('artifact_id')}: {art.get('type')} ({art.get('format')})")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Failed to connect to server: {e}")
