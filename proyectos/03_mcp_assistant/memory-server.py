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
def recall_memory(category: str = "") -> str:
    """Devuelve las memorias guardadas, opcionalmente por categoria."""
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


@mcp.resource("memory://profile")
def get_profile() -> str:
    """Devuelve el perfil completo del usuario."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT key, value FROM memories WHERE category = 'perfil'"
        ).fetchall()
    return "\n".join(f"{k}: {v}" for k, v in rows) or "Perfil vacio."


if __name__ == "__main__":
    mcp.run(transport="stdio")
