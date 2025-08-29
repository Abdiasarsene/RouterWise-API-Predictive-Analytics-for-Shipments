# Importation des bibliothèques nécessaires
import logging
import traceback
from sklearn.metrics import accuracy_score, f1_score, recall_score

# ===== LOGGING ======
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ===== FONCTION D'ÉVALUATION DES PRÉDICTIONS ======
def evaluate_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    return accuracy, f1, recall

# ===== FONCTION DE PREDICTION ET D'ÉVALUATION ======
def evaluate_and_predict(best_models, x_test, y_test):
    try:
        # Dictionnaire
        result = {}
        
        for name, model in best_models.items():
            # Prédiction
            y_pred = model.predict(x_test)
            logger.info("🚀 Prédictions effectuées")

            # Évaluation des métriques
            accuracy, f1, recall = evaluate_metrics(y_test, y_pred)
            logger.info("✅ Évaluation terminée")
            
            result[name] = {
                "model": model,
                "metrics": {
                    "accuracy": accuracy,
                    "f1_score": f1,
                    "recall": recall
                }
}
        logger.info("📊 Prédiction + Evaluation terminées")

        return result
    except Exception as e:
        logger.error("Erreur lors de l'évaluation : %s", str(e))
        logger.debug("Traceback complet : n%s", traceback.format_exc())
        raise e