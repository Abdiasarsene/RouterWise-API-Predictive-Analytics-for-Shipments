.PHONY: mlflow_server train run tests format type_check coverage check-all prometheus build run profile logs
PROFILE_FILE=trainer_profile.prof

# LANCEMENT DU PIPELINE D'ENTRAINEMENT + PREDICTION + SAUVERGADE + API
# ====== LANCER MLFLOW ======
mlflow_server:
	@echo "Lancement de MLflow"
	@mlflow ui

# ====== LANCER PIPELINE AVEC PROFILING SNAKEVIZ======
train:
	@echo Execution du pipeline avec profiling SnakeViz...
	python runner.py
	snakeviz $(PROFILE_FILE)

# ====== LANCER L'API ======
runlocal:
	@echo "Lancement de l'API..."
	@uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# ====== LANCER TOUS LES TESTS ======
tets: 
	@echo "Lancement de tous les tests..."
	pytest

# ====== LINTING + FORMATAGE ======
format :
	@echo "Linting + Formatage"
	@ruff check . --fix

# ====== MYPY ======
type_check :
	@echo "Type Checking"
	mypy .

# ====== COVERAGE ======
coverage:
	@echo "Coverage Report"
	coverage run -m pytest
	coverage report -m	
	coverage html

check-all : test format type_check coverage
	@echo "Tous les checks sont passes"

# ====== LANCER PROMETHEUS =====
.PHONY: prometheus
prometheus : 
	@echo : "Lancement de Prometheus"
	@cd "C:\Program Files\Prometheus"



# ====== DOCKER COMMANDES TRAINERS ======
build:
	docker build -t trainer-service ./trainer

run:
	docker run --rm trainer-service

profile:
	docker run --rm trainer-service viztracer runner.py

logs:
	docker logs trainer-service
