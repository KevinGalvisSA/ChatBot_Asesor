from fastapi import FastAPI
from pydantic import BaseModel
from app.langgraph_flow import build_langgraph
from app.utils.database_manager import save_user_data, save_conversation_history  # Importar funciones para manejar los archivos JSON
from app.utils.prompts import get_detection_prompt

app = FastAPI()

class UserInput(BaseModel):
    question: str
    name: str
    phone: str

langgraph = build_langgraph()

@app.post("/ask")
async def ask(user_input: UserInput):
    # Guardar la información del usuario en el archivo JSON (simulando la base de datos)
    user_data = {
        "name": user_input.name,
        "phone": user_input.phone
    }
    
    # Guardar o actualizar los datos del usuario (esto simula la base de datos de usuarios)
    save_user_data(user_data)

    # Usar get_detection_prompt para detectar nombre y teléfono si es necesario
    user_message = user_input.question
    detection_prompt = get_detection_prompt(user_message, user_data)
    
    # Construir el estado para el grafo, asegurándote de que 'question' esté presente
    state = {
        "question": user_input.question,
        "conversation_history": [],
        "user_data": {
            "username": user_input.name,
            "phone": user_input.phone,
        },
    }

    # Verificar si el estado contiene la clave 'question'
    if "question" not in state:
        raise ValueError("La clave 'question' no está presente en el estado.")
    
    # Obtener la respuesta del bot usando el flujo de Langchain
    result = langgraph.invoke(state)  # Pasa todo el estado
    
    # Guardar la conversación en el historial (archivo JSON)
    conversation_history = save_conversation_history(user_input.phone, user_input.question, result["response"])
    
    # Reformatear la respuesta (si es necesario) para incluir más detalles o personalización
    formatted_response = result["response"]
    
    return {"response": formatted_response}
