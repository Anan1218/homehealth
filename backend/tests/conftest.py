import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from unittest.mock import Mock


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_db():
    """Mock database dependency for testing."""
    mock = Mock()
    return mock


@pytest.fixture
def client(mock_db):
    """Test client with mocked dependencies."""
    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(mock_db):
    """Async test client for async endpoint testing."""
    app.dependency_overrides[get_db] = lambda: mock_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_auth_headers():
    """Sample authentication headers for testing."""
    return {"Authorization": "Bearer test_token"} 