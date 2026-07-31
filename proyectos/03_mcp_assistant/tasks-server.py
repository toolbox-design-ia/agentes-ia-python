"""Servidor MCP de tareas (capitulo 25): lista de tareas en SQLite."""
import os
import sqlite3
from datetime import date

from mcp.server import MCPServer

DB_PATH = os.getenv("ASSISTANT_DB", "assistant.db")
mcp = MCPServer("tasks")

PRIORIDADES = ("low", "medium", "high")


def _formatear(rows) -> str:
    return "\n".join(
        f"[{i}] {t}"
        + (f" (limite {d})" if d else "")
        + (f" prioridad {p}" if p else "")
        + (" HECHA" if done else "")
        for i, t, d, p, done in rows)


@mcp.tool()
def create_task(title: str, due_date: str = "", priority: str = "medium",
                notes: str = "") -> str:
    """Crea una tarea.

    title: obligatorio. due_date: opcional, ISO 8601 (YYYY-MM-DD).
    priority: low, medium o high. notes: texto libre opcional.
    """
    if priority not in PRIORIDADES:
        return f"Prioridad no valida: {priority}. Usa low, medium o high."
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO tasks (title, due, priority, notes, done) "
            "VALUES (?, ?, ?, ?, 0)", (title, due_date, priority, notes))
    return f"Tarea creada: {title}"


@mcp.tool()
def list_tasks(pending_only: bool = True) -> str:
    """Lista las tareas, por defecto solo las pendientes."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, title, due, priority, done FROM tasks"
        if pending_only:
            query += " WHERE done = 0"
        rows = conn.execute(query + " ORDER BY due").fetchall()
    return _formatear(rows) if rows else "Sin tareas pendientes."


@mcp.tool()
def complete_task(task_id: int) -> str:
    """Marca una tarea como hecha."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    if cur.rowcount:
        return f"Tarea {task_id} completada."
    return f"No existe la tarea {task_id}."


@mcp.tool()
def delete_task(task_id: int) -> str:
    """Borra una tarea por su identificador."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cur.rowcount:
        return f"Tarea {task_id} borrada."
    return f"No existe la tarea {task_id}."


@mcp.resource("tasks://today")
def tasks_today() -> str:
    """Tareas cuyo limite es hoy."""
    hoy = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, title, due, priority, done FROM tasks "
            "WHERE done = 0 AND due = ? ORDER BY priority", (hoy,)).fetchall()
    return _formatear(rows) if rows else "Nada con limite para hoy."


@mcp.resource("tasks://pending")
def tasks_pending() -> str:
    """Todas las tareas sin completar."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, title, due, priority, done FROM tasks "
            "WHERE done = 0 ORDER BY due").fetchall()
    return _formatear(rows) if rows else "Sin tareas pendientes."


@mcp.prompt()
def weekly_review_prompt() -> str:
    """Inicia una revision semanal de tareas y prioridades."""
    return ("Hoy es dia de revision semanal. Lista mis tareas pendientes, "
            "agrupalas por urgencia y proponme un orden para la semana, "
            "preguntando antes de mover cualquier fecha limite.")


if __name__ == "__main__":
    mcp.run(transport="stdio")
