"""Módulo de rutas para docentes (estructura base sin modificaciones)."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/docentes", tags=["docentes"])
