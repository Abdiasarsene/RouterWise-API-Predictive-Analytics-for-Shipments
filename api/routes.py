# Importation des modules nécessaires
from fastapi import APIRouter, HTTPException
from .schema import LogistikData
from .predictor import make_prediction
from .events import get_model
import logging
import traceback

# ====== PARAMETRAGE & LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# ====== ROUTE DE PRÉDICTION ======
@router.post("/v1/predict")
async def predict_logistic(data: LogistikData):
    try:
        # Prédiction + Affichage du message
        logger.info("🔄 Démarrage de la prédiction...")
        model, model_type = get_model()
        input_dict = data.dict(by_alias=True)
        predicted_class, message = make_prediction(model, model_type, input_dict)
        logger.info("📢 Prediction faite.")
        
        # Retourner la réponse formatée
        return {
            "Deliver Status": message,
            "Code": predicted_class,
            "Statut": "Success",
            "Model Used": model_type
        }

    except Exception as e:
        logger.error(f"Prediction Error: {str(e)}")
        logger.debug(f"Traceback: \n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")