import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa la app de Firebase
cred = credentials.Certificate("services/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Inicializa Firestore
db = firestore.client()