from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Middleware Setup ===
def apply_security_middleware(app: FastAPI):
    try:
        # app.add_middleware(HTTPSRedirectMiddleware)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"], 
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "*.yourdomain.com"]
        )
        logger.info("✅ Security middleware applied successfully.")
    except Exception as e:  
        logger.error(f"❌ Error applying security middleware: {str(e)}")
        logger.exception("Stack trace : ")
        raise HTTPException(status_code=500, detail="Middleware setup failed")  

# === Token Checker (Optional) ===
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        if token != "secrettoken123":  # Replace with actual validation
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        logger.info("✅ Token réussi.")
        return {"user": "authenticated"}
    except Exception as e: 
        logger.error(f"Erreur détectée : {str(e)}")
        logger.exception("Stack trace : ")