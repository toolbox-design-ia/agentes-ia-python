def consultar_agenda(
    fecha_inicio: str,
    fecha_fin: str
) -> dict:
    """
    Consulta eventos del calendario principal en un rango de fechas.

    Args:
        fecha_inicio: Inicio del rango en ISO 8601 (ej. '2026-07-10T09:00:00')
        fecha_fin:    Fin del rango en ISO 8601    (ej. '2026-07-10T18:00:00')

    Returns:
        Lista de eventos con título, hora de inicio y fin, y asistentes
    """
    creds = obtener_credenciales()
    service = build("calendar", "v3", credentials=creds)

    # Las marcas sin zona se interpretan en la zona de timeZone;
    # anadir una "Z" a una hora local la declararia UTC por error.
    eventos = service.events().list(
        calendarId="primary",
        timeMin=fecha_inicio,
        timeMax=fecha_fin,
        timeZone="Europe/Madrid",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return {
        "eventos": [
            {
                "titulo":     e.get("summary", "Sin título"),
                "inicio":     e["start"].get("dateTime", e["start"].get("date")),
                "fin":        e["end"].get("dateTime", e["end"].get("date")),
                "asistentes": [a["email"] for a in e.get("attendees", [])]
            }
            for e in eventos.get("items", [])
        ]
    }
