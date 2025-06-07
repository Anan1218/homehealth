import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.features.auth.service import AuthService
from app.features.auth.router import get_auth_service
from unittest.mock import Mock, AsyncMock


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_auth_service():
    """Mock auth service for testing."""
    mock = AsyncMock(spec=AuthService)
    return mock


@pytest.fixture
def client(mock_auth_service):
    """Test client for API testing with mocked dependencies."""
    # Override the dependency
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(mock_auth_service):
    """Async test client for async endpoint testing."""
    # Override the dependency
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # Clean up
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
def sample_login_data():
    """Sample login data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def sample_token_response():
    """Sample token response for testing."""
    return {
        "access_token": "test_access_token",
        "token_type": "bearer"
    }


@pytest.fixture
def sample_user_response():
    """Sample user response for testing."""
    return {
        "id": "123",
        "email": "test@example.com",
        "full_name": "Test User",
        "created_at": "2023-01-01T00:00:00Z"
    }


@pytest.fixture
def auth_headers():
    """Authentication headers for testing protected routes."""
    return {"Authorization": "Bearer test_token"} 