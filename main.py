import customtkinter as ctk
from controllers.auth_controller import AuthController
from views.login_view import Login
from utils.utils import centrar_ventana


def main():
    """
    Punto de entrada principal de la aplicación.
    """
    # Inicializar la ventana principal
    root = ctk.CTk()
    centrar_ventana(root, 600, 400)

    # Inicializar el controlador de autenticación
    controller = AuthController()

    # Crear la vista principal (login)
    app = Login(root, controller)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()
