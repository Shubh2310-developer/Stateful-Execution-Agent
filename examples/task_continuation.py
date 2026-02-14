import asyncio
import httpx

async def main():
    base_url = "http://localhost:8000/api/v1"
    task_id = "task_example_123" # Replace with a real task ID from basic_task_creation.py

    print(f"--- Continuing Task {task_id} ---")
    update_data = {
        "user_input": "Please ensure the report includes a section on multi-agent collaboration.",
        "mode": "resume"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/tasks/{task_id}/continue", json=update_data)
        if response.status_code == 404:
            print(f"Task {task_id} not found. Run basic_task_creation.py first and copy the ID.")
            return

        result = response.json()
        print(f"Resumption Status: {result.get('status')}")
        print(f"New Progress: {result.get('progress', {}).get('percentage')}%")

if __name__ == "__main__":
    asyncio.run(main())
