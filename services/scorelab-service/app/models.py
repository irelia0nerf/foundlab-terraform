from pydantic import BaseModel, Field
from typing import Literal

class ScoreRequest(BaseModel):
    client_id: str = Field(..., example="client-uuid-12345")

class ScoreResponse(BaseModel):
    client_id: str
    psrr_score: float = Field(..., example=85.5)
    risk_tier: Literal["LOW", "MODERATE", "HIGH"]