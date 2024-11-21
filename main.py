from controllers.auth_controller import AuthController


def main():
    controller = AuthController()
    while True:
        print("\nOpciones:")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        choice = input("Selecciona una opción: ")
        if choice == "1":
            email = input("Correo electrónico: ")
            password = input("Contraseña: ")
            controller.signup(email, password)
        elif choice == "2":
            email = input("Correo electrónico: ")
            password = input("Contraseña: ")
            controller.login(email, password)
        elif choice == "3":
            print("¡Adiós!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
