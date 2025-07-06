import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_pubsub():
    with patch('app.main.publisher', autospec=True) as mock_publisher:
        if mock_publisher:
            mock_publisher.publish.return_value = MagicMock(result=lambda: "mock_message_id")
        yield mock_publisher

def test_verify_identity_approved(mock_pubsub):
    """Testa um caso de sucesso onde o cliente é aprovado."""
    response = client.post(
        "/v1/verify",
        json={"document_id": "12345678900", "full_name": "Cliente Aprovado"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "APPROVED"
    assert "decision_id" in data

    if mock_pubsub:
      mock_pubsub.publish.assert_called_once()