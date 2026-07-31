from agents import Agent
from agents import WebSearchTool, CodeInterpreterTool, FileSearchTool

agente_investigador = Agent(
    name="Investigador editorial",
    instructions="Investigas temas usando búsqueda web y analizas datos con código cuando sea necesario. "
                 "Citas las fuentes que encuentres.",
    model="gpt-4o",
    tools=[
        WebSearchTool(),
        CodeInterpreterTool(),
        FileSearchTool(vector_store_ids=["vs_catalogo_editorial"]),
    ],
)
