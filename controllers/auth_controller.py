# Simulación de un controlador básico para probar la clase Login
from models import auth_model

class AuthController:
    def __init__(self):
        # Aquí podrías inicializar variables si fuera necesario
        pass

    def signup(self, email, password):
        print("Registrando...")
        result = auth_model.signup_user(email, password)
        if result["success"]:
            print(f"Usuario creado exitosamente. UID: {result['user_id']}")
        else:
            print(f"Error al crear usuario: {result['error']}")

    def login(self, email, password):
        result = auth_model.login_user(email, password)
        if result["success"]:
            print("Inicio de sesión exitoso.")
        else:
            print(f"Error al iniciar sesión: {result['message']}")



    def handle_login(self, username, password, remember_me):
        """
        Lógica del login (se conecta al modelo o a Firebase).
        """
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Remember Me: {remember_me}")
        # Aquí implementarías la lógica para verificar con Firebase