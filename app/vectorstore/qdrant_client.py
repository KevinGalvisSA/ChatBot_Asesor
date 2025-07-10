import os
from dotenv import load_dotenv  # Asegúrate de importar load_dotenv
from langchain_community.vectorstores import Qdrant  # type: ignore
from langchain_community.embeddings import GooglePalmEmbeddings  # type: ignore
from qdrant_client import QdrantClient 

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_qdrant_retriever():
    # Asegurarse de que las claves están disponibles
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    # Verificar si alguna clave es None
    if not qdrant_url or not qdrant_api_key or not google_api_key:
        raise ValueError("Faltan claves de API en las variables de entorno. Asegúrate de definir QDRANT_URL, QDRANT_API_KEY, y GOOGLE_API_KEY en el archivo .env.")

    # Crear la conexión con Qdrant Cloud
    client = QdrantClient(
        url=qdrant_url, 
        api_key=qdrant_api_key  
    ) # type: ignore
    
    # Crear el modelo de embeddings usando Google Palm
    embeddings = GooglePalmEmbeddings(google_api_key=google_api_key, client=client)  
    
    # Crear el vectorstore y lo conecta con Qdrant
    vectorstore = Qdrant(client=client, collection_name="asesorias", embeddings=embeddings)
    
    # Devuelve el retriever
    return vectorstore.as_retriever()
