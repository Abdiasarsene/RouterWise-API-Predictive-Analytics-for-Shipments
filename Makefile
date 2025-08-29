.PHONY: mlflow bentoml train api radon format mypy bandit

# Directories
PROFILE_FILE=trainer_profile.prof
TRAINER_DIR=trainer
API_DIR=api

# ======= DEFAUL PIPELINE ======
default: format radon bandit mypy
	@echo "Default pipeline done"

# ====== LANCER MLFLOW ======
mlflow:
	@echo "Lancement de MLflow"
	@mlflow ui

# ====== ACCEDER AUX MODELS BENTOML ======
bentoml :
	@echo Acces a la base des modèles
	@python -m bentoml models list

# ====== LANCER PIPELINE AVEC PROFILING SNAKEVIZ======
train:
	@echo Execution du pipeline avec profiling SnakeViz...
	python runner.py

# ====== LANCER L'API ======
api:
	@echo "Lancement de l'API..."
	@uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1

# ====== LANCER L'ANALYSE CYCLOMATIQUE ======
radon: 
	@echo "Analyse cyclomatique"
	@radon mi $(TRAINER_DIR)/ $(API_DIR)/ -s

# ====== LINTING + FORMATAGE ======
format :
	@echo "Linting + Formatage"
	@ruff check . --fix

# ====== MYPY ======
mypy :
	@echo "Type Checking"
	@mypy --config mypy.ini

# ====== ANALYSE DU CODE ======
bandit:
	@echo "Analyse du code"
	@bandit -r $(TRAINER_DIR)/ $(API_DIR)/ -ll

# ====== LANCER PROMETHEUS =====
.PHONY: prometheus
prometheus : 
	@echo : "Lancement de Prometheus"
	@cd "C:\Program Files\Prometheus"