"""
Tests unitarios de app/core/config.py.

Ningún test lee el archivo .env real ni abre conexión de red.
El fixture aislar_config (conftest.py) garantiza:
  - cwd apunta a un directorio temporal vacío (sin .env).
  - la caché de obtener_config() se limpia antes y después de cada test.
"""

import pytest
from pydantic import ValidationError

from app.core.config import obtener_config


def test_config_con_variables_validas(monkeypatch):
    """obtener_config() devuelve los valores inyectados por monkeypatch."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake/db")
    monkeypatch.setenv("ADMIN_API_KEY", "clave-falsa")

    config = obtener_config()

    assert config.DATABASE_URL.get_secret_value() == "postgresql://fake/db"
    assert config.ADMIN_API_KEY.get_secret_value() == "clave-falsa"


def test_secretstr_no_expone_valor(monkeypatch):
    """SecretStr nunca imprime el valor real en str() ni en repr()."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake/db")
    monkeypatch.setenv("ADMIN_API_KEY", "clave-super-secreta")

    config = obtener_config()

    assert "clave-super-secreta" not in str(config.ADMIN_API_KEY)
    assert "clave-super-secreta" not in repr(config.ADMIN_API_KEY)
    assert "clave-super-secreta" not in repr(config)


def test_sin_variables_lanza_validation_error(monkeypatch):
    """Sin DATABASE_URL ni ADMIN_API_KEY, obtener_config() lanza ValidationError."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)

    with pytest.raises(ValidationError):
        obtener_config()


def test_variables_extra_son_ignoradas():
    """Con extra='ignore', una clave no declarada en el .env no causa error.

    Las variables de entorno desconocidas no pasan por la validación 'extra'
    de pydantic-settings; el caso que importa es un archivo .env con una
    clave no declarada. El fixture aislar_config ya cambió el cwd a un
    directorio temporal vacío, así que el .env que creamos aquí no es el real.
    """
    import pathlib

    pathlib.Path(".env").write_text(
        "DATABASE_URL=postgresql://fake/db\n"
        "ADMIN_API_KEY=clave-falsa\n"
        "VARIABLE_DESCONOCIDA=valor-extra\n",
        encoding="utf-8",
    )

    config = obtener_config()  # no debe lanzar ValidationError

    assert config.DATABASE_URL.get_secret_value() == "postgresql://fake/db"
    assert not hasattr(config, "VARIABLE_DESCONOCIDA")
