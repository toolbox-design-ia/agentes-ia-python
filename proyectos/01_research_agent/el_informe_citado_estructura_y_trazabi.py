PROMPT_REDACTOR = """
Eres un redactor de informes de investigación rigurosos.

Escribe un informe en Markdown sobre la pregunta dada usando EXCLUSIVAMENTE
la información de las evidencias proporcionadas.

Estructura obligatoria:
1. ## Resumen ejecutivo (3-4 párrafos)
2. ## Hallazgos por subpregunta (una sección ### por subpregunta)
3. ## Contradicciones detectadas (lista de puntos donde las fuentes difieren)
4. ## Notas al pie (una por evidencia citada, formato [^ev_xxx])
5. ## Bibliografía (lista completa de fuentes)

Reglas:
- Cada afirmación termina con [^ev_xxx] donde xxx es el ID de la evidencia.
- Las inferencias se introducen con "Puede inferirse que..." o "Los datos sugieren que...".
- Las contradicciones se reportan en la sección correspondiente; no se resuelven.
- No añadas información que no esté en las evidencias proporcionadas.
"""

def escribir_informe(
    pregunta: str,
    evidencias: list[EvidenceRecord],
    spec: dict,
) -> str:
    contexto = "\n\n".join(
        f"[{ev.id}] (tipo={ev.tipo}, fiabilidad={ev.fiabilidad}, "
        f"inferencia={'sí' if ev.es_inferencia else 'no'}, "
        f"contradice={ev.contradice})\n"
        f"Fuente: {ev.source}\n"
        f"Título: {ev.title}\n"
        f"Subpregunta: {ev.subpregunta}\n"
        f"Contenido: {ev.snippet}"
        for ev in evidencias
    )
    respuesta = cliente.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        system=PROMPT_REDACTOR,
        messages=[{
            "role": "user",
            "content": f"Pregunta: {pregunta}\n\nEvidencias:\n{contexto}",
        }],
    )
    return respuesta.content[0].text
