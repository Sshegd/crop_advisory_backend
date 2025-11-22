import joblib
import random

class MLAdvisor:

    def __init__(self):
        self.existing_model = joblib.load("models/existing_model.pkl")
        self.new_crop_rec = joblib.load("models/new_crop_recommender.pkl")

    def existing_crop_advice(self, logs):
        predicted = self.existing_model.predict([[
            logs.get("avgSoilMoisture", 0),
            logs.get("avgFertilizer", 0),
            logs.get("avgPestIndex", 0)
        ]])[0]

        base = f"Based on farm progress, the next optimal action is: {predicted}"
        recommendations = [
            "Use drip irrigation to avoid fungal growth.",
            "Apply neem cake once every 20–30 days.",
            "Monitor pest presence after rainfall."
        ]
        random.shuffle(recommendations)
        return base, recommendations

    def new_crop_recommend(self, farm):
        best_crop = self.new_crop_rec.predict([[
            farm.get("rainfall", 200),
            farm.get("temperature", 26),
            farm.get("soilTypeIndex", 1)
        ]])[0]

        advisory = f"We recommend growing {best_crop} for highest profitability."
        recommendations = [
            "Use high-quality certified seedlings",
            "Drip irrigation recommended",
            "Soil test twice per year",
            "Pest monitoring during peak season"
        ]
        return advisory, recommendations
