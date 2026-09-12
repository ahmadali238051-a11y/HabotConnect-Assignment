resource "google_bigquery_row_access_policy" "regional_analyst_policy" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_onboarding.table_id

  policy_id = "regional_analyst_region"

  filter_predicate = "region = '${var.regional_analyst_region}'"

  grantees = [
    var.regional_analyst_principal
  ]
}
