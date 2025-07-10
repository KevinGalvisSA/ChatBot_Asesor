from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from dotenv import load_dotenv
import os

load_dotenv()  # Carga el archivo .env

# Cargar el modelo de embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Función para generar embeddings
def generate_embeddings(text):
    return model.encode(text)

# Crear la conexión con Qdrant Cloud
client = QdrantClient(
        url=os.getenv("QDRANT_URL"), 
        api_key=os.getenv("QDRANT_API_KEY")  
    ) # type: ignore

# Crear el vectorstore usando embeddings generados por sentence-transformers
vectorstore = Qdrant(client=client, collection_name="asesorias", embeddings=generate_embeddings) # type: ignore

# Devuelve el retriever
def get_qdrant_retriever():
    return vectorstore.as_retriever()
