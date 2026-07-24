def cargar_memoria(conn: sqlite3.Connection, tipos: list[str] | None = None) -> str:
    if tipos is None:
        tipos = ['preferencia', 'estado', 'hecho']
    
    marcadores = ",".join("?" * len(tipos))
    filas = conn.execute(
        f"SELECT tipo, clave, contenido FROM recuerdos "
        f"WHERE tipo IN ({marcadores}) AND activo = 1 "
        f"ORDER BY tipo, id",
        tipos
    ).fetchall()
    
    if not filas:
        return ""
    
    bloques = []
    for tipo, clave, contenido in filas:
        etiqueta = f"[{tipo.upper()}]" + (f" {clave}:" if clave else ":")
        bloques.append(f"{etiqueta} {contenido}")
    
    return "MEMORIA DEL AGENTE:\n" + "\n".join(bloques)
