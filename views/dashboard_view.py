import tkinter as tk
from customtkinter import CTkFrame, CTkLabel, set_appearance_mode
import pandas as pd
import matplotlib.pyplot as plt
from models.usage_model import get_user_usage_data
from models.speed_model import get_user_velocity_data
from models.mouse_model import get_user_movement_data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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

        # Contenedor para los gráficos (2x2)
        self.grid_container = CTkFrame(self)
        self.grid_container.pack(fill="both", expand=True, padx=10, pady=10)

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

        # Datos de ejemplo
        self.data = {
            "usage": usage_data or {f"2024-11-{i+1}": i * 10 for i in range(10)},
            "velocity": velocity_data or {f"2024-11-{i+1}": i * 5 for i in range(10)},
            "movement": movement_data or {f"2024-11-{i+1}": i * 3 for i in range(10)},
            "heatmap": np.random.rand(5, 5),  # Ejemplo de datos para el heatmap
        }

    def render_all_charts(self):
        """
        Renderiza los gráficos en una grilla 2x2.
        """
        # Gráficos en la grilla (bar, plot, bar, heatmap)
        self.render_chart_bar(self.grid_container, "Tiempo de Uso", "Minutos", self.data["usage"], 0, 0)
        self.render_chart_plot(self.grid_container, "Velocidad Promedio", "Pixeles/seg", self.data["velocity"], 0, 1)
        self.render_chart_bar(self.grid_container, "Número de Movimientos", "Movimientos", self.data["movement"], 1, 0)
        self.render_chart_heatmap(self.grid_container, "Mapa de Calor", self.data["heatmap"], 1, 1)

    def render_chart_bar(self, parent, title, ylabel, data, row, col):
        """
        Renderiza un gráfico de barras dentro de la grilla.
        """
        chart_container = self.create_chart_container(parent, row, col)

        if not data:
            CTkLabel(chart_container, text="No hay datos para mostrar").pack()
            return

        df = pd.DataFrame(list(data.items()), columns=["Día", ylabel])
        df["Día"] = pd.to_datetime(df["Día"])
        df = df.sort_values(by="Día")

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(2.5, 1.5), dpi=96, facecolor="#2B2B2B")

        ax.bar(df["Día"].dt.strftime("%m-%d"), df[ylabel], color="#1E88E5", label=ylabel)

        self.style_chart(ax, title, ylabel)
        self.display_chart(fig, chart_container)

    def render_chart_plot(self, parent, title, ylabel, data, row, col):
        """
        Renderiza un gráfico de líneas dentro de la grilla.
        """
        chart_container = self.create_chart_container(parent, row, col)

        if not data:
            CTkLabel(chart_container, text="No hay datos para mostrar").pack()
            return

        df = pd.DataFrame(list(data.items()), columns=["Día", ylabel])
        df["Día"] = pd.to_datetime(df["Día"])
        df = df.sort_values(by="Día")

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(2.5, 1.5), dpi=96, facecolor="#2B2B2B")

        ax.plot(df["Día"].dt.strftime("%m-%d"), df[ylabel], color="#1E88E5", marker="o", linestyle="-")

        self.style_chart(ax, title, ylabel)
        self.display_chart(fig, chart_container)

    def render_chart_heatmap(self, parent, title, data, row, col):
        """
        Renderiza un heatmap dentro de la grilla.
        """
        chart_container = self.create_chart_container(parent, row, col)

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(2.5, 1.5), dpi=96, facecolor="#2B2B2B")

        cax = ax.matshow(data, cmap="viridis")

        fig.colorbar(cax)
        ax.set_title(title, color="white", fontsize=5, pad=10)
        ax.tick_params(axis="both", which="both", length=0, labelsize=4, colors="white")

        self.display_chart(fig, chart_container)

    def create_chart_container(self, parent, row, col):
        """
        Crea un contenedor para los gráficos dentro de la grilla.
        """
        chart_container = CTkFrame(parent, width=400, height=300)
        chart_container.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        chart_container.grid_propagate(False)
        return chart_container

    def style_chart(self, ax, title, ylabel):
        """
        Aplica estilos al gráfico.
        """
        ax.set_title(title, color="white", fontsize=5)
        ax.set_ylabel(ylabel, color="white", fontsize=3)
        ax.tick_params(axis="x", colors="white", labelsize=3)
        ax.tick_params(axis="y", colors="white", labelsize=3)
        ax.spines["top"].set_color("#444")
        ax.spines["bottom"].set_color("#444")
        ax.spines["left"].set_color("#444")
        ax.spines["right"].set_color("#444")

    def display_chart(self, fig, container):
        """
        Muestra el gráfico en el contenedor de Tkinter.
        """
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)