from google.cloud import translate_v2 as translate

translate_client = translate.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var

def translate_text(text: str, target: str):
    if target == "en":
        return text
    if not text:
        return text
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]
