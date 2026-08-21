def buscar_web_alojada_anthropic(subpregunta: str) -> list[dict]:
    respuesta = cliente.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": subpregunta}],
    )
    resumen = "".join(
        b.text for b in respuesta.content if b.type == "text"
    )[:800]

    resultados = []
    for bloque in respuesta.content:
        # El bloque es web_search_tool_result y sus elementos son
        # objetos con atributos, no diccionarios
        if bloque.type == "web_search_tool_result":
            for item in bloque.content:
                resultados.append({
                    "url": item.url,
                    "title": item.title,
                    "snippet": resumen,
                })
    return resultados
