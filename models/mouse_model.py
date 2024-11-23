from services.firebase_config import db

def get_user_movement_data(user_id):
    """
    Recupera los datos de uso de un usuario desde Firestore.
    La estructura del documento se ha modificado para almacenar el tiempo de uso dentro de un campo 'usage_data'.
    """
    doc_ref = db.collection("movement_data").document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        # Recupera solo los datos de uso (el campo 'usage_data')
        movement_data = doc.to_dict().get("movement_data", {})
        return {"success": True, "movement_data": movement_data}

    return {"success": False, "error": "Usuario no encontrado."}

def store_movement_data(user_id, date, new_movements):
    """
    Almacena o actualiza el promedio de movimientos del usuario por día en Firestore,
    con la estructura solicitada.
    """
    try:
        # Accede al documento "movement_data" por user_id
        doc_ref = db.collection("movement_data").document(user_id)
        doc = doc_ref.get()

        # Si el documento ya existe
        if doc.exists:
            data = doc.to_dict()

            # Si ya existe el campo movement_data
            if "movement_data" in data:
                movement_data = data["movement_data"]

                # Verificar si ya existe la fecha, si existe promedia o actualiza
                if date in movement_data:
                    current_value = movement_data[date]
                    # Actualizar el valor con el nuevo movimiento (promedio en este caso, puedes cambiarlo si quieres)
                    updated_value = (current_value + new_movements) / 2  # Ejemplo de promedio, o puedes hacer otra operación
                    movement_data[date] = updated_value
                else:
                    # Si no existe la fecha, agregarla
                    movement_data[date] = new_movements

                # Actualizar la información en Firestore
                data["movement_data"] = movement_data
            else:
                # Si no existe el campo "movement_data", lo creamos
                data["movement_data"] = {date: new_movements}

            # Asegurarse de que siempre haya un campo de "user_id" (en caso de que no exista)
            data["user_id"] = user_id

            # Guardar los datos actualizados
            doc_ref.set(data, merge=True)

        else:
            # Si no existe el documento, crear uno nuevo con los datos
            data = {
                "user_id": user_id,
                "movement_data": {date: new_movements}
            }
            doc_ref.set(data)

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}


