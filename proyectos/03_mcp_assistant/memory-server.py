"""Servidor MCP de memoria (capitulo 25): perfil y resumenes en SQLite."""
import os
import sqlite3

from mcp.server import MCPServer

DB_PATH = os.getenv("ASSISTANT_DB", "assistant.db")
mcp = MCPServer("memory")


@mcp.tool()
def save_memory(key: str, value: str, category: str = "general") -> str:
    """Guarda o actualiza una memoria del usuario."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO memories (key, value, category) VALUES (?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value, "
            "category = excluded.category",
            (key, value, category))
    return f"Memoria guardada: {key}"


@mcp.tool()
def get_memory(key: str) -> str:
    """Devuelve el valor asociado a una clave concreta."""
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT value FROM memories WHERE key = ?", (key,)).fetchone()
    return row[0] if row else f"Sin memoria para la clave '{key}'."


@mcp.tool()
def list_memories(category: str = "") -> str:
    """Lista las memorias guardadas, opcionalmente filtradas por categoria."""
    with sqlite3.connect(DB_PATH) as conn:
        if category:
            rows = conn.execute(
                "SELECT key, value FROM memories WHERE category = ?",
                (category,)).fetchall()
        else:
            rows = conn.execute("SELECT key, value FROM memories").fetchall()
    if not rows:
        return "Sin memorias guardadas."
    return "\n".join(f"- {k}: {v}" for k, v in rows)


@mcp.tool()
def delete_memory(key: str) -> str:
    """Borra una memoria por su clave."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM memories WHERE key = ?", (key,))
    if cur.rowcount:
        return f"Memoria borrada: {key}"
    return f"No habia ninguna memoria con la clave '{key}'."


@mcp.resource("memory://profile")
def get_profile() -> str:
    """Devuelve el perfil completo del usuario."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT key, value FROM memories WHERE category = 'profile'"
        ).fetchall()
    return "\n".join(f"{k}: {v}" for k, v in rows) or "Perfil vacio."


@mcp.resource("memory://recent")
def get_recent() -> str:
    """Devuelve los ultimos resumenes de conversacion guardados."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT key, value FROM memories WHERE category = 'summary' "
            "ORDER BY rowid DESC LIMIT 5").fetchall()
    return "\n".join(f"{k}: {v}" for k, v in rows) or "Sin resumenes recientes."


if __name__ == "__main__":
    mcp.run(transport="stdio")
