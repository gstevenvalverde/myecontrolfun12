from services.firebase_config import db

def get_user_usage_data(user_id):
    """
    Recupera los datos de uso de un usuario desde Firestore.
    La estructura del documento se ha modificado para almacenar el tiempo de uso dentro de un campo 'usage_data'.
    """
    doc_ref = db.collection("usage_data").document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        # Recupera solo los datos de uso (el campo 'usage_data')
        user_data = doc.to_dict().get("usage_data", {})
        return {"success": True, "usage_data": user_data}

    return {"success": False, "error": "Usuario no encontrado."}


def update_user_usage_data(user_id, date, minutes):
    """
    Actualiza el tiempo de uso acumulado de un usuario en Firestore.
    Suma los minutos al tiempo existente en lugar de reemplazarlo.
    Agrega el campo `user_id` al documento si no está presente.
    """
    try:
        doc_ref = db.collection("usage_data").document(user_id)
        user_doc = doc_ref.get()

        if user_doc.exists:
            # Si el documento existe, obtenemos los minutos actuales para el día
            existing_data = user_doc.to_dict().get("usage_data", {})
            current_minutes = existing_data.get(date, 0)
            new_minutes = current_minutes + minutes  # Sumar los minutos

            # Actualizar el campo con el nuevo total de minutos
            doc_ref.set(
                {
                    "user_id": user_id,
                    "usage_data": {date: new_minutes}  # Actualizar solo los minutos para el día
                },
                merge=True
            )
        else:
            # Si no existe, creamos el documento con los minutos del día
            doc_ref.set(
                {
                    "user_id": user_id,
                    "usage_data": {date: minutes}  # Inicializar los minutos para el día
                }
            )

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}

