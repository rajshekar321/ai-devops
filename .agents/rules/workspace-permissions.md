# Autonomous Workspace Operations and Execution Permissions

## 1. Scope & Execution Authorization
This workspace is authorized for end-to-end autonomous DevOps engineering.
- **Root Directory:** `C:\AI-DevOps`
- **File Operations:** Full authorization to create directories, create source code, configuration files, Dockerfiles, Terraform scripts, GitHub Actions workflows, tests, and documentation.
- **Command Execution:** Full authorization to run Python runtime checks, virtual environment operations, dependency verification, pytest test suites, linters, Terraform format/validate, Docker build/config, and Git status/staging/commits.
- **Autonomous Progress:** Proceed seamlessly through development, testing, fixing, containerization, and configuration phases without prompting for routine file or command approvals.

## 2. Hard Boundaries & Security Guardrails
- **File System Boundary:** All read, write, and command operations must remain strictly inside `C:\AI-DevOps`. Modifying or reading files outside `C:\AI-DevOps` is forbidden.
- **Destructive Commands:** Prohibited (no drive formatting, recursive system deletion, or terminating system services).
- **Secrets & Credentials:** Never invent, request, or commit real API keys, tokens, or AWS credentials. Use `.env.example` and environment variables.
- **Cost Protection:** Do NOT execute `terraform apply` or provision live paid AWS resources without explicit budget authorization. Offline validation (`terraform validate`, `terraform plan` with mocked state) is permitted.
