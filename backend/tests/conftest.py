import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Test client for API testing."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client():
    """Async test client for async endpoint testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac 