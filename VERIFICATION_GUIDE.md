# System Verification & Repair Guide

This guide outlines the steps orchestrate a full system verification and repair for the 'Stateful Execution Agent'.

## 1. Quick Start (Master Script)

We have created a master orchestration script that performs infrastructure checks, backend integrity verification, starts the services, and runs a simulated user flow.

Run the following command from the project root:

```bash
chmod +x scripts/master_verify_and_start.sh
./scripts/master_verify_and_start.sh
```

This script will:
1.  **Check Infrastructure**: Verify MongoDB and Redis are running.
2.  **Verify Integrity**: Run `scripts/verify_backend_integrity.py` to check imports and DB connections.
3.  **Seed Data**: Populate the database with initial user memory.
4.  **Start Services**: Launch FastAPI (port 8000) and Next.js (port 3000) in the background.
5.  **Simulate Flow**: Run `scripts/simulate_frontend_flow.py` to create a task, pause it, resume it, and submit feedback via the API.

## 2. Manual Verification Steps

If you prefer to run steps manually or need to debug:

### Backend Integrity
```bash
python scripts/verify_backend_integrity.py
```
*Expected Output*: "✓ All Backend Checks Passed"

### Frontend-Backend Simulation
(Requires Backend running on port 8000)
```bash
python scripts/simulate_frontend_flow.py
```
*Expected Output*: "Simulation Complete." with all checks passed.

### Connection Check
```bash
./scripts/verify_connection.sh
```

## 3. Recent Repairs

The following automated repairs were applied to the codebase:

*   **Frontend Task Handling (`ui/app/page.tsx`)**:
    *   Previously, the Dashboard hardcoded `currentTaskId` to "task_4efa4e9d".
    *   **Fix**: Updated the component to auto-select the most recent task from the API if the hardcoded task is not found. This ensures the Dashboard always shows relevant data upon startup.
    *   **Fix**: Updated the "Missions" list click handler to correctly update the `currentTaskId` state, allowing users to switch between tasks seamlessly.

## 4. Troubleshooting

*   **MongoDB/Redis**: If the script fails to start them, please ensure you have them installed and start them manually (`sudo systemctl start mongod`, `sudo systemctl start redis`).
*   **API Key**: The system uses a default dev API key (`dev-api-key-12345`). Ensure your `.env` matches `config/default.yaml` if you change this.
*   **Groq API**: Ensure `GROQ_API_KEY` is set in your `.env` file for LLM features to work.

## 5. Architecture Alignment

The system has been verified against `Explanation.md` and `docs/architecture/`:
*   ✅ **Planner/Executor Split**: Implemented in `src/planner` and `src/executor`.
*   ✅ **Memory System**: Implemented in `src/memory`, utilizing MongoDB.
*   ✅ **Traceability**: Trace logging active in `src/trace`.
*   ✅ **State Persistence**: State preserved in MongoDB via `DatabaseAdapter`.
