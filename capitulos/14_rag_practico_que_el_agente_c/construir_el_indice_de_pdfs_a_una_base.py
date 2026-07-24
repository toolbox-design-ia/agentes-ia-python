import os
import pdfplumber
import tiktoken
import chromadb
from openai import OpenAI

# ── Configuración ──────────────────────────────────────────────
CARPETA_DOCUMENTOS = "documentos"
TAMANO_CHUNK = 700        # tokens por fragmento
SOLAPAMIENTO_CHARS = 200  # caracteres de solapamiento entre chunks
MODELO_EMBEDDINGS = "text-embedding-3-small"

# Clientes: OpenAI para embeddings, ChromaDB para el índice local
client_openai = OpenAI()   # lee OPENAI_API_KEY del entorno
client_chroma = chromadb.PersistentClient(path="indice_vectorial")
coleccion = client_chroma.get_or_create_collection("documentos")

# El tokenizador que usa OpenAI internamente
tokenizer = tiktoken.get_encoding("cl100k_base")


def contar_tokens(texto):
    """Devuelve cuántos tokens ocupa un texto."""
    return len(tokenizer.encode(texto))


def trocear_texto(texto, nombre_archivo, numero_pagina):
    """
    Divide texto en chunks con metadatos de origen.
    Cada chunk incluye un solapamiento con el anterior para
    no perder contexto en los cortes.
    """
    chunks = []
    inicio = 0
    indice_chunk = 0

    while inicio < len(texto):
        # Avanza carácter a carácter hasta alcanzar TAMANO_CHUNK tokens
        fin = inicio
        while fin < len(texto) and contar_tokens(texto[inicio:fin]) < TAMANO_CHUNK:
            fin += 1

        fragmento = texto[inicio:fin].strip()
        if fragmento:
            chunks.append({
                "texto": fragmento,
                "archivo": nombre_archivo,
                "pagina": numero_pagina,
                "indice": indice_chunk,
            })
            indice_chunk += 1

        if fin >= len(texto):
            break

        # El siguiente chunk empieza SOLAPAMIENTO_CHARS antes del final
        # para que los bordes del corte queden cubiertos
        inicio = max(inicio + 1, fin - SOLAPAMIENTO_CHARS)

    return chunks


def indexar_pdf(ruta_pdf):
    """Lee un PDF y devuelve todos sus chunks con metadatos."""
    nombre = os.path.basename(ruta_pdf)
    todos_los_chunks = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for numero_pagina, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if texto:  # hay páginas vacías o con solo imágenes
                chunks = trocear_texto(texto, nombre, numero_pagina)
                todos_los_chunks.extend(chunks)

    return todos_los_chunks


def guardar_en_indice(chunks):
    """Genera embeddings y los guarda en ChromaDB con sus metadatos."""
    if not chunks:
        print("  Sin texto extraíble.")
        return

    textos = [c["texto"] for c in chunks]

    # Una sola llamada a la API para todos los fragmentos: más eficiente
    respuesta = client_openai.embeddings.create(
        model=MODELO_EMBEDDINGS,
        input=textos
    )
    embeddings = [item.embedding for item in respuesta.data]

    # Cada entrada en ChromaDB necesita un ID único y estable
    ids = [f"{c['archivo']}_p{c['pagina']}_c{c['indice']}" for c in chunks]
    metadatos = [{"archivo": c["archivo"], "pagina": c["pagina"]} for c in chunks]

    coleccion.upsert(
        documents=textos,
        embeddings=embeddings,
        metadatas=metadatos,
        ids=ids,
    )
    print(f"  Guardados {len(chunks)} fragmentos.")


# ── Punto de entrada ───────────────────────────────────────────
if __name__ == "__main__":
    archivos = [
        os.path.join(CARPETA_DOCUMENTOS, f)
        for f in os.listdir(CARPETA_DOCUMENTOS)
        if f.endswith(".pdf")
    ]

    for ruta in archivos:
        print(f"Indexando: {ruta}")
        chunks = indexar_pdf(ruta)
        guardar_en_indice(chunks)

    print("Indexación completa.")
