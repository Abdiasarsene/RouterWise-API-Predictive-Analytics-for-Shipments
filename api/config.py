# Importation des librairies nécessaires
import os
from dotenv import load_dotenv

# ====== INITIALISATION ======
load_dotenv()

# ====== PARAMETRAGE ======
class Settings:
    def __init__(self):
        self.model_name = os.getenv("MODEL_NAME")
        self.model_version = os.getenv("MODEL_VERSION")
        self.mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        self.mlflow_model = os.getenv("MLFLOW_MODEL")
        self.bentoml_model = os.getenv("BENTOML_MODEL")
        self.api_mlflow_tracking_uri = os.getenv("API_MLFLOW_TRACKING_URI")
        self.api_title = os.getenv("API_TITLE")
        self.api_version = os.getenv("API_VERSION")
        self.api_description = os.getenv("API_DESCRIPTION")

settings = Settings()