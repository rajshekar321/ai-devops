output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.app_server.public_dns
}

output "application_url" {
  description = "HTTP URL to access the deployed FastAPI dashboard"
  value       = "http://${aws_instance.app_server.public_ip}:${var.app_port}"
}

output "github_actions_role_arn" {
  description = "ARN of the IAM role to configure in GitHub Actions Secrets"
  value       = aws_iam_role.github_actions_role.arn
}

output "ssm_connect_command" {
  description = "AWS CLI SSM command for zero-SSH remote terminal access"
  value       = "aws ssm start-session --target ${aws_instance.app_server.id} --region ${var.aws_region}"
}
