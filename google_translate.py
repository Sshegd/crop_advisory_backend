from google.cloud import translate_v2 as translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_translate_key.json"

translator = translate.Client()

def translate_text(data, target_language="kn"):
    if isinstance(data, dict):
        return {k: translate_text(v, target_language) for k, v in data.items()}
    if isinstance(data, list):
        return [translate_text(item, target_language) for item in data]

    if not isinstance(data, str):
        return data  # numbers etc.

    result = translator.translate(data, target_language=target_language)
    return result["translatedText"]
