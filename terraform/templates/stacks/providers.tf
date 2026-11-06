provider "aws" {
  # default profile will be used - in our case we rely on the environment to set this up
  region = var.aws_region

  default_tags {
    tags = {
      project_name    = var.project_name
      environment     = var.environment
      client          = var.client
    }
  }
}

# =============================================================================
# Data Sources
# =============================================================================

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}