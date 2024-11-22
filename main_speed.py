# main.py
from utils.speed_tracker import SpeedTracker
from datetime import datetime

def main():
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario
    speed_tracker = SpeedTracker(user_id)

    try:
        print("Iniciando rastreo de movimientos del mouse...")
        speed_tracker.start_tracking()

        while True:
            print("\nOpciones:")
            print("1. Ver velocidad promedio")
            print("2. Salir")
            choice = input("Selecciona una opción: ")

            if choice == "1":
                # Calcula y muestra la velocidad promedio actual
                average_speed = sum(speed_tracker.movement_speeds) / len(speed_tracker.movement_speeds) if speed_tracker.movement_speeds else 0
                print(f"Velocidad promedio del minuto: {average_speed:.2f} px/s")
            elif choice == "2":
                print("Cerrando aplicación...")
                break
            else:
                print("Opción no válida.")
    finally:
        speed_tracker.stop_tracking()

if __name__ == "__main__":
    main()
