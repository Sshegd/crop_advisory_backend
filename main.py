from fastapi import FastAPI
from ml_advisor import MLAdvisor
from translation import translate_text
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app
import os, json

# ---------------- FIREBASE INITIALIZATION ---------------- #
if "FIREBASE_KEY" in os.environ:
    key_json = json.loads(os.environ["FIREBASE_KEY"])
    cred = credentials.Certificate(key_json)
else:
    cred = credentials.Certificate("serviceAccountKey.json")  # local fallback

initialize_app(cred)

# ---------------- FASTAPI APP + ML ---------------- #
app = FastAPI()
advisor = MLAdvisor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow Android or web access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HELPERS ---------------- #
def maybe_translate(text, lang):
    """Translate only if not English"""
    return translate_text(text, lang) if lang != "en" else text

# ---------------- EXISTING CROP ADVICE ---------------- #
@app.post("/advice/existing")
async def advice_existing(data: dict):
    logs = data.get("logs", [])
    lang = data.get("language", "en")

    base, rec = advisor.existing_crop_advice(logs)

    base = maybe_translate(base, lang)
    rec = [maybe_translate(r, lang) for r in rec]

    return {
        "success": True,
        "advisory": base,
        "recommendations": rec
    }

# ---------------- NEW CROP RECOMMENDATION ---------------- #
@app.post("/advice/new")
async def advice_new(data: dict):
    lang = data.get("language", "en")

    base, rec = advisor.new_crop_recommend(data)

    base = maybe_translate(base, lang)
    rec = [maybe_translate(r, lang) for r in rec]

    return {
        "success": True,
        "advisory": base,
        "recommendations": rec
    }
