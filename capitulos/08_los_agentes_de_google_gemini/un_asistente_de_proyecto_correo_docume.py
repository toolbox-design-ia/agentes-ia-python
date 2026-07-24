from googleapiclient.discovery import build
from auth import obtener_credenciales

def buscar_correos_gmail(
    query: str,
    max_resultados: int = 5
) -> dict:
    """
    Busca correos en Gmail con la sintaxis de búsqueda de Gmail.
    Ejemplos de query: 'from:juan@empresa.com', 'subject:presupuesto',
    'proyecto mercurio newer_than:7d'.

    Args:
        query: Expresión de búsqueda de Gmail
        max_resultados: Máximo de correos a devolver (1-20)

    Returns:
        Lista de correos con remitente, asunto, fecha y fragmento del cuerpo
    """
    creds = obtener_credenciales()
    service = build("gmail", "v1", credentials=creds)

    resultado = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_resultados
    ).execute()

    mensajes = resultado.get("messages", [])
    correos = []

    for msg in mensajes:
        detalle = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = {h["name"]: h["value"] for h in detalle["payload"]["headers"]}
        correos.append({
            "de": headers.get("From", ""),
            "asunto": headers.get("Subject", ""),
            "fecha": headers.get("Date", ""),
            "fragmento": detalle.get("snippet", "")
        })

    return {"correos": correos, "total_encontrados": len(correos)}
