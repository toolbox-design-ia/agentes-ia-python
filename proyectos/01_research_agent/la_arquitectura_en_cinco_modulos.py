from dataclasses import dataclass, field

@dataclass
class EvidenceRecord:
    id: str                         # identificador único, p. ej. "ev_001"
    source: str                     # URL o ruta de archivo
    title: str
    snippet: str                    # fragmento relevante (≤ 800 caracteres)
    fecha_recuperacion: str         # formato ISO 8601
    fiabilidad: str                 # "alta" | "media" | "baja"
    tipo: str                       # "web" | "local"
    subpregunta: str                # a qué subpregunta responde
    es_inferencia: bool = False
    contradice: list[str] = field(default_factory=list)
