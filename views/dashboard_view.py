import customtkinter as ctk

# light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme-blue, green, dark-blue
ctk.set_default_color_theme("blue")

class Dashboard:
    def __init__(self, root, controller):
        """
        Clase para gestionar la vista del dashboard.
        :param root: Ventana principal de Tkinter.
        :param controller: Controlador que manejará la lógica del dashboard.
        """
        self.root = root
        self.controller = controller
        self.root.title("Dashboard")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        # Llamar a los métodos para construir la interfaz
