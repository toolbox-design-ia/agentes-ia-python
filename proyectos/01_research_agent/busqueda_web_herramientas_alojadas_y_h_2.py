from openai import OpenAI
cliente_oai = OpenAI()

def buscar_web_alojada_openai(subpregunta: str) -> list[dict]:
    respuesta = cliente_oai.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=subpregunta,
    )
    return [
        {"url": ann.url, "title": ann.title, "snippet": ""}
        for ann in getattr(respuesta, "annotations", [])
        if ann.type == "url_citation"
    ]
