from agents import Agent
from agents import WebSearchTool

agente_redaccion = Agent(
    name="Especialista en redacción",
    instructions="Revisas y mejoras textos en español. "
                 "Tu foco es claridad, coherencia y estilo editorial.",
    model="gpt-5.6-sol",
)

agente_investigacion = Agent(
    name="Especialista en investigación",
    instructions="Buscas información actualizada y la sintetizas con rigor. "
                 "Citas tus fuentes cuando las conoces.",
    model="gpt-5.6-sol",
    tools=[WebSearchTool()],
)

agente_coordinador = Agent(
    name="Coordinador editorial",
    instructions="Decides si la petición del usuario requiere investigación o revisión de texto "
                 "y derivas al especialista adecuado. No respondes directamente.",
    model="gpt-5.6-terra",
    handoffs=[agente_investigacion, agente_redaccion],
)
