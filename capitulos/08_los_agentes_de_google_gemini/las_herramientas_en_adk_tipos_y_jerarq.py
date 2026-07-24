"""Contrato de herramienta ADK impreso en el capitulo 8.

En ADK la firma y el docstring SON la definicion de la herramienta (el
framework los lee para describirla al modelo); el cuerpo con ... es
intencional: el capitulo explica el patron, no una implementacion.
"""

def buscar_correos(query: str, max_resultados: int = 5) -> dict:
    """
    Busca correos en Gmail usando la cadena de búsqueda especificada.

    Args:
        query: Cadena de búsqueda en formato Gmail (ej. "from:cliente@empresa.com")
        max_resultados: Número máximo de correos a devolver

    Returns:
        Diccionario con lista de correos encontrados
    """
    ...
