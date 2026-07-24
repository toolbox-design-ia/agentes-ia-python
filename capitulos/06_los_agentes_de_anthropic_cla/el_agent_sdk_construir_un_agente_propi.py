buscar_archivos = {
    "name": "buscar_archivos",
    "description": "Busca archivos en un directorio por nombre o extensión.",
    "input_schema": {
        "type": "object",
        "properties": {
            "directorio": {
                "type": "string",
                "description": "Ruta del directorio donde buscar"
            },
            "extension": {
                "type": "string",
                "description": "Extensión de archivo a buscar, por ejemplo .py o .md"
            }
        },
        "required": ["directorio"]
    }
}
