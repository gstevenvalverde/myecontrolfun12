import re
import requests

FIREBASE_API_KEY = "AIzaSyDFsCwAFYJvnMVjCZg8zF2ZnZiFPdBO6wQ"

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
        return {"success": True, "id_token": data["idToken"]}
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
        return {"success": True, "user_id": data["localId"]}
    else:
        return {"success": False, "error": response.json()["error"]["message"]}
