import os
from fastapi import FastAPI, HTTPException
from google.cloud import aiplatform
from .models import ScoreRequest, ScoreResponse

app = FastAPI(title="FoundLab ScoreLab Service")

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "southamerica-east1")
VERTEX_AI_ENDPOINT_ID = os.getenv("VERTEX_AI_ENDPOINT_ID")

@app.post("/v1/calculate-psrr", response_model=ScoreResponse)
async def calculate_psrr(request: ScoreRequest):
    # Lógica para chamar a Vertex AI (será implementada)
    print(f"Cálculo de score solicitado para o cliente: {request.client_id}")
    
    # Simulação de resposta
    return ScoreResponse(
        client_id=request.client_id,
        psrr_score=75.0,
        risk_tier="HIGH"
    )