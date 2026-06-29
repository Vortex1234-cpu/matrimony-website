import os
import firebase_admin
from firebase_admin import credentials

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to Firebase service account key
FIREBASE_KEY = os.path.join(BASE_DIR, "firebase_key.json")


def initialize_firebase():
    """
    Initialize Firebase Admin SDK only once.
    """
    if not firebase_admin._apps:
        if not os.path.exists(FIREBASE_KEY):
            raise FileNotFoundError(
                f"Firebase key file not found: {FIREBASE_KEY}"
            )

        cred = credentials.Certificate(FIREBASE_KEY)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized")


# Initialize Firebase automatically when imported
try:
    initialize_firebase()
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")