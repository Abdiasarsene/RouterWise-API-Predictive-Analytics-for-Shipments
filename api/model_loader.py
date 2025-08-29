# Importation des librairies nécessaires
import logging
import mlflow
import bentoml
from api.config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== FONCTIONS DE CHARGEMENT DU MODELE MLFLOW ======
def load_mlflow_model(path):
    try:
        logger.info("🚀 Connexion à MLflow")
        mlflow.set_tracking_uri(settings.tracking_uri)
        logger.info(f"🔗 MLflow Tracking URI utilisé : {settings.tracking_uri}")

        model = mlflow.pyfunc.load_model(path)
        if model is None:
            raise RuntimeError("⚠️ Échec MLflow.")
        
        logger.info("✅ Modèle chargé avec succès.")
        return model
    
    except Exception as e:
        logger.error(f"❌ Erreur via MLflow : {str(e)}")
        logger.exception("Stack trace : ")
        raise RuntimeError("⚠️ Échec via MLflow.") from e

# ====== FONCTION DE CHARGEMENT DU MODELE BENTOML ======
def load_bentoml_model(tag):
    try:
        logger.info("🔄 Chargement via BentoML...")
        model = bentoml.sklearn.load_model(tag)
        if model is None:
            raise RuntimeError("⚠️ Échec BentoML.")
        return model
    
    except Exception as e:
        logger.error(f"Erreur via BentoML : {str(e)}")
        logger.exception("Stack trace :")
        raise RuntimeError("⚠️ Échec via BentoML.") from e  
