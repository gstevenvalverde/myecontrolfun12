import pyautogui
import time
import threading

class CursorTracker:
    def __init__(self):
        self.running = True
        self.current_position = (0, 0)
        self.lock = threading.Lock()  # Para manejar acceso concurrente seguro a la posición

    def track_position(self):
        """Hilo que rastrea la posición del cursor en tiempo real."""
        while self.running:
            x, y = pyautogui.position()
            with self.lock:
                self.current_position = (x, y)
            time.sleep(0.1)  # Ajusta este valor para la frecuencia de actualización

    def get_position(self):
        """Obtiene la posición actual del cursor."""
        with self.lock:
            return self.current_position

    def start(self):
        """Inicia el rastreador en un hilo separado."""
        thread = threading.Thread(target=self.track_position)
        thread.daemon = True
        thread.start()

    def stop(self):
        """Detiene el rastreo."""
        self.running = False
        print("Rastreador de posición detenido")
