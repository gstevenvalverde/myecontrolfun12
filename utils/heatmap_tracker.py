import time
import threading
from pynput.mouse import Listener
from datetime import datetime
from models.heatmap_model import store_heatmap

class HeatmapTracker:
    def __init__(self, user_id, screen_width=1920, screen_height=1080, grid_size_x=10, grid_size_y=10):
        self.user_id = user_id
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size_x = grid_size_x  # Cambio de grid_size a grid_size_x y grid_size_y
        self.grid_size_y = grid_size_y
        self.heatmap = [[0 for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)]
        self.running = True

    def calculate_bin(self, x, y):
        """
        Calcula el bin de la cuadrícula donde se encuentra la coordenada (x, y).
        """
        bin_x = min(int(x / self.screen_width * self.grid_size_x), self.grid_size_x - 1)
        bin_y = min(int(y / self.screen_height * self.grid_size_y), self.grid_size_y - 1)
        return bin_x, bin_y

    def track_mouse(self):
        """
        Escucha los movimientos del mouse y actualiza el heatmap.
        """
        def on_move(x, y):
            bin_x, bin_y = self.calculate_bin(x, y)
            self.heatmap[bin_y][bin_x] += 1

        with Listener(on_move=on_move) as listener:
            listener.join()

    def start_tracking(self):
        """
        Inicia el rastreo del mouse y las tareas periódicas en hilos separados.
        """
        # Hilo para rastrear el mouse
        tracking_thread = threading.Thread(target=self.track_mouse)
        tracking_thread.daemon = True
        tracking_thread.start()

        # Hilo para guardar heatmap cada 5 minutos
        save_thread = threading.Thread(target=self.save_heatmap_periodically)
        save_thread.daemon = True
        save_thread.start()

        # Hilo para mostrar heatmap cada minuto
        show_thread = threading.Thread(target=self.show_heatmap_periodically)
        show_thread.daemon = True
        show_thread.start()

    def save_heatmap_periodically(self):
        """
        Guarda el heatmap en Firebase cada 5 minutos.
        """
        while self.running:
            time.sleep(300)  # 5 minutos
            self.save_heatmap()

    def show_heatmap_periodically(self):
        """
        Muestra el heatmap en la consola cada minuto.
        """
        while self.running:
            time.sleep(60)  # 1 minuto
            self.display_heatmap()

    def display_heatmap(self):
        """
        Imprime el heatmap en la consola.
        """
        print(f"Heatmap actual (tamaño {self.grid_size_x}x{self.grid_size_y}):")
        for row in self.heatmap:
            print(" ".join(f"{val:2}" for val in row))
        print("\n")

    def save_heatmap(self):
        """
        Guarda el heatmap actual en Firebase.
        """
        date = datetime.now().strftime("%Y-%m-%d")
        store_heatmap(self.user_id, date, self.heatmap)
        self.reset_heatmap()

    def reset_heatmap(self):
        """
        Reinicia la matriz del heatmap.
        """
        self.heatmap = [[0 for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)]

    def stop_tracking(self):
        """
        Detiene el rastreo y guarda los datos finales.
        """
        self.running = False
        self.save_heatmap()