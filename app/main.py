from fastapi import FastAPI
from pydantic import BaseModel
from app.langgraph_flow import build_langgraph
from app.utils.database_manager import save_user_data, save_conversation_history
from app.utils.prompts import get_detection_prompt
from app.graph_nodes.state import State  # Importa el TypedDict para el estado

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
    
    # Construir el estado para el grafo, asegurándote de que el estado esté alineado con la definición de `State`
    state: State = {
        "messages": [],  # Asegúrate de agregar un valor adecuado aquí, por ejemplo, una lista de mensajes.
        "phone": user_input.phone,
        "chatType": "user",  # Esto es solo un ejemplo, usa el valor correcto según tu lógica.
        "data_user": user_data,  # Información del usuario
        "retrival": None,  # Agrega lo que necesites aquí
        "system_message": "Sistema en espera",  # Agrega un mensaje predeterminado o lo que necesites.
        "token_usage": {},  # Asegúrate de agregar una estructura adecuada.
        "question": user_input.question  # Agregar la pregunta al estado
    }

    # Imprimir el estado para depuración
    print("Estado antes de pasar al grafo:", state)

    # Verificar si el estado contiene la clave 'question'
    if "question" not in state:
        raise ValueError("La clave 'question' no está en el estado.")

    # Obtener la respuesta del bot usando el flujo de Langchain
    result = langgraph.invoke(state)  # Pasa todo el estado
    
    # Guardar la conversación en el historial (archivo JSON)
    conversation_history = save_conversation_history(user_input.phone, user_input.question, result["response"])
    
    # Reformatear la respuesta (si es necesario) para incluir más detalles o personalización
    formatted_response = result["response"]
    
    return {"response": formatted_response}
