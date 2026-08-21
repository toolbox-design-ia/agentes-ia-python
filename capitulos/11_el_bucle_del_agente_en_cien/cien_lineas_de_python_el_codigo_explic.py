import json
from anthropic import Anthropic

TOOLS = [
    {
        "name": "read_file",
        "description": "Lee el contenido de un archivo de texto del disco.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Ruta absoluta o relativa al archivo."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_directory",
        "description": "Lista los archivos y subdirectorios de una ruta.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Ruta del directorio a listar."
                }
            },
            "required": ["path"]
        }
    }
]

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[Error] Archivo no encontrado: {path}"
    except Exception as e:
        return f"[Error] {type(e).__name__}: {e}"

def list_directory(path: str) -> str:
    import os
    try:
        entries = os.listdir(path)
        return "\n".join(entries) if entries else "[Directorio vacío]"
    except FileNotFoundError:
        return f"[Error] Directorio no encontrado: {path}"
    except Exception as e:
        return f"[Error] {type(e).__name__}: {e}"

TOOL_REGISTRY = {
    "read_file": read_file,
    "list_directory": list_directory,
}

SYSTEM_PROMPT = """Eres un agente de investigación local.
Puedes usar herramientas solo cuando necesites consultar datos externos.
Devuelve una respuesta final cuando tengas suficiente información.
No inventes resultados de herramientas.
Si una herramienta falla, intenta una recuperación simple o informa el fallo."""

def run_agent(user_request: str, max_steps: int = 10) -> str:
    client = Anthropic()
    messages = [{"role": "user", "content": user_request}]
    total_input_tokens = 0
    total_output_tokens = 0

    for step in range(1, max_steps + 1):
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens
        print(f"[Paso {step}] stop_reason={response.stop_reason} "
              f"tokens_entrada={response.usage.input_tokens}")

        if response.stop_reason == "end_turn":
            final_text = next(
                (b.text for b in response.content if hasattr(b, "text")), ""
            )
            print(f"[Final] tokens totales — entrada: {total_input_tokens}, "
                  f"salida: {total_output_tokens}")
            return final_text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    name = block.name
                    inputs = block.input
                    print(f"[Acción] {name}({json.dumps(inputs, ensure_ascii=False)})")
                    if name in TOOL_REGISTRY:
                        try:
                            observation = TOOL_REGISTRY[name](**inputs)
                        except Exception as e:
                            observation = f"[Error en {name}] {e}"
                    else:
                        observation = f"[Error] Herramienta desconocida: {name}"
                    preview = observation[:120] + ("..." if len(observation) > 120 else "")
                    print(f"[Observación] {preview}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": observation
                    })
            messages.append({"role": "user", "content": tool_results})
        else:
            print(f"[Advertencia] stop_reason inesperado: {response.stop_reason}")
            break

    print(f"[Límite] El agente alcanzó {max_steps} pasos sin completar la tarea.")
    return "El agente alcanzó el límite de pasos sin producir una respuesta final."

if __name__ == "__main__":
    resultado = run_agent(
        "¿Qué archivos hay en el directorio actual y qué contiene README.md?"
    )
    print("\n=== RESPUESTA FINAL ===")
    print(resultado)
