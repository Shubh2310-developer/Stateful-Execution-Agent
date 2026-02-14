# Troubleshooting Guide

This guide covers common issues encountered when setting up or running the Stateful Execution Agent.

## Infrastructure Connectivity

### Cannot connect to MongoDB
- **Error:** `ServerSelectionTimeoutError` or `Connection refused`.
- **Solution:**
  - Ensure the MongoDB service is running (`docker ps` or `systemctl status mongodb`).
  - Verify the `MONGODB_URL` in your `.env` matches the correct host and port.
  - Check if the port 27017 is blocked by a firewall.

### Cannot connect to PostgreSQL
- **Error:** `OperationalError: could not connect to server`.
- **Solution:**
  - Verify the `POSTGRES_SERVER`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` in `.env`.
  - Ensure the database specified in `POSTGRES_DB` was created by running `scripts/setup/init_database.py`.

## LLM / Groq API Issues

### Authentication Failure
- **Error:** `LLMError: Groq API key is not configured` or `401 Unauthorized`.
- **Solution:**
  - Double-check the `GROQ_API_KEY` in your `.env` file.
  - Ensure the key has not expired or been revoked in the Groq console.

### Rate Limiting
- **Error:** `RateLimitError`.
- **Solution:**
  - Implement a delay between task creations.
  - Check your Groq usage limits and billing status.

## Execution Failures

### Step Validation Failed
- **Description:** The agent completed a step, but the output did not meet the success criteria.
- **Action:**
  - Review the Decision Trace (`GET /trace/{task_id}`) to see why the output was deemed insufficient.
  - You can use the `Continue Task` endpoint with `user_input` to provide more guidance to the agent.

### Tool Not Found
- **Error:** `ToolError: No tool found for action: X`.
- **Solution:**
  - Verify the tool is registered in the `tool_registry`.
  - Check if the tool name in the generated plan matches the registered tool name.
