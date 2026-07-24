from agents import Agent, Runner, SQLiteSession

agente = Agent(
    name="asistente_proyecto",
    instructions="Eres un asistente técnico que ayuda a desarrollar pipelines en Python.",
)

# La sesión persiste el historial en SQLite automáticamente
sesion = SQLiteSession("sesion_pipeline_001", "sesiones.db")

resultado = await Runner.run(
    agente,
    input="¿Dónde quedamos con el parser de CSV?",
    session=sesion,
)
