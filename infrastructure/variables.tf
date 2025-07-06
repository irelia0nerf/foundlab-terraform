# --- variables.tf ---

variable "gcp_project_id" {
  type        = string
  description = "O ID do projeto GCP onde a infraestrutura será criada."
}

variable "gcp_region" {
  type        = string
  description = "A região GCP para provisionar os recursos."
  default     = "southamerica-east1"
}

variable "gcp_zone" {
  type        = string
  description = "A zona GCP para provisionar os recursos."
  default     = "southamerica-east1-b"
}

variable "terraform_state_bucket" {
  type        = string
  description = "O nome do bucket GCS para armazenar o estado do Terraform."
}

variable "db_instance_name" {
  type        = string
  description = "O nome da instância principal do Cloud SQL PostgreSQL."
  default     = "foundlab-pg-main"
}

variable "db_user" {
  type        = string
  description = "O nome de usuário para a aplicação se conectar ao banco de dados."
  default     = "foundlab_user"
}

variable "api_config_id" {
  type        = string
  description = "O ID para a configuração da API no API Gateway."
  default     = "foundlab-api-config-v1"
}