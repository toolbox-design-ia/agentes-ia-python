from agents import Agent
from agents.tools import WebSearchTool

agente_redaccion = Agent(
    name="Especialista en redacción",
    instructions="Revisas y mejoras textos en español. "
                 "Tu foco es claridad, coherencia y estilo editorial.",
    model="gpt-4o",
)

agente_investigacion = Agent(
    name="Especialista en investigación",
    instructions="Buscas información actualizada y la sintetizas con rigor. "
                 "Citas tus fuentes cuando las conoces.",
    model="gpt-4o",
    tools=[WebSearchTool()],
)

agente_coordinador = Agent(
    name="Coordinador editorial",
    instructions="Decides si la petición del usuario requiere investigación o revisión de texto "
                 "y derivas al especialista adecuado. No respondes directamente.",
    model="gpt-4o-mini",
    handoffs=[agente_investigacion, agente_redaccion],
)
