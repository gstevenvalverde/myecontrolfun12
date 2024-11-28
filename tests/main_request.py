import sys
from models.usage_model import get_user_usage_data
from models.speed_model import get_user_velocity_data
from models.mouse_model import get_user_movement_data


def show_usage_data(user_id):
    """
    Consulta y muestra los datos de tiempo de uso del usuario.
    """
    result = get_user_usage_data(user_id)
    if result.get("success"):
        usage_data = result.get("usage_data", {})
        if usage_data:
            print("\n--- Tiempo de Uso (Minutos) ---")
            for date, minutes in usage_data.items():
                print(f"{date}: {minutes} minutos")
        else:
            print("No hay datos de tiempo de uso para este usuario.")
    else:
        print(f"Error al obtener los datos: {result.get('error')}")


def show_velocity_data(user_id):
    """
    Consulta y muestra los datos de velocidad del usuario.
    """
    result = get_user_velocity_data(user_id)
    if result.get("success"):
        velocity_data = result.get("velocity_data", {})
        if velocity_data:
            print("\n--- Velocidad Promedio (px/s) ---")
            for date, speed in velocity_data.items():
                print(f"{date}: {speed} px/s")
        else:
            print("No hay datos de velocidad para este usuario.")
    else:
        print(f"Error al obtener los datos: {result.get('error')}")


def show_movement_data(user_id):
    """
    Consulta y muestra los datos de movimientos del usuario.
    """
    result = get_user_movement_data(user_id)
    if result.get("success"):
        movement_data = result.get("movement_data", {})
        if movement_data:
            print("\n--- Número de Movimientos ---")
            for date, movements in movement_data.items():
                print(f"{date}: {movements} movimientos")
        else:
            print("No hay datos de movimientos para este usuario.")
    else:
        print(f"Error al obtener los datos: {result.get('error')}")


def main():
    """
    Interfaz de consola para consultar los datos de Firebase.
    """
    print("=== Interfaz de Datos ===")
    user_id = input("Ingrese el ID del usuario: ").strip()

    while True:
        print("\nOpciones:")
        print("1. Consultar Tiempo de Uso")
        print("2. Consultar Velocidad Promedio")
        print("3. Consultar Número de Movimientos")
        print("4. Salir")

        choice = input("Seleccione una opción (1-4): ").strip()

        if choice == "1":
            show_usage_data(user_id)
        elif choice == "2":
            show_velocity_data(user_id)
        elif choice == "3":
            show_movement_data(user_id)
        elif choice == "4":
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
