variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "asia-south1"
}

variable "bigquery_location" {
  description = "BigQuery dataset location"
  type        = string
  default     = "asia-south1"
}

variable "raw_bucket_name" {
  description = "Globally unique name for the D0 raw landing bucket"
  type        = string
}

variable "administrator_principal" {
  description = "IAM principal allowed to view the staged table"
  type        = string
}

variable "regional_analyst_principal" {
  description = "IAM principal for regional filtered access"
  type        = string
}

variable "regional_analyst_region" {
  description = "Region allowed for the regional analyst"
  type        = string
  default     = "UAE-DUBAI"
}
