# Importation des librairies nécessaires
import logging
import traceback
import pandas as pd
from fastapi import HTTPException
from .monitor import increment_inference_count

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== MAPPING DES CLASSES ======
logistik_mapping = {
    0: "On Time",
    1: "Late"
}

# ====== Fonction dédiée au formatage du message ======
def format_message(predicted_class: int) -> str:
    label = logistik_mapping.get(predicted_class, "Unknown")
    return f"Your delivery status prediction is: {label}. Stay informed and plan accordingly!"

# ====== Fonction de prédiction ======
def make_prediction(model, model_type: str, input_dict: dict) -> tuple:
    try:
        df = pd.DataFrame([input_dict])
        if model_type in ["MLflow", "BentoML"]:
            prediction = model.predict(df)
            predicted_class = int(prediction[0])
            message = format_message(predicted_class)
            increment_inference_count()
            logger.info('🚀 Prédiction faite')
            return predicted_class, message
        
    except Exception as e:
        logger.error(f"Erreur de prédiction : {e}")
        logger.debug(f"Traceback : \n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Modèle non initialisé correctement")
