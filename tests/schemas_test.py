from api.schema import LogistikData

example = {
    "Transportation_Cost": 1200.0,
    "Distance_Km": 1500.0,
    "State": "Florida",
    "Delivery_Urgency": "Express",
    "Urgency_Level": "High",
    "Client_Type": "Private_Collector",
    "Carrier_Type": "External",
    "Transportation_Method": "Truck",
    "Day_of_Week": "Monday",
    "Weather_Condition": "Clear"
}

try:
    data = LogistikData(**example)
    print("✅ Validé :", data)
except Exception as e:
    print("❌ Erreur :", e)
