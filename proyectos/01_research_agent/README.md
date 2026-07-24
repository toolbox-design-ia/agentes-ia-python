# Proyecto 1 — Agente de investigacion (cap. 23)

`config.py` guarda el contrato (ESPECIFICACION) como documentacion viva; `research_agent.py` contiene las funciones impresas en el capitulo, completas: planificar, leer_pagina, extraer_fragmento, buscar_local, buscar_web_propia, registro de evidencias, criterio de parada, contradicciones e informe citado.

Necesita: ANTHROPIC_API_KEY en el .env (Anexo A campo a campo) y, para busqueda web, SERPER_API_KEY. Ejecutar:

```
python research_agent.py "tu pregunta"
```
