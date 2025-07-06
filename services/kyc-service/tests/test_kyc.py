import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

import sys
import os

# Adiciona o diretório pai (kyc-service) ao sys.path para permitir a importação de 'app'.
# Isso é necessário porque os testes agora estão dentro da pasta do serviço.
kyc_service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if kyc_service_dir not in sys.path:
    sys.path.insert(0, kyc_service_dir)

from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_pubsub():
    """Fixture que mocka o publisher do Pub/Sub."""
    with patch('app.main.publisher', autospec=True) as mock_publisher:
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

    mock_pubsub.publish.assert_called_once()