class MLAdvisor:

    def existing_crop_advice(self, logs):
        """Generate advisory based on latest farm log information (no ML yet)"""
        if not logs:
            return (
                "No log data found for this crop.",
                ["Please record activities such as watering, fertilization, pest symptoms etc."]
            )

        last = logs[-1]  # latest activity

        sub = last.get("subActivity", "").lower()

        if "water" in sub:
            base = "Continue regulated irrigation schedule."
            rec = [
                "Maintain soil moisture but avoid waterlogging.",
                "Apply irrigation during early morning to reduce evaporation."
            ]
        elif "nutrient" in sub:
            base = "Continue nutrient management based on crop uptake."
            rec = [
                "Apply fertilizers based on soil test.",
                "Avoid excess nitrogen to prevent weak growth."
            ]
        elif "pest" in sub or "disease" in sub:
            base = "Attention required — pest/disease symptoms noticed."
            rec = [
                "Apply recommended bio-pesticides immediately.",
                "Remove affected leaves and maintain field hygiene."
            ]
        else:
            base = "Crop is in good condition."
            rec = [
                "Maintain field sanitation.",
                "Periodic irrigation and monitoring recommended."
            ]

        return base, rec

    def new_crop_recommend(self, farm):
        """Suggest new crop based on location, soil & weather"""
        soil = farm.get("soilType", "").lower()
        district = farm.get("district", "").lower()
        weather = farm.get("weather", "").lower()

        if "red" in soil:
            crop = "Arecanut"
        elif "black" in soil:
            crop = "Cotton"
        elif "sandy" in soil:
            crop = "Groundnut"
        else:
            crop = "Maize"

        base = f"Recommended crop to plant: {crop}"
        rec = [
            f"Choose high-yielding variety of {crop}.",
            "Ensure soil preparation before sowing.",
            "Use drip irrigation for water efficiency.",
            "Apply organic manure + NPK as per requirement.",
            "Monitor for pests from early stage."
        ]
        return base, rec
