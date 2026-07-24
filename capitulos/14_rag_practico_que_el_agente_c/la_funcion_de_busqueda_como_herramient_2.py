import anthropic

client_claude = anthropic.Anthropic()

herramientas = [
    {
        "name": "buscar_en_documentos",
        "description": (
            "Busca información en los documentos del usuario. "
            "Úsala cuando la pregunta se refiera a contenido de archivos propios: "
            "manuales, contratos, reportes u otra documentación indexada. "
            "Devuelve fragmentos con su fuente (archivo y página)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pregunta": {
                    "type": "string",
                    "description": "La consulta a buscar en los documentos."
                }
            },
            "required": ["pregunta"],
        },
    }
]


def ejecutar_herramienta(nombre, argumentos):
    if nombre == "buscar_en_documentos":
        return buscar_en_documentos(**argumentos)
    raise ValueError(f"Herramienta desconocida: {nombre}")
