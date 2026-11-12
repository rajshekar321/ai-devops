# Autonomous DevOps Agent Execution Policy

## 1. Operating Scope & Boundaries
- **Workspace Boundary:** All operations, file reads, and file writes MUST strictly remain within `C:\AI-DevOps`. Never access, read, or modify files outside this directory.
- **Destructive Operations:** Strictly prohibited. Never execute destructive system commands (e.g., formatting disks, deleting system trees, force-killing host services).
- **Security & Credentials:**
  - Never generate fake secrets or commit real API keys, AWS credentials, SSH private keys, or tokens.
  - All sensitive configuration must use placeholders, environment variable references, or `.env.example`.
- **Approved AWS Cloud Budget:**
  - Approved monthly ceiling: **₹5,000 INR** (~$60 USD).
  - Target AWS Region: `us-east-1`.
  - Architecture must prioritize AWS Free Tier (`t3.micro` / `t2.micro`, 20GB gp3 storage, estimated at ~$9.10 USD/mo or ₹760 INR/mo).
  - `terraform apply` is authorized ONLY after generating and reviewing `terraform plan` to verify that planned resources remain strictly within the ₹5,000 monthly budget.

## 2. Pre-Approved Autonomous Local Execution (Narrow Allowlist)
The agent is authorized to execute the following commands autonomously without repetitive user confirmation:
- **Python:** Runtime checks (`python --version`), virtual environment tasks, dependency checks, test runs (`pytest`), and linting (`flake8`, `ruff`).
- **Git:** Status, diffs, branch checks, staging, commits, and remote push (`git status`, `git diff`, `git add`, `git commit`, `git push origin main`).
- **Docker:** Local daemon checks, configuration verification (`docker compose config`), Dockerfile linting, and local image builds.
- **Terraform:** Formatting (`terraform fmt`), syntax checking (`terraform validate`), provider initialization (`terraform init`), and speculative execution planning (`terraform plan`).
- **File System:** Creating, reading, editing, and maintaining project files inside `C:\AI-DevOps`.

## 3. Autonomous Problem Solving & Self-Healing
- Autonomously inspect error logs, apply code/configuration fixes, and re-test.
- Do not stop for routine manual approval between normal development phases.
- Halt and prompt the user ONLY for genuine external blockers:
  - AWS account credentials / authorization when `aws sts get-caller-identity` reports `NoCredentials`.
  - Financial decisions exceeding the ₹5,000 monthly ceiling.
  - GitHub authentication when interactive web authorization is required.
