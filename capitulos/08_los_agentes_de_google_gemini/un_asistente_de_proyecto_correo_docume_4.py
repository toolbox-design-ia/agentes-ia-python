from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from tools.gmail_tools import buscar_correos_gmail
from tools.drive_tools import buscar_en_drive
from tools.calendar_tools import consultar_agenda

root_agent = Agent(
    name="asistente_proyecto",
    model="gemini-3.5-flash",
    instruction="""Eres un asistente de coordinación de proyectos con acceso a
    Gmail, Drive y Calendar del usuario.

    Cuando el usuario haga una pregunta sobre correos, documentos o agenda:
    1. Usa las herramientas disponibles para obtener datos reales.
    2. No inventes ni supongas datos que no hayas recuperado con herramientas.
    3. Si la pregunta requiere más de una herramienta, úsalas en secuencia.
    4. Responde en español, de forma concisa y útil.
    5. Para búsquedas en Gmail, usa la sintaxis nativa:
       'from:', 'subject:', 'newer_than:7d', etc.
    6. Para fechas en Calendar, usa el formato ISO 8601:
       '2026-07-10T09:00:00'.
    7. Antes de buscar, informa brevemente al usuario qué vas a consultar.
    """,
    tools=[
        buscar_correos_gmail,
        buscar_en_drive,
        consultar_agenda,
    ]
)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="asistente_proyecto",
    session_service=session_service
)
