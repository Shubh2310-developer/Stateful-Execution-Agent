# Antigravity Edge UI Patterns

For tasks running on local devices (IoT, edge servers, or browsers), Antigravity provides specialized "Edge UI" patterns that prioritize low-resource visibility and offline stability.

## 1. The "Edge Pulse" (Minimalist Widget)
- **Visual**: A tiny, persistent status dot or tray icon.
- **Function**: Shows the core "Heartbeat" (Running/Success/Error) without opening a full browser window.
- **Latency**: Sub-50ms status updates for local processes.

## 2. Local State Management
- **Offline Workspace**: The UI remains fully interactive even without an internet connection, allowing users to view cached traces and artifacts.
- **Sync Status**: A "Cloud Sync" icon showing the progress of syncing local state versions to the central MongoDB/S3 storage.
- **Conflict UI**: If a local state version conflicts with a cloud version, show a side-by-side [State Diff](./STATE_DIFF_VISUALIZATION.md) and ask the user to resolve.

## 3. Resource Constrained Views
- **Low-bandwidth Mode**: Automatically switches the Decision Trace to text-only (no avatars or complex icons) and disables high-res chart rendering.
- **CPU/RAM Guard**: An integrated gauge showing the impact of the local agent execution on the device's hardware.

## 4. Local Tool Interaction
- **Permission Popups**: Native OS notifications for local tool access (e.g., "Antigravity wants to read your local Downloads folder").
- **Local File Explorer**: A specialized artifact viewer optimized for interacting with files directly on the user's hard drive.

## 5. Edge Dashboard
- **Nearby Agents**: A view showing other agents running on the same local network (mDNS/Bonjour discovery).
- **Peer-to-peer Handoff**: Visualizing the transfer of a task state directly between two edge devices without hitting the cloud.
