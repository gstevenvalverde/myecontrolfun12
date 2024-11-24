import json
import os
import re
import requests

FIREBASE_API_KEY = "AIzaSyDFsCwAFYJvnMVjCZg8zF2ZnZiFPdBO6wQ"
SESSION_FILE = "user_session.json"  # Archivo para almacenar la sesión localmente

def is_valid_email(email):
    """
    Verifica si un correo electrónico tiene un formato válido.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    """
    Verifica si una contraseña es válida según los requisitos de Firebase.
    """
    return len(password) >= 6

def login_user(email, password):
    """
    Inicia sesión con Firebase si el correo y contraseña son válidos.
    """
    if not is_valid_email(email):
        return {"success": False, "error": "Correo electrónico no válido"}

    if not is_valid_password(password):
        return {"success": False, "error": "La contraseña debe tener al menos 6 caracteres"}

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        _save_session(data["idToken"], data["localId"])
        return {"success": True, "id_token": data["idToken"], "user_id": data["localId"]}
    else:
        return {"success": False, "error": response.json()["error"]["message"]}

def signup_user(email, password):
    """
    Registra un nuevo usuario en Firebase si el correo y contraseña son válidos.
    """
    if not is_valid_email(email):
        return {"success": False, "error": "Correo electrónico no válido"}

    if not is_valid_password(password):
        return {"success": False, "error": "La contraseña debe tener al menos 6 caracteres"}

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        _save_session(data["idToken"], data["localId"])
        return {"success": True, "user_id": data["localId"]}
    else:
        return {"success": False, "error": response.json()["error"]["message"]}

def is_logged_in():
    """
    Verifica si el usuario tiene una sesión activa.
    """
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            session_data = json.load(file)
            if "id_token" in session_data:
                return True
    return False

def logout_user():
    """
    Cierra la sesión eliminando el archivo de sesión.
    """
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    return {"success": True, "message": "Sesión cerrada"}

def _save_session(id_token, user_id):
    """
    Guarda la sesión del usuario en un archivo.
    """
    session_data = {"id_token": id_token, "user_id": user_id}
    with open(SESSION_FILE, "w") as file:
        json.dump(session_data, file)
