output "raw_bucket_name" {
  description = "Name of the D0 raw landing bucket"
  value       = google_storage_bucket.d0_raw_landing.name
}

output "student_onboarding_table" {
  description = "Fully qualified BigQuery student onboarding table"
  value       = "${var.project_id}.${google_bigquery_dataset.d1_staged_enforced.dataset_id}.${google_bigquery_table.student_onboarding.table_id}"
}

output "ingestion_service_account" {
  description = "Email address of the staging ingestion service account"
  value       = google_service_account.ingestion.email
}
