# Autonomous DevOps Agent Execution Policy

## 1. Operating Scope & Boundaries
- **Workspace Boundary:** All operations, file reads, and file writes MUST strictly remain within `C:\AI-DevOps`. Never access, read, or modify files outside this directory.
- **Destructive Operations:** Strictly prohibited. Never execute destructive system commands (e.g., formatting disks, deleting system trees, force-killing host services).
- **Security & Credentials:**
  - Never generate fake secrets or commit real API keys, AWS credentials, SSH private keys, or tokens.
  - All sensitive configuration must use placeholders, environment variable references, or `.env.example`.
- **Cost & Cloud Resource Protection:**
  - Do NOT run `terraform apply` or provision live AWS resources without an explicit budget and confirmation.
  - Offline validation (`terraform fmt`, `terraform validate`, `terraform plan` with mocked state) is permitted.

## 2. Autonomous Local Execution
The agent is authorized to execute the following non-destructive commands without interruption:
- **Python:** Runtime checks (`python --version`), virtual environment operations, testing (`pytest`), linting (`flake8`, `ruff`, `black`), and local script validation.
- **Git:** Repository status, diffs, staging, semantic commits (`git add`, `git commit`, `git status`, `git log`).
- **Terraform:** Formatting, syntax checking, and static validation (`terraform fmt`, `terraform validate`).
- **Docker:** Local daemon checks, configuration verification (`docker compose config`), Dockerfile linting, and local image builds.
- **File System:** Creating, editing, and reading files inside `C:\AI-DevOps`.

## 3. Autonomous Problem Solving & Self-Healing
- Autonomously inspect error logs, apply code/configuration fixes, and re-test.
- Do not stop for manual approval between development phases (scaffolding -> code generation -> containerization -> testing -> CI/CD -> IaC).
- Only halt and prompt the user when a genuine external blocker occurs (e.g., GitHub remote authentication credentials, AWS account authorization, or explicit financial approvals).
