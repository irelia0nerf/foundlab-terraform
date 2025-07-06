# --- gateway.tf ---

# Garante que a API do API Gateway está ativa no projeto.
resource "google_project_service" "apigateway" {
  project            = var.gcp_project_id
  service            = "apigateway.googleapis.com"
  disable_on_destroy = false
}

# Cria o recurso da API que servirá como container para as configurações.
resource "google_api_gateway_api" "foundlab_api" {
  provider = google-beta
  api_id   = "foundlab-unified-api"
  project  = var.gcp_project_id
  
  depends_on = [google_project_service.apigateway]
}

# Cria uma configuração da API a partir da especificação OpenAPI.
resource "google_api_gateway_api_config" "foundlab_api_config" {
  provider      = google-beta
  api           = google_api_gateway_api.foundlab_api.api_id
  api_config_id = var.api_config_id
  project       = var.gcp_project_id

  openapi_documents {
    document {
      path     = "openapi_spec.yaml"
      contents = filebase64("openapi_spec.yaml")
    }
  }

  # Configura o gateway para usar a Service Account que tem permissão para invocar os serviços Cloud Run.
  gateway_config {
    backend_config {
      google_service_account = google_service_account.cloud_run_sa.email
    }
  }

  depends_on = [google_api_gateway_api.foundlab_api]
}

# Implanta a configuração em uma instância de Gateway, tornando-a pública e acessível.
resource "google_api_gateway_gateway" "foundlab_gateway" {
  provider     = google-beta
  api_config   = google_api_gateway_api_config.foundlab_api_config.id
  gateway_id   = "foundlab-main-gateway"
  region       = var.gcp_region
  project      = var.gcp_project_id
  display_name = "FoundLab Main Gateway"

  depends_on = [google_api_gateway_api_config.foundlab_api_config]
}

# Exporta a URL do gateway para fácil acesso após a implantação.
output "api_gateway_url" {
  value       = "https://${google_api_gateway_gateway.foundlab_gateway.default_hostname}"
  description = "A URL base do API Gateway implantado."
}