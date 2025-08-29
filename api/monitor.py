from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
import time
import logging

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== METRIQUES PROMETHEUS ======

# 1. Nombre total d'inférences du modèle
model_inference_count = Counter(
    "ml_model_inference_total",
    "Nombre total d'inférences réalisées par le modèle"
)

# 2. Nombre total de requêtes échouées
failed_request_count = Counter(
    "failed_requests_total",
    "Nombre total de requêtes ayant échoué"
)

# 3. Nombre total de requêtes réussies
successful_request_count = Counter(
    "successful_requests_total",
    "Nombre total de requêtes traitées avec succès"
)

# 4. Temps de réponse des requêtes
request_duration = Histogram(
    "request_duration_seconds",
    "Temps de traitement de chaque requête"
)

# ====== FONCTION D'AJOUT AU SERVEUR FASTAPI ======
def add_monitoring(app: FastAPI):
    try:
        instrumentator = Instrumentator()
        instrumentator.instrument(app).expose(app, endpoint="/metrics")
        logger.info("✅ Monitoring Prometheus activé sur /metrics")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ajout du monitoring Prometheus : {str(e)}")
        logger.exception("Stack trace : ")

# ====== MIDDLEWARE POUR LES METRIQUES MANUELLES ======
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        successful_request_count.inc()
        return response
    except Exception:
        failed_request_count.inc()
        raise
    finally:
        duration = time.time() - start
        request_duration.observe(duration)

# ====== A UTILISER DANS LE CODE DE PREDICTION POUR COMPTER ======
def increment_inference_count():
    try:
        model_inference_count.inc()
        logger.debug("📈 Incrémentation de model_inference_count")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'incrémentation du compteur d'inférence : {str(e)}")
        logger.exception("Stack trace : ")
