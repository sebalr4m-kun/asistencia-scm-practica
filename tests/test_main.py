"""Pruebas unitarias iniciales del servidor FastAPI."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_api_root_responde_ok() -> None:
    """Verifica que el endpoint raíz /api devuelva estado 200."""
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert data["sistema"] == "Gestión de Asistencia"
