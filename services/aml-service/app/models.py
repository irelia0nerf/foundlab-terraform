from pydantic import BaseModel, Field
from typing import Literal

class AmlScreeningRequest(BaseModel):
    transaction_id: str = Field(..., example="txn_123abc")
    origin_wallet: str = Field(..., example="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B")
    amount_brl: float = Field(..., gt=0, example=5000.50)

class AmlScreeningResponse(BaseModel):
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    verdict: Literal["ALLOW", "REVIEW", "BLOCK"]
    transaction_id: str