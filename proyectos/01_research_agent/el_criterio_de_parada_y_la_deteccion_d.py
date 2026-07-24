def criterio_parada_cumplido(
    evidencias: list[EvidenceRecord],
    subpreguntas: list[str],
    spec: dict,
) -> bool:
    umbral = spec["criterio_de_parada"]

    if len(evidencias) < umbral["fuentes_minimas"]:
        return False

    cubiertas = {ev.subpregunta for ev in evidencias}
    cobertura = len(cubiertas) / len(subpreguntas)
    if cobertura < umbral["cobertura_minima"]:
        return False

    contradicciones_criticas = [
        ev for ev in evidencias
        if ev.contradice and ev.fiabilidad == "alta"
    ]
    if len(contradicciones_criticas) > umbral["contradicciones_criticas_sin_resolver"]:
        return False

    return True
