# Antigravity Privacy Shield UX

Privacy Shield defines the UI patterns for handling sensitive data, redaction, and user privacy within the Antigravity platform.

## 1. Auto-Redaction Visibility
- **The "Blurred" State**: Sensitive PII (emails, keys, IDs) in the Decision Trace are blurred by default (`backdrop-blur-sm`).
- **"Click to Reveal"**: A persistent icon next to redacted data that requires an intentional click to view.
- **Redaction Logs**: A summary showing how many pieces of sensitive data the "Shield" has protected during a task.

## 2. Data Boundary UI
- **Internal vs. External Tints**: Use a subtle background tint (e.g., light purple) for views where the agent is interacting with "External/Public" data vs. "Internal/Private" data.
- **"Leak" Prevention Alerts**: If the agent attempts to send internal data to an external tool (e.g., posting a private KPI to a public Slack channel), a high-visibility warning appears.

## 3. User Privacy Controls
- **Incognito Task**: A mode where no traces or state snapshots are saved permanently (useful for one-off sensitive queries).
- **Memory Opt-out**: A toggle for each task: "Allow agent to learn from this task."
- **Self-Destruct Timer**: Configure artifacts and task logs to automatically delete after X hours.

## 4. Transparency of Access
- **"Who saw this?"**: A list of all users and agents that have accessed a specific artifact or state version.
- **Access Level Badges**: Clearly show if the user is in "Full Access" or "Redacted View" mode.

## 5. Secure Input Patterns
- **Secret Masks**: All API keys and credentials in forms are masked by default (`●●●●●●●●`).
- **One-time Inputs**: Allow users to provide a secret that is used for a single task and never saved to the database.
