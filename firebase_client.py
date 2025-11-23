import os, json
import firebase_admin
from firebase_admin import credentials, firestore, db

def init_firebase():
    if not firebase_admin._apps:
        if "FIREBASE_KEY" in os.environ:
            key_json = json.loads(os.environ["FIREBASE_KEY"])
            cred = credentials.Certificate(key_json)
        else:
            cred = credentials.Certificate("serviceAccountKey.json")  # local fallback
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://<your-project-id>.firebaseio.com"
        })

init_firebase()
