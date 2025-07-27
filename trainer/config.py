# importations des librairies nécessaires
import os 
from dotenv import load_dotenv

# ====== INITIALISATION ======
load_dotenv()

# ====== PARAMETRAGE ======
class Settings:
    TARGET_COLUMN = "Delivery_Status"
    DATASET_PATH = os.getenv("TRAIN_DATASET_PATH")
    EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME")
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    N_SPLITE= 5

settings = Settings()