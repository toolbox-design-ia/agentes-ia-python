from anthropic import Anthropic

cliente = Anthropic()       # lee ANTHROPIC_API_KEY del entorno

respuesta = cliente.messages.create(
    model="claude-sonnet-5",
    max_tokens=256,
    messages=[
        {
            "role": "user",
            "content": (
                "Explica en tres frases qué hace un agente de IA "
                "cuando usa una herramienta."
            ),
        }
    ],
)

texto = respuesta.content[0].text
print(texto)

entrada = respuesta.usage.input_tokens
salida = respuesta.usage.output_tokens
print(f"Tokens - entrada: {entrada} / salida: {salida}")
