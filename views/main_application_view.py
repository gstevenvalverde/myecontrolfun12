import customtkinter as ctk
from customtkinter import CTk, CTkButton, CTkFrame, set_appearance_mode

from controllers.auth_controller import AuthController
from views.dashboard_realtime_view import DashboardRealtime
from views.dashboard_view import DashboardView
from views.eye_control_frame import EyeControlFrame

# Establecer el tema oscuro
set_appearance_mode("dark")


class MainApplication(CTk):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Dashboard Principal")
        self.geometry("1000x800")
        self.controller = AuthController()
        self.user_id = user_id

        # Crear el contenedor principal
        self.main_container = CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        # Dividir la ventana en frame_top y frame_body
        self.frame_top = CTkFrame(self.main_container, height=50)
        self.frame_top.pack(side="top", fill="x", padx=10, pady=5)

        self.frame_body = CTkFrame(self.main_container)
        self.frame_body.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        # Inicializar los dashboards en None
        self.current_dashboard = None
        self.dashboard_realtime = None
        self.dashboard_view = None
        self.dashboard_eye_control = None

        # Crear los botones en frame_top
        self.button_detect_face = CTkButton(
            self.frame_top,
            text="Detectar rostro",
            command=self.show_view_eye_control,
        )
        self.button_detect_face.pack(side="left", padx=5)

        self.button_realtime = CTkButton(
            self.frame_top,
            text="Realtime Dashboard",
            command=self.show_realtime_dashboard,
        )
        self.button_realtime.pack(side="left", padx=5)

        self.button_view = CTkButton(
            self.frame_top,
            text="View Dashboard",
            command=self.show_view_dashboard,
        )
        self.button_view.pack(side="left", padx=5)

        self.button_logout = CTkButton(
            self.frame_top,
            text="Cerrar sesión",
            command=self.logout,
        )
        self.button_logout.pack(side="left", padx=5)

        # Mostrar el primer dashboard por defecto
        self.show_realtime_dashboard()

    def detect_face(self):
        """
        Función que será llamada cuando se haga clic en el botón 'Detectar rostro'.
        Aquí puedes integrar el código de detección de rostro.
        """
        print("Detectando rostro...")  # Aquí va el código para detección de rostro

    def logout(self):
        """
        Función para cerrar sesión.
        Llama a auth_controller.logout() y luego redirige al login.
        """
        self.dashboard_realtime.stop_trackers()
        from views.login_view import Login  # Importación retardada para evitar el ciclo de importación
        print("Cerrando sesión...")  # Mensaje de depuración
        self.controller.logout()  # Llamada al metodo de cierre de sesión en auth_controller
        self.destroy()  # Cierra la aplicación actual

        # Redirigir al login
        root = ctk.CTk()  # Crear una nueva instancia de Tkinter para el login
        login_app = Login(root, self.controller)  # Pasar root y controller al login
        root.mainloop()

    def show_view_eye_control(self):
        """Muestra el DashboardView en el frame_body."""
        self.clear_frame_body()

        if not self.dashboard_eye_control:
            self.dashboard_eye_control = EyeControlFrame(self.frame_body)
        self.dashboard_eye_control.pack(fill="both", expand=True)

        self.current_dashboard = self.dashboard_eye_control

    def show_realtime_dashboard(self):
        """Muestra el DashboardRealtime en el frame_body."""
        self.clear_frame_body()

        if not self.dashboard_realtime:
            self.dashboard_realtime = DashboardRealtime(self.frame_body, self.user_id)
        self.dashboard_realtime.pack(fill="both", expand=True)

        self.current_dashboard = self.dashboard_realtime

    def show_view_dashboard(self):
        """Muestra el DashboardView en el frame_body."""
        self.clear_frame_body()

        if not self.dashboard_view:
            self.dashboard_view = DashboardView(self.frame_body, self.user_id)
        self.dashboard_view.pack(fill="both", expand=True)

        self.current_dashboard = self.dashboard_view

    def clear_frame_body(self):
        """Limpia el contenido actual del frame_body."""
        if self.current_dashboard is not None:
            self.current_dashboard.pack_forget()


def main():
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario

    app = MainApplication(user_id)
    app.mainloop()


if __name__ == "__main__":
    main()
