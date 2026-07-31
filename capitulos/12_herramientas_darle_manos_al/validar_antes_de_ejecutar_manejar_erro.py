from pathlib import Path

def leer_archivo(ruta: str, codificacion: str = "utf-8") -> dict:
    ruta_base = Path("/srv/proyecto/documentos").resolve()
    ruta_completa = (ruta_base / ruta).resolve()

    # startswith() dejaria pasar /srv/proyecto/documentos-privados
    if not ruta_completa.is_relative_to(ruta_base):
        return {"exito": False, "contenido": "Ruta no permitida: fuera del directorio del proyecto."}

    if not ruta_completa.exists():
        return {"exito": False, "contenido": f"El archivo '{ruta}' no existe."}

    try:
        texto = ruta_completa.read_text(encoding=codificacion)
        return {"exito": True, "contenido": texto}
    except Exception as e:
        return {"exito": False, "contenido": f"Error al leer el archivo: {str(e)}"}
