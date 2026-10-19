"""Aplicación FastAPI — punto de entrada del sistema de préstamo de equipos."""

from fastapi import FastAPI

app = FastAPI(title="Sistema de Préstamo de Equipos de Laboratorio")


@app.get("/health")
def health():
    """Comprueba que la API responde. No consulta la base de datos ni la configuración."""
    return {"estado": "ok"}
