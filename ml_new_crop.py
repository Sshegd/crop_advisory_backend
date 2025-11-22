# ml_new_crop.py

from typing import Dict, Any, List
import numpy as np
import joblib
import os

class NewCropAdvisor:
    """
    Recommends best crop and management plan based on location, soil, farm size, weather.
    """

    def __init__(self, model_path: str = "models/new_crop_model.pkl"):
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception:
                self.model = None

        # Candidate crops (scope: 4 crops)
        self.candidate_crops = ["Areca nut", "Paddy", "Banana", "Chilli"]

    def build_features(self,
                       farm_details: Dict[str, Any],
                       extra: Dict[str, Any],
                       crop_name: str) -> np.ndarray:
        soil_type = extra.get("soilType") or farm_details.get("soilType", "")
        farm_size = float(extra.get("farmSizeAcre", 0) or 0)
        rainfall = float(extra.get("avgRainfall", 0) or 0)
        temp = float(extra.get("avgTemp", 0) or 0)

        soil_code = {
            "Red Soil": 1,
            "Black Soil": 2,
            "Laterite": 3,
            "Sandy": 4
        }.get(soil_type, 0)

        crop_code = {
            "Areca nut": 1,
            "Paddy": 2,
            "Banana": 3,
            "Chilli": 4
        }.get(crop_name, 0)

        features = np.array([
            farm_size,
            soil_code,
            rainfall,
            temp,
            crop_code
        ], dtype=float)

        return features.reshape(1, -1)

    def generate_advice(self,
                        farm_details: Dict[str, Any],
                        extra: Dict[str, Any]) -> Dict[str, Any]:

        best_crop = None
        best_score = -1.0
        crop_scores: Dict[str, float] = {}

        for crop in self.candidate_crops:
            X = self.build_features(farm_details, extra, crop)

            if self.model is not None:
                # Example: model predicts expected profit per acre
                score = float(self.model.predict(X)[0])
            else:
                # Dummy heuristic until model is trained
                score = self._dummy_score(crop, extra)

            crop_scores[crop] = score
            if score > best_score:
                best_score = score
                best_crop = crop

        # Build management suggestions for best crop (template for now)
        if best_crop is None:
            best_crop = "Areca nut"  # fallback

        seed_advice = self._seed_advice(best_crop)
        water_advice = self._water_advice(best_crop, extra)
        nutrient_advice = self._nutrient_advice(best_crop, extra)
        pest_advice = self._pest_advice(best_crop)

        expected_yield = f"Model-based expected yield: {best_score:.1f} units/acre" if self.model else \
                         "Expected yield: moderate to high based on soil and rainfall."

        risk_factors = [
            "Market price fluctuations",
            "Climate variability (drought or excess rain)"
        ]

        return {
            "recommendedCrop": best_crop,
            "reasoning": f"Based on your soil type, rainfall and temperature, {best_crop} shows the best balance of yield and profit among the candidate crops.",
            "expectedYield": expected_yield,
            "seedPlantAdvice": seed_advice,
            "waterManagementAdvice": water_advice,
            "nutrientManagementAdvice": nutrient_advice,
            "pestManagementAdvice": pest_advice,
            "riskFactors": risk_factors
        }

    def _dummy_score(self, crop: str, extra: Dict[str, Any]) -> float:
        # Simple non-ruley heuristic but deterministic (placeholder)
        rainfall = float(extra.get("avgRainfall", 0) or 0)
        if crop == "Areca nut":
            return rainfall / 10.0  # likes high rainfall
        if crop == "Paddy":
            return rainfall / 12.0
        if crop == "Banana":
            return rainfall / 15.0
        if crop == "Chilli":
            return 50.0 - abs(rainfall - 800) / 10.0
        return 0.0

    def _seed_advice(self, crop: str) -> str:
        return f"Select certified seedlings/seed of {crop} from an authorized nursery or dealer with good germination and disease-free status."

    def _water_advice(self, crop: str, extra: Dict[str, Any]) -> str:
        return f"Align irrigation schedule for {crop} with local rainfall. Avoid waterlogging and long dry spells."

    def _nutrient_advice(self, crop: str, extra: Dict[str, Any]) -> str:
        return f"Base nutrient management for {crop} on soil test values. Split N and K into 3–4 applications across the season."

    def _pest_advice(self, crop: str) -> str:
        return f"Monitor {crop} weekly for major pests and diseases. Prefer biocontrol and need-based pesticide use."
