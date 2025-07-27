# runner.py

# ===== Importation des librairies nécessaires =====
import mlflow
import logging
import time
import cProfile  # Ajout pour profiling
from trainer.config import settings
from trainer.data_loader import load_and_prepare_data
from trainer.preprocessing import get_preprocessor
from trainer.training import trainer_models
from trainer.predEvalSave import evaluate_and_predict
from trainer.monitoring import (
    log_data_overview,
    log_preprocessing_info,
    log_training_info,
    log_prediction_info
)

# ===== CONFIGURATION LOGGING =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# ===== PIPELINE PRINCIPAL =====
def main():
    try:
        # Initialisation de MLflow
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(settings.EXPERIMENT_NAME)

        with mlflow.start_run(run_name="training_pipeline"):

            # ===== ÉTAPE 1 : Chargement & encodage =====
            x_train, x_test, y_train, y_test, supply = load_and_prepare_data()
            log_data_overview(supply)

            # ===== ÉTAPE 2 : Prétraitement =====
            preprocessor = get_preprocessor(supply)
            num_cols = supply.select_dtypes(include=["int64", "float64"]).columns.tolist()
            cat_cols = supply.select_dtypes(include=["object"]).columns.tolist()
            log_preprocessing_info(num_cols, cat_cols)

            # ===== ÉTAPE 3 : Entraînement des modèles =====
            start_time = time.time()
            best_models = trainer_models(x_train, y_train, preprocessor)
            duration = time.time() - start_time
            for model_name in best_models:
                log_training_info(model_name, duration)

            # ===== ÉTAPE 4 : Prédiction et évaluation =====
            evaluation_results = evaluate_and_predict(best_models, x_test, y_test)

            # ===== ÉTAPE 5 : Logging & Sauvegarde =====
            log_prediction_info(evaluation_results)

            logger.info("🎉 Pipeline complet exécuté avec succès.")

    except Exception as e:
        logger.error(f"❌ Échec du pipeline : {str(e)}", exc_info=True)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    profiler.dump_stats("trainer_profile.prof")
