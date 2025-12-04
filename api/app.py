from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from api.schemas import PredictionRequest, PredictionResponse
from api.predict import predict_price  # import relative from api package mounted in container



app = FastAPI(
    title="Immo Eliza Deployment API",
    description="FastAPI backend for Belgian real-estate price prediction.",
    version="0.1.0",
    default_response_class=JSONResponse,
)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "alive"}


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
)
async def predict_endpoint(payload: PredictionRequest) -> PredictionResponse:
    try:
        price = predict_price(payload.data)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": 500,
                "error": "Model artifact not found on server.",
            },
        )
    except Exception as exc:
        # No silent fails.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": 500,
                "error": "Internal server error during prediction.",
                "details": str(exc),
            },
        )

    # Compute price_per_m2 AFTER prediction, never as input.
    price_per_m2: Optional[float] = None
    livable_surface = payload.data.livable_surface
    if livable_surface and livable_surface > 0:
        price_per_m2 = price / livable_surface

    return PredictionResponse(
        prediction=price,
        price_per_m2=price_per_m2,
        status_code=200,
    )
