from openai import OpenAI
cliente_oai = OpenAI()

def buscar_web_alojada_openai(subpregunta: str) -> list[dict]:
    respuesta = cliente_oai.responses.create(
        model="gpt-5.6-sol",
        tools=[{"type": "web_search"}],
        input=subpregunta,
    )
    # Las anotaciones viven en cada bloque de texto de la salida,
    # no en la raiz de la respuesta
    resultados = []
    for item in respuesta.output:
        if item.type != "message":
            continue
        for bloque in item.content:
            if bloque.type != "output_text":
                continue
            for ann in bloque.annotations:
                if ann.type == "url_citation":
                    resultados.append({
                        "url": ann.url,
                        "title": ann.title,
                        "snippet": respuesta.output_text[:800],
                    })
    return resultados
