from datetime import datetime
from utils.usage_tracker import UsageTracker
from models.usage_model import get_user_usage_data, update_user_usage_data

def main():

    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario
    tracker = UsageTracker(user_id)
    today = datetime.now().strftime("%Y-%m-%d")  # Fecha actual

    try:
        print("Iniciando rastreador de tiempo...")
        tracker.start_tracking()

        while True:
            print("\nOpciones:")
            print("1. Agregar tiempo manualmente")
            print("2. Recuperar tiempo acumulado")
            print("3. Salir")
            choice = input("Selecciona una opción: ")

            if choice == "1":
                # Agregar tiempo manualmente
                minutes = int(input("Minutos utilizados: "))
                tracker.add_time(minutes)

                # Actualizar el tiempo acumulado para hoy y en Firestore
                update_user_usage_data(user_id, today, minutes)

                print(f"Tiempo actualizado para hoy: {minutes} minutos")

            elif choice == "2":
                # Recuperar tiempo acumulado desde Firestore
                result = get_user_usage_data(user_id)  # Llamar a la función que recupera los datos del usuario
                print(f"Minutos {tracker.get_current_usage()}")
                if result["success"]:
                    usage_data = result["usage_data"]  # Acceder a los datos de uso
                    today_minutes = usage_data.get(today, 0)  # Obtener el tiempo acumulado para el día actual
                    print(f"Tiempo acumulado para hoy ({today}): {today_minutes} minutos")
                else:
                    print(f"Error al recuperar datos: {result['error']}")

            elif choice == "3":
                print("Cerrando aplicación...")
                break
            else:
                print("Opción no válida.")
    finally:
        # Detener el rastreador al salir
        tracker.stop_tracking()

if __name__ == "__main__":
    main()
