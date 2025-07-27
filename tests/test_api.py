import pytest
from httpx import AsyncClient
from main import app

# Exemple d'entrée valide basée sur ton schema LogistikData
valid_payload = {
    "Transportation_Cost": 1500,
    "Distance_Km": 2100,
    "State": "California",
    "Delivery_Urgency": "Critical",
    "Urgency_Level": "High",
    "Client_Type": "Gallery",
    "Carrier_Type": "Specialized",
    "Transportation_Method": "Airplane",
    "Day_of_Week": "Friday",
    "Weather_Condition": "Clear"
}

@pytest.mark.asyncio
async def test_predict_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/predict", json=valid_payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert "Deliver Status" in json_resp
    assert "Code" in json_resp
    assert json_resp["Statut"] == "Success"
    assert json_resp["Model Used"] in ["MLflow", "BentoML"]

@pytest.mark.asyncio
async def test_predict_invalid_payload():
    # Payload avec une valeur invalide (coût trop bas)
    invalid_payload = valid_payload.copy()
    invalid_payload["Transportation_Cost"] = 10  # en dessous du minimum ge=300

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/predict", json=invalid_payload)
    assert response.status_code == 422  # Validation error de Pydantic