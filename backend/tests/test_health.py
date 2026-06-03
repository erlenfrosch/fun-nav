from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_cors_header_for_frontend_origin():
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_health_cors_blocked_for_unknown_origin():
    response = client.get(
        "/health",
        headers={"Origin": "http://evil.example.com"},
    )
    assert response.headers.get("access-control-allow-origin") is None
