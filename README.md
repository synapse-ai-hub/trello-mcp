<p align="center">
  <img src="./src/LogoBlancoGrande2.png" alt="Logo Synapse" width="150">
</p>

<h1 align="center">Servidor MCP para Trello</h1>

<p align="center">
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Licencia: MIT" />
  </a>
  <a href="https://modelcontextprotocol.io">
    <img src="https://img.shields.io/badge/MCP-Compatible-blue" alt="MCP" />
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+" />
  </a>
</p>

<h3 align="center">Gestioná tableros, listas, tarjetas, etiquetas y checklists de Trello desde cualquier cliente MCP (Cursor, Claude, VSC, etc.)</h3>

---

## Presentación

**Trello MCP** es un servidor [Model Context Protocol](https://modelcontextprotocol.io) que expone la API REST de Trello como herramientas que un asistente de IA puede usar desde el editor o el chat. Sin salir del flujo de trabajo, podés listar tableros, crear y mover tarjetas, gestionar checklists, comentarios y adjuntos, y buscar en Trello.

Ideal para equipos que usan Trello y quieren integrarlo con el asistente del IDE para automatizar tareas, consultar estado de proyectos o actualizar tarjetas por lenguaje natural.

### ✨ Características principales

- **Tableros y listas**: Listar tus tableros, obtener listas de un board, crear listas.
- **Tarjetas**: Crear, editar, mover, archivar; obtener detalle completo (incluye IDs de checklists, miembros, badges y metadatos).
- **Checklists**: Obtener checklist con ítems, crear checklists en una tarjeta, agregar ítems.
- **Comentarios y adjuntos**: Leer y agregar comentarios; adjuntar URLs o archivos; eliminar adjuntos.
- **Etiquetas**: Listar etiquetas de un board, crear etiquetas.
- **Búsqueda**: Buscar tarjetas y/o tableros en Trello.
- **Perfil**: Obtener el perfil del miembro autenticado.

---

## Herramientas disponibles

| Herramienta | Descripción |
|-------------|-------------|
| `list_my_boards` | Lista todos los tableros del usuario autenticado |
| `get_board` | Detalle de un tablero |
| `get_board_lists` | Listas de un tablero |
| `create_list` | Crear una lista en un tablero |
| `get_list_cards` | Tarjetas de una lista |
| `get_board_cards` | Tarjetas de un tablero |
| `get_card` | Detalle completo de una tarjeta (incl. idChecklists, idMembers, badges, etc.) |
| `create_card` | Crear una tarjeta en una lista |
| `update_card` | Actualizar campos de una tarjeta |
| `move_card` | Mover una tarjeta a otra lista o tablero |
| `archive_card` | Archivar (cerrar) una tarjeta |
| `get_card_comments` | Comentarios de una tarjeta |
| `add_card_comment` | Agregar un comentario a una tarjeta |
| `get_card_attachments` | Adjuntos de una tarjeta |
| `add_card_attachment` | Subir un archivo como adjunto |
| `add_card_url_attachment` | Adjuntar una URL |
| `delete_card_attachment` | Eliminar un adjunto |
| `get_board_labels` | Etiquetas de un tablero |
| `create_label` | Crear una etiqueta en un tablero |
| `get_checklist` | Obtener un checklist y sus ítems |
| `create_checklist` | Crear un checklist en una tarjeta |
| `add_checklist_item` | Agregar un ítem a un checklist |
| `update_checklist_item` | Marcar un ítem del checklist como hecho o no hecho (checked/unchecked) |
| `get_me` | Perfil del miembro autenticado |
| `search_trello` | Buscar tarjetas y/o tableros |

---

## Requisitos previos

1. Entrá a [trello.com/power-ups/admin](https://trello.com/power-ups/admin) y creá un Power-Up.
2. Copiá tu **API Key**.
3. Generá un **Token** con el enlace que aparece en la misma página.

---

## Instalación

El servidor se instala como paquete Python. Para evitar conflictos con otras dependencias (por ejemplo FastAPI/Starlette), se recomienda **usar un entorno virtual dedicado**.

### 1. Dónde instalar

Elegí una carpeta para el venv (o la ruta que prefieras), por ejemplo:

- **Windows:** `ruta\al\mcp-venv` (ej. en la unidad que uses).
- **Linux/macOS:** `~/.local/venvs/mcp-venv` o la que prefieras.

No hace falta clonar el repo para usar el servidor: se instala desde GitHub con pip/uv.

### 2. Crear el venv e instalar el paquete

**Windows (PowerShell):** reemplazá `RUTA_AL_VENV` por la ruta que prefieras.

```powershell
python -m venv RUTA_AL_VENV
RUTA_AL_VENV\Scripts\Activate.ps1
pip install "git+https://github.com/synapse-ai-hub/trello-mcp.git"
```

**Linux/macOS:** reemplazá `RUTA_AL_VENV` por la ruta que prefieras.

```bash
python3 -m venv RUTA_AL_VENV
source RUTA_AL_VENV/bin/activate
pip install "git+https://github.com/synapse-ai-hub/trello-mcp.git"
```

Si preferís **uv**:

```bash
uv pip install "git+https://github.com/synapse-ai-hub/trello-mcp.git"
```

(En ese caso, el intérprete que debés usar en el cliente MCP es el del entorno donde corriste `uv pip install`.)

### 3. Ruta del ejecutable Python

El IDE tiene que ejecutar **ese** Python, no otro. La ruta es:

- **Windows:** `RUTA_AL_VENV\Scripts\python.exe` (la misma que elegiste en el paso 1).
- **Linux/macOS:** `RUTA_AL_VENV/bin/python` (o la ruta absoluta que prefieras).

Para comprobar que el paquete está instalado, ejecutá con esa ruta:

```bash
RUTA_AL_VENV\Scripts\python.exe -c "import trello_mcp; print('OK')"
```

(En Linux/macOS: `RUTA_AL_VENV/bin/python -c "import trello_mcp; print('OK')"`.)

En la configuración MCP del cliente tenés que poner **esa misma ruta** en `command`.

En el archivo de configuración MCP de tu IDE, poné **esa misma ruta** en `command`. Cada IDE indica dónde está ese archivo (por lo general en la carpeta de configuración del usuario).

**Ejemplo de configuración** (reemplazá `RUTA_AL_PYTHON` por la ruta al ejecutable del paso 3 y tus credenciales):

```json
{
  "mcpServers": {
    "trello": {
      "command": "RUTA_AL_PYTHON",
      "args": ["-m", "trello_mcp"],
      "env": {
        "TRELLO_API_KEY": "tu-api-key",
        "TRELLO_TOKEN": "tu-token"
      }
    }
  }
}
```

En Windows la ruta suele ser absoluta, ej. `"C:/ruta/al/venv/Scripts/python.exe"`. En Linux/macOS, ej. `"/home/usuario/.local/venvs/mcp-venv/bin/python"`.

Reiniciá el IDE después de cambiar la configuración.

---

## Variables de entorno

| Variable | Requerida | Descripción |
|----------|:---------:|-------------|
| `TRELLO_API_KEY` | Sí | API key del Power-Up de Trello |
| `TRELLO_TOKEN` | Sí | Token de usuario generado para tu API key |

---

## Conflicto con FastAPI / Starlette

Este servidor usa **Starlette** y **sse-starlette**. Si en el mismo entorno tenés **FastAPI**, pueden generarse conflictos de versiones. Por eso se recomienda el venv dedicado y apuntar el cliente MCP a ese Python.

---

## Desarrollo

Para contribuir o correr tests localmente:

```bash
git clone https://github.com/synapse-ai-hub/trello-mcp.git
cd trello-mcp
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

---

## Estructura del proyecto

```plaintext
trello-mcp/
├── src/
│   └── trello_mcp/
│       ├── tools/          # boards, cards, lists, checklists, labels, attachments, search, members
│       ├── client.py
│       ├── config.py
│       ├── exceptions.py
│       ├── server.py
│       └── __main__.py
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE).

---

## Sobre este repositorio

Mantenido por [synapse.ai](https://github.com/synapse-ai-hub).
