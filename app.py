from flask import Flask, render_template, request

from src.prediction import (
    predict_soil,
    compare_reinforcements
)

from src.recommendation import SoilRecommendation


app = Flask(__name__)


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def home():

    return render_template(
        "dashboard.html"
    )


# ============================================================
# PREDICTION PAGE
# ============================================================

@app.route("/predict", methods=["GET"])
def prediction_page():

    return render_template(
        "predict.html"
    )


# ============================================================
# PREDICTION PROCESS
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # INPUT PARAMETERS
        # ----------------------------------------------------

        LL = float(
            request.form["LL"]
        )

        PL = float(
            request.form["PL"]
        )

        # Automatically calculate PI
        PI = LL - PL

        OMC = float(
            request.form["OMC"]
        )

        MDD = float(
            request.form["MDD"]
        )

        DEPTH = float(
            request.form["Depth"]
        )

        REINFORCEMENT = int(
            request.form["Reinforcement"]
        )

        SOAKED = int(
            request.form["Soaked"]
        )

        CBR = float(
            request.form["CBR"]
        )


        # ----------------------------------------------------
        # PREDICTION FOR SELECTED REINFORCEMENT
        # ----------------------------------------------------

        predictions = predict_soil(

            LL=LL,
            PL=PL,
            PI=PI,
            OMC=OMC,
            MDD=MDD,
            Depth=DEPTH,
            Reinforcement=REINFORCEMENT,
            Soaked=SOAKED,
            CBR=CBR

        )


        # ----------------------------------------------------
        # COMPARE ALL REINFORCEMENT TYPES
        # ----------------------------------------------------

        reinforcement_result = compare_reinforcements(

            LL=LL,
            PL=PL,
            PI=PI,
            OMC=OMC,
            MDD=MDD,
            Depth=DEPTH,
            Soaked=SOAKED,
            CBR=CBR

        )


        # ----------------------------------------------------
        # ENGINEERING RECOMMENDATION
        # ----------------------------------------------------

        recommendation = SoilRecommendation(
            predictions,
            selected_reinforcement=REINFORCEMENT,
            best_reinforcement=reinforcement_result[
                "best_reinforcement"
            ]
        ).report()


        # ----------------------------------------------------
        # RESULT PAGE
        # ----------------------------------------------------

        return render_template(

            "result.html",

            prediction=predictions,

            report=recommendation,

            reinforcement_comparison=reinforcement_result[
                "comparison"
            ],

            best_reinforcement=reinforcement_result[
                "best_reinforcement"
            ],

            best_average=reinforcement_result[
                "best_average"
            ],

            selected_reinforcement=REINFORCEMENT

        )


    except Exception as e:

        return render_template(

            "predict.html",

            error=str(e)

        )


# ============================================================
# ABOUT PAGE
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )