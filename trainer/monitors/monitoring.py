# Importation des librairies
import mlflow
import logging
import bentoml
import traceback 

# ====== LOGGING ======
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# === DATA LOADING METRICS ===
def log_data_overview(df):
    try:
        mlflow.log_metric("n_rows", df.shape[0])
        mlflow.log_metric("n_columns", df.shape[1])
        missing_total = df.isnull().sum().sum()
        mlflow.log_metric("missing_total", missing_total)
        missing_percent = (missing_total / df.size) * 100
        mlflow.log_metric("missing_percent", missing_percent)

        logger.info("✅ Aperçu des données suivi")
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement de l'aperçu des données : {str(e)}")
        logger.debug(f"Traceback complet : \n{traceback.format_exc()}")

# ====== OUTLIERS ======
def log_outliers(outlier_count):
    mlflow.log_metric("outlier_count", outlier_count)
    logger.info(f"[MLflow] Logged outlier count: {outlier_count}")


# === PREPROCESSING METRICS ===
def log_preprocessing_info(num_cols, cat_cols, text_cols=None):
    try:
        mlflow.log_metric("n_numeric_cols", len(num_cols))
        mlflow.log_metric("n_categorical_cols", len(cat_cols))
        if text_cols:
            mlflow.log_metric("n_text_cols", len(text_cols))
        logger.info("✅ Prétraitement des données suivi")
    except Exception as e:
        logger.error(f"Erreur durant l'observabilité : {str(e)}")
        logger.debug(f"Traceback complet : \n{traceback.format_exc()}")

# === TRAINING METRICS ===
def log_training_info(model_name, duration_seconds):
    try :
        mlflow.log_param("trained_model", model_name)
        mlflow.log_metric(f"{model_name}_train_duration", duration_seconds)
        logger.info("✅ Entrainement suivi")
    except Exception as e:
        logger.error(f" Erreur des métriques d'entraînement : {str(e)}")
        logger.debug(f"Traceback complet : \n{traceback.format_exc()})")

# === PREDICTION & EVALUATION ===
def log_prediction_info(evaluation_results):
    try:
        for model_name, content in evaluation_results.items():
            model = content["model"]
            metrics = content["metrics"]

            with mlflow.start_run(run_name=f"{model_name}_eval", nested=True):

                # MLflow Logging
                mlflow.log_param("model_type", model_name)
                mlflow.log_params(model.get_params())
                logger.info(f"✅ Modèle {model_name} suivi avec MLflow.")

                # Log Metrics
                for metric_name, value in metrics.items():
                    mlflow.log_metric(metric_name, value)
                logger.info("📊 Metriques suivi avec MLflow")
                
                # Backup MLFLOW
                mlflow.sklearn.log_model(model, model_name)
                logger.info(f"✅ Modèle {model_name} loggé avec MLflow.")

                # Register model to MLflow Registry
                model_uri = f"run:/{mlflow.active_run().info.run_id}/{model_name}"
                result = mlflow.register_model(model_uri=model_uri, name=model_name)

                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=model_name,
                    version=result.version,
                    stage="Production",
                    archive_existing_versions=True
                )
                logger.info(f"🚀 {model_name} promu en Production.")

            # Save with BentoML
            bentoml.sklearn.save_model(model_name, model)
        logger.info(f"💾 Modèle {model_name} sauvegardé avec BentoML.")
    except Exception as e:
        logger.error(f"Erreur des métriques PredEvalSave : {str(e)}")
        logger.debug(f"Traceback complet : \n{traceback.format_exc()}")
