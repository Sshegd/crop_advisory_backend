import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate("firebase_config.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": os.getenv("FIREBASE_DB_URL")
})

def get_user_data(user_id: str):
    ref = db.reference("Users").child(user_id)
    return ref.get()