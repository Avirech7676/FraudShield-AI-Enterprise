from fastapi.testclient import TestClient
from app.api.main import app


def test_cors_configuration():
    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "https://fraudshield-frontend.vercel.app",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_allow_all_origins_wildcard():
    client = TestClient(app)
    response = client.options(
        "/predict",
        headers={
            "Origin": "https://random-client-domain.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
