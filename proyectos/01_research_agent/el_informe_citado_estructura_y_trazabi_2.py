def actualizar_contradicciones(ev: EvidenceRecord, evidencias: list[EvidenceRecord]) -> None:
    ev.contradice = detectar_contradiccion(ev, evidencias)
    for ev_id in ev.contradice:
        for ev_existente in evidencias:
            if ev_existente.id == ev_id and ev.id not in ev_existente.contradice:
                ev_existente.contradice.append(ev.id)

def investigar(pregunta: str, coleccion_local=None, spec=None) -> str:
    if spec is None:
        spec = ESPECIFICACION

    evidencias: list[EvidenceRecord] = []
    subpreguntas = planificar(pregunta)
    max_iteraciones = 3

    for iteracion in range(max_iteraciones):
        if criterio_parada_cumplido(evidencias, subpreguntas, spec):
            break

        for sp in subpreguntas:
            for resultado in buscar_web(sp):
                texto = leer_pagina(resultado["url"])
                if texto:
                    frag = extraer_fragmento(texto, sp)
                    ev = registrar_evidencia(
                        resultado={
                            "url": resultado["url"],
                            "title": resultado["title"],
                            "snippet": frag["snippet"],
                        },
                        subpregunta=sp,
                        tipo="web",
                        es_inferencia=frag["es_inferencia"],
                    )
                    actualizar_contradicciones(ev, evidencias)
                    evidencias.append(ev)

            if coleccion_local:
                for resultado in buscar_local(sp, coleccion_local):
                    ev = registrar_evidencia(
                        resultado=resultado, subpregunta=sp, tipo="local"
                    )
                    actualizar_contradicciones(ev, evidencias)
                    evidencias.append(ev)

    return escribir_informe(pregunta, evidencias, spec)
