"""Servidor MCP de archivos (capitulo 25): el acceso mas sensible.

Solo lee dentro de la carpeta autorizada (NOTES_DIR); nunca escribe.
"""
import os
from pathlib import Path

from mcp.server import MCPServer

NOTES_DIR = Path(os.getenv("NOTES_DIR", "notes")).resolve()
mcp = MCPServer("files")


def _safe(path: str) -> Path:
    # Toda ruta se resuelve DENTRO de la carpeta autorizada, sin excepciones
    candidate = (NOTES_DIR / path).resolve()
    if not str(candidate).startswith(str(NOTES_DIR)):
        raise ValueError("Ruta fuera de la carpeta autorizada")
    return candidate


@mcp.tool()
def list_files() -> str:
    """Devuelve el indice de archivos con fecha y tamano."""
    rows = []
    for p in sorted(NOTES_DIR.rglob("*")):
        if p.is_file():
            stat = p.stat()
            rows.append(f"{p.relative_to(NOTES_DIR)} | {stat.st_size} B")
    return "\n".join(rows) or "Carpeta vacia."


@mcp.tool()
def read_file(path: str) -> str:
    """Devuelve el contenido de un archivo de la carpeta autorizada."""
    return _safe(path).read_text(encoding="utf-8", errors="ignore")[:8000]


@mcp.tool()
def summarize_file(path: str) -> str:
    """Devuelve las primeras lineas como resumen rapido del archivo."""
    text = _safe(path).read_text(encoding="utf-8", errors="ignore")
    return "\n".join(text.splitlines()[:20])


if __name__ == "__main__":
    mcp.run(transport="stdio")
