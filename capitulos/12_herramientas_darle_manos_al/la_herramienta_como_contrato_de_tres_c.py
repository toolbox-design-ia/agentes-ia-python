herramienta_leer_archivo = {
    "name": "leer_archivo",
    "description": (
        "Lee el contenido de un archivo de texto del proyecto. "
        "Usar cuando el usuario pide ver o revisar un documento existente. "
        "No sirve para archivos binarios ni para archivos fuera del directorio del proyecto. "
        "Devuelve el contenido como texto plano, o un mensaje de error si el archivo no existe."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ruta": {
                "type": "string",
                "description": "Ruta relativa al archivo desde la raíz del proyecto."
            },
            "codificacion": {
                "type": "string",
                "enum": ["utf-8", "latin-1"],
                "description": "Codificación del archivo. Usar utf-8 salvo indicación contraria."
            }
        },
        "required": ["ruta"],
        "additionalProperties": False
    }
}
