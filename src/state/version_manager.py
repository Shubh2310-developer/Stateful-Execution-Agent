from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from src.state.state_schema import TaskStateSchema
from src.state.persistence.database_adapter import DatabaseAdapter
from src.utils.logger import logger

class VersionManager:
    """Manages snapshots and history of task states for rollback and auditing."""

    def __init__(self, db_adapter: DatabaseAdapter):
        self.db_adapter = db_adapter

    async def create_snapshot(self, state: TaskStateSchema, summary: str = "Manual snapshot") -> bool:
        """Explicitly creates a milestone snapshot of the current state."""
        logger.debug(f"Creating explicit snapshot for task {state.task_id}")
        return await self.db_adapter.save_state(state, is_milestone=True, summary=summary)

    async def get_history(self, task_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves historical versions for a task."""
        logger.debug(f"Retrieving history for task {task_id}")
        return await self.db_adapter.get_state_history(task_id, limit=limit)

    async def rollback(self, task_id: str, to_version: int) -> Optional[TaskStateSchema]:
        """
        Rolls back the task state to a specific version number.
        This updates the 'tasks' collection with the snapshot from 'task_versions'.
        """
        logger.info(f"Rolling back task {task_id} to version {to_version}")

        # 1. Fetch the historical snapshot
        version_doc = await self.db_adapter.versions.find_one(
            {"task_id": task_id, "version": to_version}
        )

        if not version_doc:
            logger.error(f"Version {to_version} not found for task {task_id}")
            return None

        # 2. Restore the state in the main collection
        snapshot_data = version_doc["snapshot"]
        state = TaskStateSchema(**snapshot_data)

        success = await self.db_adapter.save_state(
            state,
            is_milestone=True,
            summary=f"Rollback to version {to_version}"
        )

        if success:
            return state
        return None

    async def prune_old_versions(self, days_old: int = 30) -> int:
        """
        Manually prune old versions.
        Note: DatabaseAdapter setup_indexes creates a TTL index for auto-pruning non-milestones.
        This provides explicit control for all version types.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        logger.info(f"Pruning versions older than {cutoff_date}")

        # Prune versions older than cutoff, preserving milestones if needed
        # (Though Phase 3.3 says prune old versions, usually milestones are kept longer)
        # For simplicity, we prune anything older than the cutoff.
        result = await self.db_adapter.versions.delete_many({
            "created_at": {"$lt": cutoff_date}
        })

        logger.info(f"Pruned {result.deleted_count} old versions")
        return result.deleted_count
