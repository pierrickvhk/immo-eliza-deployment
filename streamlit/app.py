# 1) Imports & config
import os
import random
from typing import Any, Dict

import requests
import streamlit as st
import random

# --- Random example helper ---

def fill_random_example() -> None:
    """Fill session_state with a random, but realistic Belgian example."""
    st.session_state["property_type"] = random.choice(
        ["house", "apartment", "villa", "duplex"]
    )
    st.session_state["subtype_of_property"] = random.choice(
        ["bungalow", "penthouse", "studio", "duplex"]
    )

    st.session_state["province"] = random.choice(
        ["Antwerpen", "Oost-Vlaanderen", "Limburg", "Vlaams-Brabant", "West-Vlaanderen"]
    )
    st.session_state["postcode"] = random.choice([2000, 3000, 8000, 9000])
    st.session_state["locality"] = random.choice(
        ["Antwerpen", "Leuven", "Gent", "Brugge"]
    )

    st.session_state["number_of_bedrooms"] = random.randint(1, 4)
    st.session_state["livable_surface"] = random.randint(60, 220)
    st.session_state["total_land_surface"] = st.session_state["livable_surface"] + random.randint(0, 400)

    st.session_state["surface_garden"] = random.choice([0, 40, 80, 120])
    st.session_state["surface_terrace"] = random.choice([0, 10, 20, 30])
    st.session_state["number_of_facades"] = random.choice([2, 3, 4])

    st.session_state["number_of_bathrooms"] = random.choice([1, 1, 2])
    st.session_state["number_of_showers"] = random.choice([0, 0, 1])
    st.session_state["number_of_toilets"] = random.choice([1, 2])

    st.session_state["garage"] = random.choice([True, False])
    st.session_state["number_of_garages"] = 1 if st.session_state["garage"] else 0

    st.session_state["furnished"] = random.choice([False, False, True])
    st.session_state["attic"] = random.choice([False, True])
    st.session_state["garden"] = st.session_state["surface_garden"] > 0
    st.session_state["terrace"] = st.session_state["surface_terrace"] > 0
    st.session_state["swimming_pool"] = False

    st.session_state["kitchen_equipment"] = random.choice(
        ["not installed", "installed", "hyper equipped"]
    )
    st.session_state["kitchen_type"] = random.choice(
        ["not installed", "semi-equipped", "installed"]
    )
    st.session_state["type_of_heating"] = random.choice(["gas", "electric", "heat pump"])
    st.session_state["type_of_glazing"] = random.choice(["single", "double", "triple"])
    st.session_state["elevator"] = random.choice([False, False, True])

    st.session_state["state_of_property"] = random.choice(
        ["to renovate", "good", "as new"]
    )
    st.session_state["availability"] = random.choice(
        ["immediately", "to be agreed", "not specified"]
    )

# Flag to control one-time random fill
if "load_random_once" not in st.session_state:
    st.session_state["load_random_once"] = False

# If the flag is set, pre-fill the session_state before widgets are rendered
if st.session_state.get("load_random_once", False):
    fill_random_example()
    st.session_state["load_random_once"] = False


# Prefer env var in production (Render / Streamlit Cloud),
# fallback to your public Render URL.
API_URL = os.getenv(
    "IMMO_API_URL",
    "https://immo-eliza-deployment-l1sk.onrender.com/predict",
)

st.set_page_config(
    page_title="Immo Eliza Price Predictor",
    page_icon="🏠",
    layout="centered",
)

