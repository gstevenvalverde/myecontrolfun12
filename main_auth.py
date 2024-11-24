from controllers.auth_controller import AuthController


def main():
    controller = AuthController()
    while True:
        print("\nOpciones:")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Verificar si está logueado")
        print("4. Cerrar sesión")
        print("5. Salir")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            email = input("Correo electrónico: ")
            password = input("Contraseña: ")
            controller.signup(email, password)
        elif choice == "2":
            email = input("Correo electrónico: ")
            password = input("Contraseña: ")
            user_id = controller.login(email, password)
            if user_id:
                print(f"Inicio de sesión exitoso. UID: {user_id}")
        elif choice == "3":
            if controller.is_logged_in():
                print("El usuario está logueado.")
            else:
                print("No hay ningún usuario logueado.")
        elif choice == "4":
            controller.logout()
        elif choice == "5":
            print("¡Adiós!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()