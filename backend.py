from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

app = FastAPI(
    title="API de Tareas - Usuario Único",
    description="API simple para gestionar tareas de un único usuario: crear, marcar como terminada y archivar.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 1. MODELOS DE DATOS
# ------------------------------------------------------------------------------

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., example="Juan Perez")

class UsuarioResponse(BaseModel):
    id: int
    nombre: str

class TareaCreate(BaseModel):
    titulo: str = Field(..., example="Estudiar FastAPI")
    descripcion: Optional[str] = Field(None, example="Repasar endpoints y Pydantic")

class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    terminada: bool
    archivada: bool

# ------------------------------------------------------------------------------
# 2. BASE DE DATOS EN MEMORIA
# ------------------------------------------------------------------------------

# Solo se permite UN usuario
db_usuario: Optional[Dict] = None

# Lista de tareas del usuario único
db_tareas: Dict[int, dict] = {}
current_tarea_id = 0

# ------------------------------------------------------------------------------
# 3. ENDPOINTS
# ------------------------------------------------------------------------------

@app.get("/")
def home():
    return {"mensaje": "API de Tareas - Usuario Único lista"}

# ---------- USUARIO ÚNICO ----------

@app.post("/usuario", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    global db_usuario
    if db_usuario is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario. Solo se permite un usuario único."
        )
    db_usuario = {"id": 1, "nombre": usuario.nombre}
    return db_usuario

@app.get("/usuario", response_model=UsuarioResponse)
def obtener_usuario():
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay ningún usuario registrado"
        )
    return db_usuario

# ---------- TAREAS ----------

@app.post("/tareas", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCreate):
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Primero debe crear el usuario único"
        )
    global current_tarea_id
    current_tarea_id += 1
    nueva_tarea = {
        "id": current_tarea_id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "terminada": False,
        "archivada": False
    }
    db_tareas[current_tarea_id] = nueva_tarea
    return nueva_tarea

@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas(incluir_archivadas: bool = False):
    """
    Por defecto solo muestra las tareas NO archivadas.
    Pasar ?incluir_archivadas=true para ver también las archivadas.
    """
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Primero debe crear el usuario único"
        )
    if incluir_archivadas:
        return list(db_tareas.values())
    return [t for t in db_tareas.values() if not t["archivada"]]

@app.patch("/tareas/{tarea_id}/terminar", response_model=TareaResponse)
def marcar_terminada(tarea_id: int):
    if tarea_id not in db_tareas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )
    tarea = db_tareas[tarea_id]
    if tarea["archivada"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede marcar como terminada una tarea ya archivada"
        )
    tarea["terminada"] = True
    return tarea

@app.patch("/tareas/{tarea_id}/archivar", response_model=TareaResponse)
def archivar_tarea(tarea_id: int):
    if tarea_id not in db_tareas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )
    tarea = db_tareas[tarea_id]
    if not tarea["terminada"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden archivar tareas que ya estén terminadas"
        )
    tarea["archivada"] = True
    return tarea