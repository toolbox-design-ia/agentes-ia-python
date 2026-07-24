"""Proyecto 1 (capitulo 23): agente de investigacion con evidencias citadas.

Los nombres de las funciones son los impresos en el capitulo: planificar,
leer_pagina, extraer_fragmento, buscar_local, buscar_web_propia,
registrar_evidencia, criterio_parada_cumplido, detectar_contradiccion,
escribir_informe e investigar.
"""
import json
import os
import sys
import uuid
from dataclasses import dataclass, field

import anthropic
import httpx
from dotenv import load_dotenv

from config import ESPECIFICACION

load_dotenv()
cliente = anthropic.Anthropic()


@dataclass
class EvidenceRecord:
    id: str                       # identificador unico, p. ej. "EV-3f2a"
    subpregunta: str
    fuente: str                   # URL o nombre de coleccion local
    fragmento: str
    tipo: str                     # "web" | "local"
    es_inferencia: bool = False
    contradice: list = field(default_factory=list)


def planificar(pregunta: str) -> list[str]:
    respuesta = cliente.messages.create(
        model=ESPECIFICACION["modelo_planificador"],
        max_tokens=512,
        messages=[{"role": "user", "content": (
            "Descompon esta pregunta de investigacion en como maximo "
            f"{ESPECIFICACION['max_subpreguntas']} subpreguntas concretas y "
            "verificables. Responde SOLO con una lista JSON de strings.\n\n"
            f"Pregunta: {pregunta}")}],
    )
    texto = respuesta.content[0].text.strip()
    inicio, fin = texto.find("["), texto.rfind("]") + 1
    return json.loads(texto[inicio:fin])


def leer_pagina(url: str) -> str:
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True,
                      headers={"User-Agent": "ResearchAgent/1.0 (libro)"})
        r.raise_for_status()
        return r.text[:ESPECIFICACION["max_caracteres_pagina"]]
    except httpx.HTTPError:
        return ""


def extraer_fragmento(texto_pagina: str, subpregunta: str) -> dict:
    respuesta = cliente.messages.create(
        model=ESPECIFICACION["modelo_extractor"],
        max_tokens=400,
        messages=[{"role": "user", "content": (
            "Del siguiente texto, extrae el fragmento (2-4 frases) que mejor "
            "responda a la subpregunta, sin parafrasear. Si no hay nada "
            "relevante responde NO_RELEVANTE.\n\n"
            f"Subpregunta: {subpregunta}\n\nTexto:\n{texto_pagina}")}],
    )
    fragmento = respuesta.content[0].text.strip()
    return {"fragmento": fragmento,
            "relevante": "NO_RELEVANTE" not in fragmento}


def buscar_local(subpregunta: str, coleccion) -> list[dict]:
    resultados = coleccion.query(query_texts=[subpregunta], n_results=3)
    return [{"fuente": f"local:{i}", "texto": doc}
            for i, doc in enumerate(resultados["documents"][0])]


def buscar_web_propia(subpregunta: str, api_key: str) -> list[dict]:
    r = httpx.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": subpregunta,
              "num": ESPECIFICACION["max_fuentes_por_subpregunta"]},
        timeout=10,
    )
    r.raise_for_status()
    return [{"fuente": item["link"], "texto": item.get("snippet", "")}
            for item in r.json().get("organic", [])]


def registrar_evidencia(resultado: dict, subpregunta: str, tipo: str,
                        es_inferencia: bool = False) -> EvidenceRecord:
    return EvidenceRecord(
        id=f"EV-{uuid.uuid4().hex[:4]}",
        subpregunta=subpregunta,
        fuente=resultado["fuente"],
        fragmento=resultado["fragmento"],
        tipo=tipo,
        es_inferencia=es_inferencia,
    )


def criterio_parada_cumplido(evidencias: list[EvidenceRecord],
                             subpreguntas: list[str], spec: dict) -> bool:
    umbral = spec["min_evidencias_por_subpregunta"]
    return all(
        sum(1 for ev in evidencias if ev.subpregunta == sp) >= umbral
        for sp in subpreguntas)


