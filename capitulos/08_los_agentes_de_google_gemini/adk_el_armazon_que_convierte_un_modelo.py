from google.adk import Agent

asistente = Agent(
    name="asistente_proyecto",
    model="gemini-3.5-flash",
    instruction="""Eres un asistente de gestión de proyectos.
    Cuando el usuario pregunte por correos, documentos o disponibilidad,
    usa las herramientas disponibles para obtener información real.
    Responde siempre en español y sé conciso.""",
    tools=[]  # Se completará en la siguiente sección
)
