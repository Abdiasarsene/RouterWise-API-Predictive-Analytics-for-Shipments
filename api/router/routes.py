# Importation des modules nécessaires
from fastapi import APIRouter, HTTPException
from api.schema.schema import LogistikData
from api.services.predictor import make_prediction
from api.events import get_model
import logging
from api.monitor import increment_inference_count

# ====== PARAMETRAGE & LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", redirect_slashes=False)

# ====== ROUTE DE VALIDATION ======
@router.post("/validate")
async def validate_logistik_input(data: LogistikData):
    try:
        logger.info("🔍 Validation des données d’entrée...")
        validated_data = data.model_dump(by_alias=True)
        logger.info("✅ Données valides.")
        return {
            "Validated Data": validated_data,
            "Message": "Données conformes au schéma LogistikData.",
            "Statut": "Success"
        }
    except Exception as e:
        logger.error(f"Validation Error: {str(e)}")
        logger.exception("Stack trace : ")
        raise HTTPException(status_code=400, detail=f"Erreur de validation : {str(e)}")

# ====== ROUTE DE PRÉDICTION ======
@router.post("/predict")
async def predict_logistic(data: LogistikData):
    try:
        # Prédiction + Affichage du message
        logger.info("🔄 Démarrage de la prédiction...")
        model, model_type = get_model()
        input_dict = data.dict(by_alias=True)
        predicted_class, message = make_prediction(model, model_type, input_dict)
        increment_inference_count()
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
        logger.exception("Stack trace : ")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")