def detectar_contradiccion(nueva: EvidenceRecord,
                           existentes: list[EvidenceRecord]) -> list[str]:
    relevantes = [ev for ev in existentes
                  if ev.subpregunta == nueva.subpregunta and ev.id != nueva.id]
    if not relevantes:
        return []
    listado = "\n".join(f"[{ev.id}] {ev.fragmento}" for ev in relevantes)
    respuesta = cliente.messages.create(
        model=ESPECIFICACION["modelo_extractor"],
        max_tokens=200,
        messages=[{"role": "user", "content": (
            "Nueva evidencia:\n" + nueva.fragmento +
            "\n\nEvidencias previas:\n" + listado +
            "\n\nResponde SOLO con una lista JSON de IDs de evidencias "
            "previas que la nueva CONTRADIGA (lista vacia si ninguna).")}],
    )
    texto = respuesta.content[0].text
    try:
        return json.loads(texto[texto.find("["):texto.rfind("]") + 1])
    except (ValueError, json.JSONDecodeError):
        return []


def actualizar_contradicciones(ev: EvidenceRecord,
                               evidencias: list[EvidenceRecord]) -> None:
    ev.contradice = detectar_contradiccion(ev, evidencias)


def escribir_informe(pregunta: str, evidencias: list[EvidenceRecord],
                     spec: dict) -> str:
    contexto = "\n\n".join(
        f"[{ev.id}] ({ev.fuente}) {ev.fragmento}" for ev in evidencias)
    contradicciones = [ev for ev in evidencias if ev.contradice]
    nota = ""
    if contradicciones:
        nota = ("\nSenala explicitamente los desacuerdos entre: " +
                ", ".join(f"{ev.id} vs {ev.contradice}"
                          for ev in contradicciones))
    respuesta = cliente.messages.create(
        model=spec["modelo_redactor"],
        max_tokens=2000,
        messages=[{"role": "user", "content": (
            f"Pregunta: {pregunta}\n\nEvidencias:\n{contexto}\n\n"
            "Redacta un informe en markdown que responda la pregunta usando "
            "SOLO estas evidencias. Cada afirmacion debe llevar el ID de la "
            "evidencia que la sostiene, entre corchetes. Cierra con la lista "
            "de fuentes por ID." + nota)}],
    )
    return respuesta.content[0].text


def investigar(pregunta: str, coleccion_local=None, spec=None) -> str:
    if spec is None:
        spec = ESPECIFICACION
    subpreguntas = planificar(pregunta)
    evidencias: list[EvidenceRecord] = []
    serper_key = os.getenv("SERPER_API_KEY", "")
    for sp in subpreguntas:
        candidatos = []
        if coleccion_local is not None:
            for res in buscar_local(sp, coleccion_local):
                candidatos.append((res, "local"))
        if serper_key:
            for res in buscar_web_propia(sp, serper_key):
                texto = leer_pagina(res["fuente"]) or res["texto"]
                candidatos.append(({"fuente": res["fuente"],
                                    "texto": texto}, "web"))
        for res, tipo in candidatos:
            extraccion = extraer_fragmento(res["texto"], sp)
            if not extraccion["relevante"]:
                continue
            ev = registrar_evidencia(
                {"fuente": res["fuente"],
                 "fragmento": extraccion["fragmento"]}, sp, tipo)
            actualizar_contradicciones(ev, evidencias)
            evidencias.append(ev)
        if criterio_parada_cumplido(evidencias, subpreguntas, spec):
            break
    informe = escribir_informe(pregunta, evidencias, spec)
    with open(spec["informe_salida"], "w", encoding="utf-8") as f:
        f.write(informe)
    return informe


if __name__ == "__main__":
    pregunta = " ".join(sys.argv[1:]) or input("Pregunta a investigar: ")
    print(investigar(pregunta))
    print(f"\nInforme guardado en {ESPECIFICACION['informe_salida']}")
