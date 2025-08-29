# Importation des librairies nécessaires
import asyncio
import logging
from fastapi import FastAPI

from api.model_loader import load_mlflow_model, load_bentoml_model
from api.config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PARAMETRAGE ======
model = None
model_type = None

# ====== FONCTIONS DE CHARGEMENT DES MODÈLES ======
def get_model():
    return model, model_type

def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 API Starting...")
        global model, model_type
        
        # Chargement du modèle MLflow
        try:
            logger.info("🔄 Chargement du model MLflow...")
            model = await asyncio.wait_for(asyncio.to_thread(load_mlflow_model, settings.mlflow_model), timeout=10.0)
            model_type = "MLflow"
            logger.info("✅ MLflow model loaded.")
        except Exception as e:
            logger.warning(f"❌ MLflow failed: {str(e)}")
            logger.exception("Stack trace :")
            
            # Chargement du modèle BentoML en fallback
            try:
                logger.info("🔄 Chargement du modèle BentoML en fallback...")
                model = load_bentoml_model(settings.bentoml_model)
                model_type = "BentoML"
                logger.info("✅ BentoML fallback succeeded.")
            except Exception as bentoml_error:
                logger.critical(f"❌ BentoML failed: {str(bentoml_error)}")
                logger.exception("Stack trace :")
                raise RuntimeError(f"All model loading failed: {e} / {bentoml_error}")