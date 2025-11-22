# ml_existing_crop.py

from typing import Dict, Any, List, Optional
import numpy as np
import joblib
import os

class ExistingCropAdvisor:
    """
    Uses farmDetails + farmActivityLogs[cropKey] to generate advisory.
    This is a skeleton – you will plug in a real ML model later.
    """

    def __init__(self, model_path: str = "models/existing_crop_model.pkl"):
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception:
                self.model = None

    def build_features_from_logs(self, farm_details: Dict[str, Any],
                                 logs: Dict[str, Any]) -> np.ndarray:
        """
        Convert logs + farm details to numeric feature vector.
        You will customize this according to your dataset.
        """
        # Example dummy features:
        soil_type = farm_details.get("soilType", "")
        acre = float(farm_details.get("acre", 0) or 0)
        gunta = float(farm_details.get("gunta", 0) or 0)
        farm_size_acre = acre + gunta / 40.0

        # Count log types
        n_irrigations = 0
        n_fert_apps = 0
        n_pest_events = 0

        for log_id, log in logs.items():
            stage = log.get("stage")
            sub = log.get("subActivity")
            if stage == "planting_cultivation" and sub == "water_management":
                n_irrigations += 1
            if stage == "planting_cultivation" and sub == "nutrient_management":
                apps = log.get("applications", [])
                n_fert_apps += len(apps)
            if stage == "planting_cultivation" and sub == "crop_protection_maintenance":
                if log.get("pestDiseaseName"):
                    n_pest_events += 1

        # Dummy numeric encoding for soil type (you'll replace with real encoding)
        soil_code = {
            "Red Soil": 1,
            "Black Soil": 2,
            "Loam": 3
        }.get(soil_type, 0)

        features = np.array([
            farm_size_acre,
            soil_code,
            n_irrigations,
            n_fert_apps,
            n_pest_events
        ], dtype=float)

        return features.reshape(1, -1)

    def generate_advice(self,
                        farm_details: Dict[str, Any],
                        logs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return structured advice dict.
        If no ML model yet, use simple template based on features.
        """
        X = self.build_features_from_logs(farm_details, logs)

        # If you have a trained model:
        risk_score: Optional[float] = None
        if self.model is not None:
            risk_score = float(self.model.predict_proba(X)[0, 1])  # example classification

        # Derive simple suggestions from features (placeholder; later map from model output)
        _, _, n_irrigations, n_fert_apps, n_pest_events = X[0]

        stage_status = {
            "pre_planting": "completed" if any(
                log.get("stage") == "pre_planting" for log in logs.values()
            ) else "not_started",
            "planting_cultivation": "in_progress" if any(
                log.get("stage") == "planting_cultivation" for log in logs.values()
            ) else "not_started",
            "harvest_post_harvest": "in_progress" if any(
                log.get("stage") == "harvest_post_harvest" for log in logs.values()
            ) else "not_started",
        }

        water_advice = "Maintain regular irrigation schedule based on soil moisture."
        if n_irrigations == 0:
            water_advice = "No irrigation logs found. Ensure adequate watering, especially during dry spells."

        nutrient_advice = "Your fertilizer applications look moderate. Follow recommended split doses."
        if n_fert_apps == 0:
            nutrient_advice = "No nutrient management logs found. Consider applying a basal dose as per recommendations."

        pest_advice = "Monitor the crop weekly for pests and diseases."
        if n_pest_events > 0:
            pest_advice = "Pest/disease issues recorded. Continue monitoring and rotate control measures to avoid resistance."

        next_plan: List[str] = [
            "Scout the field for pests and diseases.",
            "Check soil moisture before next irrigation.",
            "Review fertilizer schedule and plan next application."
        ]

        if risk_score is not None:
            if risk_score > 0.7:
                next_plan.insert(0, "High risk of yield loss detected. Intensify monitoring and consult a local expert if symptoms appear.")
            elif risk_score < 0.3:
                next_plan.insert(0, "Crop condition seems stable. Maintain current management practices.")

        return {
            "stageStatus": stage_status,
            "waterManagementAdvice": water_advice,
            "nutrientManagementAdvice": nutrient_advice,
            "pestManagementAdvice": pest_advice,
            "next7DaysPlan": next_plan,
        }
