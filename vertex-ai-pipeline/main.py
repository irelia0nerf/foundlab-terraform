# Este script automatiza o treinamento e a implantação de um modelo de classificação
# na Vertex AI para prever o 'risk_tier' de um cliente.

# --- Exemplo de dados (psrr_training_data.csv) ---
# Este arquivo CSV deve ser enviado para um bucket no Google Cloud Storage.
#
# client_age_days,wallet_risk_exposure_score,fiat_identity_credit_score,wallets_per_identity_count,recent_pix_velocity_inbound,risk_tier
# 5,80,250,4,20,HIGH
# 365,10,850,1,2,LOW
# 180,45,600,2,5,MODERATE
# 12,95,150,5,30,HIGH

import os
from datetime import datetime
from google.cloud import aiplatform

# --- Configuração ---
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-gcp-project-id")
REGION = "southamerica-east1"
BUCKET_URI = f"gs://{PROJECT_ID}-foundlab-ml-artifacts"
DATASET_GCS_URI = f"{BUCKET_URI}/data/psrr_training_data.csv"

# Nomes para os recursos da Vertex AI
TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")
DATASET_DISPLAY_NAME = f"psrr_dataset_{TIMESTAMP}"
TRAINING_JOB_DISPLAY_NAME = f"psrr_training_job_{TIMESTAMP}"
MODEL_DISPLAY_NAME = f"psrr_model_{TIMESTAMP}"
ENDPOINT_DISPLAY_NAME = "foundlab-psrr-endpoint"

def main():
    """Executa o pipeline completo: criar dataset, treinar modelo e implantar."""
    print(f"Iniciando pipeline de ML no projeto {PROJECT_ID}...")
    aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)

    # --- 1. Criar o Dataset Tabular ---
    dataset = aiplatform.TabularDataset.create(
        display_name=DATASET_DISPLAY_NAME,
        gcs_source=[DATASET_GCS_URI],
    )
    dataset.wait()
    print(f"Dataset criado: {dataset.resource_name}")

    # --- 2. Criar e Executar o Job de Treinamento AutoML ---
    training_job = aiplatform.AutoMLTabularTrainingJob(
        display_name=TRAINING_JOB_DISPLAY_NAME,
        optimization_prediction_type="classification",
    )

    # --- 3. Treinar o Modelo ---
    model = training_job.run(
        dataset=dataset,
        target_column="risk_tier",
        model_display_name=MODEL_DISPLAY_NAME,
        budget_milli_node_hours=1000,
        sync=True,
    )

    # --- 4. Implantar o Modelo em um Endpoint ---
    endpoints = aiplatform.Endpoint.list(filter=f'display_name="{ENDPOINT_DISPLAY_NAME}"')
    endpoint = endpoints[0] if endpoints else aiplatform.Endpoint.create(display_name=ENDPOINT_DISPLAY_NAME)

    model.deploy(
        endpoint=endpoint,
        traffic_split={"0": 100},
        machine_type="n1-standard-2",
        sync=True,
    )
    model.wait()

    print(f"--- Pipeline Concluído! Endpoint: {endpoint.resource_name} ---")

if __name__ == "__main__":
    main()