import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import joblib

def main():
    df = pd.read_csv("data/crop_choice_training.csv")

    target = "profit_rs_per_acre"
    y = df[target]
    X = df.drop(columns=[target])

    cat_cols = ["soil_type", "district", "taluk", "crop_name"]
    num_cols = [c for c in X.columns if c not in cat_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols)
        ]
    )

    reg = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )

    pipe = Pipeline(steps=[
        ("pre", preprocessor),
        ("reg", reg)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipe.fit(X_train, y_train)
    print("Train R2:", pipe.score(X_train, y_train))
    print("Test R2:", pipe.score(X_test, y_test))

    joblib.dump(pipe, "models/new_crop_model.pkl")
    print("Saved model to models/new_crop_model.pkl")

if __name__ == "__main__":
    main()
