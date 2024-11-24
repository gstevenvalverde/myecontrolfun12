import time
import threading
from datetime import datetime
from models.heatmap_model import store_heatmap

class HeatmapTracker:
    def __init__(self, user_id, cursor_tracker, screen_width=1920, screen_height=1080, total_cells=40):
        """
        Inicializa el rastreador de heatmap.
        :param user_id: ID del usuario.
        :param cursor_tracker: Instancia de CursorTracker que provee la posición del cursor.
        :param screen_width: Ancho de la pantalla.
        :param screen_height: Alto de la pantalla.
        :param total_cells: Número total de celdas en el heatmap (aproximado).
        """
        self.user_id = user_id
        self.cursor_tracker = cursor_tracker
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Calcular el tamaño del grid basado en la relación de aspecto
        aspect_ratio = screen_width / screen_height
        self.grid_size_x = int((total_cells * aspect_ratio) ** 0.5)  # Columnas
        self.grid_size_y = int(total_cells / self.grid_size_x)       # Filas

        # Inicializar la matriz del heatmap
        self.heatmap = [[0 for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)]
        self.running = True
        self.lock = threading.Lock()

    def calculate_bin(self, x, y):
        """
        Calcula el bin de la cuadrícula donde se encuentra la coordenada (x, y).
        """
        bin_x = min(int(x / self.screen_width * self.grid_size_x), self.grid_size_x - 1)
        bin_y = min(int(y / self.screen_height * self.grid_size_y), self.grid_size_y - 1)
        return bin_x, bin_y

    def track_mouse(self):
        """
        Rastrea la posición del mouse obtenida desde el CursorTracker y actualiza el heatmap.
        """
        while self.running:
            current_position = self.cursor_tracker.get_position()  # Obtiene la posición actual del cursor
            x, y = current_position
            bin_x, bin_y = self.calculate_bin(x, y)

            # Adquiere el lock para acceder de manera segura al heatmap
            with self.lock:
                self.heatmap[bin_y][bin_x] += 1

            time.sleep(0.1)  # Intervalo pequeño para evitar sobrecargar la CPU

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
        # Adquiere el lock antes de acceder a la variable heatmap
        with self.lock:
            for row in self.heatmap:
                print(" ".join(f"{val:2}" for val in row))
        print("\n")

    def save_heatmap(self):
        """
        Guarda el heatmap actual en Firebase.
        """
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            # Adquiere el lock antes de guardar el heatmap
            with self.lock:
                store_heatmap(self.user_id, date, self.heatmap)
            self.reset_heatmap()
        except Exception as e:
            print(f"Error al guardar el heatmap: {e}")

    def reset_heatmap(self):
        """
        Reinicia la matriz del heatmap.
        """
        with self.lock:
            self.heatmap = [[0 for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)]

    def stop_tracking(self):
        """
        Detiene el rastreo y guarda los datos finales.
        """
        self.running = False
        self.save_heatmap()

    def get_current_heatmap(self):
        """
        Devuelve el estado actual del heatmap.
        """
        with self.lock:
            return self.heatmap