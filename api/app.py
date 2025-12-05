from typing import Any, Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from api.schemas import PredictionRequest, PredictionResponse 
from api.predict import predict_price



app = FastAPI(
    title="Immo Eliza Deployment API",
    description="FastAPI backend for Belgian real-estate price prediction.",
    version="0.1.0",
    default_response_class=JSONResponse,
)

# WHY: return documented JSON errors even when something crashes unexpectedly
@app.exception_handler(Exception)
def global_exception_handler(_: Any, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": {
                "status_code": 500,
                "error": "Internal server error",
                "message": str(exc)
            }
        }
    )



# WHY: easy uptime validation from browser or external service
@app.get("/", response_model=Dict[str, str])
def root() -> Dict[str, str]:
    return {"status": "alive"}



# WHY: location + property_type must be mandatory and not guessed or skipped
@app.post("/predict", response_model=PredictionResponse)
def predict(features: PredictionRequest) -> JSONResponse:
    try:
        # Validate mandatory data BEFORE prediction
        if not features.data.property_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status_code": 400,
                    "error": "Property type is required."
                }
            )

        loc = features.data.location
        if not loc or not loc.province or not loc.postcode or not loc.locality:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status_code": 400,
                    "error": "Province, postcode, and locality are required."
                }
            )

        # Call model service
        price = predict_price(features.data)

        # Prevent leakage — compute AFTER inference
        price_per_m2 = price / price if price else None

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "prediction": price,
                "price_per_m2": price_per_m2,
                "status_code": 200
            }
        )

    except HTTPException as http_exc:
        # Already formatted JSON errors should pass cleanly
        raise http_exc
    except Exception as model_exc:
        # WHY: model errors must be explicit and wrapped in JSON
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": {
                    "status_code": 500,
                    "error": "Prediction service failed.",
                    "details": str(model_exc)
                }
            }
        )

