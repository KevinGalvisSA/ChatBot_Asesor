import os
import fitz  # Para leer PDFs
from sentence_transformers import SentenceTransformer  # Para crear embeddings
from qdrant_client import QdrantClient  # Para interactuar con Qdrant
from qdrant_client.models import VectorParams, Distance, PointStruct  # Tipos necesarios para Qdrant
import uuid
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "asesorias")  # Valor por defecto si no se encuentra

PDF_PATH = "app/knowledge/asesoria.pdf"  # Ruta del PDF a procesar

# Función para extraer texto del archivo PDF
def extract_text(path: str) -> str:
    doc = fitz.open(path) # type: ignore
    text = ""
    for page in doc:
        text += page.get_text() # type: ignore
    return text

# Función para dividir el texto en fragmentos de tamaño máximo
def split_text(text: str, max_len: int = 500) -> list[str]:
    chunks = []
    current = ""
    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) < max_len:
            current += paragraph + " "
        else:
            chunks.append(current.strip())
            current = paragraph + " "
    if current:
        chunks.append(current.strip())
    return chunks

# Función para cargar los fragmentos y subirlos a Qdrant
def upload_chunks(chunks: list[str]):
    # Usamos el modelo SentenceTransformer para obtener los embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Conectar a Qdrant
    qdrant = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY if QDRANT_API_KEY else None,
    )

    # Verificar si la colección existe, si no, crearla
    existing_collections = [col.name for col in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing_collections:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    # Filtramos fragmentos vacíos antes de procesarlos
    chunks = [chunk for chunk in chunks if chunk.strip()]

    if not chunks:
        print("⚠️ No se encontraron fragmentos válidos para subir a Qdrant.")
        return

    # Generar los embeddings
    vectors = model.encode(chunks).tolist()

    # Crear puntos con un ID único y los embeddings
    points = [
        PointStruct(
            id=str(uuid.uuid4()),  # ID único generado
            vector=vec,  # El vector de embedding
            payload={"text": chunk}  # Información adicional
        )
        for vec, chunk in zip(vectors, chunks)
    ]

    # Subir los puntos a la colección de Qdrant
    qdrant.upload_points(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"✅ Subidos {len(points)} fragmentos a Qdrant.")

# Función principal
if __name__ == "__main__":
    # Extraer el texto del PDF
    print("📥 Extrayendo texto del PDF...")
    raw_text = extract_text(PDF_PATH)

    # Dividir el texto en fragmentos
    print("✂️ Dividiendo texto...")
    chunks = split_text(raw_text)

    # Subir los fragmentos generados a Qdrant
    print(f"📡 Subiendo {len(chunks)} fragmentos a Qdrant...")
    upload_chunks(chunks)
