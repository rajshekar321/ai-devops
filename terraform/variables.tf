variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ai-devops"
}

variable "instance_type" {
  description = "EC2 instance size (Free Tier eligible default)"
  type        = string
  default     = "t3.micro"
}

variable "github_repo" {
  description = "GitHub repository formatted as owner/repo (e.g., octocat/my-app) for OIDC trust"
  type        = string
  default     = "rajshekar321/ai-devops"
}

variable "app_port" {
  description = "Application HTTP port"
  type        = number
  default     = 8000
}
