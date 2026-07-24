ESPECIFICACION = {
    "objetivo": (
        "Responder preguntas de investigación con trazabilidad documental completa."
    ),
    "alcance": [
        "web abierta (sin muros de pago)",
        "documentos locales indexados en la colección RAG",
        "dominios permitidos: configurable por proyecto",
    ],
    "salida": (
        "informe Markdown con resumen ejecutivo, hallazgos por subpregunta, "
        "contradicciones detectadas, notas al pie y bibliografía"
    ),
    "restricciones": [
        "toda afirmación necesita fuente identificable",
        "las inferencias se etiquetan explícitamente",
        "las contradicciones entre fuentes se señalan, no se resuelven por defecto",
    ],
    "criterio_de_parada": {
        "fuentes_minimas": 5,
        "cobertura_minima": 0.8,
        "contradicciones_criticas_sin_resolver": 0,
    },
}
