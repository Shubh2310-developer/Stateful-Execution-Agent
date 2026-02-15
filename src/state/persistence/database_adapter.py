from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING
from src.core.config import settings
from src.state.state_schema import TaskStateSchema
from src.core.types import Artifact
from src.utils.logger import logger
from src.cache.redis_cache import cache_manager
import time

class DatabaseAdapter:
    """Adapter for persisting task state, versions, and artifacts to MongoDB."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
        self.db = self.client[settings.database.mongodb_db]

        # Collections
        self.tasks = self.db.tasks
        self.versions = self.db.task_versions
        self.artifacts = self.db.artifacts
        self.traces = self.db.trace
        self.decisions = self.db.decisions

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

            # Trace indexes
            await self.traces.create_index([("task_id", ASCENDING), ("timestamp", ASCENDING)])
            await self.traces.create_index([("tags", ASCENDING)])
            # TTL for traces (30 days)
            await self.traces.create_index([("timestamp", ASCENDING)], expireAfterSeconds=2592000)

            # Decision indexes
            # Primary query: Get all decisions for task X, sorted by step/time
            await self.decisions.create_index([("task_id", ASCENDING), ("step_id", ASCENDING), ("timestamp", ASCENDING)])
            # Analytics: Low confidence
            await self.decisions.create_index([("confidence_score", ASCENDING)])
            # Filtering by tag
            await self.decisions.create_index([("tags", ASCENDING)])
            # TTL for decisions (30 days)
            await self.decisions.create_index([("timestamp", ASCENDING)], expireAfterSeconds=2592000)

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
                    state_dict = state.model_dump()
                    state_dict["updated_at"] = datetime.now(timezone.utc)

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
                            "created_at": datetime.now(timezone.utc)
                        }
                        await self.versions.insert_one(version_doc, session=session)

            # Invalidate cache after successful save
            try:
                await cache_manager.invalidate_task(state.task_id)
            except Exception as e:
                logger.warning(f"Failed to invalidate cache for task {state.task_id}: {str(e)}")

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
            state_dict = state.model_dump()
            state_dict["updated_at"] = datetime.now(timezone.utc)

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
                    "created_at": datetime.now(timezone.utc)
                }
                await self.versions.insert_one(version_doc)

            # Invalidate cache after successful save
            try:
                await cache_manager.invalidate_task(state.task_id)
            except Exception as e:
                logger.warning(f"Failed to invalidate cache for task {state.task_id}: {str(e)}")

            return True
        except Exception as e:
            logger.error(f"Sequential save failed: {str(e)}")
            return False

    async def load_state(self, task_id: str) -> Optional[TaskStateSchema]:
        logger.debug(f"Loading state for task {task_id}")

        # Try cache first
        cache_key = f"{cache_manager.PREFIX_TASK_STATE}{task_id}"
        start_time = time.time()

        try:
            cached_data = await cache_manager.get(cache_key)
            if cached_data:
                query_time = (time.time() - start_time) * 1000
                logger.debug(f"Cache HIT for task state {task_id} ({query_time:.2f}ms)")
                # Reconstruct TaskStateSchema from cached dict
                return TaskStateSchema(**cached_data)
        except Exception as e:
            logger.warning(f"Cache error for task {task_id}: {str(e)}")

        # Cache miss - query database
        start_time = time.time()
        try:
            doc = await self.tasks.find_one({"task_id": task_id})
            query_time = (time.time() - start_time) * 1000
            logger.debug(f"Database query for task state {task_id} ({query_time:.2f}ms)")

            if doc:
                state = TaskStateSchema(**doc)

                # Cache the result with timestamp
                try:
                    await cache_manager.set(
                        cache_key,
                        state.model_dump(),
                        last_modified=state.updated_at
                    )
                except Exception as e:
                    logger.warning(f"Failed to cache task state {task_id}: {str(e)}")

                return state
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
                {"$set": artifact.model_dump()},
                upsert=True
            )

            # Invalidate artifacts cache for this task
            try:
                await cache_manager.delete(f"{cache_manager.PREFIX_TASK_ARTIFACTS}{artifact.task_id}")
            except Exception as e:
                logger.warning(f"Failed to invalidate artifacts cache: {str(e)}")

            return True
        except Exception as e:
            logger.error(f"Failed to register artifact: {str(e)}")
            return False

    async def get_artifacts(self, task_id: str) -> List[Artifact]:
        """Retrieves all artifacts for a task."""
        logger.debug(f"Getting artifacts for task {task_id}")

        # Try cache first
        cache_key = f"{cache_manager.PREFIX_TASK_ARTIFACTS}{task_id}"
        start_time = time.time()

        try:
            cached_data = await cache_manager.get(cache_key)
            if cached_data:
                query_time = (time.time() - start_time) * 1000
                logger.debug(f"Cache HIT for task artifacts {task_id} ({query_time:.2f}ms)")
                # Reconstruct Artifact objects from cached list
                return [Artifact(**item) for item in cached_data]
        except Exception as e:
            logger.warning(f"Cache error for artifacts {task_id}: {str(e)}")

        # Cache miss - query database
        start_time = time.time()
        try:
            cursor = self.artifacts.find({"task_id": task_id})
            results = await cursor.to_list(length=100)
            query_time = (time.time() - start_time) * 1000
            logger.debug(f"Database query for task artifacts {task_id} ({query_time:.2f}ms)")

            artifacts = [Artifact(**doc) for doc in results]

            # Cache the results
            try:
                await cache_manager.set(
                    cache_key,
                    [art.model_dump() for art in artifacts]
                )
            except Exception as e:
                logger.warning(f"Failed to cache artifacts for {task_id}: {str(e)}")

            return artifacts
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
