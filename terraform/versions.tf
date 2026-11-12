terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # In production, configure remote state backend here (e.g. S3 + DynamoDB)
  # backend "s3" {
  #   bucket         = "my-terraform-state-bucket"
  #   key            = "aidevops/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "terraform-locks"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform-AI-DevOps"
    }
  }
}
