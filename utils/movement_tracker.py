import threading
import time
from datetime import datetime
from models.mouse_model import store_movement_data

class MovementTracker:
    def __init__(self, user_id, cursor_tracker):
        """
        Inicializa el rastreador de movimientos del mouse.

        Args:
            user_id (str): ID del usuario.
            cursor_tracker (CursorTracker): Instancia de CursorTracker para obtener la posición del cursor.
        """
        self.user_id = user_id
        self.cursor_tracker = cursor_tracker  # CursorTracker para obtener la posición del cursor
        self.total_movements = 0  # Total de movimientos registrados
        self.minute_movements = 0  # Movimientos en el minuto actual
        self.minutes_logged = 0  # Minutos registrados
        self.running = True
        self.today = datetime.now().strftime("%Y-%m-%d")  # Fecha actual
        self.lock = threading.Lock()  # Lock para sincronizar el acceso a los datos
        self.last_position = None  # Última posición registrada del mouse

    def track_movements(self):
        """
        Rastrea movimientos del mouse consultando a CursorTracker.
        """
        while self.running:
            current_position = self.cursor_tracker.get_position()  # Obtiene posición actual del cursor
            with self.lock:
                # Compara la posición actual con la última registrada
                if self.last_position is not None and current_position != self.last_position:
                    self.minute_movements += 1
                    self.total_movements += 1
                self.last_position = current_position
            time.sleep(0.1)  # Frecuencia de rastreo

    def log_minute_data(self):
        """
        Registra los movimientos cada minuto y los imprime en consola.
        """
        while self.running:
            start_time = time.time()
            with self.lock:
                self.minute_movements = 0  # Reinicia el contador de movimientos del minuto
            while time.time() - start_time < 60:  # Espera un minuto
                time.sleep(1)
            with self.lock:
                self.minutes_logged += 1
                print(f"Movimientos este minuto: {self.minute_movements}")

    def start_tracking(self):
        """
        Inicia el rastreo y el registro en hilos separados.
        """
        # Hilo para rastrear movimientos
        tracking_thread = threading.Thread(target=self.track_movements)
        tracking_thread.daemon = True
        tracking_thread.start()

        # Hilo para registrar datos cada minuto
        logging_thread = threading.Thread(target=self.log_minute_data)
        logging_thread.daemon = True
        logging_thread.start()

    def stop_tracking(self):
        """
        Detiene el rastreo y guarda los datos en Firebase.
        """
        self.running = False
        with self.lock:
            if self.minutes_logged > 0:
                average_movements = self.total_movements / self.minutes_logged
                store_movement_data(
                    user_id=self.user_id,
                    date=self.today,
                    new_movements=average_movements
                )
                print(f"Promedio diario guardado: {average_movements}")

    def get_current_movement(self):
        """
        Devuelve el número total de movimientos registrados hasta el momento.
        """
        with self.lock:
            return self.total_movements
