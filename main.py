from fastapi import FastAPI
from prometheus_client import REGISTRY
import logging

from api.config import settings
from api.events import register_startup_event
from api.routes import router as app_router
from api.monitor import add_monitoring, metrics_middleware
from api.secure import apply_security_middleware

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description
    )

    # Middleware Sécurité
    apply_security_middleware(app)

    # Monitoring (Prometheus)
    add_monitoring(app)
    app.middleware("http")(metrics_middleware)

    # Startup event : chargement modèle
    register_startup_event(app)

    # Routes app
    app.include_router(app_router)

    # Test de monitoring
    @app.get("/health", tags=["Health"])
    async def health_check():
        try:
            metric_names = [m.name for m in REGISTRY.collect()]
            assert "ml_model_inference_total" in metric_names
            return {"status": "ok", "metrics": "available"}
        except Exception:
            return {"status": "degraded", "metrics": "unavailable"}

    logger.info("✅ FastAPI app created and configured.")
    return app

app = create_app()
