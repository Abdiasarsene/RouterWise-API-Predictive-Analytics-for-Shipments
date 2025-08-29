import os
from dotenv import load_dotenv

# === Charger d'abord le fichier commun, toujours ===
load_dotenv(dotenv_path=".env")  # Agit pour tous les services

# === Ensuite, charger celui spécifique à l'environnement ===
def load_env():
    force = os.getenv("FORCE_ENV_MODE")
    if force == "docker":
        load_dotenv(dotenv_path="/app/.env.docker", override=True)
    elif force == "local":
        load_dotenv(dotenv_path=".env.local", override=True)
    else:
        if os.path.exists("/.dockerenv"):
            load_dotenv(dotenv_path="/app/.env.docker", override=True)
        else:
            load_dotenv(dotenv_path=".env.local", override=True)

load_env()

# === Configuration centralisée ===
class Settings:
    def __init__(self):
        self.env_mode = os.getenv("ENV_MODE","")
        self.tracking_uri = os.getenv("TRACKING_URI", "")
        self.model_name = os.getenv("MODEL_NAME", "")
        self.mlflow_model = os.getenv("LOADED_MODEL", "")
        self.bentoml_model = os.getenv("BENTOML_MODEL")
        self.api_title = os.getenv("API_TITLE","")
        self.api_version = os.getenv("API_VERSION", "")
        self.api_description = os.getenv("API_DESCRIPTION", "")

        # Log simple pour debug
        print(f"✅ ENV_MODE: {self.env_mode}")
        print(f"⚙️ API: {self.api_title} v{self.api_version}")

settings = Settings()