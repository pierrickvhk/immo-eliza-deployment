from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd

from api.schemas import PropertyFeatures

# Path to model file
_MODEL_PATH = Path(__file__).parent / "models" / "immo_eliza_rf_small.joblib"
_MODEL = None  # lazy-loaded cache


def _load_model():
    """
    Lazy-load the trained pipeline.

    - If the file is directly a model/pipeline (has .predict) -> use that.
    - If it is a dict, try common keys such as ‘model’, ‘pipeline’, ‘pipe’, ‘estimator’.
    """
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    loaded = joblib.load(_MODEL_PATH)

    # Case 1: immediately a pipeline/model
    if hasattr(loaded, "predict"):
        _MODEL = loaded
        return _MODEL

    # Case 2: dict with a model inside
    if isinstance(loaded, dict):
        for key in ("model", "pipeline", "pipe", "estimator"):
            candidate = loaded.get(key)
            if hasattr(candidate, "predict"):
                _MODEL = candidate
                return _MODEL

        raise TypeError(
            "Loaded joblib file is a dict but no usable model was found under keys "
            "'model', 'pipeline', 'pipe', or 'estimator'."
        )

    # Case 3: compleet ander type
    raise TypeError(
        f"Loaded joblib object of type {type(loaded)}, which has no 'predict' method."
    )


def preprocess_for_model(features: PropertyFeatures) -> Dict[str, Any]:
    """
    Create a feature dictionary with exactly the same column names
    as in your training (with capital letters and spaces).

    We use ALL 23 features that the model expects here.
    If the user does not fill in some of them, they will be included as None,
    and your preprocessing pipeline should be able to handle that.
    """
    feature_dict: Dict[str, Any] = {
        # 23 expected feature columns:

        # Size & physical attributes
        "Number of bedrooms": features.number_of_bedrooms,
        "Livable surface": features.livable_surface,
        "Total land surface": features.total_land_surface,
        "Surface garden": features.surface_garden,
        "Surface terrace": features.surface_terrace,
        "Number of facades": features.number_of_facades,
        "Number of bathrooms": features.number_of_bathrooms,
        "Number of showers": features.number_of_showers,
        "Number of toilets": features.number_of_toilets,
        "Garage": features.garage,
        "Number of garages": features.number_of_garages,

        # Condition & comfort indicators
        "Furnished": features.furnished,
        "Attic": features.attic,
        "Garden": features.garden,
        "Terrace": features.terrace,
        "Swimming pool": features.swimming_pool,
        "Kitchen equipment": features.kitchen_equipment,
        "Kitchen type": features.kitchen_type,
        "Type of heating": features.type_of_heating,
        "Type of glazing": features.type_of_glazing,
        "Elevator": features.elevator,
        "Availability": features.availability,
        "State of the property": features.state_of_property,
    }

    return feature_dict


def predict_price(features: PropertyFeatures) -> float:
    """
    - Takes validated PropertyFeatures (with location, property_type for the API).
    - Converts to DataFrame with exact column names for the model.
    - Uses your trained pipeline to predict a price.
    """
    model = _load_model()
    feature_dict = preprocess_for_model(features)

    # Model expects DataFrame with the correct column names
    input_df = pd.DataFrame([feature_dict])

    y_pred = model.predict(input_df)
    price = float(np.asarray(y_pred)[0])

    return price
