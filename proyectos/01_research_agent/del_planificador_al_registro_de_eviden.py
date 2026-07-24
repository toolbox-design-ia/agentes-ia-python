import json
import anthropic

cliente = anthropic.Anthropic()

def planificar(pregunta: str) -> list[str]:
    respuesta = cliente.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        system=(
            "Descompón la pregunta en 3-5 subpreguntas concretas y necesarias "
            "para responderla con rigor. Devuelve SOLO una lista JSON de strings, "
            "sin explicaciones adicionales."
        ),
        messages=[{"role": "user", "content": pregunta}],
    )
    texto = respuesta.content[0].text.strip()
    inicio = texto.index("[")
    fin = texto.rindex("]") + 1
    return json.loads(texto[inicio:fin])
