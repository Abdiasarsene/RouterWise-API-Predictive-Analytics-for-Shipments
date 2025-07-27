# Importation des librairies nécessaires
import logging
import mlflow
import bentoml
import traceback
from .config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== FONCTIONS DE CHARGEMENT DU MODELE MLFLOW ======
def load_mlflow_model(path):
    try:
        logger.info(f"🔄 Chargement MLflow depuis: {path}")
        mlflow.set_tracking_uri(settings.api_mlflow_tracking_uri)
        model = mlflow.pyfunc.load_model(path)
        if model is None:
            raise RuntimeError("⚠️ Échec MLflow.")
        return model
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle MLflow : {str(e)}")
        logger.debug("Traceback complet : \n%s", traceback.format_exc())
        raise RuntimeError("⚠️ Échec du chargement du modèle MLflow.") from e

# ====== FONCTION DE CHARGEMENT DU MODELE BENTOML ======
def load_bentoml_model(tag):
    try:
        logger.info("🔄 Chargement via BentoML...")
        model = bentoml.sklearn.load_model(tag)
        if model is None:
            raise RuntimeError("⚠️ Échec BentoML.")
        return model
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle BentoML : {str(e)}")
        logger.debug("Traceback complet : \n%s", traceback.format_exc())
        raise RuntimeError("⚠️ Échec du chargement du modèle BentoML.") from e  
