import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

# Payload valide selon schema.py LogistikData (en respectant alias et enums)
valid_payload = {
    "Transportation_Cost": 1000.0,
    "Distance_Km": 2000.0,
    "State": "New York",
    "Delivery_Urgency": "Express",
    "Urgency_Level": "High",
    "Client_Type": "Private_Collector",
    "Carrier_Type": "External",
    "Transportation_Method": "Truck",
    "Day_of_Week": "Monday",
    "Weather_Condition": "Clear"
}

@pytest.mark.parametrize("payload", [
    valid_payload,
])
def test_validate_logistikdata_valid(payload):
    response = client.post("/v1/validate", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["Statut"] == "Success"
    assert "Validated Data" in json_data

@pytest.mark.parametrize("payload", [
    {},  # payload vide -> fail
    {"Transportation_Cost": 10},  # données incomplètes
    {**valid_payload, "Transportation_Cost": -1},  # hors contraintes
    {**valid_payload, "State": "UnknownState"},  # enum invalide
])
def test_validate_logistikdata_invalid(payload):
    response = client.post("/v1/validate", json=payload)
    assert response.status_code == 400

@pytest.mark.parametrize("payload", [
    valid_payload,
])
def test_predict_logistikdata_valid(payload):
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["Statut"] == "Success"
    assert "Deliver Status" in json_data
    assert "Code" in json_data
    assert json_data["Model Used"] in ["MLflow", "BentoML"]

@pytest.mark.parametrize("payload", [
    {},  # vide -> fail
    {"Transportation_Cost": 10},  # incomplet
])
def test_predict_logistikdata_invalid(payload):
    response = client.post("/v1/predict", json=payload)
    assert response.status_code in (400, 500)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    # Vérifie que la réponse contient la métrique d'inférence (nom approximatif)
    assert "ml_model_inference_total" in response.text
