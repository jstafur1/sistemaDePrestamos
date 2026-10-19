"""
Fixtures globales de pytest.

aislar_config (autouse):
  - Cambia el directorio de trabajo a un directorio temporal vacío para que
    pydantic-settings no encuentre el archivo .env real del proyecto.
  - Limpia la caché de obtener_config() antes y después de cada test, de modo
    que cada test parte de una configuración nueva.
"""

import pytest

from app.core.config import obtener_config


@pytest.fixture(autouse=True)
def aislar_config(monkeypatch, tmp_path):
    """Evita que cualquier test lea el .env real y garantiza caché limpia."""
    obtener_config.cache_clear()
    monkeypatch.chdir(tmp_path)
    yield
    obtener_config.cache_clear()
