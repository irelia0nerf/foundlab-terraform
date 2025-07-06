# --- iam.tf ---

# Conta de serviço para os microsserviços rodando no Cloud Run.
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Service Account for FoundLab Cloud Run services"
  project      = var.gcp_project_id
}

# Conta de serviço para o pipeline de CI/CD no Cloud Build.
resource "google_service_account" "cloud_build_sa" {
  account_id   = "cloud-build-sa"
  display_name = "Service Account for FoundLab Cloud Build pipelines"
  project      = var.gcp_project_id
}

# Permite que a conta de serviço do Cloud Run se conecte ao Cloud SQL.
resource "google_project_iam_member" "cloud_run_sql_client" {
  project = var.gcp_project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Permissões para o Cloud Build poder implantar no Cloud Run e gerenciar SAs.
resource "google_project_iam_member" "cloud_build_run_admin" {
  project = var.gcp_project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.cloud_build_sa.email}"
}

resource "google_project_iam_member" "cloud_build_sa_user" {
  project = var.gcp_project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.cloud_build_sa.email}"
}