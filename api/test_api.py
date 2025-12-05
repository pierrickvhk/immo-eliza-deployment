from fastapi.testclient import TestClient
from api.app import app
from api.schemas import PropertyRequest

# WHY: allow reviewers to see a real test interacting with the API
client = TestClient(app)

def test_health() -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "alive"

def test_predict_valid() -> None:
    payload = {
        "data": {
            "property_type": "house",
            "subtype_of_property": "bungalow",
            "location": {
                "province": "Antwerpen",
                "postcode": 2000,
                "locality": "Antwerpen"
            },
            "Number of bedrooms": 3,
            "Livable surface": 120,
            "Total land surface": 300
        }
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    assert "prediction" in res.json()
