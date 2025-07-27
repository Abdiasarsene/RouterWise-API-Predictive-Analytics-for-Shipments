# Utiliser une image Python légère
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements.txt
COPY api/requirements.txt ./

# Installer les dépendances avec cache pip activé pour accélérer les téléchargements
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y curl && apt-get autoremove -y && apt-get clean

# Copier le code de l’API dans le conteneur
COPY api/ ./api/

# Exposer le port d'écoute de l’API
EXPOSE 8000

# Lancer l’API FastAPI via uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
