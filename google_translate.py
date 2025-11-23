import os, json
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

def get_translate_client():
    # If running on Railway (ENV variable)
    if "GOOGLE_TRANSLATE_KEY" in os.environ:
        key_json = json.loads(os.environ["GOOGLE_TRANSLATE_KEY"])
        credentials = service_account.Credentials.from_service_account_info(key_json)
    else:
        # Local fallback
        credentials = service_account.Credentials.from_service_account_file(
            "google_translate_key.json"
        )

    return translate.Client(credentials=credentials)


# 🔥 this is the function your main.py expects
def translate_text(text: str, target_lang: str):
    """
    Translates text into target language using Google Cloud Translate API
    """
    client = get_translate_client()

    if not text or not target_lang:
        return text

    response = client.translate(text, target_language=target_lang)
    return response["translatedText"]
