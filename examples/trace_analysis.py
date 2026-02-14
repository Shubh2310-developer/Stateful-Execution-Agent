import asyncio
import httpx
import json

async def main():
    base_url = "http://localhost:8000/api/v1"
    task_id = "task_example_123" # Replace with a real task ID

    print(f"--- Analyzing Decision Trace for Task {task_id} ---")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/trace/{task_id}")
            if response.status_code == 404:
                print(f"Task {task_id} not found. Run basic_task_creation.py first.")
                return

            trace_data = response.json()
            decisions = trace_data.get("decisions", [])

            print(f"Total decisions recorded: {len(decisions)}")

            for i, dec in enumerate(decisions):
                print(f"\nDecision {i+1}: {dec.get('decision_point')}")
                print(f"Rationale: {dec.get('reasoning')}")
                print(f"Choice: {dec.get('choice_made')}")
                print(f"Confidence: {dec.get('confidence')}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
