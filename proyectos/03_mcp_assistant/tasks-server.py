"""Servidor MCP de tareas (capitulo 25): lista de tareas en SQLite."""
import os
import sqlite3

from mcp.server import MCPServer

DB_PATH = os.getenv("ASSISTANT_DB", "assistant.db")
mcp = MCPServer("tasks")


@mcp.tool()
def add_task(title: str, due: str = "") -> str:
    """Crea una tarea con titulo y fecha limite opcional (YYYY-MM-DD)."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO tasks (title, due, done) VALUES (?, ?, 0)",
                     (title, due))
    return f"Tarea creada: {title}"


@mcp.tool()
def list_tasks(pending_only: bool = True) -> str:
    """Lista las tareas, por defecto solo las pendientes."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, title, due, done FROM tasks"
        if pending_only:
            query += " WHERE done = 0"
        rows = conn.execute(query + " ORDER BY due").fetchall()
    if not rows:
        return "Sin tareas pendientes."
    return "\n".join(f"[{i}] {t}" + (f" (limite {d})" if d else "") +
                     (" HECHA" if done else "") for i, t, d, done in rows)


@mcp.tool()
def complete_task(task_id: int) -> str:
    """Marca una tarea como hecha."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    return f"Tarea {task_id} completada."


@mcp.prompt()
def weekly_review_prompt() -> str:
    """Inicia una revision semanal de tareas y prioridades."""
    return ("Hoy es dia de revision semanal. Lista mis tareas pendientes, "
            "agrupalas por urgencia y proponme un orden para la semana, "
            "preguntando antes de mover cualquier fecha limite.")


if __name__ == "__main__":
    mcp.run(transport="stdio")
