import os
import joblib
import pandas as pd


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = "saved_models"


# ============================================================
# LOAD MODELS
# ============================================================

models = {
    "PLT E": joblib.load(
        os.path.join(MODEL_PATH, "PLT_E.pkl")
    ),

    "Geogauge E": joblib.load(
        os.path.join(MODEL_PATH, "Geogauge_E.pkl")
    ),

    "DCP E": joblib.load(
        os.path.join(MODEL_PATH, "DCP_E.pkl")
    ),

    "LWD E": joblib.load(
        os.path.join(MODEL_PATH, "LWD_E.pkl")
    )
}


# ============================================================
# FEATURE COLUMNS
# ============================================================

FEATURE_COLUMNS = [
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


# ============================================================
# REINFORCEMENT NAMES
# ============================================================

REINFORCEMENT_NAMES = {
    0: "Unreinforced",
    1: "400 GSM",
    2: "700 GSM"
}


# ============================================================
# SINGLE PREDICTION
# ============================================================

def predict_soil(
    LL,
    PL,
    PI,
    OMC,
    MDD,
    Depth,
    Reinforcement,
    Soaked,
    CBR
):

    sample = pd.DataFrame(
        [[
            LL,
            PL,
            PI,
            OMC,
            MDD,
            Depth,
            Reinforcement,
            Soaked,
            CBR
        ]],
        columns=FEATURE_COLUMNS
    )

    predictions = {}

    for target, model in models.items():

        value = model.predict(sample)[0]

        predictions[target] = round(float(value), 2)

    return predictions


# ============================================================
# COMPARE ALL REINFORCEMENT TYPES
# ============================================================

def compare_reinforcements(
    LL,
    PL,
    PI,
    OMC,
    MDD,
    Depth,
    Soaked,
    CBR
):

    comparison = {}

    # --------------------------------------------------------
    # Test all three reinforcement conditions
    # --------------------------------------------------------

    for reinforcement_code in [0, 1, 2]:

        predictions = predict_soil(
            LL=LL,
            PL=PL,
            PI=PI,
            OMC=OMC,
            MDD=MDD,
            Depth=Depth,
            Reinforcement=reinforcement_code,
            Soaked=Soaked,
            CBR=CBR
        )

        # Calculate average predicted modulus
        average_modulus = sum(
            predictions.values()
        ) / len(predictions)

        comparison[
            REINFORCEMENT_NAMES[reinforcement_code]
        ] = {
            "code": reinforcement_code,
            "predictions": predictions,
            "average": round(average_modulus, 2)
        }

    # --------------------------------------------------------
    # Find best reinforcement
    # --------------------------------------------------------

    best_type = max(
        comparison,
        key=lambda x: comparison[x]["average"]
    )

    best_data = comparison[best_type]

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "comparison": comparison,

        "best_reinforcement": best_type,

        "best_code": best_data["code"],

        "best_predictions": best_data["predictions"],

        "best_average": best_data["average"]
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = compare_reinforcements(

        LL=25,

        PL=15,

        PI=10,

        OMC=14,

        MDD=1.95,

        Depth=0,

        Soaked=0,

        CBR=8

    )

    print("\n")
    print("=" * 70)
    print("REINFORCEMENT COMPARISON")
    print("=" * 70)

    for reinforcement, data in result["comparison"].items():

        print("\nReinforcement :", reinforcement)

        print(
            "PLT E          :",
            data["predictions"]["PLT E"]
        )

        print(
            "Geogauge E     :",
            data["predictions"]["Geogauge E"]
        )

        print(
            "DCP E          :",
            data["predictions"]["DCP E"]
        )

        print(
            "LWD E          :",
            data["predictions"]["LWD E"]
        )

        print(
            "Average Modulus:",
            data["average"]
        )

    print("\n")
    print("=" * 70)

    print(
        "BEST REINFORCEMENT :",
        result["best_reinforcement"]
    )

    print(
        "BEST AVERAGE MODULUS:",
        result["best_average"]
    )

    print("=" * 70)