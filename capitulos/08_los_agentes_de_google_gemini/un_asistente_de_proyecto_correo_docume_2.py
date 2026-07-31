def buscar_en_drive(
    termino: str,
    tipo_archivo: str = ""
) -> dict:
    """
    Busca archivos en Google Drive por nombre o contenido.

    Args:
        termino: Palabra o frase a buscar
        tipo_archivo: Opcional — 'documento', 'hoja_calculo',
                      'presentacion' o 'pdf'

    Returns:
        Lista de archivos encontrados con nombre, tipo, fecha y enlace
    """
    creds = obtener_credenciales()
    service = build("drive", "v3", credentials=creds)

    mime_types = {
        "documento":      "application/vnd.google-apps.document",
        "hoja_calculo":   "application/vnd.google-apps.spreadsheet",
        "presentacion":   "application/vnd.google-apps.presentation",
        "pdf":            "application/pdf",
    }

    # Las comillas simples del termino romperian la consulta
    seguro = termino.replace("\\", "\\\\").replace("'", "\\'")
    query = f"(name contains '{seguro}' or fullText contains '{seguro}')"
    if tipo_archivo in mime_types:
        query += f" and mimeType='{mime_types[tipo_archivo]}'"

    resultado = service.files().list(
        q=query,
        pageSize=10,
        fields="files(id, name, mimeType, modifiedTime, webViewLink)"
    ).execute()

    return {
        "archivos": [
            {
                "nombre":     f["name"],
                "tipo":       f["mimeType"],
                "modificado": f["modifiedTime"],
                "enlace":     f["webViewLink"]
            }
            for f in resultado.get("files", [])
        ]
    }
