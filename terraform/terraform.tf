terraform {
  required_version = ">= 1.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "tfstates" {
    bucket       = "uoe-rit-edris-tfstates"
    key          = "data/${var.environment}/tfstate"
    region       = var.aws_region
    use_lockfile = true
  }
}
