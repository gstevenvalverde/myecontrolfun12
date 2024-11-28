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
        """Inicia el escaneo de rostro."""
        print("Escaneo de rostro iniciado...")
        scan_face()

    def start_tracking(self):
        """Calibra el cursor y comienza el seguimiento ocular."""
        global cap
        if cap is None:
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("No se pudo abrir la cámara.")
            return

        print("Calibrando el cursor...")
        calibrate_cursor(cap)

        print("Iniciando seguimiento ocular...")
        tracking_thread = Thread(target=track_eyes_and_blinks, args=(cap,))
        tracking_thread.start()

    def stop_tracking(self):
        """Detiene el seguimiento ocular y libera la cámara."""
        global cap
        if cap and cap.isOpened():
            cap.release()
            print("Seguimiento ocular detenido.")
        else:
            print("No hay seguimiento en curso.")


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
