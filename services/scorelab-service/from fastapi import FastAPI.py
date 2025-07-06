from fastapi import FastAPI
from .models import AmlScreeningRequest, AmlScreeningResponse

app = FastAPI(title="FoundLab AML Service")

@app.post("/v1/screen", response_model=AmlScreeningResponse)
async def screen_transaction(request: AmlScreeningRequest):
    if request.amount_brl > 10000:
        risk_level = "HIGH"
        verdict = "REVIEW"
    else:
        risk_level = "LOW"
        verdict = "ALLOW"

    return AmlScreeningResponse(
        risk_level=risk_level,
        verdict=verdict,
        transaction_id=request.transaction_id
    )