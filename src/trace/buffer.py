import asyncio
import atexit
import time
from typing import List, Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from src.utils.logger import logger

class AsyncTraceBuffer:
    """
    Asynchronous buffer for high-volume trace logging.
    Implements a Producer-Consumer pattern to prevent database writes from blocking
    the main execution loop.
    """

    def __init__(self, collection: AsyncIOMotorCollection, batch_size: int = 50, flush_interval: float = 2.0, max_buffer_size: int = 1000):
        self.collection = collection
        self._queue: Optional[asyncio.Queue] = None
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._max_buffer_size = max_buffer_size
        self._stop_event = asyncio.Event()
        self._worker_task: Optional[asyncio.Task] = None

    @property
    def queue(self) -> asyncio.Queue:
        if self._queue is None:
            self._queue = asyncio.Queue(maxsize=self._max_buffer_size)
        return self._queue

    async def start(self):
        """Starts the background worker task."""
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker_loop())
            logger.info(f"AsyncTraceBuffer started for collection: {self.collection.name}")

    async def stop(self):
        """Stops the worker and flushes remaining items."""
        self._stop_event.set()
        if self._worker_task:
            await self._worker_task

    async def add(self, document: Dict[str, Any]):
        """Adds a document to the buffer (non-blocking)."""
        if self._worker_task is None:
             await self.start()

        try:
            self.queue.put_nowait(document)
        except asyncio.QueueFull:
            logger.warning("Trace buffer full, dropping trace to prevent blocking")

    async def _worker_loop(self):
        batch = []
        last_flush = time.time()

        while not self._stop_event.is_set():
            try:
                # Wait for item with timeout
                try:
                    # calculated timeout to meet flush_interval
                    timeout = max(0.1, self._flush_interval - (time.time() - last_flush))
                    item = await asyncio.wait_for(self.queue.get(), timeout=timeout)
                    batch.append(item)
                    self.queue.task_done()
                except asyncio.TimeoutError:
                    pass

                current_time = time.time()
                time_since_flush = current_time - last_flush

                # Flush conditions
                if len(batch) >= self._batch_size or (batch and time_since_flush >= self._flush_interval):
                    await self._flush_batch(batch)
                    batch = []
                    last_flush = current_time

            except Exception as e:
                logger.error(f"Error in trace buffer worker: {e}")
                await asyncio.sleep(1) # Prevent tight loop on error

        # Final flush
        if batch:
            await self._flush_batch(batch)

        # Flush remaining in queue
        remaining_batch = []
        while not self._queue.empty():
            try:
                remaining_batch.append(self._queue.get_nowait())
                self._queue.task_done()
            except asyncio.QueueEmpty:
                break

        if remaining_batch:
            await self._flush_batch(remaining_batch)

    async def _flush_batch(self, batch: List[Dict[str, Any]]):
        if not batch:
            return

        try:
            await self.collection.insert_many(batch, ordered=False)
            logger.debug(f"Flushed {len(batch)} traces to {self.collection.name}")
        except Exception as e:
            logger.error(f"Failed to write batch to DB: {e}")
            # In a real production system, we might dump to disk here
