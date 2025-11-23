import os, json
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

def get_translate_client():
    # If running on Railway (ENV variable)
    if "GOOGLE_TRANSLATE_KEY" in os.environ:
        key_json = json.loads(os.environ["GOOGLE_TRANSLATE_KEY"])
        credentials = service_account.Credentials.from_service_account_info(key_json)
    else:
        # local fallback for development
        credentials = service_account.Credentials.from_service_account_file(
            "google_translate_key.json"
        )

    return translate.Client(credentials=credentials)
