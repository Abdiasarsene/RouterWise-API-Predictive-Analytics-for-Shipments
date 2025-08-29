# Importation des bibliothèques nécessaires
import logging
import traceback
from .config import settings
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

# ====== LOGGING ======
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ====== CREATION DES PIPELINES ======
def trainer_models(x_train, y_train, preprocessor):
    try :
        # Dictionnaires pour les modelès d'entraînement
        models = {
            "logistic": LogisticRegression(max_iter=1000, solver='liblinear', class_weight="balanced"),
            "random_forest": RandomForestClassifier(),
        }

        param_dist = {
            "logistic": {
                'classifier__C': [0.1, 1, 10],
                'classifier__penalty': ["l1", "l2"]
            },
            "random_forest": {
                'classifier__n_estimators': [100, 200, 300],
                'classifier__max_depth': [3, 6, 10],
                'classifier__min_samples_split': [2, 5, 10]
            },
        }

        best_models = {}
        cv = StratifiedKFold(n_splits=settings.N_SPLITE, shuffle=True, random_state=settings.RANDOM_STATE)

        for name, model in models.items():
            logger.info(f"\n🎓 Entraînement du modèle : {name}")

            # Pipeline avant l'entraînement
            pipe = Pipeline([
                ('preprocessing', preprocessor),
                ('classifier', model)
            ])

            # Application de RandomizedSearchCV pour l'optimisation des hyperparamètres
            search = RandomizedSearchCV(
                    pipe,
                    param_distributions=param_dist[name],
                    n_iter=10,
                    cv=cv,
                    n_jobs=-1,
                    scoring='accuracy',
                    random_state=settings.RANDOM_STATE
                )

                # Entraînement du modèle avec RandomizedSearchCV
            search.fit(x_train, y_train)
            best_models[name] = search.best_estimator_

                # Log des meilleurs hyperparams choisis par RandomizedSearch
            logger.info(f"✅ {name} entraîné et suivi avec MLflow.")

        logger.info("💡 Entraînements terminés ✅✅")
        return best_models
    except Exception as e:
        logger.error("Erreur durant l'entraînement : %s", str(e))
        logger.debug("Traceback complet : n%s", traceback.format_exc())
        raise e