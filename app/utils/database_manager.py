import json
import os

def create_file_if_not_exists(file_path, default_data=None):
    """Verifica si el archivo JSON existe, si no, lo crea con datos predeterminados."""
    if not os.path.exists(file_path):
        print(f"[INFO] El archivo {file_path} no existe. Creando archivo nuevo...")
        # Si no existe, lo crea con los datos predeterminados
        with open(file_path, "w") as file:
            json.dump(default_data or {}, file, indent=4)
        print(f"[INFO] Archivo {file_path} creado con éxito.")
    else:
        print(f"[INFO] El archivo {file_path} ya existe.")

def load_json_data(file_path):
    """Carga los datos de un archivo JSON. Si no existe, lo crea con un diccionario vacío."""
    create_file_if_not_exists(file_path)  # Verifica si el archivo existe
    with open(file_path, "r") as file:
        return json.load(file)

def save_user_data(user_data):
    """Guarda la información del usuario en el archivo "users.json"."""
    users_file = "users.json"
    users_db = load_json_data(users_file)  # Cargar los datos de usuarios (o diccionario vacío)

    # Usar el teléfono como clave única
    phone = user_data["phone"]
    
    # Si el usuario no existe, lo agregamos
    if phone not in users_db:
        users_db[phone] = {
            "name": user_data["name"],
            "phone": user_data["phone"]
        }
        print(f"[INFO] Usuario {user_data["name"]} agregado.")
    else:
        print(f"[INFO] El usuario {user_data["name"]} ya existe.")
    
    # Guardar la información actualizada de los usuarios
    with open(users_file, "w") as file:
        json.dump(users_db, file, indent=4)
    
    return users_db

def save_conversation_history(phone, user_message, agent_response):
    """Guarda el historial de conversación en un archivo JSON en la carpeta "conversations/"."""
    conversation_file = f"conversations/{phone}_history.json"
    
    create_file_if_not_exists(conversation_file, default_data=[])  # Verifica si el archivo existe
    
    # Cargar el historial de conversaciones
    conversation_history = load_json_data(conversation_file)
    
    # Agregar la nueva interacción al historial
    conversation_history.append({
        "user_message": user_message,
        "agent_response": agent_response,
        "timestamp": "fecha y hora aquí"  # Puedes añadir un timestamp si es necesario
    })
    
    # Guardar el historial actualizado
    with open(conversation_file, "w") as file:
        json.dump(conversation_history, file, indent=4)
    
    return conversation_history

# Ejemplo de uso en la función principal (main.py)
if __name__ == "__main__":
    # Ejemplo de usuario
    user_data = {"name": "Juan Pérez", "phone": "3001234567"}
    
    # Guardar datos del usuario en "users.json"
    save_user_data(user_data)
    
    # Ejemplo de mensaje de usuario y respuesta del agente
    user_message = "¿Cómo automatizo mi negocio?"
    agent_response = "Te puedo recomendar herramientas como Zapier..."
    
    # Guardar el historial de conversación en "conversations/3001234567_history.json"
    save_conversation_history(user_data["phone"], user_message, agent_response)
