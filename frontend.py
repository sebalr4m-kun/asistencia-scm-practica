"""Módulo de interfaz web (HTML/CSS/JS) para el Sistema de Asistencia."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML_BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sistema de Asistencia</title>
<style>
:root {
    --bg: #0f172a;
    --card: #1e293b;
    --accent: #38bdf8;
    --accent2: #22c55e;
    --danger: #ef4444;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --border: #334155;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: var(--text);
    min-height: 100vh;
    padding: 20px;
}
.container { max-width: 1100px; margin: 0 auto; }
header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border);
}
h1 { font-size: 1.6rem; color: var(--accent); }
h2 { font-size: 1.25rem; margin-bottom: 12px; color: var(--accent2); }
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }
label { display: block; margin-bottom: 6px; font-size: 0.9rem; color: var(--muted); }
input, select, button {
    width: 100%; padding: 10px 14px; border-radius: 8px;
    border: 1px solid var(--border); background: #0f172a; color: var(--text);
    font-size: 1rem; margin-bottom: 12px;
}
input:focus, select:focus { outline: 2px solid var(--accent); border-color: transparent; }
button {
    background: var(--accent); color: #0f172a; font-weight: 600;
    cursor: pointer; border: none; transition: all 0.2s;
}
button:hover { background: #7dd3fc; transform: translateY(-1px); }
button.secondary { background: #475569; color: white; }
button.danger { background: var(--danger); color: white; }
button.success { background: var(--accent2); color: #0f172a; }
.msg { padding: 10px 14px; border-radius: 8px; margin-bottom: 12px; font-size: 0.95rem; }
.msg.ok { background: #14532d; border: 1px solid #22c55e; }
.msg.err { background: #7f1d1d; border: 1px solid #ef4444; }
.msg.info { background: #1e3a5f; border: 1px solid #38bdf8; }
table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); }
th { color: var(--muted); font-weight: 600; }
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600;
}
.badge.presente { background: #14532d; color: #4ade80; }
.badge.tardanza { background: #713f12; color: #fbbf24; }
.badge.ausente { background: #7f1d1d; color: #f87171; }
.historial { max-height: 320px; overflow-y: auto; }
.historial-item { margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px dashed var(--border); }
.historial-item h3 { font-size: 1rem; color: var(--accent); margin-bottom: 8px; }
.hidden { display: none !important; }
#auth-section, #main-section { animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
.user-bar { display: flex; gap: 12px; align-items: center; }
.user-bar span { color: var(--muted); font-size: 0.9rem; }
.small { font-size: 0.85rem; color: var(--muted); }
</style>
</head>
<body>
<div class="container">
    <!-- ========== AUTH ========== -->
    <div id="auth-section">
        <header>
            <h1>Sistema de Asistencia</h1>
        </header>
        <div class="grid">
            <div class="card">
                <h2>Crear cuenta (Sign In)</h2>
                <p class="small" style="margin-bottom:12px;">Solo nombre de usuario único. Sin contraseña (requisito del laboratorio).</p>
                <div id="msg-signup"></div>
                <label>Nombre de usuario</label>
                <input type="text" id="signup-user" placeholder="Ej: profesor1" maxlength="30" autocomplete="off">
                <button onclick="hacerSignIn()">Crear cuenta</button>
            </div>
            <div class="card">
                <h2>Iniciar sesión (Login)</h2>
                <div id="msg-login"></div>
                <label>Nombre de usuario</label>
                <input type="text" id="login-user" placeholder="Tu usuario" maxlength="30" autocomplete="off">
                <button class="success" onclick="hacerLogin()">Entrar</button>
            </div>
        </div>
    </div>

    <!-- ========== MAIN ========== -->
    <div id="main-section" class="hidden">
        <header>
            <h1>Sistema de Asistencia</h1>
            <div class="user-bar">
                <span id="user-display"></span>
                <button class="secondary" style="width:auto;padding:8px 16px;" onclick="hacerLogout()">Log Out</button>
            </div>
        </header>

        <div class="grid">
            <!-- Alta de alumno -->
            <div class="card">
                <h2>Alta de alumno</h2>
                <div id="msg-alta"></div>
                <label>Nombre completo</label>
                <input type="text" id="nuevo-nombre" placeholder="Apellido Nombre" maxlength="80">
                <label>DNI (solo números, sin espacios ni caracteres especiales)</label>
                <input type="text" id="nuevo-dni" placeholder="40123456" maxlength="10" inputmode="numeric">
                <button onclick="altaAlumno()">Registrar alumno</button>
            </div>

            <!-- Control de asistencia -->
            <div class="card">
                <h2>Control de asistencia (hoy: <span id="fecha-hoy"></span>)</h2>
                <div id="msg-asistencia"></div>
                <label>Inserte DNI</label>
                <input type="text" id="asistencia-dni" placeholder="Escribe el DNI completo" maxlength="10" inputmode="numeric"
                       oninput="verificarDNI()">
                <div id="dni-feedback" class="msg info hidden"></div>
                <div id="opciones-asistencia" class="hidden">
                    <label>Estado</label>
                    <select id="asistencia-estado">
                        <option value="Presente">Presente</option>
                        <option value="Tardanza">Tardanza</option>
                        <option value="Ausente">Ausente</option>
                    </select>
                    <button class="success" onclick="guardarAsistencia()">GUARDAR</button>
                </div>
            </div>
        </div>

        <!-- Listado del día -->
        <div class="card">
            <h2>Listado de hoy</h2>
            <div id="listado-hoy"></div>
        </div>

        <!-- Historial por días (inmutable) -->
        <div class="card">
            <h2>Historial de días anteriores (inmutable, orden descendente)</h2>
            <div id="historial" class="historial"></div>
        </div>

        <!-- Informe por DNI -->
        <div class="card">
            <h2>Informe de asistencia por alumno (por DNI)</h2>
            <p class="small">Escribe un DNI para ver todas las inserciones históricas. Vacía el campo para limpiar el informe.</p>
            <label>DNI a consultar</label>
            <input type="text" id="informe-dni" placeholder="DNI del alumno" maxlength="10" inputmode="numeric"
                   oninput="generarInforme()">
            <div id="informe-resultado"></div>
        </div>
    </div>
</div>

<script>
const API = window.location.origin;
let tokenActual = localStorage.getItem("asistencia_token") || "";
let usuarioActual = localStorage.getItem("asistencia_user") || "";

// ---------- Auth ----------
async function hacerSignIn() {
    const user = document.getElementById("signup-user").value.trim();
    const msg = document.getElementById("msg-signup");
    if (!user) { msg.innerHTML = '<div class="msg err">Usuario obligatorio</div>'; return; }
    try {
        const r = await fetch(API + "/api/signup", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: user})
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Error");
        msg.innerHTML = '<div class="msg ok">Cuenta creada. Ahora puedes hacer Login.</div>';
        document.getElementById("signup-user").value = "";
    } catch (e) {
        msg.innerHTML = `<div class="msg err">${e.message}</div>`;
    }
}

async function hacerLogin() {
    const user = document.getElementById("login-user").value.trim();
    const msg = document.getElementById("msg-login");
    if (!user) { msg.innerHTML = '<div class="msg err">Usuario obligatorio</div>'; return; }
    try {
        const r = await fetch(API + "/api/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: user})
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Error");
        tokenActual = data.token;
        usuarioActual = data.username;
        localStorage.setItem("asistencia_token", tokenActual);
        localStorage.setItem("asistencia_user", usuarioActual);
        mostrarMain();
    } catch (e) {
        msg.innerHTML = `<div class="msg err">${e.message}</div>`;
    }
}

function hacerLogout() {
    tokenActual = "";
    usuarioActual = "";
    localStorage.removeItem("asistencia_token");
    localStorage.removeItem("asistencia_user");
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("main-section").classList.add("hidden");
    document.getElementById("login-user").value = "";
}

function mostrarMain() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("main-section").classList.remove("hidden");
    document.getElementById("user-display").textContent = "Usuario: " + usuarioActual;
    document.getElementById("fecha-hoy").textContent = new Date().toLocaleDateString("es-AR");
    cargarListadoHoy();
    cargarHistorial();
}

// ---------- Alumnos ----------
async function altaAlumno() {
    const nombre = document.getElementById("nuevo-nombre").value.trim();
    const dni = document.getElementById("nuevo-dni").value.trim();
    const msg = document.getElementById("msg-alta");
    if (!nombre || !dni) {
        msg.innerHTML = '<div class="msg err">Nombre y DNI son obligatorios</div>';
        return;
    }
    if (/\s/.test(dni) || !/^\d+$/.test(dni)) {
        msg.innerHTML = '<div class="msg err">DNI: solo números, sin espacios ni caracteres especiales</div>';
        return;
    }
    try {
        const r = await fetch(API + "/api/alumnos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Token": tokenActual
            },
            body: JSON.stringify({nombre, dni})
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Error");
        msg.innerHTML = '<div class="msg ok">Alumno registrado correctamente</div>';
        document.getElementById("nuevo-nombre").value = "";
        document.getElementById("nuevo-dni").value = "";
    } catch (e) {
        msg.innerHTML = `<div class="msg err">${e.message}</div>`;
    }
}

// ---------- Asistencia ----------
let alumnoEncontrado = null;

async function verificarDNI() {
    const dni = document.getElementById("asistencia-dni").value.trim();
    const feedback = document.getElementById("dni-feedback");
    const opts = document.getElementById("opciones-asistencia");
    alumnoEncontrado = null;
    opts.classList.add("hidden");
    if (dni.length < 7) {
        feedback.classList.add("hidden");
        return;
    }
    try {
        const r = await fetch(API + "/api/alumnos/" + encodeURIComponent(dni), {
            headers: {"X-Token": tokenActual}
        });
        if (r.status === 404) {
            feedback.className = "msg err";
            feedback.textContent = "El alumno no existe";
            feedback.classList.remove("hidden");
            return;
        }
        if (!r.ok) throw new Error("Error de servidor");
        const data = await r.json();
        alumnoEncontrado = data;
        feedback.className = "msg ok";
        feedback.textContent = `Alumno encontrado: ${data.nombre}`;
        feedback.classList.remove("hidden");
        opts.classList.remove("hidden");
    } catch (e) {
        feedback.className = "msg err";
        feedback.textContent = e.message;
        feedback.classList.remove("hidden");
    }
}

async function guardarAsistencia() {
    if (!alumnoEncontrado) return;
    const estado = document.getElementById("asistencia-estado").value;
    const msg = document.getElementById("msg-asistencia");
    try {
        const r = await fetch(API + "/api/asistencia", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Token": tokenActual
            },
            body: JSON.stringify({dni: alumnoEncontrado.dni, estado})
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Error");
        msg.innerHTML = `<div class="msg ok">Asistencia registrada: ${estado}</div>`;
        document.getElementById("asistencia-dni").value = "";
        document.getElementById("dni-feedback").classList.add("hidden");
        document.getElementById("opciones-asistencia").classList.add("hidden");
        alumnoEncontrado = null;
        cargarListadoHoy();
        cargarHistorial();
    } catch (e) {
        msg.innerHTML = `<div class="msg err">${e.message}</div>`;
    }
}

async function cargarListadoHoy() {
    const cont = document.getElementById("listado-hoy");
    try {
        const r = await fetch(API + "/api/asistencia/hoy", {headers: {"X-Token": tokenActual}});
        const data = await r.json();
        if (!data.length) {
            cont.innerHTML = '<p class="small">Todavía no hay registros para hoy.</p>';
            return;
        }
        let html = '<table><thead><tr><th>DNI</th><th>Nombre</th><th>Estado</th><th>Hora</th></tr></thead><tbody>';
        data.forEach(reg => {
            const cls = reg.estado.toLowerCase();
            html += `<tr>
                <td>${reg.dni}</td>
                <td>${reg.nombre}</td>
                <td><span class="badge ${cls}">${reg.estado}</span></td>
                <td>${reg.hora}</td>
            </tr>`;
        });
        html += '</tbody></table>';
        cont.innerHTML = html;
    } catch (e) {
        cont.innerHTML = '<p class="msg err">Error al cargar listado</p>';
    }
}

async function cargarHistorial() {
    const cont = document.getElementById("historial");
    try {
        const r = await fetch(API + "/api/asistencia/historial", {headers: {"X-Token": tokenActual}});
        const data = await r.json();
        if (!data.length) {
            cont.innerHTML = '<p class="small">No hay días anteriores registrados.</p>';
            return;
        }
        let html = "";
        data.forEach(dia => {
            html += `<div class="historial-item">
                <h3>${dia.fecha} (${dia.registros.length} registros)</h3>
                <table><thead><tr><th>DNI</th><th>Nombre</th><th>Estado</th><th>Hora</th></tr></thead><tbody>`;
            dia.registros.forEach(reg => {
                const cls = reg.estado.toLowerCase();
                html += `<tr>
                    <td>${reg.dni}</td>
                    <td>${reg.nombre}</td>
                    <td><span class="badge ${cls}">${reg.estado}</span></td>
                    <td>${reg.hora}</td>
                </tr>`;
            });
            html += '</tbody></table></div>';
        });
        cont.innerHTML = html;
    } catch (e) {
        cont.innerHTML = '<p class="msg err">Error al cargar historial</p>';
    }
}

async function generarInforme() {
    const dni = document.getElementById("informe-dni").value.trim();
    const cont = document.getElementById("informe-resultado");
    if (!dni) {
        cont.innerHTML = "";
        return;
    }
    try {
        const r = await fetch(API + "/api/informe/" + encodeURIComponent(dni), {
            headers: {"X-Token": tokenActual}
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Error");
        if (!data.length) {
            cont.innerHTML = '<div class="msg info">No se encontraron registros de asistencia para este DNI.</div>';
            return;
        }
        let html = '<table><thead><tr><th>Fecha</th><th>Estado</th><th>Hora</th></tr></thead><tbody>';
        data.forEach(reg => {
            const cls = reg.estado.toLowerCase();
            html += `<tr>
                <td>${reg.fecha}</td>
                <td><span class="badge ${cls}">${reg.estado}</span></td>
                <td>${reg.hora}</td>
            </tr>`;
        });
        html += '</tbody></table>';
        cont.innerHTML = html;
    } catch (e) {
        cont.innerHTML = `<div class="msg err">${e.message}</div>`;
    }
}

// ---------- Init ----------
if (tokenActual && usuarioActual) {
    // Verificar que el token siga válido
    fetch(API + "/api/me", {headers: {"X-Token": tokenActual}})
        .then(r => {
            if (r.ok) mostrarMain();
            else hacerLogout();
        })
        .catch(() => hacerLogout());
}
</script>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    """Devuelve la interfaz HTML principal del sistema."""
    return HTMLResponse(content=HTML_BASE)
