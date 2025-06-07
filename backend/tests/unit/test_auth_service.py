import pytest
from unittest.mock import Mock, AsyncMock
from app.features.auth.service import AuthService
from app.features.auth.schemas import UserCreate, UserLogin, Token, UserResponse


@pytest.mark.unit
class TestAuthService:
    """Unit tests for AuthService"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_supabase = Mock()
        self.auth_service = AuthService(supabase=self.mock_supabase)
    
    @pytest.mark.asyncio
    async def test_register_user_with_valid_data_should_return_token(self, sample_user_data):
        """Test successful user registration"""
        # Arrange
        user_data = UserCreate(**sample_user_data)
        mock_response = Mock()
        mock_response.user = Mock()
        mock_response.user.id = "user_123"
        mock_response.user.email = sample_user_data["email"]
        mock_response.user.user_metadata = {"full_name": sample_user_data["full_name"]}
        mock_response.user.created_at = "2023-01-01T00:00:00Z"
        mock_response.session = Mock()
        mock_response.session.access_token = "test_token"
        mock_response.session.expires_at = 1234567890
        
        self.mock_supabase.auth.sign_up.return_value = mock_response
        
        # Act
        result = await self.auth_service.register_user(user_data)
        
        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "test_token"
        assert result.token_type == "bearer"
        assert result.user.email == sample_user_data["email"]
        assert result.user.full_name == sample_user_data["full_name"]
        
        # Verify supabase was called correctly
        self.mock_supabase.auth.sign_up.assert_called_once_with({
            "email": sample_user_data["email"],
            "password": sample_user_data["password"],
            "options": {
                "data": {
                    "full_name": sample_user_data["full_name"]
                }
            }
        })
    
    @pytest.mark.asyncio
    async def test_register_user_with_failed_response_should_raise_exception(self, sample_user_data):
        """Test registration failure"""
        # Arrange
        user_data = UserCreate(**sample_user_data)
        mock_response = Mock()
        mock_response.user = None
        
        self.mock_supabase.auth.sign_up.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(Exception, match="Failed to create user"):
            await self.auth_service.register_user(user_data)
    
    @pytest.mark.asyncio
    async def test_login_user_with_valid_credentials_should_return_token(self, sample_login_data):
        """Test successful user login"""
        # Arrange
        credentials = UserLogin(**sample_login_data)
        mock_response = Mock()
        mock_response.user = Mock()
        mock_response.user.id = "user_123"
        mock_response.user.email = sample_login_data["email"]
        mock_response.user.user_metadata = {"full_name": "Test User"}
        mock_response.user.created_at = "2023-01-01T00:00:00Z"
        mock_response.session = Mock()
        mock_response.session.access_token = "login_token"
        mock_response.session.expires_at = 1234567890
        
        self.mock_supabase.auth.sign_in_with_password.return_value = mock_response
        
        # Act
        result = await self.auth_service.login_user(credentials)
        
        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "login_token"
        assert result.user.email == sample_login_data["email"]
        
        # Verify supabase was called correctly
        self.mock_supabase.auth.sign_in_with_password.assert_called_once_with({
            "email": sample_login_data["email"],
            "password": sample_login_data["password"]
        })
    
    @pytest.mark.asyncio
    async def test_login_user_with_invalid_credentials_should_raise_exception(self, sample_login_data):
        """Test login failure"""
        # Arrange
        credentials = UserLogin(**sample_login_data)
        mock_response = Mock()
        mock_response.user = None
        
        self.mock_supabase.auth.sign_in_with_password.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(Exception, match="Invalid credentials"):
            await self.auth_service.login_user(credentials)
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_valid_token_should_return_user(self):
        """Test getting current user with valid token"""
        # Arrange
        token = "valid_token"
        mock_response = Mock()
        mock_response.user = Mock()
        mock_response.user.id = "user_123"
        mock_response.user.email = "test@example.com"
        mock_response.user.user_metadata = {"full_name": "Test User"}
        mock_response.user.created_at = "2023-01-01T00:00:00Z"
        
        self.mock_supabase.auth.get_user.return_value = mock_response
        
        # Act
        result = await self.auth_service.get_current_user(token)
        
        # Assert
        assert isinstance(result, UserResponse)
        assert result.email == "test@example.com"
        assert result.full_name == "Test User"
        
        # Verify supabase was called correctly
        self.mock_supabase.auth.get_user.assert_called_once_with(token)
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_invalid_token_should_return_none(self):
        """Test getting current user with invalid token"""
        # Arrange
        token = "invalid_token"
        self.mock_supabase.auth.get_user.side_effect = Exception("Invalid token")
        
        # Act
        result = await self.auth_service.get_current_user(token)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_no_user_in_response_should_return_none(self):
        """Test getting current user when no user in response"""
        # Arrange
        token = "valid_token"
        mock_response = Mock()
        mock_response.user = None
        
        self.mock_supabase.auth.get_user.return_value = mock_response
        
        # Act
        result = await self.auth_service.get_current_user(token)
        
        # Assert
        assert result is None 