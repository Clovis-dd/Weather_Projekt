"""
Analyse eines gespeicherten ML-Modells.
"""

from pathlib import Path

import joblib



# ------------------------------------------------------
# Pfade
# ------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


MODEL_PATH = (
    BASE_DIR
    /
    "models"
    /
    "lin_reg_v1.pkl"
)



# ------------------------------------------------------
# Modell laden
# ------------------------------------------------------

print("=" * 50)
print("MODEL INSPECTION")
print("=" * 50)


print(
    "\nModellpfad:"
)

print(
    MODEL_PATH
)


if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Modell nicht gefunden: {MODEL_PATH}"
    )


model = joblib.load(
    MODEL_PATH
)



# ------------------------------------------------------
# Informationen
# ------------------------------------------------------

print(
    "\nModelltyp:"
)

print(
    type(model)
)



print(
    "\nErwartete Features:"
)


if hasattr(
    model,
    "n_features_in_"
):

    print(
        model.n_features_in_
    )

else:

    print(
        "Keine Information vorhanden."
    )



print(
    "\nParameter:"
)


if hasattr(
    model,
    "get_params"
):

    print(
        model.get_params()
    )



print(
    "\nKoeffizienten:"
)


if hasattr(
    model,
    "coef_"
):

    print(
        model.coef_
    )



print(
    "\nIntercept:"
)


if hasattr(
    model,
    "intercept_"
):

    print(
        model.intercept_
    )


print(
    "\nAnalyse abgeschlossen."
)