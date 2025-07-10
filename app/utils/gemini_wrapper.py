import os
from dotenv import load_dotenv
import google.genai as genai  # type: ignore # Asegúrate de importar desde google.genai

load_dotenv()

# Configurar la clave API de Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Crear el cliente con la clave API
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_gemini_llm():
    try:
        # Usar el modelo "gemini-2.5-flash" para generar texto
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Nombre del modelo de Google Gemini
            contents="¿Cómo estás?",  # El prompt o mensaje que envías al modelo
        )
        return response.text  # Obtén la respuesta del modelo
    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"

# Probar la función
response = get_gemini_llm()
print(response)  # Imprimir la respuesta del modelo
