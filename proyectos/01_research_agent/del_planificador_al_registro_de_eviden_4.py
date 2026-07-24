import chromadb

def buscar_local(subpregunta: str, coleccion) -> list[dict]:
    resultados = coleccion.query(
        query_texts=[subpregunta],
        n_results=3,
    )
    return [
        {
            "url": meta.get("fuente", "local"),
            "title": meta.get("titulo", "Documento local"),
            "snippet": doc,
        }
        for doc, meta in zip(
            resultados["documents"][0],
            resultados["metadatas"][0],
        )
    ]
