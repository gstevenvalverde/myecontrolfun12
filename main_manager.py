import threading
import time
from utils.usage_tracker import UsageTracker
from utils.speed_tracker import SpeedTracker
from utils.mouse_tracker import MouseTracker
from utils.heatmap_tracker import HeatmapTracker

def main():
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario
    # Inicializar los trackers
    usage_tracker = UsageTracker(user_id)
    speed_tracker = SpeedTracker(user_id)
    mouse_tracker = MouseTracker(user_id)
    heatmap_tracker = HeatmapTracker(user_id)

    # Iniciar todos los trackers en threads
    usage_tracker.start_tracking()
    speed_tracker.start_tracking()
    # mouse_tracker.start_tracking()
    heatmap_tracker.start_tracking()

    print("Todos los trackers se han iniciado. Usa el menú para interactuar.")

    # Menú de consola
    while True:
        print("\n---- MENÚ ----")
        print("1. Consultar tiempo de uso actual")
        print("2. Consultar velocidad promedio actual")
        print("3. Consultar movimientos del mouse actuales")
        print("4. Consultar mapa de calor actual")
        print("5. Salir y guardar datos")
        option = input("Selecciona una opción: ")

        if option == "1":
            print(f"Tiempo de uso actual: {usage_tracker.get_current_usage()} minutos")
            # print("no iniciado")
        elif option == "2":
            print(f"Velocidad promedio actual: {speed_tracker.get_current_speed()} píxeles/seg")
        elif option == "3":
            #print(f"Movimientos del mouse actuales: {mouse_tracker.get_current_movement()}")
            print("no iniciado")
        elif option == "4":
            print(f"Datos del mapa de calor: {heatmap_tracker.get_current_heatmap()}")
        elif option == "5":
            print("Guardando datos en Firebase y cerrando el programa...")
            usage_tracker.stop_tracking()
            speed_tracker.stop_tracking()
            #mouse_tracker.stop_tracking()
            heatmap_tracker.stop_tracking()
            print("¡Datos guardados exitosamente!")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
