import time
import math
import threading
from datetime import datetime
from models.speed_model import store_velocity  # Asegúrate de que esta importación sea correcta

class SpeedTracker:
    def __init__(self, user_id, cursor_tracker):
        """
        Inicializa el rastreador de velocidad del mouse.
        :param user_id: ID del usuario.
        :param cursor_tracker: Instancia de CursorTracker que provee la posición del cursor.
        """
        self.user_id = user_id
        self.cursor_tracker = cursor_tracker  # Instancia de CursorTracker
        self.previous_position = (0, 0)  # Posición previa del cursor
        self.previous_time = time.time()  # Tiempo del último cálculo
        self.movement_speeds = []  # Lista para almacenar velocidades calculadas
        self.running = True  # Estado del rastreador
        self.lock = threading.Lock()  # Lock para manejar accesos concurrentes

    def calculate_distance(self, p1, p2):
        """
        Calcula la distancia entre dos puntos (p1, p2) usando la fórmula euclidiana.
        """
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def track_mouse_movements(self):
        """
        Rastrea el movimiento del mouse consultando la posición desde CursorTracker.
        Calcula la distancia y velocidad cada segundo.
        """
        while self.running:
            current_position = self.cursor_tracker.get_position()  # Obtiene la posición actual del cursor
            current_time = time.time()  # Tiempo actual
            time_diff = current_time - self.previous_time  # Diferencia de tiempo desde el último cálculo

            if time_diff >= 1:  # Calcula la velocidad cada segundo
                distance = self.calculate_distance(self.previous_position, current_position)
                velocity = distance / time_diff  # Velocidad en px/s

                with self.lock:
                    # Se guarda la velocidad, pero se limita a no acumular demasiado
                    self.movement_speeds.append(velocity)

                # Actualiza la posición y el tiempo para el siguiente cálculo
                self.previous_position = current_position
                self.previous_time = current_time

            time.sleep(0.1)  # Pequeño intervalo para evitar sobrecargar la CPU

    def print_average_speed(self):
        """
        Cada minuto imprime y guarda la velocidad promedio de los movimientos del mouse.
        La lista de velocidades se limpia después de cada cálculo.
        """
        while self.running:
            time.sleep(60)  # Espera 60 segundos
            with self.lock:
                if len(self.movement_speeds) > 0:
                    average_speed = sum(self.movement_speeds) / len(self.movement_speeds)
                    print(f"Velocidad promedio del minuto: {average_speed:.2f} px/s")
                    # Guarda la velocidad promedio en Firebase
                    date_today = datetime.now().strftime("%Y-%m-%d")
                    try:
                        store_velocity(self.user_id, date_today, average_speed)
                    except Exception as e:
                        print(f"Error al guardar los datos: {e}")
                    # Limpia la lista de velocidades para el siguiente minuto
                    self.movement_speeds.clear()  # Más eficiente que asignar una nueva lista vacía
                else:
                    print("No hay suficientes datos para calcular la velocidad promedio.")

    def start_tracking(self):
        """
        Inicia el rastreo de velocidad en hilos separados.
        """
        tracking_thread = threading.Thread(target=self.track_mouse_movements)
        tracking_thread.daemon = True  # Permite que el hilo se cierre junto con el programa principal
        tracking_thread.start()

        print_speed_thread = threading.Thread(target=self.print_average_speed)
        print_speed_thread.daemon = True  # Permite que el hilo se cierre junto con el programa principal
        print_speed_thread.start()

    def stop_tracking(self):
        """
        Detiene el rastreo de los movimientos del mouse.
        """
        self.running = False
        # Pequeña espera para permitir que los hilos terminen correctamente
        time.sleep(1)

        # Guarda la velocidad promedio si hay datos pendientes
        with self.lock:
            if len(self.movement_speeds) > 0:
                average_speed = sum(self.movement_speeds) / len(self.movement_speeds)
                date_today = datetime.now().strftime("%Y-%m-%d")
                try:
                    store_velocity(self.user_id, date_today, average_speed)
                except Exception as e:
                    print(f"Error al guardar los datos al finalizar: {e}")
        print("Rastreo de velocidad detenido.")

    def get_current_speed(self):
        """
        Devuelve la velocidad promedio actual, si hay datos disponibles.
        """
        with self.lock:
            if len(self.movement_speeds) > 0:
                current_speed = sum(self.movement_speeds) / len(self.movement_speeds)
                return current_speed
        return 0  # Si no hay datos disponibles, devuelve 0
