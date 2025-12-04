from api.predict import predict_price
from api.schemas import PropertyFeatures, Location

loc = Location(
    province="Antwerpen",
    postcode=2000,
    locality="Antwerpen",
    region="Vlaanderen",
    country="Belgium",
)

features = PropertyFeatures(
    property_type="house",
    subtype_of_property="bungalow",
    location=loc,
    livable_surface=120,
    number_of_bedrooms=3,
)

print(predict_price(features))
