def extraer_fragmento(texto_pagina: str, subpregunta: str) -> dict:
    respuesta = cliente.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=(
            "Extrae el fragmento más relevante del texto para responder la subpregunta. "
            'Devuelve JSON: {"snippet": str, "es_inferencia": bool}. '
            "es_inferencia=true si el texto sugiere la respuesta pero no la afirma directamente."
        ),
        messages=[{
            "role": "user",
            "content": f"Subpregunta: {subpregunta}\n\nTexto:\n{texto_pagina}",
        }],
    )
    return json.loads(respuesta.content[0].text)
