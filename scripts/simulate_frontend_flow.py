import httpx
import time
import json
import sys
import asyncio

BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "dev-api-key-12345"
HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def log(msg, success=True):
    symbol = "✓" if success else "✗"
    print(f"{symbol} {msg}")

async def run_simulation():
    print("Starting Frontend Flow Simulation...")

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Health Check
        try:
            resp = await client.get(f"{BASE_URL}/health", headers=HEADERS)
            if resp.status_code == 200:
                log("Health Check Passed")
            else:
                log(f"Health Check Failed: {resp.status_code}", False)
                return False
        except Exception as e:
            log(f"Backend not reachable: {e}", False)
            return False

        # 2. Create Task
        print("\n[Task Creation]")
        payload = {
            "user_id": "usr_api_key_user",
            "goal": "Verify the system integrity by running a simulation."
        }
        try:
            resp = await client.post(f"{BASE_URL}/tasks", json=payload, headers=HEADERS)
            if resp.status_code == 201:
                task_data = resp.json()
                task_id = task_data["task_id"]
                log(f"Task Created: {task_id}")
            else:
                log(f"Task Creation Failed: {resp.text}", False)
                return False
        except Exception as e:
            log(f"Task Creation Error: {e}", False)
            return False

        # 3. Poll Status (Simulation)
        print(f"\n[Polling Status for {task_id}]")
        for _ in range(3):
            resp = await client.get(f"{BASE_URL}/tasks/{task_id}", headers=HEADERS)
            if resp.status_code == 200:
                status = resp.json()
                log(f"Current Status: {status['status']} | Progress: {status['progress']['percentage']}%")
            else:
                log(f"Status Poll Failed: {resp.text}", False)
            await asyncio.sleep(1)

        # 4. Pause Task
        print("\n[Pausing Task]")
        resp = await client.post(f"{BASE_URL}/tasks/{task_id}/pause", headers=HEADERS)
        if resp.status_code == 200:
            log("Task Paused Successfully")
        else:
            log(f"Pause Failed: {resp.text}", False)

        # 5. Resume Task
        print("\n[Resuming Task]")
        resume_payload = {"user_input": "Proceed with verification", "mode": "resume"}
        resp = await client.post(f"{BASE_URL}/tasks/{task_id}/continue", json=resume_payload, headers=HEADERS)
        if resp.status_code == 200:
            log("Task Resumed Successfully")
        else:
            log(f"Resume Failed: {resp.text}", False)

        # 6. Submit Feedback (Mock completion for feedback)
        print("\n[Submitting Feedback]")
        feedback_payload = {
            "rating": 5,
            "text_feedback": "System integrity looks good."
        }
        # Note: Feedback might fail if task isn't completed, but we check endpoint reachability
        resp = await client.post(f"{BASE_URL}/tasks/{task_id}/feedback", json=feedback_payload, headers=HEADERS)
        if resp.status_code in [201, 400, 403]: # 400/403 acceptable if task state prevents feedback
            log(f"Feedback Endpoint Reachable (Status: {resp.status_code})")
        else:
            log(f"Feedback Submission Failed completely: {resp.status_code}", False)

        # 7. Get User Memory
        print("\n[Fetching User Memory]")
        user_id = "usr_api_key_user"
        try:
            resp = await client.get(f"{BASE_URL}/memory/{user_id}", headers=HEADERS)
            if resp.status_code == 200:
                memory_data = resp.json()
                log(f"User Memory Retrieved: {len(memory_data.get('short_term', []))} short-term items")
            else:
                log(f"User Memory Fetch Failed: {resp.status_code} - {resp.text}", False)
        except Exception as e:
            log(f"User Memory Error: {e}", False)

        # 8. Get Mermaid Visualization
        print("\n[Fetching Mermaid Visualization]")
        try:
            resp = await client.get(f"{BASE_URL}/trace/task/{task_id}/visualization/mermaid", headers=HEADERS)
            if resp.status_code == 200:
                viz_data = resp.text
                if "graph TD" in viz_data:
                    log("Mermaid Visualization Retrieved Successfully")
                else:
                    log(f"Mermaid Visualization Invalid Content: {viz_data[:50]}...", False)
            else:
                log(f"Mermaid Visualization Failed: {resp.status_code} - {resp.text}", False)
        except Exception as e:
            log(f"Mermaid Visualization Error: {e}", False)

    print("\nSimulation Complete.")
    return True

if __name__ == "__main__":
    success = asyncio.run(run_simulation())
    sys.exit(0 if success else 1)
