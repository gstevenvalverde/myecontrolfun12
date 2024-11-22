from services.firebase_config import db

def flatten_heatmap(heatmap):
    """
    Convierte el heatmap de una matriz bidimensional a una lista plana.
    """
    return [value for row in heatmap for value in row]

def unflatten_heatmap(flattened, grid_size):
    """
    Convierte una lista plana a una matriz bidimensional.
    """
    return [flattened[i:i + grid_size] for i in range(0, len(flattened), grid_size)]

def store_heatmap(user_id, date, heatmap):
    """
    Guarda o actualiza los datos del heatmap en Firestore.
    """
    try:
        doc_ref = db.collection("heatmap_data").document(user_id)
        doc = doc_ref.get()

        # Convertir el heatmap actual a una lista plana
        flattened_heatmap = flatten_heatmap(heatmap)

        if doc.exists:
            data = doc.to_dict()
            heatmap_data = data.get("heatmap_data", {})

            if date in heatmap_data:
                # Recuperar y combinar datos de heatmap existentes
                existing_flattened = heatmap_data[date]
                combined_flattened = [
                    existing_flattened[i] + flattened_heatmap[i]
                    for i in range(len(flattened_heatmap))
                ]
                heatmap_data[date] = combined_flattened
            else:
                # Guardar nuevos datos si no existe para la fecha
                heatmap_data[date] = flattened_heatmap

            # Actualizar Firestore
            data["heatmap_data"] = heatmap_data
            doc_ref.set(data, merge=True)
        else:
            # Crear nuevo documento si no existe
            data = {
                "user_id": user_id,
                "heatmap_data": {date: flattened_heatmap}
            }
            doc_ref.set(data)

        print(f"Heatmap guardado para el {date}")

    except Exception as e:
        print(f"Error al guardar el heatmap: {str(e)}")