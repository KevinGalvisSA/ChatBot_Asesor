import os
from dotenv import load_dotenv
import google.generativeai as genai # type: ignore

load_dotenv()
# Configurar la clave API de Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_llm():
    try:
        # Usar el modelo "gemini-1.5-pro" para generar texto
        response = genai.generate_content( 
            model="gemini-1.5-pro",  # Nombre del modelo de Google Gemini
            prompt="¿Cómo estás?",  # El prompt o mensaje que envías al modelo
            temperature=0.4  # Controla la creatividad de la respuesta
        )
        return response.result  # Obtén la respuesta del modelo
    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"

# Probar la función
response = get_gemini_llm()
print(response)  # Imprimir la respuesta del modelo
