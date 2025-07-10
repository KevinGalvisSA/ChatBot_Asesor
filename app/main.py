# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel, root_validator, ValidationError
from app.langgraph_flow import build_langgraph
from app.utils.database_manager import save_user_data, save_conversation_history  # Importar funciones para manejar los archivos JSON
from app.utils.prompts import get_detection_prompt

app = FastAPI()

class UserInput(BaseModel):
    question: str
    name: str
    phone: str

    @root_validator(pre=True)
    def check_for_none(cls, values):
        # Validación para asegurarse de que no haya valores None
        if not values.get('question'):
            raise ValueError('El campo question no puede ser vacío')
        if not values.get('name'):
            raise ValueError('El campo name no puede ser vacío')
        if not values.get('phone'):
            raise ValueError('El campo phone no puede ser vacío')
        return values

# Construir el grafo del bot
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
    
    # Obtener la respuesta del bot usando el flujo de Langchain
    result = langgraph.invoke({"question": user_input.question}) # type: ignore
    
    # Guardar la conversación en el historial (archivo JSON)
    conversation_history = save_conversation_history(user_input.phone, user_input.question, result["response"])
    
    # Reformatear la respuesta (si es necesario) para incluir más detalles o personalización
    formatted_response = result["response"]
    
    return {"response": formatted_response}
