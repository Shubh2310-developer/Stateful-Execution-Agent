# Getting Started with Stateful Execution Agent

This guide will help you set up and run the Stateful Execution Agent on your local machine.

## Prerequisites

- Python 3.10 or higher
- MongoDB Atlas account (for state management)
- Supabase account (for relational data)
- Groq API Key (get one at [console.groq.com](https://console.groq.com))

## Database Setup

### MongoDB Atlas
1. Create a free cluster on MongoDB Atlas.
2. Under "Database Access", create a user with read/write permissions.
3. Under "Network Access", allow your current IP address (or `0.0.0.0/0` for all).
4. Get your connection string from Cluster -> Connect -> Connect your application.

### Supabase
1. Create a new project on Supabase.
2. Go to Settings -> Database to find your connection string and credentials.
3. Note your database password as it's needed for the URI.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd stateful-execution-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Copy the example environment file and edit it with your Groq API key:
    ```bash
    cp .env.example .env
    ```

## Initializing and Running the System

The easiest way to initialize the database and start the system is to use the master verification script. This script handles:
1. Infrastructure checks (MongoDB, Redis)
2. Backend integrity verification
3. Database seeding
4. Starting the Backend API
5. Starting the Frontend UI

```bash
chmod +x scripts/master_verify_and_start.sh
./scripts/master_verify_and_start.sh
```

The system will be available at:
- Frontend: `http://localhost:3000`
- Backend API docs: `http://localhost:8000/api/v1/docs`

## Manual Initialization (Advanced)

If you prefer to run steps manually:

1. **Initialize Database**:
   ```bash
   PYTHONPATH=. python scripts/setup/seed_data.py
   ```

2. **Start Backend**:
   ```bash
   uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Start Frontend**:
   ```bash
   npm run dev
   ```

## Running Your First Task

You can use the provided example script to create your first autonomous task:

```bash
python examples/basic_task_creation.py
```

This will create a task, poll for its status as it moves through planning and execution, and display the final artifacts produced.
