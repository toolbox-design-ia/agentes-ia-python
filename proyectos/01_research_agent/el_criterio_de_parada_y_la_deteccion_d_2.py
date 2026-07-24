def detectar_contradiccion(
    nueva: EvidenceRecord,
    existentes: list[EvidenceRecord],
) -> list[str]:
    relevantes = [ev for ev in existentes if ev.subpregunta == nueva.subpregunta]
    if not relevantes:
        return []

    contexto = "\n".join(f"[{ev.id}] {ev.snippet}" for ev in relevantes)
    respuesta = cliente.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=128,
        system=(
            "Compara el snippet nuevo con los existentes. "
            "Si alguno contradice directamente al nuevo, devuelve sus IDs en JSON: "
            '["ev_xxx", ...]. Si no hay contradicción, devuelve [].'
        ),
        messages=[{
            "role": "user",
            "content": f"Snippet nuevo: {nueva.snippet}\n\nExistentes:\n{contexto}",
        }],
    )
    try:
        return json.loads(respuesta.content[0].text)
    except json.JSONDecodeError:
        return []
