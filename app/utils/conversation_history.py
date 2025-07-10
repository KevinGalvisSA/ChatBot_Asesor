import json
import os

def save_conversation(user_data, user_message, agent_response):
    """Guarda el historial de la conversación en un archivo JSON"""
    conversation_file = f"conversations/{user_data["phone"]}_history.json"
    
    # Verificar si el archivo ya existe
    if os.path.exists(conversation_file):
        with open(conversation_file, "r") as file:
            conversation_history = json.load(file)
    else:
        conversation_history = []
    
    # Agregar el nuevo mensaje y respuesta al historial
    conversation_history.append({
        "user_message": user_message,
        "agent_response": agent_response,
        "timestamp": "fecha y hora aquí"  # Puedes añadir un timestamp si es necesario
    })
    
    # Guardar el historial de nuevo
    with open(conversation_file, "w") as file:
        json.dump(conversation_history, file, indent=4)
    
    # Retornar el historial actualizado
    return conversation_history
