resource "google_storage_bucket_iam_member" "ingestion_object_creator" {
  bucket = google_storage_bucket.d0_raw_landing.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.ingestion.email}"
}

resource "google_bigquery_dataset_iam_member" "ingestion_data_editor" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.ingestion.email}"
}

resource "google_project_iam_member" "ingestion_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.ingestion.email}"
}

resource "google_bigquery_table_iam_member" "administrator_data_viewer" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_onboarding.table_id
  role       = "roles/bigquery.dataViewer"
  member     = var.administrator_principal
}

resource "google_bigquery_table_iam_member" "regional_analyst_data_viewer" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_onboarding.table_id
  role       = "roles/bigquery.dataViewer"
  member     = var.regional_analyst_principal
}
