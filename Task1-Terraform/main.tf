resource "google_storage_bucket" "d0_raw_landing" {

  name     = var.raw_bucket_name
  project  = var.project_id
  location = var.region

  force_destroy = false

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }

    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age                   = 365
      matches_storage_class = ["ARCHIVE"]
    }

    action {
      type = "Delete"
    }
  }

  labels = {
    data_layer  = "d0-raw-landing"
    environment = "staging"
    managed_by  = "terraform"
  }
}


resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id = "d1_staged_enforced"
  project    = var.project_id
  location   = var.bigquery_location

  description = "Validated and schema-enforced student onboarding records."

  delete_contents_on_destroy = false

  labels = {
    data_layer  = "d1-staged-enforced"
    environment = "staging"
    managed_by  = "terraform"
  }
}

resource "google_bigquery_table" "student_onboarding" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_onboarding"

  deletion_protection = true

  schema = <<EOF
[
  {
    "name": "student_reference",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "student_age",
    "type": "INTEGER",
    "mode": "REQUIRED"
  },
  {
    "name": "parent_email",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "region",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "has_learning_difficulty",
    "type": "BOOLEAN",
    "mode": "REQUIRED"
  },
  {
    "name": "requires_lsa_support",
    "type": "BOOLEAN",
    "mode": "REQUIRED"
  },
  {
    "name": "consent_to_process_data",
    "type": "BOOLEAN",
    "mode": "REQUIRED"
  },
  {
    "name": "requires_transport_support",
    "type": "BOOLEAN",
    "mode": "REQUIRED"
  },
  {
    "name": "requires_medical_assistance",
    "type": "BOOLEAN",
    "mode": "REQUIRED"
  },
  {
    "name": "ingested_at",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  }
]
EOF
}

resource "google_service_account" "ingestion" {
  account_id   = "staging-data-ingestion"
  display_name = "Staging Data Ingestion"
  description  = "Writes raw objects and validated BigQuery rows without broad administrative access."
}
