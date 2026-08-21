from agents import input_guardrail, GuardrailFunctionOutput, Agent, Runner
import asyncio

@input_guardrail
async def verificar_alcance_editorial(ctx, agente, input):
    terminos_fuera_de_alcance = ["datos personales", "información confidencial", "contraseñas"]
    if any(t in input.lower() for t in terminos_fuera_de_alcance):
        return GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info="Petición fuera del alcance del sistema editorial."
        )
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)

asistente_protegido = Agent(
    name="Asistente editorial protegido",
    instructions="Asistes en tareas editoriales: investigación, redacción y revisión.",
    model="gpt-5.6-sol",
    input_guardrails=[verificar_alcance_editorial],
)
