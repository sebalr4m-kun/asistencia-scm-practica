"""Base de datos en memoria para el Sistema de Asistencia Escolar."""

from datetime import date
from typing import Dict, List, Optional, Set

# Usuarios (solo nombre, sin contraseña – requisito de la consigna)
usuarios: Set[str] = set()

# Alumnos: dni -> {"nombre": str, "dni": str}
alumnos: Dict[str, dict] = {}

# Asistencia por día:
# "YYYY-MM-DD" -> list[{"dni": str, "nombre": str, "estado": str, "hora": str}]
asistencia_por_dia: Dict[str, List[dict]] = {}

# Sesión simple en memoria: token_simple -> username
sesiones_activas: Dict[str, str] = {}


def hoy() -> str:
    """Devuelve la fecha actual del servidor en formato ISO (YYYY-MM-DD)."""
    return date.today().isoformat()


def obtener_o_crear_dia(fecha: Optional[str] = None) -> List[dict]:
    """Obtiene la lista de registros de un día o la inicializa si no existe."""
    fecha_objetivo = fecha or hoy()
    if fecha_objetivo not in asistencia_por_dia:
        asistencia_por_dia[fecha_objetivo] = []
    return asistencia_por_dia[fecha_objetivo]
