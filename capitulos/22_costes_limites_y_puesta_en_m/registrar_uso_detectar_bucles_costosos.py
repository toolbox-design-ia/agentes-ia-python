import logging
import json
from datetime import datetime, timezone

logger = logging.getLogger("agente.uso")

def registrar_uso(response, modelo: str, precios: dict, presupuesto=None):
    uso = response.usage
    tokens_entrada = uso.input_tokens
    tokens_salida = uso.output_tokens
    cache_lectura = getattr(uso, "cache_read_input_tokens", 0)
    cache_escritura = getattr(uso, "cache_creation_input_tokens", 0)
    tokens_normales = tokens_entrada - cache_lectura - cache_escritura

    p = precios[modelo]
    coste = (
        tokens_normales * p["entrada"]
        + cache_escritura * p["cache_escritura"]
        + cache_lectura * p["cache_lectura"]
        + tokens_salida * p["salida"]
    ) / 1_000_000  # precios en USD por millón de tokens

    registro = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "modelo": modelo,
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "cache_lectura": cache_lectura,
        "cache_escritura": cache_escritura,
        "coste_usd": round(coste, 6),
    }
    logger.info(json.dumps(registro))

    if presupuesto:
        presupuesto.registrar_llamada(tokens_salida, coste)

    return coste
