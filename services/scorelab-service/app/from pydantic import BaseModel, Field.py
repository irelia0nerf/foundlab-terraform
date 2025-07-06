from pydantic import BaseModel, Field
from typing import Literal

class AmlScreeningRequest(BaseModel):
    transaction_id: str = Field(..., example="txn_123abc")
    amount_brl: float = Field(..., gt=0, example=5000.50)

class AmlScreeningResponse(BaseModel):
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    verdict: Literal["ALLOW", "REVIEW", "BLOCK"]
    transaction_id: str