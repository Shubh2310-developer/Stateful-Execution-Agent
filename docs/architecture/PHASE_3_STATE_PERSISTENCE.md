# Phase 3: State Management & Persistence

This phase focuses on how the agent maintains its "brain" across sessions, ensuring that no work is lost and that every transition is auditable.

## Goals
- Implement the primary state database (MongoDB).
- Create atomic state transition logic.
- Implement state versioning and snapshots.
- Set up the artifact metadata storage.

## 3.1 Database Layer (`src/state/persistence/database_adapter.py`)
- **Primary DB**: MongoDB (chosen for JSON-native storage and schema flexibility).
- **Library**: `Motor` (async driver for MongoDB).
- **Implementation**:
    - Connection pooling and lifecycle management.
    - `save_state(task_id, state_data)`: Upsert state.
    - `load_state(task_id)`: Retrieve current state.
    - `get_state_history(task_id)`: Retrieve previous versions.

## 3.2 State Manager (`src/state/state_manager.py`)
- **Implementation**:
    - High-level interface for orchestration layer.
    - Logic to increment version numbers on every significant update.
    - Differential updates (optional): Update only changed fields to minimize DB write load.
    - State checksumming: Ensure state integrity before and after persistence.

## 3.3 Versioning Logic (`src/state/version_manager.py`)
- **Implementation**:
    - Implement the "Time Travel" capability.
    - Snapshot management: Keep full copies of state at key milestones (e.g., step completion).
    - Cleanup policy: Logic to prune old versions after a configurable retention period (e.g., 30 days).

## 3.4 Artifact Registry (`src/executor/artifact_manager.py`)
- **Implementation**:
    - Track metadata for all files/data produced by tools.
    - Map `artifact_id` to storage URIs (S3, Local).
    - Support for artifact categorization (Document, Data, Image).
    - Integrity checks: Store hashes of artifacts to detect tampering or corruption.

## 3.5 Serialization (`src/state/serialization/json_serializer.py`)
- **Implementation**:
    - Custom Pydantic to JSON serialization.
    - Handling of complex types (datetimes, UUIDs, Enums).
    - Optional compression for large state objects to save storage costs.

## Verification Criteria
- [ ] Successfully save and retrieve a complex `TaskState` object from MongoDB.
- [ ] Verify that version numbers increment correctly on subsequent saves.
- [ ] Artifact manager correctly tracks a simulated file output.
- [ ] State validation fails if mandatory fields (e.g., `task_id`) are missing.
- [ ] "Rollback" function successfully restores state to version `N-1`.
