from models import auth_model

class AuthController:
    def __init__(self):
        # Instanciar el modelo de autenticación
        self.auth_model = auth_model

    def signup(self, email, password):
        """
        Registra un nuevo usuario.
        """
        result = self.auth_model.signup_user(email, password)
        if result["success"]:
            print(f"Usuario creado exitosamente. UID: {result['user_id']}")
            return result["user_id"]  # Retorna el UID para uso posterior
        else:
            print(f"Error al crear usuario: {result['error']}")
            return None

    def login(self, email, password):
        """
        Inicia sesión con un usuario existente.
        """
        result = self.auth_model.login_user(email, password)
        if result["success"]:
            print("Inicio de sesión exitoso.")
            return result["user_id"]  # Retorna el UID para utilizarlo en la aplicación
        else:
            print(f"Error al iniciar sesión: {result['error']}")
            return None

    def is_logged_in(self):
        """
        Verifica si el usuario ya está logueado.
        """
        return self.auth_model.is_logged_in()

    def logout(self):
        """
        Cierra la sesión del usuario.
        """
        result = self.auth_model.logout_user()
        if result["success"]:
            print("Sesión cerrada correctamente.")
        else:
            print(f"Error al cerrar sesión: {result['error']}")

    def show_welcome_message(self, user_id):
        """
        Muestra un mensaje de bienvenida después de un inicio de sesión exitoso.
        """
        print(f"Bienvenido, {user_id}! Sesión iniciada con éxito.")

    def show_error_message(self, error):
        """
        Muestra un mensaje de error si el login o registro falla.
        """
        print(f"Error: {error}")
