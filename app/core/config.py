"""
Configuración tipada de la aplicación con pydantic-settings.

- DATABASE_URL y ADMIN_API_KEY se declaran como SecretStr: nunca aparecen
  en str() ni repr() de la configuración, lo que evita filtrarlos en logs.
- La función obtener_config() usa @lru_cache para carga perezosa: la
  instancia de Configuracion no se crea al importar el módulo, sino la
  primera vez que alguien llama a obtener_config(). Esto permite importar
  app.main sin que haya variables de entorno presentes (útil en tests).
- extra="ignore" descarta silenciosamente cualquier variable de entorno que
  no esté declarada en la clase, en lugar de lanzar un error.
"""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    DATABASE_URL: SecretStr
    ADMIN_API_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def obtener_config() -> Configuracion:
    """Devuelve la configuración de la aplicación (instancia única en caché)."""
    return Configuracion()
