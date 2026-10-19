"""
Tests unitarios del endpoint GET /health.

No usan base de datos ni red (tests/unit, según AGENTS.md).
El fixture aislar_config (conftest.py) garantiza:
  - cwd apunta a un directorio temporal vacío (sin .env).
  - la caché de obtener_config() se limpia antes y después de cada test.
"""

import importlib
import sys

from starlette.testclient import TestClient

from app.core.config import obtener_config


def test_health_sin_variables_de_entorno(monkeypatch):
    """
    GET /health responde 200 {"estado": "ok"} aunque DATABASE_URL y
    ADMIN_API_KEY no estén en el entorno, y no llama a obtener_config()
    (la caché permanece vacía después de la llamada).
    """
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)
    # Forzar reimportación fresca para que el test no dependa del orden
    monkeypatch.delitem(sys.modules, "app.main", raising=False)

    modulo = importlib.import_module("app.main")
    cliente = TestClient(modulo.app)

    respuesta = cliente.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}
    assert obtener_config.cache_info().currsize == 0
