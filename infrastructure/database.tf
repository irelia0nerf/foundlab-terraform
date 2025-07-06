# --- database.tf ---

# Gera uma senha segura e aleatória para o banco de dados.
resource "random_password" "db_password" {
  length  = 32
  special = true
  # Garante que caracteres problemáticos em URLs ou shells não sejam usados.
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Provisiona a instância do banco de dados PostgreSQL.
resource "google_sql_database_instance" "main" {
  name             = var.db_instance_name
  database_version = "POSTGRES_14"
  region           = var.gcp_region
  project          = var.gcp_project_id

  settings {
    tier              = "db-n1-standard-1"
    availability_type = "REGIONAL" # Alta disponibilidade

    ip_configuration {
      ipv4_enabled    = false # Apenas acesso privado
      private_network = google_compute_network.vpc.id
    }

    backup_configuration {
      enabled = true
    }

    location_preference {
      zone = var.gcp_zone
    }
  }

  # Previne a exclusão acidental da instância em produção.
  deletion_protection = true
}

# Cria o usuário da aplicação no banco de dados.
resource "google_sql_user" "main_user" {
  name     = var.db_user
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
  project  = var.gcp_project_id
}