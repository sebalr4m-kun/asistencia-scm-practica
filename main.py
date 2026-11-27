import subprocess
import sys

from fastapi import FastAPI
import uvicorn


def ensure_packages() -> None:
    """Verifica e instala las dependencias necesarias en el entorno."""
    required = ["fastapi", "uvicorn", "jinja2", "python-multipart"]
    for pkg in required:
        mod_name = pkg.replace("-", "_") if pkg == "python-multipart" else pkg
        try:
            __import__(mod_name)
        except ImportError:
            print(f"[SETUP] Instalando {pkg}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"]
            )
            print(f"[SETUP] {pkg} listo.")


ensure_packages()

from alumnos import router as alumnos_router  # noqa: E402
from asistencia import router as asistencia_router  # noqa: E402
from auth import router as auth_router  # noqa: E402
from cursos import router as cursos_router  # noqa: E402
from database import alumnos, asistencia_por_dia, hoy  # noqa: E402
from docentes import router as docentes_router  # noqa: E402
from frontend import router as frontend_router  # noqa: E402

app = FastAPI(
    title="Sistema de Asistencia Escolar",
    description=(
        "Registro de alumnos + control de asistencia diario "
        "con historial inmutable"
    ),
    version="1.0.0",
)

app.include_router(frontend_router)
app.include_router(auth_router)
app.include_router(alumnos_router)
app.include_router(docentes_router)
app.include_router(cursos_router)
app.include_router(asistencia_router)


@app.get("/api")
def api_root() -> dict:
    """Devuelve el estado general y métricas básicas de la API."""
    return {
        "sistema": "Gestión de Asistencia",
        "version": "1.0.0",
        "fecha_servidor": hoy(),
        "alumnos_registrados": len(alumnos),
        "dias_con_asistencia": len(asistencia_por_dia),
    }


if __name__ == "__main__":
    print("Iniciando Sistema de Asistencia en http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)