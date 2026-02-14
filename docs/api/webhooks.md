# Webhooks and Async Notifications

The Stateful Execution Agent supports webhooks to notify external systems of task events.

## Configuration

To enable webhooks, set the following environment variables:
- `WEBHOOK_URL`: The endpoint to send POST requests to.
- `WEBHOOK_SECRET`: A secret key for signing requests.

## Event Types

The agent emits the following events:

### `task.planned`
Emitted when the initial plan for a goal is generated and validated.

### `step.completed`
Emitted after each successful step execution and validation.

### `task.completed`
Emitted when the final goal is achieved and all artifacts are produced.

### `task.failed`
Emitted when an unrecoverable error occurs or validation fails repeatedly.

## Payload Schema

```json
{
  "event_id": "evt_123",
  "event_type": "task.completed",
  "timestamp": "2024-02-14T12:00:00Z",
  "data": {
    "task_id": "task_abc",
    "status": "completed",
    "artifacts": ["art_1", "art_2"]
  },
  "signature": "hmac-sha256-..."
}
```

## Security

Webhooks include an `X-Agent-Signature` header calculated using HMAC-SHA256 with the `WEBHOOK_SECRET`. Receivers should verify this signature to ensure authenticity.
