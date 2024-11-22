import pandas as pd
import matplotlib.pyplot as plt
from models.usage_model import get_user_usage_data

def plot_usage(user_id):
    # Recuperar datos de Firestore
    result = get_user_usage_data(user_id)

    if result["success"]:
        usage_data = result["usage_data"]

        # Convertir a DataFrame
        df = pd.DataFrame(list(usage_data.items()), columns=["Date", "Minutes"])
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # Crear gráfico de líneas
        plt.figure(figsize=(10, 5))
        plt.plot(df["Date"], df["Minutes"], marker="o", color="blue")
        plt.title("Tiempo de Uso Diario")
        plt.xlabel("Fecha")
        plt.ylabel("Minutos")
        plt.grid(True)
        plt.show()
    else:
        print(f"Error: {result['error']}")
