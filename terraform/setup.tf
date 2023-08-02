terraform {
    cloud {
        # cloud block configured via Environment Variables
        # https://developer.hashicorp.com/terraform/cli/cloud/settings#environment-variables
    }
    required_providers {
        aws = {
        source  = "hashicorp/aws"
        version = "5.9"
        }
    }
}

# Configure the AWS Provider
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}