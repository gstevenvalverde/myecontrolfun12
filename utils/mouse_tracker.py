from pynput import mouse
import threading
import time
from datetime import datetime
from models.mouse_model import store_movement_data

class MouseTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.total_movements = 0  # Total de movimientos registrados
        self.minute_movements = 0  # Movimientos en el minuto actual
        self.minutes_logged = 0  # Minutos registrados
        self.running = True
        self.today = datetime.now().strftime("%Y-%m-%d")  # Fecha actual

    def _on_move(self, x, y):
        """Callback para registrar movimientos."""
        self.minute_movements += 1
        self.total_movements += 1

    def start_tracking(self):
        """Inicia el rastreo de movimientos."""
        def track():
            with mouse.Listener(on_move=self._on_move) as listener:
                while self.running:
                    self.minute_movements = 0
                    start_time = time.time()
                    while time.time() - start_time < 60:  # Un minuto
                        time.sleep(0.1)  # Espera para reducir carga
                    self.minutes_logged += 1
                    print(f"Movimientos este minuto: {self.minute_movements}")
                listener.stop()

        # Ejecuta el rastreo en un hilo
        thread = threading.Thread(target=track)
        thread.daemon = True
        thread.start()

    def stop_tracking(self):
        """Detiene el rastreo y guarda los datos en Firebase."""
        self.running = False
        if self.minutes_logged > 0:
            average_movements = self.total_movements / self.minutes_logged
            store_movement_data(
                user_id=self.user_id,
                date=self.today,
                new_movements=average_movements
            )
            print(f"Promedio diario guardado: {average_movements}")
