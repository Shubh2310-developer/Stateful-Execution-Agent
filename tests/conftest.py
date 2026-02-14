import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from tests.fixtures.sample_user_data import SAMPLE_USER_MEMORY
from tests.fixtures.sample_plans import SAMPLE_PLAN
from tests.fixtures.sample_tasks import SAMPLE_TASK_DATA

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def mongodb_client():
    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    yield client
    client.close()

@pytest.fixture
def mock_user_memory():
    return SAMPLE_USER_MEMORY

@pytest.fixture
def mock_plan():
    return SAMPLE_PLAN

@pytest.fixture
def mock_task_state():
    from src.state.state_schema import TaskStateSchema
    return TaskStateSchema(**SAMPLE_TASK_DATA)
