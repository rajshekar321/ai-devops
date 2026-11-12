# AI-DevOps: Autonomous Cloud Application & Pipeline

[![CI](https://github.com/your-org/ai-devops/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/ai-devops/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.5+-purple.svg)](https://www.terraform.io/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)

An end-to-end, production-grade DevOps automation platform. Enables generating full-stack services, running automated test cycles, building multi-stage containers, provisioning secure AWS EC2 infrastructure using Terraform, and deploying automatically through GitHub Actions with passwordless IAM OIDC and AWS Systems Manager (SSM).

---

## Key Features

- **Backend:** Python FastAPI with asynchronous endpoints, Pydantic v2 schemas, and SQLAlchemy ORM.
- **Frontend Dashboard:** Built-in responsive dark-mode control center for real-time health monitoring, DevOps task tracking, and deployment logs.
- **Database:** PostgreSQL 16 containerized with automatic schema initialization and SQLite fallback for local/test isolation.
- **Containerization:** Multi-stage `Dockerfile` with non-root security context, layer caching, and healthcheck probes.
- **Infrastructure as Code (IaC):** Modular Terraform configurations for AWS EC2 (Free-tier eligible default), VPC, Security Groups, and IAM roles.
- **Zero-Secret CI/CD:** GitHub Actions workflows with OpenID Connect (OIDC) identity federation and zero-SSH remote execution via AWS Systems Manager.
- **Self-Healing Test Suite:** Fully automated pytest suite covering 100% of endpoints and integration flows.

---

## Directory Structure

```text
C:\AI-DevOps\
├── .agents/
│   └── rules/                  # Workspace autonomous execution policies
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI: Tests, linting, Docker build & TF validation
│       └── cd.yml              # CD: AWS EC2 automated deployment via SSM
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/      # Health, task & deployment routes
│   ├── static/                 # Frontend dashboard (HTML/CSS/JS)
│   ├── config.py               # Application configuration & env settings
│   ├── crud.py                 # Database access layer
│   ├── database.py             # Engine & session management
│   ├── main.py                 # FastAPI entrypoint
│   ├── models.py               # SQLAlchemy ORM models
│   └── schemas.py              # Pydantic v2 validation models
├── docs/
│   ├── ARCHITECTURE.md         # Detailed architectural diagram & system design
│   └── DEPLOYMENT_GUIDE.md     # Step-by-step setup for GitHub & AWS
├── scripts/
│   └── run_tests.py            # Local static analysis and pytest execution runner
├── terraform/
│   ├── ec2.tf                  # EC2 instance and Docker bootstrap user-data
│   ├── iam.tf                  # GitHub OIDC provider and EC2 SSM role
│   ├── main.tf                 # VPC and Security Group rules
│   ├── outputs.tf              # Public IP, DNS, and OIDC Role outputs
│   ├── variables.tf            # Configurable inputs
│   ├── versions.tf             # Terraform and AWS provider constraints
│   └── terraform.tfvars.example
├── tests/
│   ├── conftest.py             # Pytest fixtures and in-memory test database
│   ├── test_health.py          # Ping and health check unit tests
│   ├── test_integration.py     # End-to-end task and deployment lifecycle test
│   └── test_tasks.py           # CRUD API unit tests
├── .dockerignore
├── .env.example
├── .gitignore
├── AGENTS.md                   # Workspace agent execution policy
├── docker-compose.yml          # Local container orchestration (app + postgres)
├── Dockerfile                  # Multi-stage production container build
├── pyproject.toml              # Pytest and packaging metadata
└── requirements.txt            # Python dependencies
```

---

## Quick Start (Local Development)

### 1. Run Automated Test Suite
```powershell
python scripts/run_tests.py
```
Or directly via pytest:
```powershell
.\.venv\Scripts\pytest.exe -v tests/
```

### 2. Run with Docker Compose
```powershell
docker compose up -d --build
```
Access the application dashboard at: `http://localhost:8000`
API documentation (Swagger UI): `http://localhost:8000/docs`

---

## Documentation

- [System Architecture](file:///C:/AI-DevOps/docs/ARCHITECTURE.md)
- [Deployment & GitHub Actions Guide](file:///C:/AI-DevOps/docs/DEPLOYMENT_GUIDE.md)
