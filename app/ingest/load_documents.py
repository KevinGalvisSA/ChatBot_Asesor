import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "asesorias")  # Valor por defecto si no se encuentra

# Cargar el modelo de Sentence-Transformers (usamos "paraphrase-MiniLM-L6-v2" para 768 dimensiones)
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def load_and_split_documents(file_path: str):
    """Carga el documento PDF y lo divide en fragmentos."""
    # Cargar el archivo PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Dividir el documento en fragmentos más pequeños para facilitar la búsqueda
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)

def generate_embeddings(docs):
    """Genera embeddings utilizando Sentence-Transformers."""
    embeddings = model.encode([doc.page_content for doc in docs], show_progress_bar=True)
    return embeddings

def upload_to_qdrant(docs):
    """Sube los documentos a Qdrant y genera los embeddings."""
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Verificar si la colección existe, si no, crearla
    existing_collections = [col.name for col in client.get_collections().collections]
    if COLLECTION_NAME not in existing_collections:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    # Generar los embeddings
    embeddings = generate_embeddings(docs)

    # Crear los textos y metadatos
    texts = [doc.page_content for doc in docs]
    metadatas = [{"source": "asesoria.pdf"} for _ in docs]  # Asumiendo que todos los documentos son de este archivo

    # Subir los embeddings y metadatos a Qdrant usando upsert
    points = [
        {
            "id": i,  # Generamos un ID único para cada punto
            "vector": embedding.tolist(),  # Aseguramos que el embedding sea un array estándar
            "payload": metadata  # Los metadatos asociados
        }
        for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))
    ]

    # Insertamos los puntos en la colección de Qdrant
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

if __name__ == "__main__":
    # Ruta del archivo PDF
    file_path = "app/knowledge/asesoria.pdf"  # Asegúrate de que esta ruta sea correcta

    print("[🚀] Cargando y dividiendo documentos...")
    docs = load_and_split_documents(file_path)  # Cargar el PDF y dividirlo en fragmentos
    print(f"[✅] {len(docs)} fragmentos generados. Subiendo a Qdrant Cloud...")
    upload_to_qdrant(docs)
    print("[🎉] ¡Documentos subidos exitosamente a Qdrant Cloud!")
