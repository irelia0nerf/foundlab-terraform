import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import sys
import os

# Adiciona o diretório do serviço ao sys.path para permitir a importação de 'app'
scorelab_service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if scorelab_service_dir not in sys.path:
    sys.path.insert(0, scorelab_service_dir)

# É importante importar 'app' depois de ajustar o path
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_vertex_ai_endpoint():
    """Fixture que mocka o endpoint da Vertex AI para os testes."""
    with patch('app.main.endpoint', autospec=True) as mock_endpoint:
        yield mock_endpoint

def test_calculate_psrr_success(mock_vertex_ai_endpoint):
    """
    Testa o caso de sucesso para o cálculo do PSRR, mockando a resposta da Vertex AI.
    """
    # Configura o retorno do mock
    mock_prediction_result = MagicMock()
    mock_prediction_result.predictions = [
        {"psrr_score": 95.5, "risk_tier": "HIGH"}
    ]
    mock_vertex_ai_endpoint.predict.return_value = mock_prediction_result

    # Faz a requisição
    response = client.post("/v1/calculate-psrr", json={"client_id": "client-123"})

    # Verifica as asserções
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == "client-123"
    assert data["psrr_score"] == 95.5
    assert data["risk_tier"] == "HIGH"
    
    # Verifica se o método predict foi chamado com os argumentos corretos
    mock_vertex_ai_endpoint.predict.assert_called_once_with(instances=[{"client_id": "client-123"}])

def test_calculate_psrr_vertex_ai_error(mock_vertex_ai_endpoint):
    """
    Testa o tratamento de erro quando a chamada para a Vertex AI falha.
    """
    # Configura o mock para levantar uma exceção
    mock_vertex_ai_endpoint.predict.side_effect = Exception("Vertex AI is down")

    response = client.post("/v1/calculate-psrr", json={"client_id": "client-456"})

    assert response.status_code == 500
    assert response.json() == {"detail": "An internal error occurred while calling the prediction model."}

def test_calculate_psrr_empty_prediction(mock_vertex_ai_endpoint):
    """
    Testa o tratamento de erro quando a Vertex AI retorna uma predição vazia.
    """
    mock_prediction_result = MagicMock()
    mock_prediction_result.predictions = []
    mock_vertex_ai_endpoint.predict.return_value = mock_prediction_result

    response = client.post("/v1/calculate-psrr", json={"client_id": "client-789"})

    assert response.status_code == 500
    assert response.json() == {"detail": "An internal error occurred while calling the prediction model."}

@patch('app.main.endpoint', None)
def test_calculate_psrr_endpoint_not_configured():
    """
    Testa o caso em que o endpoint da Vertex AI não está configurado.
    """
    response = client.post("/v1/calculate-psrr", json={"client_id": "client-000"})

    assert response.status_code == 503
    assert response.json() == {"detail": "Vertex AI service is not available or configured correctly."}

def test_health_check():
    """Testa o endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}