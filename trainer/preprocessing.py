# Importation des bibliothèques nécessaires
import logging
import traceback
from .config import settings
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer, KNNImputer
from category_encoders import CatBoostEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler

# ====== LOGGING ======
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ====== PRETRAITEMENT DES DONNEES ======
def get_preprocessor(supply):
    try:
        # Séparation des types de données
        features = supply.drop(columns=[settings.TARGET_COLUMN])
        num_col = features.select_dtypes(include=["int64", "float64"]).columns.tolist()
        cat_col = features.select_dtypes(include=["object"]).columns.tolist()
        
        # Log les colonnes numériques et catégorielles
        logger.info(f"📊 Colonnes numériques: {num_col}")
        logger.info(f"📊 Colonnes catégorielles: {cat_col}")

        # Colonnes numériques
        num_transformer = Pipeline([
            ('imputer', KNNImputer(n_neighbors=3)),
            ('scaler', MinMaxScaler()),
        ])

        # Colonnes catégorielles
        cat_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', CatBoostEncoder())
        ])

        # ColumnTransformer
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', num_transformer, num_col),
                ('cat', cat_transformer, cat_col)
            ]
        )
        logger.info("✅ Préprocesseur créé avec succès")

        return preprocessor
    except Exception as e:
        logger.error("Erreur lors du prétraitement des données : %s", str(e))
        logger.debug("Traceback complet : n%s", traceback.format_exc())
        raise e