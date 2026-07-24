def guardar_recuerdo(
    conn: sqlite3.Connection,
    tipo: str,
    contenido: str,
    clave: str | None = None
) -> None:
    fecha = datetime.now().isoformat()
    
    if clave:
        # Si existe una entrada con esta clave, la desactiva antes de insertar
        conn.execute(
            "UPDATE recuerdos SET activo = 0 WHERE clave = ? AND activo = 1",
            (clave,)
        )
    
    conn.execute(
        "INSERT INTO recuerdos (tipo, clave, contenido, fecha) VALUES (?, ?, ?, ?)",
        (tipo, clave, contenido, fecha)
    )
    conn.commit()
