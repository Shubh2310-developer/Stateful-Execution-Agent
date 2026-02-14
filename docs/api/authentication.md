# Authentication and Security

The Stateful Execution Agent API uses Bearer Token authentication to secure its endpoints.

## Authentication Flow

1.  **Clients must include** an `Authorization` header with every request:
    `Authorization: Bearer <token>`

2.  **Token Validation** is handled in `src/api/dependencies/auth.py`.

## Current Implementation (Development)

In the current development state:
- A placeholder token `demo-token-123` maps to a demo user.
- If `DEBUG=true` is set in `.env`, any token will be accepted and map to `usr_dev_user`.

## Production Hardening

To secure the agent for production:

1.  **Implement JWT Validation**: Update `get_current_user` in `src/api/dependencies/auth.py` to decode and verify JSON Web Tokens from your identity provider (e.g., Auth0, Keycloak, or a custom service).

2.  **Enable Rate Limiting**: Configure the `RateLimiter` in `src/api/middleware/rate_limiting.py` to prevent abuse.

3.  **Scope Permissions**: Implement Role-Based Access Control (RBAC) to ensure users can only access their own tasks and artifacts.

## API Security

- **TLS**: Always serve the API over HTTPS in production.
- **CORS**: Restrict the `allow_origins` in `src/api/app.py` to your trusted domains.
- **Input Validation**: All request bodies are validated using Pydantic models in `src/api/schemas/`.
