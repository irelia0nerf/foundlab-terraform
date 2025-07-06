# --- secrets.tf ---

# Cria o segredo no Secret Manager para armazenar a senha do banco de dados.
resource "google_secret_manager_secret" "db_password_secret" {
  secret_id = "db-password"
  project   = var.gcp_project_id

  replication {
    automatic = true
  }
}

# Adiciona a senha gerada como a primeira versão do segredo.
resource "google_secret_manager_secret_version" "db_password_secret_version" {
  secret      = google_secret_manager_secret.db_password_secret.id
  secret_data = random_password.db_password.result
}

# Concede à conta de serviço do Cloud Run permissão para ler o segredo.
resource "google_secret_manager_secret_iam_member" "cloud_run_secret_accessor" {
  project   = google_secret_manager_secret.db_password_secret.project
  secret_id = google_secret_manager_secret.db_password_secret.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"

  depends_on = [google_secret_manager_secret.db_password_secret]
}