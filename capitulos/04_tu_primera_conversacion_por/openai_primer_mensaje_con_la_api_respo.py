from openai import OpenAI

cliente = OpenAI()          # lee OPENAI_API_KEY del entorno

respuesta = cliente.responses.create(
    model="gpt-5.6-terra",
    input=(
        "Explica en tres frases qué hace un agente de IA "
        "cuando usa una herramienta."
    ),
)

print(respuesta.output_text)

entrada = respuesta.usage.input_tokens
salida = respuesta.usage.output_tokens
PRECIO_ENTRADA = 2.00  # USD por millón de tokens; verifica el precio vigente
PRECIO_SALIDA = 12.00   # USD por millón de tokens; verifica el precio vigente

coste = (entrada / 1_000_000 * PRECIO_ENTRADA) + (
    salida / 1_000_000 * PRECIO_SALIDA
)

print(f"Tokens - entrada: {entrada} / salida: {salida}")
print(f"Coste estimado: ${coste:.6f}")
