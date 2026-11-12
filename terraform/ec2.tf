# EC2 Compute Infrastructure with Automated Docker Bootstrap

# Latest Amazon Linux 2023 AMI (HVM, SSD Volume Type, x86_64)
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance
resource "aws_instance" "app_server" {
  ami                  = data.aws_ami.amazon_linux_2023.id
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # Root Block Device
  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
    tags = {
      Name = "${var.project_name}-root-volume"
    }
  }

  # Automated Docker & Service Bootstrap via Cloud-Init / User Data
  user_data = <<-EOF
              #!/bin/bash
              set -e

              # Update system packages
              dnf update -y

              # Install Docker and git
              dnf install -y docker git

              # Start and enable Docker daemon
              systemctl start docker
              systemctl enable docker

              # Add ec2-user to docker group
              usermod -aG docker ec2-user

              # Install Docker Compose Plugin
              DOCKER_CONFIG=/usr/local/lib/docker
              mkdir -p $DOCKER_CONFIG/cli-plugins
              curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
              chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

              # Prepare deployment directory
              mkdir -p /opt/aidevops
              chown -R ec2-user:ec2-user /opt/aidevops

              echo "AI-DevOps instance bootstrap completed successfully." > /var/log/bootstrap.log
              EOF

  tags = {
    Name        = "${var.project_name}-ec2-instance"
    Role        = "ApplicationServer"
    Environment = var.environment
  }
}
