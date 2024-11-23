import firebase_admin
import os
from firebase_admin import credentials, firestore

# Obtiene la ruta absoluta del archivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "serviceAccountKey.json")

# Inicializa la app de Firebase
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)

# Inicializa Firestore
db = firestore.client()
