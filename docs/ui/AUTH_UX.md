# Antigravity Auth & Session UX

Security is foundational to the Antigravity experience. This document defines the patterns for authentication, session management, and secure access.

## 1. Authentication Flow
- **Professional Login**: A clean, minimalist login screen with high-contrast typography.
- **Multi-Factor Authentication (MFA)**: Support for TOTP (Google Authenticator) or WebAuthn (Passkeys) for enterprise environments.
- **SSO Integration**: One-click login for Google, GitHub, or Enterprise SAML providers.

## 2. Session Security
- **Inactivity Timeout**: Configurable auto-logout after X minutes of inactivity.
- **Active Session Management**: A view in Settings where users can see and "Sign Out" of other active devices.
- **Session Persistence**: Since tasks are long-running, the user's *identity* must remain secure even if the *task execution* continues in the background.

## 3. Scoped Permissions
- **Admin vs. Operator**: Clear visual distinction in the UI for administrative vs. operational accounts.
- **Temporary Access**: Allow admins to grant "Viewer-only" access to a specific task for a limited time (e.g., 24 hours).

## 4. Credential Management (The Vault)
- **Secrets Visibility**: API keys and connection strings are masked by default (`********`).
- **Secret Reveal**: Requires a second confirmation or re-authentication to "View" a secret.
- **Audit Log**: Every time a secret is accessed or modified, it is recorded in the system audit log.

## 5. Security Onboarding
- **First-time Auth**: Guide the user to set up MFA immediately upon first login.
- **Password Strength**: Real-time feedback on password complexity during account creation.
- **Privacy Policy**: A clear, readable summary of how user data and task logs are handled.
