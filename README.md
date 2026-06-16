# LLM Jailbreak CTF Platform — Secure CI/CD Demo

This repository contains a small full-stack LLM security project used to demonstrate a security-focused CI/CD pipeline with GitHub Actions.

The application is an LLM Jailbreak CTF-style platform built with React, FastAPI, and OpenAI. Users interact with progressively secured levels and attempt to extract a hidden secret from the model. The application itself is intentionally lightweight because the main focus of this repository is the CI/CD pipeline, security checks, and deployment workflow.

## Tech Stack

* Frontend: React + Vite
* Backend: FastAPI + Python
* AI integration: OpenAI API
* CI/CD: GitHub Actions
* Deployment target: GitHub Container Registry
* Security tooling: Bandit, pip-audit, npm audit, Gitleaks, Trivy

## GitHub Actions Workflows

### 1. CI and Security Checks

Workflow: `.github/workflows/ci-security.yml`

This workflow runs on pushes and pull requests to `main`.

It performs:

* Backend dependency installation
* Backend API tests with pytest
* Python static security scanning with Bandit
* Python dependency auditing with pip-audit
* Frontend dependency installation
* Frontend dependency audit with npm audit
* React production build
* Secret scanning with Gitleaks

The goal is to catch common issues before code is merged or deployed.

### 2. Build, Scan, and Publish Container

Workflow: `.github/workflows/docker-publish.yml`

This workflow runs on pushes to `main` and can also be triggered manually.

It performs:

* Docker image build for the FastAPI backend
* Container vulnerability scanning with Trivy
* Publishing the container image to GitHub Container Registry

This acts as the deploy step for the challenge.

## Security Choices

The pipeline includes multiple security controls:

* Bandit checks Python code for common insecure patterns.
* pip-audit checks Python dependencies for known vulnerabilities.
* npm audit checks frontend dependencies for high-severity issues.
* Gitleaks scans the repository for accidentally committed secrets.
* Trivy scans the container image for high and critical vulnerabilities before publishing.
* GitHub Actions permissions are kept minimal, with package write permissions only used in the container publishing workflow.
* The application keeps secret values server-side and does not expose hidden level secrets through the public `/api/levels` endpoint.

## Running Locally

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn main:app --reload --port 8000
```

Create a local `.env` file based on `.env.example`:

```env
OPENAI_API_KEY=your_local_api_key_here
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173` and calls the backend at `http://127.0.0.1:8000`.

## Docker

Build the backend image locally:

```bash
cd backend
docker build -t llm-ctf-backend .
docker run -p 8000:8000 llm-ctf-backend
```

## Future Improvements

If this were production-bound, I would add branch protection rules, required status checks, pinned GitHub Actions by commit SHA, signed container images, SBOM generation, deployment environments with approvals, runtime monitoring, rate limiting, and stronger authentication/authorization controls.
