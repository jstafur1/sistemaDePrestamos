# AGENTS.md

## Contexto del proyecto
Es un sistema basado en el seguimiento de equipos de laboratorio los cuales son prestados; en este sistema se debe tener presente sus actores, sus equipos y categorías, como también sus plazos, entregas y retrasos de los mismos.

## Stack
Python 3.x, FastAPI, SQLAlchemy, PostgreSQL, Alembic

## Reglas de negocio (no negociables)
1. Solicitante con préstamo vencido no puede pedir otro equipo.
2. Equipo en mantenimiento no aparece como disponible.
3. El plazo de préstamo depende de la categoría, no del solicitante.
4. Devolución con novedad bloquea el equipo hasta liberación manual.

## Convenciones que debe seguir el agente

## Historial de correcciones al agente
