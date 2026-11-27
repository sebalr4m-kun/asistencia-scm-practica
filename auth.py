"""Endpoints y utilidades de autenticación básica en memoria."""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Request

from database import sesiones_activas, usuarios

router = APIRouter()


@router.post("/api/signup")
def signup(payload: dict) -> dict:
    """Registra un nuevo nombre de usuario único."""
    username = (payload.get("username") or "").strip()
    if not username:
        raise HTTPException(status_code=400, detail="Usuario obligatorio")
    if len(username) < 2 or len(username) > 30:
        raise HTTPException(
            status_code=400, detail="Usuario entre 2 y 30 caracteres"
        )
    if username in usuarios:
        raise HTTPException(
            status_code=400, detail="Ese nombre de usuario ya existe"
        )
    usuarios.add(username)
    return {"ok": True, "username": username}


@router.post("/api/login")
def login(payload: dict) -> dict:
    """Inicia sesión y devuelve un token simple en memoria."""
    username = (payload.get("username") or "").strip()
    if not username:
        raise HTTPException(status_code=400, detail="Usuario obligatorio")
    if username not in usuarios:
        raise HTTPException(
            status_code=401,
            detail="Usuario no registrado. Crea una cuenta primero.",
        )
    token = f"tok_{username}_{datetime.now().timestamp()}"
    sesiones_activas[token] = username
    return {"token": token, "username": username}


@router.get("/api/me")
def me(request: Request) -> dict:
    """Verifica la sesión activa mediante cabecera X-Token."""
    token = request.headers.get("X-Token") or ""
    if token not in sesiones_activas:
        raise HTTPException(status_code=401, detail="Sesión inválida")
    return {"username": sesiones_activas[token]}


def require_auth(request: Request) -> str:
    """Valida que la petición tenga una sesión activa."""
    token = request.headers.get("X-Token") or ""
    if token not in sesiones_activas:
        raise HTTPException(status_code=401, detail="Debes iniciar sesión")
    return sesiones_activas[token]
