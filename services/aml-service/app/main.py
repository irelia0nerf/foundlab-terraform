from fastapi import FastAPI
from .models import AmlScreeningRequest, AmlScreeningResponse

app = FastAPI(
    title="FoundLab AML Service",
    version="1.0.0"
)

@app.post("/v1/screen", response_model=AmlScreeningResponse)
async def screen_transaction(request: AmlScreeningRequest):
    """
    Recebe os dados de uma transação e simula uma análise de risco AML.
    """
    if request.amount_brl > 10000:
        risk_level = "HIGH"
        verdict = "REVIEW"
    elif request.amount_brl > 2000:
        risk_level = "MEDIUM"
        verdict = "ALLOW"
    else:
        risk_level = "LOW"
        verdict = "ALLOW"

    return AmlScreeningResponse(
        risk_level=risk_level,
        verdict=verdict,
        transaction_id=request.transaction_id
    )

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "ok"}