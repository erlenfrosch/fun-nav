from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

ROOT = Path(__file__).parent.parent
BACKEND_APP = ROOT / "backend" / "app"

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_ok(self):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}


class TestCORS:
    def test_cors_allows_frontend_origin(self):
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.headers.get("access-control-allow-origin") in (
            "http://localhost:5173",
            "*",
        )


class TestBackendStructure:
    def test_routers_directory_exists(self):
        assert (BACKEND_APP / "routers").is_dir()

    def test_services_directory_exists(self):
        assert (BACKEND_APP / "services").is_dir()

    def test_models_directory_exists(self):
        assert (BACKEND_APP / "models").is_dir()

    def test_routers_has_init(self):
        assert (BACKEND_APP / "routers" / "__init__.py").exists()

    def test_services_has_init(self):
        assert (BACKEND_APP / "services" / "__init__.py").exists()

    def test_models_has_init(self):
        assert (BACKEND_APP / "models" / "__init__.py").exists()


class TestRequirements:
    def test_pydantic_in_requirements(self):
        reqs = (ROOT / "backend" / "requirements.txt").read_text()
        assert "pydantic" in reqs

    def test_fastapi_in_requirements(self):
        reqs = (ROOT / "backend" / "requirements.txt").read_text()
        assert "fastapi" in reqs

    def test_uvicorn_in_requirements(self):
        reqs = (ROOT / "backend" / "requirements.txt").read_text()
        assert "uvicorn" in reqs

    def test_httpx_in_requirements(self):
        reqs = (ROOT / "backend" / "requirements.txt").read_text()
        assert "httpx" in reqs
