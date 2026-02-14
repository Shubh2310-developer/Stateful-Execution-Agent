from fastapi import APIRouter, HTTPException
from src.memory.memory_manager import MemoryManager
from src.core.types import UserMemory

router = APIRouter(prefix="/memory", tags=["memory"])
memory_manager = MemoryManager()

@router.get("/{user_id}", response_model=UserMemory)
async def get_user_memory(user_id: str):
    """Retrieves the long-term memory for a specific user."""
    memory = await memory_manager.get_user_memory(user_id)
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory for user {user_id} not found")
    return memory
