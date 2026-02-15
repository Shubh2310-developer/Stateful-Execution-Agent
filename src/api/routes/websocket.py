from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import json
from src.utils.logger import logger

router = APIRouter(prefix="/ws", tags=["websocket"])

# Store active WebSocket connections per task
active_connections: Dict[str, Set[WebSocket]] = {}
# Store general connections (dashboard updates)
dashboard_connections: Set[WebSocket] = set()


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""

    @staticmethod
    async def connect(websocket: WebSocket, task_id: str = None):
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        
        if task_id:
            if task_id not in active_connections:
                active_connections[task_id] = set()
            active_connections[task_id].add(websocket)
            logger.info(f"WebSocket connected for task: {task_id}")
        else:
            dashboard_connections.add(websocket)
            logger.info("WebSocket connected to dashboard")

    @staticmethod
    async def disconnect(websocket: WebSocket, task_id: str = None):
        """Remove a WebSocket connection."""
        if task_id:
            if task_id in active_connections:
                active_connections[task_id].discard(websocket)
                if not active_connections[task_id]:
                    del active_connections[task_id]
            logger.info(f"WebSocket disconnected from task: {task_id}")
        else:
            dashboard_connections.discard(websocket)
            logger.info("WebSocket disconnected from dashboard")

    @staticmethod
    async def send_task_update(task_id: str, data: dict):
        """Send update to all connections subscribed to a specific task."""
        if task_id in active_connections:
            disconnected = set()
            for connection in active_connections[task_id]:
                try:
                    await connection.send_json(data)
                except Exception as e:
                    logger.error(f"Error sending to WebSocket: {e}")
                    disconnected.add(connection)
            
            # Clean up disconnected clients
            for conn in disconnected:
                active_connections[task_id].discard(conn)

    @staticmethod
    async def broadcast_dashboard(data: dict):
        """Broadcast update to all dashboard connections."""
        disconnected = set()
        for connection in dashboard_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting to dashboard: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            dashboard_connections.discard(conn)


manager = ConnectionManager()


@router.websocket("/task/{task_id}")
async def websocket_task_endpoint(websocket: WebSocket, task_id: str):
    """
    WebSocket endpoint for real-time task updates.
    
    Connect to this endpoint to receive live updates about a specific task's progress,
    including status changes, step completions, and artifact generation.
    """
    await manager.connect(websocket, task_id)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "task_id": task_id,
            "message": f"Connected to task {task_id} updates"
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for messages from client (ping/pong for keepalive)
                data = await websocket.receive_text()
                
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
                
    finally:
        await manager.disconnect(websocket, task_id)


@router.websocket("/dashboard")
async def websocket_dashboard_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time dashboard updates.
    
    Connect to this endpoint to receive live updates about all tasks,
    including new task creations and overall system status.
    """
    await manager.connect(websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to dashboard updates"
        })
        
        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
                
    finally:
        await manager.disconnect(websocket)
