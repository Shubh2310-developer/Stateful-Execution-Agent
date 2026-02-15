from fastapi import APIRouter, HTTPException, Request
from src.memory.memory_manager import MemoryManager
from src.core.types import UserMemory

router = APIRouter(prefix="/memory", tags=["memory"])
memory_manager = MemoryManager()

@router.get("/{user_id}", response_model=UserMemory)
async def get_user_memory(request: Request, user_id: str):
    """Retrieves the long-term memory for a specific user."""
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    # Session isolation: Ensure user only accesses their own memory
    if current_user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user memory")

    memory = await memory_manager.get_user_memory(user_id)
    if not memory:
        # Auto-create default memory for new users
        memory = await memory_manager.initialize_user_memory(user_id)
    return memory
