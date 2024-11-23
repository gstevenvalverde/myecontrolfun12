import tkinter as tk
from customtkinter import CTk

from views.dashboard_view import DashboardView


class HomeView(CTk):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("Dashboard")

        # Inicia el Dashboard
        self.dashboard = DashboardView(self, "1zeMM4Vsl9OuIq8DwZUM7GaTge82")
        self.dashboard.pack(fill="both", expand=True)
        self.dashboard.load_data()

if __name__ == "__main__":
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # Reemplaza con el ID del usuario actual
    app = HomeView(user_id)
    app.mainloop()
