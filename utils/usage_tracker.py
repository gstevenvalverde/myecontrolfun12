import threading
import time
from models.usage_model import update_user_usage_data
from datetime import datetime

class UsageTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.total_minutes = 0
        self.running = True
        self.today = datetime.now().strftime("%Y-%m-%d")  # Fecha actual
        self.lock = threading.Lock()  # Lock para sincronizar el acceso a total_minutes
        self.track_thread = threading.Thread(target=self.track_time)  # Hilo para cronómetro
        self.track_thread.daemon = True
        self.track_thread.start()

    def track_time(self):
        """Inicia un cronómetro que suma minutos cada 60 segundos."""
        while self.running:
            time.sleep(60)  # Espera 60 segundos (1 minuto)
            self.add_time(1)  # Suma 1 minuto

    def add_time(self, minutes):
        """Agrega tiempo al total acumulado de manera segura."""
        with self.lock:
            self.total_minutes += minutes

    def get_current_usage(self):
        """Devuelve el tiempo total acumulado en minutos."""
        with self.lock:
            return self.total_minutes

    def save_periodically(self):
        """Guarda los datos de uso en Firebase cada 30 minutos."""
        while self.running:
            time.sleep(1800)  # 30 minutos
            with self.lock:
                if self.total_minutes > 0:
                    try:
                        update_user_usage_data(self.user_id, self.today, self.total_minutes)
                        print(f"Guardado automáticamente: {self.total_minutes} minutos")
                        self.total_minutes = 0  # Resetea el contador después de guardar
                    except Exception as e:
                        print(f"Error al guardar los datos: {e}")

    def start_tracking(self):
        """Inicia el guardado periódico en un thread."""
        save_thread = threading.Thread(target=self.save_periodically)
        save_thread.daemon = True
        save_thread.start()

    def stop_tracking(self):
        """Detiene el tracker y guarda cualquier dato pendiente."""
        self.running = False
        with self.lock:
            if self.total_minutes > 0:
                try:
                    update_user_usage_data(self.user_id, self.today, self.total_minutes)
                    print(f"Guardado final: {self.total_minutes} minutos")
                except Exception as e:
                    print(f"Error al guardar los datos al finalizar: {e}")
