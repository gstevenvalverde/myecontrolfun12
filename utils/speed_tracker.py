import time
import math
from pynput.mouse import Listener
import threading
from datetime import datetime
from models.speed_model import store_velocity  # Asegúrate de que esta importación esté correcta

class SpeedTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.previous_position = (0, 0)
        self.previous_time = time.time()
        self.movement_speeds = []
        self.running = True

    def calculate_distance(self, p1, p2):
        """
        Calcula la distancia entre dos puntos (p1, p2) usando la fórmula euclidiana.
        """
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def track_mouse_movements(self):
        """
        Escucha los movimientos del mouse y calcula la distancia y velocidad del movimiento.
        Esta función corre en un hilo separado.
        """
        def on_move(x, y):
            # Calcula el tiempo transcurrido y la distancia del movimiento del mouse
            current_time = time.time()
            time_diff = current_time - self.previous_time

            if time_diff >= 1:
                distance = self.calculate_distance(self.previous_position, (x, y))
                velocity = distance / time_diff  # Velocidad en px/s
                self.movement_speeds.append(velocity)

                # Actualiza la posición y el tiempo para la siguiente iteración
                self.previous_position = (x, y)
                self.previous_time = current_time

        # Inicia el listener para capturar los eventos del mouse
        with Listener(on_move=on_move) as listener:
            listener.join()

    def print_average_speed(self):
        """
        Cada minuto imprime la velocidad promedio de los movimientos del mouse.
        """
        while self.running:
            time.sleep(60)  # Espera 60 segundos antes de calcular y mostrar la velocidad promedio
            if len(self.movement_speeds) > 0:
                average_speed = sum(self.movement_speeds) / len(self.movement_speeds)
                print(f"Velocidad promedio del minuto: {average_speed:.2f} px/s")
                # Limpiar la lista de velocidades para el siguiente minuto
                self.movement_speeds = []
                # Guardar la velocidad promedio en Firebase
                date_today = datetime.now().strftime("%Y-%m-%d")
                store_velocity(self.user_id, date_today, average_speed)
            else:
                print("No hay suficientes datos para calcular la velocidad promedio aún.")

    def start_tracking(self):
        """
        Inicia el rastreo del movimiento del mouse en un hilo separado.
        """
        tracking_thread = threading.Thread(target=self.track_mouse_movements)
        tracking_thread.daemon = True  # Esto permitirá que el hilo se cierre cuando se cierre el programa principal
        tracking_thread.start()

        # Inicia un hilo para imprimir la velocidad promedio cada minuto
        print_speed_thread = threading.Thread(target=self.print_average_speed)
        print_speed_thread.daemon = True  # Hilo se detendrá cuando el programa principal termine
        print_speed_thread.start()

    def stop_tracking(self):
        """
        Detiene el rastreo de los movimientos del mouse.
        Esta función es útil si deseas detener el hilo manualmente en el futuro.
        """
        self.running = False
        # Aquí también se guarda la velocidad promedio al detener el rastreo
        if len(self.movement_speeds) > 0:
            average_speed = sum(self.movement_speeds) / len(self.movement_speeds)
            date_today = datetime.now().strftime("%Y-%m-%d")
            store_velocity(self.user_id, date_today, average_speed)
        print("Rastreo detenido.")
