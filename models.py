"""Modelos Pydantic y validadores del Sistema de Asistencia Escolar."""

import re

from pydantic import BaseModel, Field, field_validator


class AlumnoCreate(BaseModel):
    """Esquema de validación para el alta de un alumno."""

    nombre: str = Field(..., min_length=2, max_length=80)
    dni: str = Field(..., min_length=7, max_length=10)

    @field_validator("dni")
    @classmethod
    def validar_dni(cls, v: str) -> str:
        """Valida que el DNI tenga solo dígitos y sin espacios."""
        v = v.strip()
        if " " in v:
            raise ValueError("El DNI no puede contener espacios")
        if not v.isdigit():
            raise ValueError(
                "El DNI solo puede contener números "
                "(sin caracteres especiales)"
            )
        return v

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        """Valida que el nombre contenga únicamente letras y espacios."""
        v = v.strip()
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\s]+$", v):
            raise ValueError("El nombre solo puede contener letras y espacios")
        return v


class AsistenciaRegistro(BaseModel):
    """Esquema de validación para el registro de asistencia diaria."""

    dni: str
    estado: str  # Presente | Tardanza | Ausente

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        """Valida que el estado pertenezca a las opciones permitidas."""
        if v not in {"Presente", "Tardanza", "Ausente"}:
            raise ValueError("Estado inválido")
        return v
