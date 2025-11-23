import os, json
from google.cloud import translate_v2 as translate
from google.oauth2.service_account import Credentials

def get_client():
    key_json = os.environ.get("GOOGLE_TRANSLATE_KEY")

    if not key_json:
        raise Exception("Translation key missing in Railway env variables!")

    info = json.loads(key_json)
    creds = Credentials.from_service_account_info(info)
    return translate.Client(credentials=creds)

translator = get_client()
