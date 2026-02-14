from typing import Any, Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING
from src.core.config import settings
from src.state.state_schema import TaskStateSchema
from src.core.types import Artifact
from src.utils.logger import logger

class DatabaseAdapter:
    """Adapter for persisting task state, versions, and artifacts to MongoDB."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
        self.db = self.client[settings.database.mongodb_db]

        # Collections
        self.tasks = self.db.tasks
        self.versions = self.db.task_versions
        self.artifacts = self.db.artifacts

    async def setup_indexes(self):
        """Initialize indexes for performance and data integrity."""
        logger.info("Setting up database indexes")
        try:
            # Task indexes
            await self.tasks.create_index([("task_id", ASCENDING)], unique=True)
            await self.tasks.create_index([("user_id", ASCENDING), ("status", ASCENDING)])

            # Version indexes
            await self.versions.create_index([("task_id", ASCENDING), ("version", DESCENDING)])
            # TTL Index: Automatically remove non-milestone versions after 30 days
            await self.versions.create_index(
                [("created_at", ASCENDING)],
                expireAfterSeconds=2592000,
                partialFilterExpression={"event_type": {"$ne": "milestone"}}
            )

            # Artifact indexes
            await self.artifacts.create_index([("artifact_id", ASCENDING)], unique=True)
            await self.artifacts.create_index([("task_id", ASCENDING)])
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Failed to setup indexes: {str(e)}")

    async def save_state(self, state: TaskStateSchema, is_milestone: bool = False, summary: Optional[str] = None) -> bool:
        """
        Saves task state with versioning. If is_milestone is True, a snapshot is preserved.
        """
        logger.debug(f"Saving state for task {state.task_id} (version: {state.version_counter})")

        try:
            # We use a session for atomicity if the deployment supports transactions (Replica Sets)
            # Falling back to sequential updates if transactions are unavailable
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    # 1. Update current state and increment version
                    state_dict = state.dict()
                    state_dict["updated_at"] = datetime.utcnow()

                    # Exclude version_counter from $set to avoid conflict with $inc
                    if "version_counter" in state_dict:
                        del state_dict["version_counter"]

                    result = await self.tasks.find_one_and_update(
                        {"task_id": state.task_id},
                        {
                            "$set": state_dict,
                            "$inc": {"version_counter": 1}
                        },
                        upsert=True,
                        return_document=True,
                        session=session
                    )

                    # 2. If it's a milestone or explicitly requested, create a snapshot
                    if is_milestone:
                        version_doc = {
                            "task_id": state.task_id,
                            "version": result["version_counter"],
                            "snapshot": state_dict,
                            "event_type": "milestone",
                            "summary": summary or "State snapshot at milestone",
                            "created_at": datetime.utcnow()
                        }
                        await self.versions.insert_one(version_doc, session=session)
            return True
        except Exception as e:
            # Handle cases where transactions might not be supported (e.g. standalone Mongo)
            if "Transaction" in str(e) or "sessions" in str(e).lower():
                logger.warning("Transactions not supported, falling back to sequential update")
                return await self._save_state_sequential(state, is_milestone, summary)

            logger.error(f"Failed to save state to database: {str(e)}")
            return False

    async def _save_state_sequential(self, state: TaskStateSchema, is_milestone: bool, summary: Optional[str]) -> bool:
        """Fallback for environments without transaction support."""
        try:
            state_dict = state.dict()
            state_dict["updated_at"] = datetime.utcnow()

            # Exclude version_counter from $set to avoid conflict with $inc
            if "version_counter" in state_dict:
                del state_dict["version_counter"]

            result = await self.tasks.find_one_and_update(
                {"task_id": state.task_id},
                {
                    "$set": state_dict,
                    "$inc": {"version_counter": 1}
                },
                upsert=True,
                return_document=True
            )

            if is_milestone:
                version_doc = {
                    "task_id": state.task_id,
                    "version": result["version_counter"],
                    "snapshot": state_dict,
                    "event_type": "milestone",
                    "summary": summary or "State snapshot at milestone",
                    "created_at": datetime.utcnow()
                }
                await self.versions.insert_one(version_doc)
            return True
        except Exception as e:
            logger.error(f"Sequential save failed: {str(e)}")
            return False

    async def load_state(self, task_id: str) -> Optional[TaskStateSchema]:
        logger.debug(f"Loading state for task {task_id} from database")
        try:
            doc = await self.tasks.find_one({"task_id": task_id})
            if doc:
                return TaskStateSchema(**doc)
            return None
        except Exception as e:
            logger.error(f"Failed to load state from database: {str(e)}")
            return None

    async def get_state_history(self, task_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves historical versions for a task."""
        try:
            cursor = self.versions.find({"task_id": task_id}).sort("version", DESCENDING).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Failed to retrieve state history: {str(e)}")
            return []

    async def register_artifact(self, artifact: Artifact) -> bool:
        """Registers artifact metadata in the database."""
        try:
            await self.artifacts.update_one(
                {"id": artifact.id},
                {"$set": artifact.dict()},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to register artifact: {str(e)}")
            return False

    async def get_artifacts(self, task_id: str) -> List[Artifact]:
        """Retrieves all artifacts for a task."""
        try:
            cursor = self.artifacts.find({"task_id": task_id})
            results = await cursor.to_list(length=100)
            return [Artifact(**doc) for doc in results]
        except Exception as e:
            logger.error(f"Failed to retrieve artifacts: {str(e)}")
            return []

    async def delete_state(self, task_id: str) -> bool:
        logger.info(f"Deleting state, versions, and artifacts for task {task_id}")
        try:
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    await self.tasks.delete_one({"task_id": task_id}, session=session)
                    await self.versions.delete_many({"task_id": task_id}, session=session)
                    await self.artifacts.delete_many({"task_id": task_id}, session=session)
            return True
        except Exception as e:
            # Fallback for non-transactional environments
            await self.tasks.delete_one({"task_id": task_id})
            await self.versions.delete_many({"task_id": task_id})
            await self.artifacts.delete_many({"task_id": task_id})
            return True
