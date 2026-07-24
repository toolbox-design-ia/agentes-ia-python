async def ejecutar_con_memoria(
    agente,
    peticion: str,
    id_sesion: str,
    conn_memoria: sqlite3.Connection,
) -> str:
    # 1. Cargar memoria persistente
    memoria = cargar_memoria(conn_memoria)
    instrucciones_completas = agente.instrucciones + "\n\n" + memoria if memoria else agente.instrucciones
    
    # 2. Recuperar y comprimir historial de sesión si es necesario
    historial = recuperar_historial(id_sesion)
    if tokens_de(historial) > UMBRAL_COMPRESION:
        resumen = await comprimir_historial(historial, agente.modelo)
        historial = [{"role": "system", "content": resumen}] + historial[-4:]
        guardar_historial(id_sesion, historial)
    
    # 3. Llamar al modelo
    respuesta = await agente.completar(
        instrucciones=instrucciones_completas,
        historial=historial,
        peticion=peticion,
    )
    
    # 4. Actualizar historial y extraer memoria nueva
    historial.append({"role": "user", "content": peticion})
    historial.append({"role": "assistant", "content": respuesta.texto})
    guardar_historial(id_sesion, historial)
    
    if respuesta.memoria_nueva:
        for recuerdo in respuesta.memoria_nueva:
            guardar_recuerdo(conn_memoria, **recuerdo)
    
    return respuesta.texto
