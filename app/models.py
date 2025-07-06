from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID, uuid4

# Pydantic model for the API request body
class KycRequest(BaseModel):
    document_id: str = Field(..., example="12345678900", description="CPF do cliente para verificação.")
    full_name: str = Field(..., example="João da Silva", description="Nome completo do cliente.")

# Pydantic model for the API response body
class KycResponse(BaseModel):
    decision_id: UUID = Field(default_factory=uuid4)
    status: Literal["APPROVED", "REVIEW", "REJECTED"]
    client_document_id: str