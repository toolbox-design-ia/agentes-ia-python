import anthropic
import os

cliente = anthropic.Anthropic()

def ejecutar_busqueda(directorio, extension=None):
    archivos = []
    for nombre in os.listdir(directorio):
        if extension is None or nombre.endswith(extension):
            archivos.append(nombre)
    return {"archivos": archivos}

def bucle_agente(pregunta_usuario):
    mensajes = [{"role": "user", "content": pregunta_usuario}]

    while True:
        respuesta = cliente.messages.create(
            model="claude-sonnet-5",
            max_tokens=4096,
            tools=[buscar_archivos],
            messages=mensajes
        )

        if respuesta.stop_reason == "end_turn":
            # El agente terminó; extraer el texto final
            return respuesta.content[0].text

        # El modelo quiere usar una herramienta
        mensajes.append({"role": "assistant", "content": respuesta.content})
        resultados_herramientas = []

        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                argumentos = bloque.input
                resultado = ejecutar_busqueda(
                    argumentos.get("directorio"),
                    argumentos.get("extension")
                )
                resultados_herramientas.append({
                    "type": "tool_result",
                    "tool_use_id": bloque.id,
                    "content": str(resultado)
                })

        mensajes.append({"role": "user", "content": resultados_herramientas})
