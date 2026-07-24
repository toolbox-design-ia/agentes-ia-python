{
    "type": "object",
    "properties": {
        "titulo": {
            "type": "string",
            "description": "Título breve de la tarea, máximo 80 caracteres."
        },
        "prioridad": {
            "type": "string",
            "enum": ["alta", "media", "baja"],
            "description": "Prioridad inicial de la tarea."
        },
        "etiquetas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Lista de etiquetas para clasificar la tarea. Puede estar vacía."
        },
        "asignado_a": {
            "type": "string",
            "description": "Identificador del miembro del equipo. Omitir si no hay asignación."
        }
    },
    "required": ["titulo", "prioridad"],
    "additionalProperties": False
}
