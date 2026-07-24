import uuid
from datetime import date

def registrar_evidencia(
    resultado: dict,
    subpregunta: str,
    tipo: str,
    es_inferencia: bool = False,
) -> EvidenceRecord:
    return EvidenceRecord(
        id=f"ev_{uuid.uuid4().hex[:6]}",
        source=resultado["url"],
        title=resultado["title"],
        snippet=resultado["snippet"],
        fecha_recuperacion=date.today().isoformat(),
        fiabilidad="alta" if tipo == "local" else "media",
        tipo=tipo,
        subpregunta=subpregunta,
        es_inferencia=es_inferencia,
    )
