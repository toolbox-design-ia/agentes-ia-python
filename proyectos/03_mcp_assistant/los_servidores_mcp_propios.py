from mcp.server.fastmcp import FastMCP
import sqlite3, os

DB_PATH = os.getenv("ASSISTANT_DB", "assistant.db")
mcp = FastMCP("memory-server")

@mcp.tool()
def save_memory(key: str, value: str, category: str = "general") -> str:
    """Guarda o actualiza una memoria del usuario."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO memories (key, value, category) VALUES (?, ?, ?)",
            (key, value, category)
        )
    return f"Memoria '{key}' guardada."

@mcp.resource("memory://profile")
def get_profile() -> str:
    """Devuelve el perfil completo del usuario."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT key, value FROM memories WHERE category='profile'"
        ).fetchall()
    return "\n".join(f"{k}: {v}" for k, v in rows)

if __name__ == "__main__":
    mcp.run()
