# AI-DevOps Deployment & Configuration Guide

This guide outlines how to connect this repository to GitHub and AWS using secure, passwordless authentication.

---

## 1. Prerequisites Checklist

- [ ] GitHub Account with a new empty repository (e.g. `https://github.com/<owner>/ai-devops`).
- [ ] AWS Account with administrative access to IAM and EC2.
- [ ] AWS CLI configured locally (`aws configure`) or AWS CloudShell.

---

## 2. Infrastructure Deployment (Zero-Secrets Setup)

### Step 1: Configure Terraform Variables
Copy the example variables file:
```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```
Update `terraform/terraform.tfvars`:
```hcl
aws_region   = "us-east-1"
environment  = "production"
project_name = "ai-devops"
instance_type = "t3.micro"  # Free-tier eligible
github_repo  = "your-username/your-repo-name"  # Used for OIDC trust
app_port     = 8000
```

### Step 2: Provision Infrastructure (When Budget Confirmed)
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Note the outputs:
* `github_actions_role_arn`
* `instance_id`
* `application_url`

---

## 3. GitHub Actions Secrets Configuration

In your GitHub repository, navigate to **Settings → Secrets and variables → Actions** and add the following repository secrets:

| Secret Name | Description | Example / Source |
| :--- | :--- | :--- |
| `AWS_DEPLOY_ROLE_ARN` | IAM Role ARN for OIDC authentication | Output from Terraform `github_actions_role_arn` |
| `AWS_REGION` | AWS Deployment Region | `us-east-1` |
| `EC2_INSTANCE_ID` | EC2 Instance ID | Output from Terraform `instance_id` |
| `APP_HOST` | Public IP or DNS of the EC2 instance | Output from Terraform `instance_public_ip` |

> [!NOTE]
> No static AWS Access Keys or Secret Keys (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) are required or used. The entire pipeline authenticates via cryptographically signed OIDC tokens.

---

## 4. Connecting Git Remote & Triggering Pipeline

Run the following commands in the project root:

```powershell
# Add your GitHub remote
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# Push code to main
git branch -M main
git push -u origin main
```

Upon pushing:
1. GitHub Actions will trigger `.github/workflows/ci.yml`.
2. All Python tests, lint checks, Docker build validations, and Terraform validations will run automatically.
3. Upon CI passing on `main`, `.github/workflows/cd.yml` will deploy the container to AWS EC2 via AWS SSM and verify application health.
