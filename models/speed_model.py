from services.firebase_config import db

def store_velocity(user_id, date, average_speed):
    """
    Guarda o actualiza la velocidad promedio del usuario en Firestore.
    """
    try:
        doc_ref = db.collection("movement_velocity").document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            velocity_data = data.get("velocity_data", {})

            if date in velocity_data:
                # Si ya existe el dato para el día, actualizamos el promedio
                current_value = velocity_data[date]
                updated_value = (current_value + average_speed) / 2
                velocity_data[date] = updated_value
            else:
                velocity_data[date] = average_speed

            # Actualizar el documento en Firestore
            data["velocity_data"] = velocity_data
            doc_ref.set(data, merge=True)
        else:
            # Si no existe el documento, lo creamos
            data = {
                "user_id": user_id,
                "velocity_data": {date: average_speed}
            }
            doc_ref.set(data)

        print(f"Velocidad promedio guardada para el {date}: {average_speed} px/s")

    except Exception as e:
        print(f"Error al guardar los datos: {str(e)}")
