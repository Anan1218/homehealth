import pytest
from pydantic import ValidationError
from app.features.auth.schemas import UserCreate, UserLogin, UserResponse, Token


@pytest.mark.unit
class TestAuthSchemas:
    """Unit tests for authentication schemas"""
    
    def test_user_create_with_valid_data_should_pass_validation(self):
        """Test UserCreate schema with valid data"""
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "password": "secure123",
            "full_name": "Test User"
        }
        
        # Act
        user = UserCreate(**valid_data)
        
        # Assert
        assert user.email == "test@example.com"
        assert user.password == "secure123"
        assert user.full_name == "Test User"
    
    def test_user_create_with_invalid_email_should_raise_validation_error(self):
        """Test UserCreate schema with invalid email"""
        # Arrange
        invalid_data = {
            "email": "not_an_email",
            "password": "secure123"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)
    
    def test_user_create_without_email_should_raise_validation_error(self):
        """Test UserCreate schema without required email"""
        # Arrange
        invalid_data = {
            "password": "secure123"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)
    
    def test_user_create_without_password_should_raise_validation_error(self):
        """Test UserCreate schema without required password"""
        # Arrange
        invalid_data = {
            "email": "test@example.com"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)
    
    def test_user_create_without_full_name_should_use_default_none(self):
        """Test UserCreate schema without optional full_name"""
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "password": "secure123"
        }
        
        # Act
        user = UserCreate(**valid_data)
        
        # Assert
        assert user.full_name is None
    
    def test_user_login_with_valid_data_should_pass_validation(self):
        """Test UserLogin schema with valid data"""
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "password": "secure123"
        }
        
        # Act
        credentials = UserLogin(**valid_data)
        
        # Assert
        assert credentials.email == "test@example.com"
        assert credentials.password == "secure123"
    
    def test_user_login_with_invalid_email_should_raise_validation_error(self):
        """Test UserLogin schema with invalid email"""
        # Arrange
        invalid_data = {
            "email": "invalid_email",
            "password": "secure123"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserLogin(**invalid_data)
    
    def test_user_response_with_valid_data_should_pass_validation(self):
        """Test UserResponse schema with valid data"""
        # Arrange
        valid_data = {
            "id": "user_123",
            "email": "test@example.com",
            "full_name": "Test User",
            "created_at": "2023-01-01T00:00:00Z"
        }
        
        # Act
        user = UserResponse(**valid_data)
        
        # Assert
        assert user.id == "user_123"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.created_at == "2023-01-01T00:00:00Z"
    
    def test_user_response_with_none_full_name_should_pass_validation(self):
        """Test UserResponse schema with None full_name"""
        # Arrange
        valid_data = {
            "id": "user_123",
            "email": "test@example.com",
            "full_name": None,
            "created_at": "2023-01-01T00:00:00Z"
        }
        
        # Act
        user = UserResponse(**valid_data)
        
        # Assert
        assert user.full_name is None
    
    def test_token_with_valid_data_should_pass_validation(self, sample_user_response):
        """Test Token schema with valid data"""
        # Arrange
        user_response = UserResponse(**sample_user_response)
        valid_data = {
            "access_token": "test_token_123",
            "token_type": "bearer",
            "expires_at": 1234567890,
            "user": user_response
        }
        
        # Act
        token = Token(**valid_data)
        
        # Assert
        assert token.access_token == "test_token_123"
        assert token.token_type == "bearer"
        assert token.expires_at == 1234567890
        assert isinstance(token.user, UserResponse)
    
    def test_token_without_required_fields_should_raise_validation_error(self):
        """Test Token schema without required fields"""
        # Arrange
        invalid_data = {
            "access_token": "test_token_123"
            # Missing required fields
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            Token(**invalid_data) 