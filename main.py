from fastapi import FastAPI
import logging

from api.config import settings
from api.events import register_startup_event
from api.router.routes import router as app_router
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

    logger.info("✅ FastAPI app created and configured.")
    return app

app = create_app()
