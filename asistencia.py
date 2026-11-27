"""Rutas y logica de control de asistencia e historial."""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Request

from auth import require_auth
from database import alumnos, asistencia_por_dia, hoy, obtener_o_crear_dia
from models import AsistenciaRegistro

router = APIRouter()


@router.post("/api/asistencia")
def registrar_asistencia(reg: AsistenciaRegistro, request: Request) -> dict:
    """Registra la asistencia diaria de un alumno sin duplicados por dia."""
    require_auth(request)
    dni = reg.dni.strip()
    if dni not in alumnos:
        raise HTTPException(status_code=404, detail="El alumno no existe")

    fecha = hoy()
    lista = obtener_o_crear_dia(fecha)
    for item in lista:
        if item["dni"] == dni:
            raise HTTPException(
                status_code=400,
                detail="Este alumno ya tiene asistencia registrada hoy",
            )

    hora = datetime.now().strftime("%H:%M:%S")
    registro = {
        "dni": dni,
        "nombre": alumnos[dni]["nombre"],
        "estado": reg.estado,
        "hora": hora,
    }
    lista.append(registro)
    return registro


@router.get("/api/asistencia/hoy")
def asistencia_hoy(request: Request) -> list:
    """Devuelve los registros de asistencia del dia actual."""
    require_auth(request)
    return obtener_o_crear_dia(hoy())


@router.get("/api/asistencia/historial")
def historial_asistencia(request: Request) -> list:
    """Devuelve el historial inmutable de dias anteriores en orden descendente."""
    require_auth(request)
    hoy_str = hoy()
    dias = []
    for fecha in sorted(asistencia_por_dia.keys(), reverse=True):
        if fecha < hoy_str:
            dias.append(
                {
                    "fecha": fecha,
                    "registros": asistencia_por_dia[fecha],
                }
            )
    return dias


@router.get("/api/informe/{dni}")
def informe_por_dni(dni: str, request: Request) -> list:
    """Devuelve todas las inserciones historicas de asistencia para un DNI."""
    require_auth(request)
    dni = dni.strip()
    if not dni:
        return []
    resultados = []
    for fecha in sorted(asistencia_por_dia.keys(), reverse=True):
        for reg in asistencia_por_dia[fecha]:
            if reg["dni"] == dni:
                resultados.append(
                    {
                        "fecha": fecha,
                        "estado": reg["estado"],
                        "hora": reg["hora"],
                    }
                )
    return resultados
