"""Inicializa la base de datos del asistente (capitulo 25, puesta en marcha)."""
import os
import sqlite3

DB_PATH = os.getenv("ASSISTANT_DB", "assistant.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS memories (
  key TEXT PRIMARY KEY, value TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'general');
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
  due TEXT, priority TEXT NOT NULL DEFAULT 'medium', notes TEXT,
  done INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT, tool TEXT NOT NULL,
  arguments TEXT, authorized INTEGER NOT NULL, ts TEXT NOT NULL,
  session TEXT);
"""

if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
    os.makedirs("notes", exist_ok=True)
    print(f"Base creada en {DB_PATH} y carpeta notes/ lista.")
