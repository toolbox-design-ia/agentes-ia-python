[Español](README.md) · [English](README.en.md) · [Français](README.fr.md)

# Agentes de IA con Python — Código del libro

Repositorio companion de **«Agentes de IA con Python»** (Henry Ramírez Reyes, serie INTELIGENCIA ARTIFICIAL, Studio35).

El código está organizado por capítulo en `capitulos/` y los tres proyectos completos en `proyectos/`. El Anexo A del libro explica, paso a paso y sin experiencia previa, cómo descargar este repositorio, crear el entorno y configurar las claves de API con límite de gasto.

**Regla del umbral:** los fragmentos de hasta 30 líneas están impresos íntegros en el libro; los archivos mayores viven aquí y el libro imprime el extracto que explica cada decisión. Los archivos `fragmentos.md` recogen los extractos impresos que forman parte de archivos mayores.

## Tabla capítulo → código

Solo aparecen los capítulos con código propio; los de criterio o comparación de plataformas no generan carpeta. Los tres proyectos finales viven aparte porque cada uno integra material de varios capítulos.

| Cap. | Título | Carpeta | Archivos |
|---|---|---|---|
| 01 | Qué es un agente de IA | `capitulos/01_que_es_un_agente_de_ia_del_c/` | 1 |
| 03 | Python mínimo para agentes | `capitulos/03_python_minimo_para_agentes_l/` | 3 |
| 04 | Tu primera conversación por código | `capitulos/04_tu_primera_conversacion_por/` | 3 |
| 06 | Los agentes de Anthropic | `capitulos/06_los_agentes_de_anthropic_cla/` | 2 |
| 07 | Los agentes de OpenAI | `capitulos/07_los_agentes_de_openai_agents/` | 3 |
| 08 | Los agentes de Google | `capitulos/08_los_agentes_de_google_gemini/` | 7 |
| 11 | El bucle del agente en cien líneas de Python | `capitulos/11_el_bucle_del_agente_en_cien/` | 1 |
| 12 | Herramientas: darle manos al agente | `capitulos/12_herramientas_darle_manos_al/` | 3 |
| 13 | Memoria: que el agente recuerde | `capitulos/13_memoria_que_el_agente_recuer/` | 6 |
| 14 | RAG práctico | `capitulos/14_rag_practico_que_el_agente_c/` | 4 |
| 15 | MCP: conectar tu agente a todo | `capitulos/15_mcp_conectar_tu_agente_a_tod/` | 1 |
| 22 | Costes, límites y puesta en marcha | `capitulos/22_costes_limites_y_puesta_en_m/` | 5 |

| Cap. | Proyecto | Carpeta | Punto de entrada |
|---|---|---|---|
| 23 | Proyecto 1: agente de investigación | `proyectos/01_research_agent/` | `research_agent.py` |
| 24 | Proyecto 2: agente de automatización personal | `proyectos/02_personal_automation/` | `gmail_agent.py` |
| 25 | Proyecto 3: tu asistente con MCP | `proyectos/03_mcp_assistant/` | `client.py + servidores` |

Dentro de cada carpeta, el nombre de archivo corresponde a la sección del capítulo de la que sale, con un sufijo numérico cuando una misma sección imprime varios bloques.

## Un repositorio, tres ediciones

Este repositorio es compartido por las ediciones en español, inglés y francés del libro. El código es único (identificadores en inglés); cada edición imprime los fragmentos con los comentarios en su idioma. Documentación: README y guías en los tres idiomas.

## Licencia

MIT para el código. El texto del libro tiene todos los derechos reservados.
