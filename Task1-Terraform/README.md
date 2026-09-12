# Task 1 - Terraform Data Platform Infrastructure

## Objective

This project provisions a secure staging data platform on Google Cloud using Terraform.

The infrastructure contains:

- A D0 raw landing layer using Google Cloud Storage
- A D1 staged and schema-enforced layer using BigQuery
- A dedicated service account for data ingestion
- Least-privilege IAM permissions
- Row-Level Security for regional analyst access

## Architecture

The platform is divided into two data layers.

### D0 - Raw Landing

- Google Cloud Storage bucket
- Receives raw student onboarding data
- Uniform bucket-level access enabled
- Public access prevention enforced
- Object versioning enabled
- Lifecycle rules move older objects to lower-cost storage

### D1 - Staged Enforced

- BigQuery dataset: `d1_staged_enforced`
- BigQuery table: `student_onboarding`
- Schema-enforced student onboarding records
- Required fields prevent incomplete records
- Row-Level Security restricts regional analyst access

### High-Level Flow

```text
Raw Student Data
        |
        v
D0 - Cloud Storage
        |
        v
Validation / Processing
        |
        v
D1 - BigQuery
        |
        v
IAM + Row-Level Security
        |
        v
Authorized Users

## Deployment Status

The Terraform configuration was successfully formatted, validated, and planned.

`terraform validate` completed successfully, and `terraform plan` produced:

- 10 resources to add
- 0 resources to change
- 0 resources to destroy

The infrastructure could not be applied because the assigned Google Cloud project has a billing account in a disabled/closed state. The Google Cloud API returned HTTP 403 with `accountDisabled` when Terraform attempted to create the D0 Cloud Storage bucket.

The Terraform implementation has therefore been retained as a deployment-ready infrastructure artifact for assessment purposes.

No Terraform resources were modified or bypassed to work around the billing restriction.
