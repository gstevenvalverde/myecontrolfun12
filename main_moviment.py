from utils.mouse_tracker import MouseTracker
from datetime import datetime

def main():
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario
    mouse_tracker = MouseTracker(user_id)

    try:
        print("Iniciando rastreo de movimientos del mouse...")
        mouse_tracker.start_tracking()

        while True:
            print("\nOpciones:")
            print("1. Ver total de movimientos registrados")
            print("2. Salir")
            choice = input("Selecciona una opción: ")

            if choice == "1":
                print(f"Movimientos totales hasta ahora: {mouse_tracker.total_movements}")
            elif choice == "2":
                print("Cerrando aplicación...")
                break
            else:
                print("Opción no válida.")
    finally:
        mouse_tracker.stop_tracking()

if __name__ == "__main__":
    main()
