import chromadb
from openai import OpenAI

client_openai = OpenAI()
client_chroma = chromadb.PersistentClient(path="indice_vectorial")
coleccion = client_chroma.get_collection("documentos")


def buscar_en_documentos(pregunta: str, n_resultados: int = 4) -> str:
    """
    Convierte la pregunta en un embedding, busca los fragmentos
    más cercanos en el índice y los devuelve con su fuente.
    """
    # La pregunta pasa por el mismo modelo de embeddings que los documentos
    respuesta_emb = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=[pregunta]
    )
    vector_pregunta = respuesta_emb.data[0].embedding

    # ChromaDB devuelve los n_resultados fragmentos más próximos
    resultados = coleccion.query(
        query_embeddings=[vector_pregunta],
        n_results=n_resultados,
        include=["documents", "metadatas", "distances"],
    )

    if not resultados["documents"][0]:
        return "No se encontraron fragmentos relevantes en los documentos."

    fragmentos = []
    for texto, meta in zip(
        resultados["documents"][0],
        resultados["metadatas"][0],
    ):
        encabezado = f"[Fuente: {meta['archivo']}, página {meta['pagina']}]"
        fragmentos.append(f"{encabezado}\n{texto}")

    # Separador visual entre fragmentos para que el modelo los distinga
    return "\n\n---\n\n".join(fragmentos)
