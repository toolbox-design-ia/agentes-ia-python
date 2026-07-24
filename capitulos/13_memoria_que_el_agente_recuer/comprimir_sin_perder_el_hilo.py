async def comprimir_historial(historial: list[dict], modelo: str) -> str:
    mensajes_a_resumir = historial[:-4]  # conserva los últimos 4 turnos
    
    prompt = f"""Resume el siguiente historial de trabajo en cuatro secciones exactas:
ESTADO_ACTUAL: [qué tarea y en qué paso]
DECISIONES: [restricciones y elecciones confirmadas]
ERRORES_DESCARTADOS: [aproximaciones que ya fallaron]
PREFERENCIAS: [estilo y formato que el usuario ha pedido]

Historial:
{formatear_mensajes(mensajes_a_resumir)}"""
    
    respuesta = await cliente_llm.completar(prompt, modelo=modelo)
    return respuesta.texto
