import tkinter as tk
from customtkinter import CTkFrame, CTkLabel, set_appearance_mode
import pandas as pd
import matplotlib.pyplot as plt
from models.usage_model import get_user_usage_data
from models.speed_model import get_user_velocity_data
from models.mouse_model import get_user_movement_data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Establecer el tema oscuro
set_appearance_mode("dark")

class DashboardView(CTkFrame):
    def __init__(self, parent, user_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_id = user_id
        self.data = {}

        # Crear título
        self.title_label = CTkLabel(self, text="Dashboard", font=("Arial", 18))
        self.title_label.pack(pady=10)

        # Crear un Canvas con scrollbar
        self.scrollable_frame = CTkFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.scrollable_frame, bg="#2B2B2B", highlightthickness=0)  # Fondo oscuro
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_content = CTkFrame(self.canvas)

        self.scrollable_content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Cargar los datos y mostrar gráficos
        self.load_data()
        self.render_all_charts()

    def load_data(self):
        """
        Carga todos los datos necesarios de los modelos.
        """
        usage_data = get_user_usage_data(self.user_id).get("usage_data", {})
        velocity_data = get_user_velocity_data(self.user_id).get("velocity_data", {})
        movement_data = get_user_movement_data(self.user_id).get("movement_data", {})

        self.data = {
            "usage": usage_data,
            "velocity": velocity_data,
            "movement": movement_data,
        }
        print(self.data)

    def render_all_charts(self):
        """
        Renderiza los tres gráficos uno debajo del otro.
        """
        # Renderizar gráfico de tiempo de uso
        self.render_chart(
            self.scrollable_content, "Tiempo de Uso", "Minutos", self.data["usage"]
        )
        # Renderizar gráfico de velocidad promedio
        self.render_chart(
            self.scrollable_content,
            "Velocidad Promedio",
            "Pixeles/seg",
            self.data["velocity"],
        )
        # Renderizar gráfico de movimientos
        self.render_chart(
            self.scrollable_content,
            "Número de Movimientos",
            "Movimientos",
            self.data["movement"],
        )

    def render_chart(self, parent, title, ylabel, data):
        """
        Renderiza un gráfico en un contenedor dado.
        """
        # Frame contenedor para cada gráfico
        chart_container = CTkFrame(parent)
        chart_container.pack(fill="both", expand=True, pady=10)

        # Agregar título
        CTkLabel(chart_container, text=title, font=("Arial", 16)).pack(pady=5)

        # Verificar si hay datos
        if not data:
            CTkLabel(chart_container, text="No hay datos para mostrar").pack()
            return

        # Crear el DataFrame para graficar
        df = pd.DataFrame(list(data.items()), columns=["Día", ylabel])
        df["Día"] = pd.to_datetime(df["Día"])
        df = df.sort_values(by="Día")

        # Graficar con Matplotlib en tema oscuro
        plt.style.use("dark_background")  # Tema oscuro para Matplotlib
        fig, ax = plt.subplots(figsize=(2, 1), dpi=100, facecolor="#2B2B2B")  # 200x100 px

        ax.bar(df["Día"].dt.strftime("%Y-%m-%d"), df[ylabel], color="#1E88E5")
        ax.set_title(title, color="white", fontsize=10)
        ax.set_xlabel("Día", color="white", fontsize=8)
        ax.set_ylabel(ylabel, color="white", fontsize=8)
        ax.tick_params(axis="x", colors="white", rotation=45, labelsize=6)
        ax.tick_params(axis="y", colors="white", labelsize=6)
        ax.spines["top"].set_color("#444")
        ax.spines["bottom"].set_color("#444")
        ax.spines["left"].set_color("#444")
        ax.spines["right"].set_color("#444")

        # Ajustar márgenes
        fig.tight_layout(pad=1.0)

        # Mostrar el gráfico en el Frame
        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)