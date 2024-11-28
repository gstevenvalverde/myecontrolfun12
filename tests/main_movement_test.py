from utils.cursor_tracker import CursorTracker
from utils.heatmap_tracker import HeatmapTracker
from utils.movement_tracker import MovementTracker
from utils.speed_tracker import SpeedTracker
import time

from utils.usage_tracker import UsageTracker


def main():
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario
    # Crear e iniciar CursorTracker
    cursor_tracker = CursorTracker()
    cursor_tracker.start()

    # Crear e iniciar MovementTracker
    movement_tracker = MovementTracker(user_id=user_id, cursor_tracker=cursor_tracker)
    movement_tracker.start_tracking()

    # Crear e iniciar SpeedTracker
    speed_tracker = SpeedTracker(user_id=user_id, cursor_tracker=cursor_tracker)
    speed_tracker.start_tracking()

    # Crear e iniciar UsageTracker
    usage_tracker = UsageTracker(user_id=user_id)
    usage_tracker.start_tracking()

    # Crear e iniciar HeatmapTracker
    heatmap_tracker = HeatmapTracker(user_id=user_id, cursor_tracker=cursor_tracker)
    heatmap_tracker.start_tracking()

    try:
        while True:
            # Imprimir los movimientos registrados cada segundo
            time.sleep(1)
            current_movements = movement_tracker.get_current_movement()
            print(f"Movimientos totales detectados: {current_movements}")

            # Imprimir la velocidad promedio actual cada 5 segundos
            if time.time() % 5 < 1:  # Condición para cada 5 segundos
                current_speed = speed_tracker.get_current_speed()
                current_usage = usage_tracker.get_current_usage()
                print(f"Tiempo utilizado: {current_usage}")
                print(f"Velocidad promedio actual: {current_speed:.2f} px/s")
            if time.time() % 20 < 1:
                current_heatmap = heatmap_tracker.get_current_heatmap()
                print(f"Mapa de calor: {current_heatmap}")
    except KeyboardInterrupt:
        print("Deteniendo rastreadores...")
        # Detener los rastreadores al finalizar
        movement_tracker.stop_tracking()
        speed_tracker.stop_tracking()
        usage_tracker.stop_tracking()
        heatmap_tracker.stop_tracking()
        cursor_tracker.stop()

if __name__ == "__main__":
    main()
