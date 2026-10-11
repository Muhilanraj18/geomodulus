class SoilRecommendation:

    def __init__(
        self,
        predictions,
        selected_reinforcement=0,
        best_reinforcement=None
    ):

        self.plt = predictions["PLT E"]
        self.geo = predictions["Geogauge E"]
        self.dcp = predictions["DCP E"]
        self.lwd = predictions["LWD E"]

        self.selected_reinforcement = int(
            selected_reinforcement
        )

        self.best_reinforcement = (
            best_reinforcement
        )


    # ========================================================
    # REINFORCEMENT NAME
    # ========================================================

    def reinforcement_name(self, code):

        names = {

            0: "Unreinforced",

            1: "400 GSM",

            2: "700 GSM"

        }

        return names.get(
            int(code),
            "Unknown"
        )


    # ========================================================
    # SOIL QUALITY
    # ========================================================

    def soil_quality(self):

        avg = (
            self.plt +
            self.geo +
            self.dcp +
            self.lwd
        ) / 4


        if avg >= 150:

            return "Excellent"


        elif avg >= 120:

            return "Very Good"


        elif avg >= 90:

            return "Good"


        elif avg >= 70:

            return "Moderate"


        else:

            return "Poor"


    # ========================================================
    # PAVEMENT RECOMMENDATION
    # ========================================================

    def pavement(self):

        avg = (
            self.plt +
            self.geo +
            self.dcp +
            self.lwd
        ) / 4


        if avg >= 140:

            return "Rigid Pavement"


        elif avg >= 90:

            return "Flexible Pavement"


        else:

            return "Ground Improvement Required"


    # ========================================================
    # REINFORCEMENT DECISION
    # ========================================================

    def reinforcement(self):

        # If comparison result is available
        if self.best_reinforcement:

            if self.best_reinforcement == "Unreinforced":

                return "Unreinforced Recommended"


            elif self.best_reinforcement == "400 GSM":

                return "400 GSM Reinforcement Recommended"


            elif self.best_reinforcement == "700 GSM":

                return "700 GSM Reinforcement Recommended"


        # Fallback
        return "Reinforcement Assessment Required"


    # ========================================================
    # OVERALL RATING
    # ========================================================

    def stars(self):

        quality = self.soil_quality()


        ratings = {

            "Excellent": "★★★★★",

            "Very Good": "★★★★☆",

            "Good": "★★★☆☆",

            "Moderate": "★★☆☆☆",

            "Poor": "★☆☆☆☆"

        }


        return ratings.get(
            quality,
            "☆☆☆☆☆"
        )


    # ========================================================
    # REPORT
    # ========================================================

    def report(self):

        return {

            # ----------------------------------------------
            # Predictions
            # ----------------------------------------------

            "PLT E": self.plt,

            "Geogauge E": self.geo,

            "DCP E": self.dcp,

            "LWD E": self.lwd,


            # ----------------------------------------------
            # Soil assessment
            # ----------------------------------------------

            "Soil Quality":
                self.soil_quality(),


            "Recommended Pavement":
                self.pavement(),


            # ----------------------------------------------
            # Reinforcement
            # ----------------------------------------------

            "Selected Reinforcement":
                self.reinforcement_name(
                    self.selected_reinforcement
                ),


            "Recommended Reinforcement":
                self.best_reinforcement
                if self.best_reinforcement
                else "Not Available",


            "Reinforcement":
                self.reinforcement(),


            # ----------------------------------------------
            # Rating
            # ----------------------------------------------

            "Overall Rating":
                self.stars()

        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample = {

        "PLT E": 72.49,

        "Geogauge E": 92.83,

        "DCP E": 60.03,

        "LWD E": 77.88

    }


    engine = SoilRecommendation(

        sample,

        selected_reinforcement=0,

        best_reinforcement="700 GSM"

    )


    report = engine.report()


    print("\n")

    print("=" * 70)

    print("SOIL ANALYSIS REPORT")

    print("=" * 70)


    for key, value in report.items():

        print(
            f"{key:30}: {value}"
        )

    print("=" * 70)