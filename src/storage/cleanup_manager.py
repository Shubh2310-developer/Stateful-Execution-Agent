import os
import time
from typing import Optional
from src.utils.logger import logger
from src.storage.artifact_store import ArtifactStore

class CleanupManager:
    """Manages the lifecycle and cleanup of temporary artifacts."""

    def __init__(self, store: Optional[ArtifactStore] = None, max_age_days: int = 30):
        self.store = store or ArtifactStore()
        # Access the backend's base_dir if it's LocalStorage
        if hasattr(self.store.backend, "base_dir"):
            self.base_dir = self.store.backend.base_dir
        else:
            self.base_dir = "data/artifacts"
        self.max_age_seconds = max_age_days * 24 * 60 * 60

    def cleanup_old_artifacts(self):
        """Deletes artifacts older than the maximum age."""
        logger.info(f"Starting artifact cleanup in {self.base_dir}...")
        now = time.time()
        count = 0

        if not os.path.exists(self.base_dir):
            return

        for root, dirs, files in os.walk(self.base_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_age = os.path.getmtime(file_path)

                if now - file_age > self.max_age_seconds:
                    try:
                        os.remove(file_path)
                        count += 1
                        logger.debug(f"Deleted old artifact: {file_path}")
                    except Exception as e:
                        logger.error(f"Failed to delete {file_path}: {e}")

        logger.info(f"Cleanup complete. Removed {count} artifacts.")
