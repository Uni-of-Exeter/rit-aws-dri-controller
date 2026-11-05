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

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}