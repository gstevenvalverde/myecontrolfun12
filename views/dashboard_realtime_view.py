import time
import threading
from tkinter import StringVar
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from utils.cursor_tracker import CursorTracker
from utils.heatmap_tracker import HeatmapTracker
from utils.movement_tracker import MovementTracker
from utils.speed_tracker import SpeedTracker
from utils.usage_tracker import UsageTracker


class DashboardRealtime(ctk.CTkFrame):
    def __init__(self, parent, user_id):
        super().__init__(parent)

        # Configuración de dos frames
        self.upper_frame = ctk.CTkFrame(self)
        self.upper_frame.pack(side="top", fill="both", expand=True)

        self.lower_frame = ctk.CTkFrame(self)
        self.lower_frame.pack(side="bottom", fill="both", expand=True)

        # Variables de estado para mostrar en el dashboard
        self.movements_var = StringVar(value="Movimientos totales: 0")
        self.speed_var = StringVar(value="Velocidad promedio: 0.00 px/s")
        self.usage_var = StringVar(value="Tiempo de uso: 0 minutos")

        # Widgets para mostrar los datos en la parte superior
        self.movements_label = ctk.CTkLabel(self.upper_frame, textvariable=self.movements_var, font=("Arial", 16))
        self.movements_label.pack(pady=10)

        self.speed_label = ctk.CTkLabel(self.upper_frame, textvariable=self.speed_var, font=("Arial", 16))
        self.speed_label.pack(pady=10)

        self.usage_label = ctk.CTkLabel(self.upper_frame, textvariable=self.usage_var, font=("Arial", 16))
        self.usage_label.pack(pady=10)

        # Configuración de Matplotlib para el heatmap
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.lower_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # User ID
        self.user_id = user_id

        # Inicialización de los trackers
        self.cursor_tracker = CursorTracker()
        self.movement_tracker = MovementTracker(user_id=user_id, cursor_tracker=self.cursor_tracker)
        self.speed_tracker = SpeedTracker(user_id=user_id, cursor_tracker=self.cursor_tracker)
        self.usage_tracker = UsageTracker(user_id=user_id)
        self.heatmap_tracker = HeatmapTracker(user_id=user_id, cursor_tracker=self.cursor_tracker)

        # Bandera para detener trackers
        self.running = True

        # Iniciar actualización periódica del dashboard
        self.start_trackers()
        self.update_dashboard()

    def start_trackers(self):
        """Inicia los hilos de los trackers."""
        self.cursor_tracker.start()
        self.movement_tracker.start_tracking()
        self.speed_tracker.start_tracking()
        self.usage_tracker.start_tracking()
        self.heatmap_tracker.start_tracking()

    def stop_trackers(self):
        """Detiene todos los trackers."""
        self.running = False
        self.cursor_tracker.stop()
        self.movement_tracker.stop_tracking()
        self.speed_tracker.stop_tracking()
        self.usage_tracker.stop_tracking()
        self.heatmap_tracker.stop_tracking()

    def update_dashboard(self):
        """Actualiza los datos y el heatmap en el dashboard."""
        if not self.running:
            return

        try:
            # Actualizar datos en la parte superior
            current_movements = self.movement_tracker.get_current_movement()
            self.movements_var.set(f"Movimientos totales: {current_movements}")

            current_speed = self.speed_tracker.get_current_speed()
            self.speed_var.set(f"Velocidad promedio: {current_speed:.2f} px/s")

            current_usage = self.usage_tracker.get_current_usage()
            self.usage_var.set(f"Tiempo de uso: {current_usage}")

            # Actualizar heatmap en la parte inferior
            current_heatmap = self.heatmap_tracker.get_current_heatmap()
            self.ax.clear()
            self.ax.imshow(current_heatmap, cmap="hot", interpolation="nearest")
            self.ax.set_title("Mapa de calor")
            self.canvas.draw()

            # Repetir cada 1 segundo
            self.after(5000, self.update_dashboard)

        except Exception as e:
            print(f"Error al actualizar el dashboard: {e}")
            self.stop_trackers()


# Ejemplo de cómo usar DashboardRealtime dentro de un Frame padre
if __name__ == "__main__":
    class MainApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("App Principal")
            self.geometry("1000x800")

            # Frame padre
            parent_frame = ctk.CTkFrame(self)
            parent_frame.pack(fill="both", expand=True)

            # Colocar DashboardRealtime dentro del frame padre
            dashboard = DashboardRealtime(parent_frame, user_id="1zeMM4Vsl9OuIq8DwZUM7GaTge82")
            dashboard.pack(fill="both", expand=True)

            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.dashboard = dashboard

        def on_closing(self):
            self.dashboard.stop_trackers()
            self.destroy()


    app = MainApp()
    app.mainloop()
