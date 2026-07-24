def buscar_web_alojada_anthropic(subpregunta: str) -> list[dict]:
    respuesta = cliente.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": subpregunta}],
    )
    resultados = []
    for bloque in respuesta.content:
        if bloque.type == "tool_result":
            for item in bloque.content:
                resultados.append({
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("encrypted_content", "")[:800],
                })
    return resultados
