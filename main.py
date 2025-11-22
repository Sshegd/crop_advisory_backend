from fastapi import FastAPI
from pydantic import BaseModel
from firebase_admin import credentials, db, initialize_app
from ml_existing_crop import ExistingCropAdvisor
from ml_new_crop import NewCropAdvisor
from google_translate import translate_text

app = FastAPI()

# ---------- Firebase Setup ----------
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred, {
    "databaseURL": "https://YOUR_PROJECT_URL.firebaseio.com/"
})

# ---------- Load ML Classes ----------
existing_advisor = ExistingCropAdvisor()
new_advisor = NewCropAdvisor()

# ---------- Requests ----------
class ExistingAdviceReq(BaseModel):
    userId: str
    cropKey: str
    languageCode: str

class NewAdviceReq(BaseModel):
    userId: str
    district: str
    taluk: str
    soilType: str
    farmSizeAcre: float
    season: str
    avgRainfall: float
    avgTemp: float
    languageCode: str

# ---------- Existing Crop Advisory ----------
@app.post("/advice/existing")
def get_existing_advice(req: ExistingAdviceReq):
    farm_ref = db.reference(f"Users/{req.userId}/farmDetails").get()
    logs_ref = db.reference(f"Users/{req.userId}/farmActivityLogs/{req.cropKey}").get()

    response = existing_advisor.generate_advice(
        farm_details=farm_ref or {},
        logs=logs_ref or {}
    )

    if req.languageCode == "kn":
        response = translate_text(response, target_language="kn")

    return response

# ---------- New Crop Advisory ----------
@app.post("/advice/new")
def get_new_advice(req: NewAdviceReq):
    farm_ref = db.reference(f"Users/{req.userId}/farmDetails").get()

    extra = {
        "district": req.district,
        "taluk": req.taluk,
        "soilType": req.soilType,
        "farmSizeAcre": req.farmSizeAcre,
        "season": req.season,
        "avgRainfall": req.avgRainfall,
        "avgTemp": req.avgTemp,
    }

    response = new_advisor.generate_advice(
        farm_details=farm_ref or {},
        extra=extra
    )

    if req.languageCode == "kn":
        response = translate_text(response, target_language="kn")

    return response

@app.get("/")
def root():
    return {"status": "Crop Advisory Backend Running ✔"}
