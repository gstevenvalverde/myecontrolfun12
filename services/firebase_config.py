import firebase_admin
from firebase_admin import credentials, auth

# Inicializa la app de Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