# --- Global CSS for background, banner & sections ---
st.markdown(
    """
<style>
/* Global page background (real-estate photo) */
.stApp {
    background-image: url('https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Card for main content */
.block-container {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 18px;
    padding: 1.5rem 1.8rem 2rem 1.8rem;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.25);
}

/* Banner styling (top hero section) */
.app-banner {
    position: sticky;
    top: 0.5rem;
    z-index: 999;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    padding: 1.4rem 1.6rem;
    background-image:
        linear-gradient(120deg, rgba(15,23,42,0.86), rgba(79,70,229,0.85)),
        url('https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg');
    background-size: cover;
    background-position: center;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

/* Banner text styles */
.app-banner-title {
    font-size: 1.7rem;
    font-weight: 700;
}

.app-banner-subtitle {
    font-size: 0.96rem;
    opacity: 0.96;
}

.app-banner-meta {
    font-size: 0.85rem;
    opacity: 0.9;
}

/* Section header styling */
.app-section-title {
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.4rem;
    padding: 0.3rem 0.6rem;
    border-left: 4px solid #4F46E5;
    background: rgba(79, 70, 229, 0.06);
    border-radius: 0 10px 10px 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# Placeholders for prediction results & errors
result_placeholder = st.empty()
error_placeholder = st.empty()


# 2) Helper: small util to map "Not specified" -> None
def none_if_not_specified(value: str | None) -> Any:
    if value is None:
        return None
    return None if value == "Not specified" else value


# 3) Helper: build payload for FastAPI
def build_payload_from_inputs() -> Dict[str, Any]:
    """
    Build the JSON payload that matches the FastAPI PredictionRequest schema.
    """
    # Basic info
    property_type = st.session_state["property_type"]
    subtype_of_property = st.session_state["subtype_of_property"]

    province = st.session_state["province"]
    postcode = st.session_state["postcode"]
    locality = st.session_state["locality"]
    region = st.session_state["region"]
    country = st.session_state["country"]

    # Size & physical attributes
    number_of_bedrooms = st.session_state["number_of_bedrooms"]
    livable_surface = st.session_state["livable_surface"]
    total_land_surface = st.session_state["total_land_surface"]
    surface_garden = st.session_state["surface_garden"]
    surface_terrace = st.session_state["surface_terrace"]
    number_of_facades = st.session_state["number_of_facades"]
    number_of_bathrooms = st.session_state["number_of_bathrooms"]
    # Safe access with default
    number_of_showers = st.session_state.get("number_of_showers", 0)
    number_of_toilets = st.session_state["number_of_toilets"]
    garage = st.session_state["garage"]
    number_of_garages = st.session_state["number_of_garages"]
    number_of_garages_numeric = (
        float(number_of_garages) if number_of_garages is not None else None
    )

    # Comfort & condition
    state_of_property = st.session_state["state_of_property"]
    availability = st.session_state["availability"]
    furnished = st.session_state["furnished"]
    attic = st.session_state["attic"]
    garden = st.session_state["garden"]
    terrace = st.session_state["terrace"]
    swimming_pool = st.session_state["swimming_pool"]
    kitchen_equipment = st.session_state["kitchen_equipment"]
    kitchen_type = st.session_state["kitchen_type"]
    type_of_heating = st.session_state["type_of_heating"]
    type_of_glazing = st.session_state["type_of_glazing"]
    elevator = st.session_state["elevator"]

    payload: Dict[str, Any] = {
        "data": {
            "property_type": property_type,
            "subtype_of_property": none_if_not_specified(subtype_of_property),
            "location": {
                "province": province,
                "postcode": postcode,
                "locality": locality,
                "region": none_if_not_specified(region),
                "country": none_if_not_specified(country),
            },
            "number_of_bedrooms": number_of_bedrooms,
            "livable_surface": livable_surface,
            "total_land_surface": total_land_surface,
            "surface_garden": surface_garden,
            "surface_terrace": surface_terrace,
            "number_of_facades": number_of_facades,
            "number_of_bathrooms": number_of_bathrooms,
            "number_of_showers": number_of_showers,
            "number_of_toilets": number_of_toilets,
            "garage": garage,
            "number_of_garages": number_of_garages,
            "number_of_garages_numeric": number_of_garages_numeric,
            "state_of_property": none_if_not_specified(state_of_property),
            "availability": none_if_not_specified(availability),
            "furnished": furnished,
            "attic": attic,
            "garden": garden,
            "terrace": terrace,
            "swimming_pool": swimming_pool,
            "kitchen_equipment": none_if_not_specified(kitchen_equipment),
            "kitchen_type": none_if_not_specified(kitchen_type),
            "type_of_heating": none_if_not_specified(type_of_heating),
            "type_of_glazing": none_if_not_specified(type_of_glazing),
            "elevator": elevator,
        }
    }

    return payload


# 4) Helper: random example filler
def fill_random_example() -> None:
    """
    Fill Streamlit session_state with a random but realistic Belgian example.
    Does NOT call the API, just pre-fills the form.
    """
    provinces = ["Antwerpen", "Oost-Vlaanderen", "Limburg", "Vlaams-Brabant", "West-Vlaanderen"]
    localities_by_province = {
        "Antwerpen": ["Antwerpen", "Mechelen", "Turnhout"],
        "Oost-Vlaanderen": ["Gent", "Sint-Niklaas", "Aalst"],
        "Limburg": ["Hasselt", "Genk", "Tongeren"],
        "Vlaams-Brabant": ["Leuven", "Tienen", "Diest"],
        "West-Vlaanderen": ["Brugge", "Kortrijk", "Oostende"],
    }
    postcodes_by_locality = {
        "Antwerpen": 2000,
        "Mechelen": 2800,
        "Turnhout": 2300,
        "Gent": 9000,
        "Sint-Niklaas": 9100,
        "Aalst": 9300,
        "Hasselt": 3500,
        "Genk": 3600,
        "Tongeren": 3700,
        "Leuven": 3000,
        "Tienen": 3300,
        "Diest": 3290,
        "Brugge": 8000,
        "Kortrijk": 8500,
        "Oostende": 8400,
    }

    province = random.choice(provinces)
    locality = random.choice(localities_by_province[province])
    postcode = postcodes_by_locality[locality]

    st.session_state["property_type"] = random.choice(["house", "apartment", "villa", "duplex"])
    st.session_state["subtype_of_property"] = random.choice(
        ["Not specified", "bungalow", "semi-detached", "terraced"]
    )

    st.session_state["province"] = province
    st.session_state["locality"] = locality
    st.session_state["postcode"] = postcode
    st.session_state["region"] = "Vlaanderen"
    st.session_state["country"] = "Belgium"

    st.session_state["livable_surface"] = random.randint(60, 220)
    st.session_state["total_land_surface"] = st.session_state["livable_surface"] + random.randint(40, 500)
    st.session_state["number_of_bedrooms"] = random.randint(1, 5)
    st.session_state["number_of_bathrooms"] = random.randint(1, 3)
    st.session_state["number_of_showers"] = random.randint(0, 2)
    st.session_state["number_of_facades"] = random.randint(2, 4)
    st.session_state["number_of_toilets"] = random.randint(1, 3)

    st.session_state["garden"] = random.choice([True, False])
    st.session_state["terrace"] = random.choice([True, False])
    st.session_state["surface_garden"] = random.randint(0, 300)
    st.session_state["surface_terrace"] = random.randint(0, 60)

    st.session_state["garage"] = random.choice([True, False])
    st.session_state["number_of_garages"] = random.randint(0, 2)

    st.session_state["swimming_pool"] = random.choice([False, False, True])  # mostly no pool
    st.session_state["furnished"] = random.choice([False, True])
    st.session_state["attic"] = random.choice([False, True])
    st.session_state["elevator"] = random.choice([False, True])

    st.session_state["state_of_property"] = random.choice(
        ["good", "as new", "to renovate", "new"]
    )
    st.session_state["availability"] = random.choice(
        ["immediately", "at deed", "to be agreed upon", "Not specified"]
    )
    st.session_state["kitchen_equipment"] = random.choice(
        ["installed", "hyper-equipped", "not installed", "Not specified"]
    )
    st.session_state["kitchen_type"] = random.choice(
        ["semi-equipped", "equipped", "usa not installed", "Not specified"]
    )
    st.session_state["type_of_heating"] = random.choice(
        ["gas", "electric", "heat pump", "oil", "Not specified"]
    )
    st.session_state["type_of_glazing"] = random.choice(
        ["double", "triple", "single", "Not specified"]
    )


# 5) UI: banner

st.markdown(
    """
<div class="app-banner">
  <div class="app-banner-title">Immo Eliza – Price Predictor</div>
  <div class="app-banner-subtitle">
    Estimate Belgian property prices using a trained machine learning model, exposed via FastAPI.
  </div>
  <div class="app-banner-meta">
    FastAPI · Random Forest · Docker · Render · Streamlit
  </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("API configuration")
    st.write("Current API URL:")
    st.code(API_URL, language="text")
    st.markdown(
        "This app sends JSON requests to the FastAPI backend and displays the prediction."
    )

# 6) UI sections

# --- Section 1: Property basics ---
st.markdown('<div class="app-section-title">1. Property basics</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    property_type_options = [
        "house",
        "apartment",
        "studio",
        "villa",
        "duplex",
        "commercial",
        "other",
    ]
    st.selectbox(
        "Property type*",
        options=property_type_options,
        index=0,
        key="property_type",
        help="Type of property. Required.",
    )

    subtype_options = [
        "Not specified",
        "bungalow",
        "penthouse",
        "loft",
        "detached",
        "semi-detached",
        "terraced",
    ]
    st.selectbox(
        "Subtype of property",
        options=subtype_options,
        index=1,
        key="subtype_of_property",
        help="Optional subtype.",
    )

with col2:
    state_options = [
        "Not specified",
        "to be done up",
        "to restore",
        "to renovate",
        "good",
        "as new",
        "new",
    ]
    st.selectbox(
        "State of property",
        options=state_options,
        index=4,
        key="state_of_property",
        help="Condition of the property.",
    )

    availability_options = [
        "Not specified",
        "immediately",
        "at deed",
        "to be agreed upon",
    ]
    st.selectbox(
        "Availability",
        options=availability_options,
        index=1,
        key="availability",
        help="Availability information.",
    )

# --- Section 2: Location ---
st.markdown('<div class="app-section-title">2. Location (Belgium, required)</div>', unsafe_allow_html=True)

col_loc1, col_loc2, col_loc3 = st.columns([1.2, 0.8, 1.2])

with col_loc1:
    st.text_input(
        "Province*",
        key="province",
        value="Antwerpen",
        help="Belgian province (required).",
    )

with col_loc2:
    st.number_input(
        "Postcode*",
        key="postcode",
        min_value=1000,
        max_value=9999,
        value=2000,
        step=1,
        help="4-digit Belgian postcode (required).",
    )

with col_loc3:
    st.text_input(
        "Locality*",
        key="locality",
        value="Antwerpen",
        help="City / municipality (required).",
    )

col_loc_extra1, col_loc_extra2 = st.columns(2)
with col_loc_extra1:
    region_options = [
        "Not specified",
        "Vlaanderen",
        "Wallonië",
        "Brussels",
    ]
    st.selectbox(
        "Region",
        options=region_options,
        index=1,
        key="region",
    )
with col_loc_extra2:
    country_options = [
        "Not specified",
        "Belgium",
        "Luxembourg",
        "France",
        "Netherlands",
        "Germany",
    ]
    st.selectbox(
        "Country",
        options=country_options,
        index=1,
        key="country",
    )

# --- Section 3: Size & structure ---
st.markdown('<div class="app-section-title">3. Size & structure</div>', unsafe_allow_html=True)

col_size1, col_size2 = st.columns(2)

with col_size1:
    st.number_input(
        "Livable surface (m²)*",
        key="livable_surface",
        min_value=1,
        max_value=1000,
        value=120,
        step=1,
    )
    st.number_input(
        "Total land surface (m²)",
        key="total_land_surface",
        min_value=1,
        max_value=5000,
        value=300,
        step=1,
    )
    st.number_input(
        "Number of bedrooms",
        key="number_of_bedrooms",
        min_value=0,
        max_value=20,
        value=3,
        step=1,
    )

with col_size2:
    st.number_input(
        "Number of bathrooms",
        key="number_of_bathrooms",
        min_value=0,
        max_value=10,
        value=1,
        step=1,
    )
    st.number_input(
        "Number of showers",
        key="number_of_showers",
        min_value=0,
        max_value=10,
        value=0,
        step=1,
    )
    st.number_input(
        "Number of facades",
        key="number_of_facades",
        min_value=1,
        max_value=4,
        value=3,
        step=1,
    )
    st.number_input(
        "Number of toilets",
        key="number_of_toilets",
        min_value=0,
        max_value=10,
        value=2,
        step=1,
    )

# --- Section 4: Comfort & extras ---
st.markdown('<div class="app-section-title">4. Comfort & extras</div>', unsafe_allow_html=True)

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.checkbox("Garden", key="garden", value=True)
    st.number_input(
        "Garden surface (m²)",
        key="surface_garden",
        min_value=0,
        max_value=2000,
        value=50,
        step=5,
    )
    st.checkbox("Terrace", key="terrace", value=True)
    st.number_input(
        "Terrace surface (m²)",
        key="surface_terrace",
        min_value=0,
        max_value=200,
        value=20,
        step=2,
    )

with col_c2:
    st.checkbox("Garage", key="garage", value=True)
    st.number_input(
        "Number of garages",
        key="number_of_garages",
        min_value=0,
        max_value=10,
        value=1,
        step=1,
    )
    st.checkbox("Swimming pool", key="swimming_pool", value=False)
    st.checkbox("Furnished", key="furnished", value=False)
    st.checkbox("Attic", key="attic", value=False)
    st.checkbox("Elevator", key="elevator", value=False)

# --- Section 5: Technical details ---
st.markdown('<div class="app-section-title">5. Technical details</div>', unsafe_allow_html=True)

col_k1, col_k2 = st.columns(2)

with col_k1:
    kitchen_equipment_options = [
        "Not specified",
        "not installed",
        "installed",
        "hyper-equipped",
    ]
    st.selectbox(
        "Kitchen equipment",
        options=kitchen_equipment_options,
        index=2,
        key="kitchen_equipment",
    )

    kitchen_type_options = [
        "Not specified",
        "usa not installed",
        "semi-equipped",
        "equipped",
    ]
    st.selectbox(
        "Kitchen type",
        options=kitchen_type_options,
        index=2,
        key="kitchen_type",
    )

with col_k2:
    heating_options = [
        "Not specified",
        "gas",
        "electric",
        "heat pump",
        "oil",
    ]
    st.selectbox(
        "Type of heating",
        options=heating_options,
        index=1,
        key="type_of_heating",
    )

    glazing_options = [
        "Not specified",
        "single",
        "double",
        "triple",
    ]
    st.selectbox(
        "Type of glazing",
        options=glazing_options,
        index=2,
        key="type_of_glazing",
    )

# --- Section 6: Prediction ---
# --- Action buttons (below all inputs) ---
st.markdown("---")
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    predict_clicked = st.button("🔮 Predict price", type="primary")

with col_btn2:
    random_clicked = st.button("🎲 Load random Belgian example")

# Handle random-click: set flag and rerun so widgets use new state safely
if random_clicked:
    st.session_state["load_random_once"] = True
    st.rerun()

# Handle prediction-click
if predict_clicked:
    try:
        payload = build_payload_from_inputs()
        response = call_api(payload)

        # Clear old error, show new result
        error_placeholder.empty()
        with result_placeholder:
            st.success("Prediction received successfully ✅")
            st.metric("Predicted price (EUR)", f"{response.prediction:,.0f}")
            st.metric("Price per m² (EUR)", f"{response.price_per_m2:,.0f}")

            st.caption("Raw API response:")
            st.json(response.dict())

    except Exception as exc:
        result_placeholder.empty()
        error_placeholder.error(
            f"Could not reach the API. Please try again.\n\nDetails: {exc}"
        )

if predict_clicked:
    # Basic client-side validation before calling API
    missing_fields = []
    if not st.session_state["property_type"]:
        missing_fields.append("property_type")
    if not st.session_state["province"]:
        missing_fields.append("province")
    if not st.session_state["postcode"]:
        missing_fields.append("postcode")
    if not st.session_state["locality"]:
        missing_fields.append("locality")
    if st.session_state["livable_surface"] <= 0:
        missing_fields.append("livable_surface (> 0)")

    if missing_fields:
        error_placeholder.error(
            f"Missing or invalid required fields: {', '.join(missing_fields)}"
        )
    else:
        payload = build_payload_from_inputs()

        with st.spinner("Contacting prediction API..."):
            try:
                # Slightly higher timeout because Render can be slow to wake
                response = requests.post(API_URL, json=payload, timeout=20)
            except requests.exceptions.RequestException as exc:
                error_placeholder.error(
                    "Could not reach the API. Please try again later.\n\n"
                    f"Details: {exc}"
                )
            else:
                if response.status_code != 200:
                    try:
                        detail = response.json()
                    except Exception:
                        detail = response.text
                    error_placeholder.error(
                        f"API returned an error "
                        f"(status {response.status_code}):\n\n{detail}"
                    )
                else:
                    data = response.json()
                    prediction = data.get("prediction")
                    price_per_m2 = data.get("price_per_m2")

                    error_placeholder.empty()
                    result_placeholder.success("Prediction received successfully ✅")

                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.metric(
                            "Predicted price (EUR)",
                            f"{prediction:,.0f}" if prediction is not None else "N/A",
                        )
                    with col_res2:
                        st.metric(
                            "Price per m² (EUR)",
                            f"{price_per_m2:,.0f}"
                            if price_per_m2 is not None
                            else "N/A",
                        )

                    with st.expander("Raw API response"):
                        st.json(data)

st.markdown(
    """
<hr style="margin-top:2.5rem;margin-bottom:0.75rem;">

<div style="display:flex;align-items:center;gap:0.75rem;opacity:0.88;">
  <div style="
      width:34px;height:34px;border-radius:50%;
      background:linear-gradient(135deg,#4F46E5,#EC4899);
      display:flex;align-items:center;justify-content:center;
      color:white;font-weight:700;font-size:0.9rem;
  ">
    B
  </div>
  <div style="font-size:0.86rem;">
    Made by <strong>Pierrick Van Hoecke</strong> – BeCode AI &amp; Data Science student.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

