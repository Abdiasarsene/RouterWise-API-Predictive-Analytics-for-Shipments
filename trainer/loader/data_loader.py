# Importations des bibliothèques nécessaires
import logging
import traceback
import pandas as pd
from ..config import settings
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ====== LOGGING ======
logging.basicConfig(
    level= logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ====== IMPORTATION ET ENCODAGE DE LA LABEL ======
def load_and_prepare_data():
    try:
        # Chargement des données
        supply = pd.read_excel(settings.DATASET_PATH)
        logger.info("📥 Jeu de données importé✅")

        # Séparation des caractéristiques et de la cible
        x = supply.drop(columns=[settings.TARGET_COLUMN])  # Features
        y = LabelEncoder().fit_transform(supply[settings.TARGET_COLUMN])  # Target

        # Division des données en ensembles d'entraînement et de test
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, random_state=settings.RANDOM_STATE, test_size=settings.TEST_SIZE
        )
        logger.info("📊 Données divisées en train/test✅")

        return x_train, x_test, y_train, y_test, supply
    except Exception as e:
        logger.error("Une erreur rencontrée : %s", str(e))
        logger.debug("Traceback complet : n%s", traceback.format_exc())
        raise e
