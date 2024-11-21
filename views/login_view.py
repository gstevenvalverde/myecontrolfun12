import customtkinter as ctk
from PIL import Image, ImageTk  # Importar Image y ImageTk desde Pillow
from controllers.auth_controller import AuthController
from controllers.dashboard_controller import DashboardController
from utils import centrar_ventana
from views.dashboard_view import Dashboard

# Selecting GUI theme - dark,
# light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme-blue, green, dark-blue
ctk.set_default_color_theme("blue")

class Login:
    def __init__(self, root, controller):
        """
        Clase para gestionar la vista del login.
        :param root: Ventana principal de Tkinter.
        :param controller: Controlador que manejará la lógica del login.
        """
        self.root = root
        self.controller = controller
        centrar_ventana(self.root, 600, 400)
        self.root.title("Login")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        # Llamar a los métodos para construir la interfaz
        self._create_left_panel()
        self._create_right_panel()

    def _create_left_panel(self):
        """
        Crear el panel izquierdo con ilustración y texto.
        """
        frame_left = ctk.CTkFrame(self.root, fg_color="#1e1e1e")  # Usar fg_color para el fondo
        frame_left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # Título en el lado izquierdo
        title_label = ctk.CTkLabel(
            frame_left,
            text="econtrol",
            font=("Arial", 18, "bold"),
            text_color="#fafafa",  # Usar text_color en lugar de fg
            justify="center",
        )
        title_label.pack(pady=20)

        # Ilustración del cohete
        try:
            logo_path = "../static/logo.jpg"  # Ruta a la imagen
            image = Image.open(logo_path)  # Usar Pillow para abrir la imagen
            logo_image = ctk.CTkImage(light_image=image,
                                      dark_image=image,
                                      size=(150, 150))  # Convertir la imagen con ImageTk
            rocket_label = ctk.CTkLabel(frame_left, image=logo_image, fg_color="#1e1e1e", text='')
            rocket_label.image = logo_image  # Evitar que la imagen sea recolectada por el GC
            rocket_label.pack(pady=10)
        except Exception as e:
            print(f"Error cargando la imagen: {e}")
            placeholder_label = ctk.CTkLabel(
                frame_left,
                text="(Ilustración aquí)",
                font=("Arial", 10),
                text_color="#ffffff",  # Usar text_color
                fg_color="#1e1e1e",  # Usar fg_color
            )
            placeholder_label.pack(pady=10)

    def _create_right_panel(self):
        """
        Crear el panel derecho con el formulario de inicio de sesión.
        """
        self.frame_right = ctk.CTkFrame(self.root, fg_color="#2e2e2e")
        self.frame_right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        self._create_login_frame()
        #self._create_sign_up_frame()

    def _create_login_frame(self):
        login_frame = ctk.CTkFrame(self.frame_right, fg_color="#2e2e2e")
        login_frame.pack(side="top", fill="both")
        # Título del formulario
        form_title = ctk.CTkLabel(
            login_frame,
            text="Iniciar sesión",
            font=("Arial", 18, "bold"),
            text_color="#fafafa",  # Usar text_color en lugar de fg
        )
        form_title.pack(pady=20)

        # Campo username
        self.username_label = ctk.CTkLabel(
            login_frame,
            text="Username",
            font=("Arial", 14),
            text_color="#fafafa",  # Usar text_color en lugar de fg
        )
        self.username_label.pack(anchor="w", padx=20)
        self.username_entry = ctk.CTkEntry(login_frame)
        self.username_entry.pack(fill="x", padx=20, pady=5)

        # Campo password
        self.password_label = ctk.CTkLabel(
            login_frame,
            text="Password",
            font=("Arial", 14),
            text_color="#fafafa",  # Usar text_color
        )
        self.password_label.pack(anchor="w", padx=20)
        self.password_entry = ctk.CTkEntry(login_frame, show="*")
        self.password_entry.pack(fill="x", padx=20, pady=5)

        # Mensaje obligatorio password
        self.password_message = ctk.CTkLabel(
            login_frame,
            text="*Rellene su usario y contraseña",
            font=("Arial", 10),
            text_color="#c51d34",  # Usar text_color
        )
        self.password_message.pack(anchor="w", padx=20)
        self.password_message.place_forget()  # Inicialmente no mostrar el mensaje

        # Checkbox "Recordar inicio de sesión"
        self.remember_me_var = ctk.BooleanVar()
        self.remember_me_checkbox = ctk.CTkCheckBox(
            login_frame,
            text="Recordar inicio de sesión",
            variable=self.remember_me_var,
            font=("Arial", 14),
            text_color="#ffffff",  # Usar text_color
        )
        self.remember_me_checkbox.pack(anchor="w", padx=20, pady=10)

        # Botón de login
        self.login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            command=self._on_login_clicked,
        )
        self.login_button.pack(pady=20)

        create_user_frame = ctk.CTkFrame(master=login_frame, fg_color="#2e2e2e")
        create_user_frame.pack(side="top", fill="x", padx=8, pady=8)

        # No tiene cuenta
        self.sign_up_label = ctk.CTkLabel(
            create_user_frame,
            text="No tiene cuenta?",
            font=("Arial", 12),
            text_color="#fafafa",  # Usar text_color
        )
        self.sign_up_label.pack(side="left")

        # Botón de login
        self.handle_create_user_button = ctk.CTkButton(
            create_user_frame,
            text="Crear usuario",
            command=lambda : self.switch_frame(page=self._create_sign_up_frame),
        )
        self.handle_create_user_button.pack(side="right")

    def _create_sign_up_frame(self):
        sign_up_frame = ctk.CTkFrame(self.frame_right, fg_color="#2e2e2e")
        sign_up_frame.pack(side="top", fill="both")
        # Título del formulario
        form_title = ctk.CTkLabel(
            sign_up_frame,
            text="Crear usuario",
            font=("Arial", 18, "bold"),
            text_color="#fafafa",  # Usar text_color en lugar de fg
        )
        form_title.pack(pady=20)

        # Campo username
        self.username_label = ctk.CTkLabel(
            sign_up_frame,
            text="Username",
            font=("Arial", 14),
            text_color="#fafafa",  # Usar text_color en lugar de fg
        )
        self.username_label.pack(anchor="w", padx=20)
        self.username_entry = ctk.CTkEntry(sign_up_frame)
        self.username_entry.pack(fill="x", padx=20, pady=5)

        # Campo password
        self.password_label = ctk.CTkLabel(
            sign_up_frame,
            text="Password",
            font=("Arial", 14),
            text_color="#fafafa",  # Usar text_color
        )
        self.password_label.pack(anchor="w", padx=20)
        self.password_entry = ctk.CTkEntry(sign_up_frame, show="*")
        self.password_entry.pack(fill="x", padx=20, pady=5)

        # Mensaje obligatorio password
        self.password_message = ctk.CTkLabel(
            sign_up_frame,
            text="*Rellene su usario y contraseña",
            font=("Arial", 10),
            text_color="#c51d34",  # Usar text_color
        )
        self.password_message.pack(anchor="w", padx=20)
        self.password_message.place_forget()  # Inicialmente no mostrar el mensaje

        # Botón de crear usuario
        self.sign_up_button = ctk.CTkButton(
            sign_up_frame,
            text="Crear usuario",
            command=lambda : self.switch_frame(page=self._create_login_frame),
        )
        self.sign_up_button.pack(pady=20)

    def _on_login_clicked(self):
        """
        Evento para manejar el clic del botón de login.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        remember_me = self.remember_me_var.get()

        # Llamar al controlador para manejar la lógica
        # Validación de campos
        valid = True

        if not password:
            self.password_message.place(x=20, y=180)  # Mostrar el mensaje si el campo está vacío
            valid = False
        else:
            self.password_message.place_forget()  # Ocultar el mensaje si el campo no está vacío

        if valid:
            # Si los campos son válidos, llamar al controlador para manejar la lógica
            self.controller.handle_login(username, password, remember_me)

    def switch_frame(self, page):
        for frame in self.frame_right.winfo_children():
            frame.destroy()
        page()

# Inicialización de la aplicación
if __name__ == "__main__":
    root = ctk.CTk()  # Ventana principal con CustomTkinter
    controller = AuthController()
    app = Login(root, controller)
    root.mainloop()