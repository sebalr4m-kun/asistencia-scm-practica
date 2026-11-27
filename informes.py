"""Módulo de informes de asistencia."""

from fastapi import APIRouter, Request

from auth import require_auth
from database import asistencia_por_dia

router = APIRouter(tags=["Informes"])


@router.get("/api/informe/{dni}")
def informe_por_dni(dni: str, request: Request) -> list:
    """Devuelve el historial de asistencia de un alumno por su DNI."""
    require_auth(request)
    dni = dni.strip()
    if not dni:
        return []
    resultados = []
    for fecha in sorted(asistencia_por_dia.keys(), reverse=True):
        for reg in asistencia_por_dia[fecha]:
            if reg["dni"] == dni:
                resultados.append({
                    "fecha": fecha,
                    "estado": reg["estado"],
                    "hora": reg["hora"],
                })
    return resultados
