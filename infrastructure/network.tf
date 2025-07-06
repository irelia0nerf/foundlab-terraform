# --- network.tf ---

resource "google_compute_network" "vpc" {
  name                    = "foundlab-vpc"
  auto_create_subnetworks = false
  project                 = var.gcp_project_id
}

resource "google_compute_subnetwork" "private" {
  name          = "foundlab-private-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.gcp_region
  network       = google_compute_network.vpc.id
  private_ip_google_access = true
}

# Regra de firewall para permitir que os serviços dentro da VPC acessem o banco de dados.
resource "google_compute_firewall" "allow_internal_postgres" {
  name    = "foundlab-vpc-allow-internal-postgres"
  network = google_compute_network.vpc.id
  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }
  source_ranges = [google_compute_subnetwork.private.ip_cidr_range]
}

# Regra de firewall para permitir checagens de saúde do Google (essencial para Cloud Run, etc.)
resource "google_compute_firewall" "allow_health_checks" {
  name    = "foundlab-vpc-allow-health-checks"
  network = google_compute_network.vpc.id
  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080"]
  }
  source_ranges = ["130.211.0.0/22", "35.191.0.0/16"]
}