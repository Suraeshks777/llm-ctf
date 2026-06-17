import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Ensure backend directory is available in Python path during GitHub Actions
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_levels_endpoint_returns_levels_without_secrets():
    response = client.get("/api/levels")

    assert response.status_code == 200

    levels = response.json()
    assert isinstance(levels, list)
    assert len(levels) >= 1

    first_level = levels[0]

    assert "id" in first_level
    assert "name" in first_level
    assert "description" in first_level
    assert "difficulty" in first_level

    assert "secret_password" not in first_level
    assert "system_prompt" not in first_level