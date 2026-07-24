import sqlite3
from datetime import datetime

def inicializar_memoria(ruta_db: str = "memoria_agente.db") -> sqlite3.Connection:
    conn = sqlite3.connect(ruta_db)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recuerdos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo     TEXT NOT NULL CHECK(tipo IN (
                         'episodico', 'preferencia', 'estado', 'hecho'
                     )),
            clave    TEXT,
            contenido TEXT NOT NULL,
            fecha    TEXT NOT NULL,
            activo   INTEGER DEFAULT 1
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_tipo_activo ON recuerdos(tipo, activo)"
    )
    conn.commit()
    return conn
