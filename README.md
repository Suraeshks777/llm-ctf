# LLM Jailbreak CTF Platform

This is a small full-stack project I used to demonstrate a security-focused CI/CD pipeline with GitHub Actions.

The application has a React frontend and a FastAPI backend. Users interact with several LLM challenge levels where the goal is to test how prompt-based defenses behave under adversarial input. The application is intentionally lightweight because the focus of this repository is the pipeline.

## Pipeline

I added two GitHub Actions workflows.

### CI and Security Checks

This workflow runs on pushes and pull requests to `main`.

It does the following:

- Runs FastAPI tests with pytest
- Builds the React frontend
- Runs Bandit against the Python backend
- Runs pip-audit against Python dependencies
- Runs npm audit against frontend dependencies
- Runs Gitleaks to check for committed secrets

The test and build steps are blocking. The audit tools are currently report-only so the pipeline remains reproducible for this exercise. In a production setup, I would make high or critical findings blocking after triage.

### Build, Scan, and Publish Container

This workflow builds the backend Docker image, scans it with Trivy, and publishes it to GitHub Container Registry.

## Running Locally

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn main:app --reload --port 8000