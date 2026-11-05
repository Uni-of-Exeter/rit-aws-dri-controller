{% extends "environments/terraform.tfvars" %}

# TODO: move these into the module implementation yaml to pull into the stacks

# --- Bastion ---
bastion_instance_type = "t3.medium"
bastion_key_name      = "exeter-bastion-key" # Must pre-exist in AWS

# --- Remote Data Source ---
remote_s3_bucket_arn = "arn:aws:s3:::external-data-bucket" # Replace

# --- GitHub ---
github_repo_url       = "your-org/your-repository" # owner/repo format
github_branch         = "main"
github_connection_arn = "arn:aws:codestar-connections:eu-west-2:123456789012:connection/xxxxxxxx" # Replace

# --- Compute ---
batch_max_vcpus      = 64
batch_instance_types = ["c5.4xlarge", "c5.9xlarge", "p3.2xlarge", "p3.8xlarge"]

# --- Identity (optional: leave empty to skip SAML federation) ---
saml_provider_arn = ""
# saml_provider_arn = "arn:aws:iam::123456789012:saml-provider/UoE-IdP"

