from utils.heatmap_tracker import HeatmapTracker

def main():
    user_id = "1zeMM4Vsl9OuIq8DwZUM7GaTge82"  # UID del usuario
    tracker = HeatmapTracker(user_id)

    try:
        print("Iniciando rastreo del heatmap...")
        tracker.start_tracking()

        while True:
            print("\nOpciones:")
            print("1. Mostrar heatmap actual")
            print("2. Salir")
            choice = input("Selecciona una opción: ")

            if choice == "1":
                print("Heatmap actual:")
                for row in tracker.heatmap:
                    print(row)
            elif choice == "2":
                print("Cerrando aplicación...")
                break
            else:
                print("Opción no válida.")
    finally:
        tracker.stop_tracking()

if __name__ == "__main__":
    main()
