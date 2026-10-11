import os
import warnings
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    KFold
)

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor
)

from xgboost import XGBRegressor
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
REPORT_PATH = "reports"

os.makedirs(MODEL_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(DATA_PATH)

# Remove duplicate rows
df = df.drop_duplicates()

# =====================================================
# FEATURES
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
# MODELS & PARAMETER GRIDS
# =====================================================

models = {

    "Random Forest": (

        RandomForestRegressor(random_state=42),

        {
            "n_estimators": [100,200,300,500],
            "max_depth": [5,10,15,20,None],
            "min_samples_split": [2,5,10],
            "min_samples_leaf": [1,2,4]
        }

    ),

    "Extra Trees": (

        ExtraTreesRegressor(random_state=42),

        {
            "n_estimators": [100,200,300,500],
            "max_depth": [5,10,15,20,None],
            "min_samples_split": [2,5,10],
            "min_samples_leaf": [1,2,4]
        }

    ),

    "XGBoost": (

        XGBRegressor(
            random_state=42,
            verbosity=0
        ),

        {
            "n_estimators":[100,200,300],
            "learning_rate":[0.01,0.05,0.1],
            "max_depth":[3,5,7,10],
            "subsample":[0.8,1.0]
        }

    ),

    "CatBoost": (

        CatBoostRegressor(
            verbose=False,
            random_state=42
        ),

        {
            "iterations":[200,400,600],
            "depth":[4,6,8],
            "learning_rate":[0.01,0.05,0.1]
        }

    )

}

# =====================================================
# RESULTS
# =====================================================

results = []

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# =====================================================
# TRAIN
# =====================================================

for target in TARGETS:

    print("\n")
    print("="*80)
    print(f"TARGET : {target}")
    print("="*80)

    data = df.dropna(subset=[target])

    X = data[FEATURES]

    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    best_r2 = -999

    best_model = None

    best_name = ""

    for model_name, (model, params) in models.items():

        print(f"\nTraining {model_name}...")

        search = RandomizedSearchCV(

            estimator=model,

            param_distributions=params,

            n_iter=10,

            cv=cv,

            scoring="r2",

            random_state=42,

            n_jobs=-1

        )

        search.fit(
            X_train,
            y_train
        )

        tuned_model = search.best_estimator_

        prediction = tuned_model.predict(X_test)

        r2 = r2_score(
            y_test,
            prediction
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                prediction
            )
        )

        mae = mean_absolute_error(
            y_test,
            prediction
        )

        print(f"R2   : {r2:.4f}")
        print(f"RMSE : {rmse:.4f}")
        print(f"MAE  : {mae:.4f}")

        results.append([

            target,

            model_name,

            r2,

            rmse,

            mae,

            search.best_params_

        ])

        if r2 > best_r2:

            best_r2 = r2
            best_model = tuned_model
            best_name = model_name

    print("\nBEST MODEL")
    print(best_name)
    print("R2 :", round(best_r2,4))

    filename = target.replace(" ", "_") + ".pkl"

    joblib.dump(

        best_model,

        os.path.join(
            MODEL_PATH,
            filename
        )

    )

# =====================================================
# SAVE REPORT
# =====================================================

results = pd.DataFrame(

    results,

    columns=[

        "Target",

        "Model",

        "R2",

        "RMSE",

        "MAE",

        "Best Parameters"

    ]

)

results.to_csv(

    os.path.join(
        REPORT_PATH,
        "hyperparameter_results.csv"
    ),

    index=False

)

print("\n")
print("="*80)
print("HYPERPARAMETER TUNING COMPLETED")
print("="*80)

print(results)