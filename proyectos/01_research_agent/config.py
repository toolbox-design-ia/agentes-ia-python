"""Contrato del agente de investigacion (capitulo 23).

Guardar la especificacion junto a la logica sirve como documentacion viva:
cualquiera que revise el codigo sabe que promete el agente y que no.
"""
ESPECIFICACION = {
    "max_subpreguntas": 5,
    "max_fuentes_por_subpregunta": 3,
    "min_evidencias_por_subpregunta": 2,
    "modelo_planificador": "claude-opus-4-8",
    "modelo_extractor": "claude-haiku-4-5",
    "modelo_redactor": "claude-opus-4-8",
    "max_caracteres_pagina": 4000,
    "informe_salida": "informe.md",
}
