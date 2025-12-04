# 1) Imports & config
from typing import Optional

from pydantic import BaseModel, Field


# 2) Pydantic schemas

class Location(BaseModel):
    """
    Belgian location axes for validation.
    We will later flatten these to match the model's expected columns
    (country, region, province, postcode, locality).
    """
    province: str = Field(
        ...,
        min_length=1,
        description="Belgian province (e.g. 'Antwerpen', 'Limburg').",
    )
    postcode: int = Field(
        ...,
        ge=1000,
        le=9999,
        description="Belgian 4-digit postcode.",
    )
    locality: str = Field(
        ...,
        min_length=1,
        description="City / municipality / locality.",
    )
    region: Optional[str] = Field(
        None,
        min_length=1,
        description="Region (e.g. 'Vlaanderen', 'Wallonië', 'Brussels').",
    )
    country: Optional[str] = Field(
        None,
        min_length=1,
        description="Country name if present. Do NOT guess.",
    )


class PropertyFeatures(BaseModel):
    """
    All feature columns expected by the trained model pipeline,
    with an extra 'location' object for API-level validation.

    IMPORTANT:
    - property_type: required
    - location: required (province, postcode, locality)
    - price_per_m2 is NOT here (it's derived AFTER prediction)
    """
    # 🏡 Property type & classification (mandatory)
    property_type: str = Field(
        ...,
        min_length=1,
        description="Type of property (e.g. house, apartment, commercial). Required and never guessed.",
    )
    subtype_of_property: Optional[str] = Field(
        None,
        min_length=1,
        description="Subtype (e.g. duplex, bungalow, penthouse).",
    )

    # Location object for validation (we will flatten this for the model)
    location: Location = Field(
        ...,
        description="Belgian location axes; required and never guessed.",
    )

    # 📊 Size & physical attributes
    number_of_bedrooms: Optional[int] = Field(
        None,
        ge=0,
        description="Number of bedrooms.",
    )
    livable_surface: int = Field(
        ...,
        ge=1,
        description="Livable surface in m² (used for price_per_m2 after prediction).",
    )
    total_land_surface: Optional[int] = Field(
        None,
        ge=1,
        description="Total land surface in m².",
    )
    surface_garden: Optional[int] = Field(
        None,
        ge=0,
        description="Garden surface in m².",
    )
    surface_terrace: Optional[int] = Field(
        None,
        ge=0,
        description="Terrace surface in m².",
    )
    number_of_facades: Optional[int] = Field(
        None,
        ge=1,
        le=4,
        description="Number of facades.",
    )
    number_of_bathrooms: Optional[int] = Field(
        None,
        ge=0,
        description="Number of bathrooms.",
    )
    number_of_showers: Optional[int] = Field(
        None,
        ge=0,
        description="Number of showers.",
    )
    number_of_toilets: Optional[int] = Field(
        None,
        ge=0,
        description="Number of toilets.",
    )
    garage: Optional[bool] = Field(
        None,
        description="Does the property have a garage? (yes/no).",
    )
    number_of_garages: Optional[int] = Field(
        None,
        ge=0,
        description="Number of garages (integer count).",
    )
    number_of_garages_numeric: Optional[float] = Field(
        None,
        ge=0,
        description="Numeric representation of garages (if used as feature).",
    )

    # 🔥 Condition & comfort indicators
    state_of_property: Optional[str] = Field(
        None,
        min_length=1,
        description="State (e.g. 'to renovate', 'good', 'new').",
    )
    availability: Optional[str] = Field(
        None,
        min_length=1,
        description="Availability information (e.g. 'immediately').",
    )
    furnished: Optional[bool] = Field(
        None,
        description="Is the property furnished?",
    )
    attic: Optional[bool] = Field(
        None,
        description="Is there an attic?",
    )
    garden: Optional[bool] = Field(
        None,
        description="Is there a garden?",
    )
    terrace: Optional[bool] = Field(
        None,
        description="Is there a terrace?",
    )
    swimming_pool: Optional[bool] = Field(
        None,
        description="Is there a swimming pool?",
    )
    kitchen_equipment: Optional[str] = Field(
        None,
        min_length=1,
        description="Kitchen equipment level.",
    )
    kitchen_type: Optional[str] = Field(
        None,
        min_length=1,
        description="Kitchen type.",
    )
    type_of_heating: Optional[str] = Field(
        None,
        min_length=1,
        description="Type of heating (e.g. 'gas', 'electric').",
    )
    type_of_glazing: Optional[str] = Field(
        None,
        min_length=1,
        description="Type of glazing (e.g. 'double', 'triple').",
    )
    elevator: Optional[bool] = Field(
        None,
        description="Is there an elevator?",
    )


class PredictionRequest(BaseModel):
    data: PropertyFeatures = Field(
        ..., description="Single property data used for prediction."
    )


class PredictionResponse(BaseModel):
    prediction: Optional[float] = Field(
        None,
        description="Predicted property price in EUR.",
    )
    price_per_m2: Optional[float] = Field(
        None,
        description="Derived price per m² = prediction / livable_surface.",
    )
    status_code: int = Field(
        ...,
        description="HTTP-like status code for this prediction.",
    )
