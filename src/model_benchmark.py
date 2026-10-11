import os
import warnings
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

warnings.filterwarnings("ignore")

# =====================================================
# PATHS
# =====================================================

DATA_PATH = os.path.join(
    "data",
    "processed",
    "cleaned_soil_data.csv"
)

MODEL_PATH = "saved_models"
os.makedirs(MODEL_PATH, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(DATA_PATH)

# Remove duplicate rows
df = df.drop_duplicates()

# =====================================================
# INPUT FEATURES
# =====================================================

FEATURES = [
    "LL",
    "PL",
    "PI",
    "OMC",
    "MDD (g/cc)",
    "Depth of reinforcement",
    "Reinforced/Unreinforced",
    "Soaked/Unsoaked",
    "CBR(%)"
]

TARGETS = [
    "PLT E",
    "Geogauge E",
    "DCP E",
    "LWD E"
]

# =====================================================
# MODELS
# =====================================================

models = {

    "Random Forest":
        RandomForestRegressor(random_state=42),

    "Extra Trees":
        ExtraTreesRegressor(random_state=42),

    "Gradient Boosting":
        GradientBoostingRegressor(random_state=42),

    "Hist Gradient":
        HistGradientBoostingRegressor(random_state=42),

    "XGBoost":
        XGBRegressor(
            random_state=42,
            verbosity=0
        ),

    "LightGBM":
        LGBMRegressor(random_state=42),

    "CatBoost":
        CatBoostRegressor(
            verbose=False,
            random_state=42
        )
}

# =====================================================
# BENCHMARK
# =====================================================

results = []

for target in TARGETS:

    print("\n" + "=" * 80)
    print(f"TARGET : {target}")
    print("=" * 80)

    # Keep only rows having target
    data = df.dropna(subset=[target])

    X = data[FEATURES]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    best_model = None
    best_score = -999

    for model_name, model in models.items():

        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        r2 = r2_score(y_test, pred)

        rmse = np.sqrt(
            mean_squared_error(y_test, pred)
        )

        mae = mean_absolute_error(
            y_test,
            pred
        )

        cv = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring="r2"
        ).mean()

        print(f"\n{model_name}")

        print(f"R2   : {r2:.4f}")
        print(f"RMSE : {rmse:.4f}")
        print(f"MAE  : {mae:.4f}")
        print(f"CV   : {cv:.4f}")

        results.append([
            target,
            model_name,
            r2,
            rmse,
            mae,
            cv
        ])

        if r2 > best_score:

            best_score = r2
            best_model = model

    print("\nBest Model :", type(best_model).__name__)
    print("Best R2    :", round(best_score,4))

    joblib.dump(
        best_model,
        os.path.join(
            MODEL_PATH,
            f"{target}.pkl"
        )
    )

# =====================================================
# SAVE RESULTS
# =====================================================

results = pd.DataFrame(
    results,
    columns=[
        "Target",
        "Model",
        "R2",
        "RMSE",
        "MAE",
        "Cross Validation"
    ]
)

results.to_csv(
    "reports/model_comparison.csv",
    index=False
)

print("\n" + "="*80)
print("MODEL BENCHMARK COMPLETED")
print("="*80)
print(results)