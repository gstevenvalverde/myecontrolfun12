import customtkinter as ctk
import tkinter as tk


class EyeControlFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        # Configuración del Frame
        self.pack(padx=20, pady=20)

        # Crear los botones
        self.create_buttons()

    def create_buttons(self):
        # Botón para escanear el rostro
        self.scan_button = ctk.CTkButton(self, text="Escaneo de rostro", command=self.scan_face)
        self.scan_button.pack(pady=10)

        # Botón para iniciar el seguimiento
        self.start_button = ctk.CTkButton(self, text="Iniciar seguimiento", command=self.start_tracking)
        self.start_button.pack(pady=10)

        # Botón para detener el seguimiento
        self.stop_button = ctk.CTkButton(self, text="Detener seguimiento", command=self.stop_tracking)
        self.stop_button.pack(pady=10)

    def scan_face(self):
        print("Escaneo de rostro iniciado...")

    def start_tracking(self):
        print("Seguimiento ocular iniciado...")

    def stop_tracking(self):
        print("Seguimiento ocular detenido...")


# Función principal para ejecutar la aplicación
def main():
    # Crear la ventana principal
    root = ctk.CTk()
    root.title("Control de Ojos")
    root.geometry("400x300")

    # Crear y mostrar el EyeControlFrame
    eye_control_frame = EyeControlFrame(root)

    # Iniciar el bucle principal
    root.mainloop()


# Ejecutar la función main
if __name__ == "__main__":
    main()
