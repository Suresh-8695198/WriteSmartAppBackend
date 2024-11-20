# speech_to_text/firebase.py
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Check if the default app has already been initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate("\\firebase\\firebase-admin-sdk.json")
        firebase_admin.initialize_app(cred)
