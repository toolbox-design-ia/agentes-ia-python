from google import genai

cliente = genai.Client()    # lee GOOGLE_API_KEY del entorno

respuesta = cliente.models.generate_content(
    model="gemini-2.5-flash",
    contents=(
        "Explica en tres frases qué hace un agente de IA "
        "cuando usa una herramienta."
    ),
)

print(respuesta.text)

entrada = respuesta.usage_metadata.prompt_token_count
salida = respuesta.usage_metadata.candidates_token_count
print(f"Tokens - entrada: {entrada} / salida: {salida}")
