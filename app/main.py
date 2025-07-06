import os
import json
import uuid
from fastapi import FastAPI, HTTPException
from google.cloud import pubsub_v1
from .models import KycRequest, KycResponse

# --- Configuration ---
app = FastAPI(
    title="FoundLab KYC Service",
    description="Serviço para verificação de identidade de clientes (Know Your Customer).",
    version="1.0.0"
)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "foundlab-events")

# --- Clients ---
publisher = pubsub_v1.PublisherClient() if PROJECT_ID else None
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC_ID) if publisher else None

@app.post("/v1/verify", response_model=KycResponse)
async def verify_identity(request: KycRequest):
    """
    Recebe os dados de um cliente, simula uma verificação de identidade,
    e publica o resultado em um tópico Pub/Sub.
    """
    decision_id = uuid.uuid4()

    # --- Simulated Business Logic ---
    if "REJECTED" in request.full_name.upper():
        status = "REJECTED"
    elif "REVIEW" in request.full_name.upper():
        status = "REVIEW"
    else:
        status = "APPROVED"

    response = KycResponse(
        decision_id=decision_id,
        status=status,
        client_document_id=request.document_id
    )

    # --- Database Persistence (Simulated) ---
    print(f"[DB LOG] Persisting verification {response.decision_id} with status {response.status}")

    # --- Publish Event to Pub/Sub ---
    if topic_path:
        try:
            message_data = response.model_dump_json().encode("utf-8")
            future = publisher.publish(
                topic_path,
                message_data,
                eventType="KycVerificationCompleted"
            )
            print(f"[Pub/Sub] Published message {future.result()} to {topic_path}")
        except Exception as e:
            print(f"Error publishing to Pub/Sub: {e}")
            raise HTTPException(status_code=500, detail="Failed to publish verification event.")

    return response

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "ok"}