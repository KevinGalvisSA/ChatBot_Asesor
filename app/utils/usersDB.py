import json
import os

def save_user_data(user_data):
    """Guarda la información del usuario en un archivo JSON"""
    users_file = "users.json"

    # Verificar si el archivo ya existe
    if os.path.exists(users_file):
        with open(users_file, "r") as file:
            users_db = json.load(file)
    else:
        # Si el archivo no existe, lo creamos
        users_db = {}

    # Usar el teléfono como clave única
    phone = user_data["phone"]
    
    # Agregar el usuario al "database"
    users_db[phone] = {
        "name": user_data["name"],
        "phone": user_data["phone"]
    }

    # Guardar los datos de los usuarios en el archivo JSON
    with open(users_file, "w") as file:
        json.dump(users_db, file, indent=4)

    return users_db
