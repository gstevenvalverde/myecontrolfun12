import time
from utils.cursor_tracker import CursorTracker

def main():
    tracker = CursorTracker()
    tracker.start()

    try:
        while True:
            # Obtiene y muestra la posición del cursor cada 0.5 segundos
            position = tracker.get_position()
            print(f"Posición del mouse: {position}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nDeteniendo el rastreo...")
        tracker.stop()

if __name__ == "__main__":
    main()
