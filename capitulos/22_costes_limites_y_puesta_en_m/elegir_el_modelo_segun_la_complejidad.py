def seleccionar_modelo(complejidad: str) -> str:
    """
    Devuelve el modelo apropiado según la complejidad estimada.
    En producción, 'complejidad' la decide un modelo ligero en el paso anterior.
    """
    MODELOS = {
        "baja": "modelo_ligero",       # clasificación, extracción, routing
        "media": "modelo_intermedio",  # síntesis moderada, redacción
        "alta": "modelo_avanzado",     # planificación compleja, diagnóstico
    }
    return MODELOS.get(complejidad, "modelo_intermedio")
