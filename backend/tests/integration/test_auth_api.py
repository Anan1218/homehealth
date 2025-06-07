import pytest
from app.features.auth.schemas import Token, UserResponse


@pytest.mark.integration
class TestAuthAPI:
    """Integration tests for authentication API endpoints"""
    
    @pytest.mark.asyncio
    async def test_register_endpoint_with_valid_data_should_return_token(self, client, mock_auth_service, sample_user_data, sample_token_response):
        """Test POST /api/v1/auth/register with valid data"""
        # Arrange
        token = Token(**{
            **sample_token_response,
            "expires_at": 1234567890,
            "user": UserResponse(
                id="123",
                email=sample_user_data["email"],
                full_name=sample_user_data["full_name"],
                created_at="2023-01-01T00:00:00Z"
            )
        })
        mock_auth_service.register_user.return_value = token
        
        # Act
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_register_endpoint_with_invalid_email_should_return_422(self, client, mock_auth_service):
        """Test POST /api/v1/auth/register with invalid email"""
        # Arrange
        invalid_data = {
            "email": "not_an_email",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_register_endpoint_with_missing_fields_should_return_422(self, client, mock_auth_service):
        """Test POST /api/v1/auth/register with missing required fields"""
        # Arrange
        invalid_data = {
            "email": "test@example.com"
            # Missing password
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_register_endpoint_with_service_error_should_return_400(self, client, mock_auth_service, sample_user_data):
        """Test POST /api/v1/auth/register when service raises exception"""
        # Arrange
        mock_auth_service.register_user.side_effect = Exception("User already exists")
        
        # Act
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_login_endpoint_with_valid_credentials_should_return_token(self, client, mock_auth_service, sample_login_data, sample_token_response):
        """Test POST /api/v1/auth/login with valid credentials"""
        # Arrange
        token = Token(**{
            **sample_token_response,
            "expires_at": 1234567890,
            "user": UserResponse(
                id="123",
                email=sample_login_data["email"],
                full_name="Test User",
                created_at="2023-01-01T00:00:00Z"
            )
        })
        mock_auth_service.login_user.return_value = token
        
        # Act
        response = client.post("/api/v1/auth/login", json=sample_login_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_endpoint_with_invalid_credentials_should_return_401(self, client, mock_auth_service, sample_login_data):
        """Test POST /api/v1/auth/login with invalid credentials"""
        # Arrange
        mock_auth_service.login_user.side_effect = Exception("Invalid credentials")
        
        # Act
        response = client.post("/api/v1/auth/login", json=sample_login_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"
    
    @pytest.mark.asyncio
    async def test_login_endpoint_with_invalid_email_should_return_422(self, client, mock_auth_service):
        """Test POST /api/v1/auth/login with invalid email format"""
        # Arrange
        invalid_data = {
            "email": "not_an_email",
            "password": "testpassword123"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_valid_token_should_return_user(self, client, mock_auth_service, sample_user_response):
        """Test GET /api/v1/auth/me with valid token"""
        # Arrange
        user = UserResponse(**sample_user_response)
        mock_auth_service.get_current_user.return_value = user
        
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer valid_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_response["email"]
        assert data["full_name"] == sample_user_response["full_name"]
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_invalid_token_should_return_401(self, client, mock_auth_service):
        """Test GET /api/v1/auth/me with invalid token"""
        # Arrange
        mock_auth_service.get_current_user.return_value = None
        
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid token"
    
    @pytest.mark.asyncio
    async def test_get_current_user_without_token_should_return_403(self, client, mock_auth_service):
        """Test GET /api/v1/auth/me without authorization header"""
        # Act
        response = client.get("/api/v1/auth/me")
        
        # Assert
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_malformed_header_should_return_403(self, client, mock_auth_service):
        """Test GET /api/v1/auth/me with malformed authorization header"""
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "InvalidFormat"}
        )
        
        # Assert
        assert response.status_code == 403 