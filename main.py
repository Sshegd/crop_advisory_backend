from fastapi import FastAPI
from ml_advisor import MLAdvisor
from google_translate import translate_text       # <-- make sure filename is google_translate.py
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
import os, json
import uvicorn


# ---------------- FIREBASE INITIALIZATION ---------------- #
if not firebase_admin._apps:
    if "SERVICE_ACCOUNT_KEY" in os.environ:
        creds_json = json.loads(os.environ["SERVICE_ACCOUNT_KEY"])
        cred = credentials.Certificate(creds_json)
    else:
        raise Exception("SERVICE_ACCOUNT_KEY missing in Railway Variables")
    firebase_admin.initialize_app(cred)

# ---------------- FASTAPI APP + ML ---------------- #
app = FastAPI()
advisor = MLAdvisor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HELPERS ---------------- #
def maybe_translate(text, lang):
    return translate_text(text, lang) if lang != "en" else text

# ---------------- EXISTING CROP ADVICE ---------------- #
@app.post("/advice/existing")
async def advice_existing(data: dict):
    logs = data.get("logs", [])
    lang = data.get("language", "en")

    base, rec = advisor.existing_crop_advice(logs)

    base = maybe_translate(base, lang)
    rec = [maybe_translate(r, lang) for r in rec]

    return {"success": True, "advisory": base, "recommendations": rec}

# ---------------- NEW CROP RECOMMENDATION ---------------- #
@app.post("/advice/new")
async def advice_new(data: dict):
    lang = data.get("language", "en")

    base, rec = advisor.new_crop_recommend(data)

    base = maybe_translate(base, lang)
    rec = [maybe_translate(r, lang) for r in rec]

    return {"success": True, "advisory": base, "recommendations": rec}
# ---------------- ROOT CHECK ENDPOINT ---------------- #
@app.get("/")
async def home():
    return {
        "status": "running",
        "service": "Crop Advisory Backend",
        "message": "API is online 🚀"
    }

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))   # default for local
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)




