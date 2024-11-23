import customtkinter as ctk

from controllers.dashboard_controller import DashboardController
from utils.utils import centrar_ventana

# Selecting GUI theme - dark,
# light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme-blue, green, dark-blue
ctk.set_default_color_theme("blue")

class Dashboard:

    def switch_frame(self,page):
        for frame in self.page_frame.winfo_children():
            frame.destroy()
        page()

    def handle_to_econtrol(self):
        voice_frame = ctk.CTkFrame(master=self.page_frame)
        voice_frame.pack(side="top", fill="both", expand=True)
        information_label = ctk.CTkLabel(master=voice_frame, text="Iniciar seguimiento")
        information_label.pack(side="top")
        voice_button = ctk.CTkButton(master=voice_frame, width=200, height=40, corner_radius=8, text="Iniciar")
        voice_button.pack()

    def handle_to_configuration_frame(self):
        configuration_frame = ctk.CTkFrame(master=self.page_frame)
        configuration_frame.pack(side="top", fill="both", expand=True)
        information_label = ctk.CTkLabel(master=configuration_frame, text="Configuración")
        information_label.pack(side="top")

    def __init__(self, root):
        self.dashboard = root
        self.dashboard.resizable(width=0, height=0)
        centrar_ventana(self.dashboard, 700, 500)

        self.buttons_frame = ctk.CTkFrame(master=self.dashboard, height=60)
        self.buttons_frame.pack(side="top", fill="x", padx=8, pady=8)

        self.page_frame = ctk.CTkFrame(master=self.dashboard)
        self.page_frame.pack(side="top", fill="both", padx=8, pady=8, expand=True)
        self.handle_to_dashboard()

        self.calibration_button = ctk.CTkButton(master=self.buttons_frame, width=100, text="Dashboard", corner_radius=4, command=lambda : self.switch_frame(page=self.handle_to_dashboard))
        self.calibration_button.pack(side="left", pady=8)

        self.voice_button = ctk.CTkButton(master=self.buttons_frame, width=100, text="Iniciar seguimiento", corner_radius=4, command=lambda : self.switch_frame(page=self.handle_to_econtrol))
        self.voice_button.pack(side="left", pady=8)

        self.configuration_button = ctk.CTkButton(master=self.buttons_frame, width=100, text="Configuraciones", corner_radius=4, command=lambda : self.switch_frame(page=self.handle_to_configuration_frame))
        self.configuration_button.pack(side="left", pady=8)

    def handle_to_dashboard(self):
        calibration_frame = ctk.CTkFrame(master=self.page_frame)
        calibration_frame.pack(side="top", fill="both", expand=True)
        information_label = ctk.CTkLabel(master=calibration_frame, text="Dashboard")
        information_label.pack(side="top")

# Inicialización de la aplicación
if __name__ == "__main__":
    root = ctk.CTk()  # Ventana principal con CustomTkinter
    controller = DashboardController()
    app = Dashboard(root=root)
    root.mainloop()