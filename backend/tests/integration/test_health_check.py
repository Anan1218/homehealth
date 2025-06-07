import pytest


@pytest.mark.integration
class TestHealthCheck:
    """Integration tests for health check endpoints"""
    
    def test_health_endpoint_should_return_healthy_status(self, client, mock_auth_service):
        """Test GET /health returns healthy status"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "homehealth-api"
    
    def test_root_endpoint_should_return_welcome_message(self, client, mock_auth_service):
        """Test GET / returns welcome message"""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "HomeHealth API" in data["message"] 