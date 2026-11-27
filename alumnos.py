"""Rutas y operaciones CRUD para la gestión de alumnos."""

from fastapi import APIRouter, HTTPException, Request

from auth import require_auth
from database import alumnos
from models import AlumnoCreate

router = APIRouter(prefix="/api/alumnos", tags=["alumnos"])


@router.post("", status_code=201)
def crear_alumno(alumno: AlumnoCreate, request: Request) -> dict:
    """Registra un nuevo alumno validando que su DNI sea único."""
    require_auth(request)
    if alumno.dni in alumnos:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un alumno con ese DNI (debe ser único)",
        )
    alumnos[alumno.dni] = {"nombre": alumno.nombre, "dni": alumno.dni}
    return alumnos[alumno.dni]


@router.get("/{dni}")
def obtener_alumno(dni: str, request: Request) -> dict:
    """Obtiene los datos de un alumno registrado a partir de su DNI."""
    require_auth(request)
    dni_limpio = dni.strip()
    if dni_limpio not in alumnos:
        raise HTTPException(status_code=404, detail="El alumno no existe")
    return alumnos[dni_limpio]


@router.get("")
def listar_alumnos(request: Request) -> list:
    """Devuelve el listado completo de alumnos registrados."""
    require_auth(request)
    return list(alumnos.values())
