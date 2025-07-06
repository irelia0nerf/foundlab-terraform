# --- provider.tf ---

terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }

  backend "gcs" {
    bucket = "foundlab-tf-state-prod-9876" # SUBSTITUIR PELO NOME DO SEU BUCKET
    prefix = "prod/gcp/core-infra"
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}