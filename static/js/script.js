document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // ELEMENTS
    // ==========================================

    const form = document.getElementById("predictionForm");

    const ll = document.getElementById("LL");
    const pl = document.getElementById("PL");
    const pi = document.getElementById("PI");

    const omc = document.getElementById("OMC");
    const mdd = document.getElementById("MDD");
    const cbr = document.getElementById("CBR");
    const depth = document.getElementById("Depth");

    const button = document.getElementById("predictButton");

    const validationMessage =
        document.getElementById("validationMessage");

    const validationText =
        document.getElementById("validationText");


    // ==========================================
    // PI CALCULATION
    // ==========================================

    function calculatePI() {

        const llValue = parseFloat(ll.value);
        const plValue = parseFloat(pl.value);

        if (
            !isNaN(llValue) &&
            !isNaN(plValue)
        ) {

            const result = llValue - plValue;

            if (result >= 0) {
                pi.value = result.toFixed(2);
            } else {
                pi.value = "";
            }

        } else {

            pi.value = "";

        }
    }


    ll.addEventListener("input", calculatePI);
    pl.addEventListener("input", calculatePI);


    // ==========================================
    // VALIDATION MESSAGE
    // ==========================================

    function showError(message) {

        validationText.textContent = message;

        validationMessage.classList.remove("d-none");

        window.scrollTo({
            top: validationMessage.offsetTop - 100,
            behavior: "smooth"
        });
    }


    function clearError() {

        validationMessage.classList.add("d-none");

        validationText.textContent = "";

    }


    // ==========================================
    // FORM VALIDATION
    // ==========================================

    form.addEventListener("submit", function (event) {

        clearError();

        const llValue = parseFloat(ll.value);
        const plValue = parseFloat(pl.value);
        const omcValue = parseFloat(omc.value);
        const mddValue = parseFloat(mdd.value);
        const cbrValue = parseFloat(cbr.value);
        const depthValue = parseFloat(depth.value);


        // LL

        if (
            isNaN(llValue) ||
            llValue < 0 ||
            llValue > 100
        ) {

            event.preventDefault();

            showError(
                "Liquid Limit (LL) must be between 0 and 100."
            );

            ll.focus();

            return;
        }


        // PL

        if (
            isNaN(plValue) ||
            plValue < 0 ||
            plValue > 100
        ) {

            event.preventDefault();

            showError(
                "Plastic Limit (PL) must be between 0 and 100."
            );

            pl.focus();

            return;
        }


        // PL cannot be greater than LL

        if (plValue > llValue) {

            event.preventDefault();

            showError(
                "Plastic Limit (PL) cannot be greater than Liquid Limit (LL)."
            );

            pl.focus();

            return;
        }


        // OMC

        if (
            isNaN(omcValue) ||
            omcValue < 0 ||
            omcValue > 100
        ) {

            event.preventDefault();

            showError(
                "Optimum Moisture Content (OMC) must be between 0 and 100%."
            );

            omc.focus();

            return;
        }


        // MDD

        if (
            isNaN(mddValue) ||
            mddValue < 0.5 ||
            mddValue > 3.5
        ) {

            event.preventDefault();

            showError(
                "Maximum Dry Density (MDD) must be between 0.5 and 3.5 g/cc."
            );

            mdd.focus();

            return;
        }


        // CBR

        if (
            isNaN(cbrValue) ||
            cbrValue < 0 ||
            cbrValue > 100
        ) {

            event.preventDefault();

            showError(
                "CBR must be between 0 and 100%."
            );

            cbr.focus();

            return;
        }


        // DEPTH

        if (
            isNaN(depthValue) ||
            depthValue < 0 ||
            depthValue > 2000
        ) {

            event.preventDefault();

            showError(
                "Depth of reinforcement must be between 0 and 2000 mm."
            );

            depth.focus();

            return;
        }


        // ==========================================
        // VALIDATION SUCCESS
        // ==========================================

        button.disabled = true;

        button.innerHTML =
            '<span class="spinner-border spinner-border-sm me-2"></span>' +
            'Running AI Prediction...';

    });

});