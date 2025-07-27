from diagrams import Cluster, Diagram
from diagrams.programming.flowchart import Action
# from diagrams.onprem.mlflow import Mlflow
from diagrams.onprem.queue import Celery
from diagrams.onprem.client import Users
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server

with Diagram("ML System Architecture - Modular View", show=True, direction="LR"):

    # Entrée : les données
    user = Users("Client / Data")

    with Cluster("Training Phase"):
        data_source = Action("Raw Data Ingestion")
        preprocessing = Action("Preprocessing / Feature Engineering")
        training = Action("Model Training")
        # registry = Mlflow("Model Registry")
        data_source >> preprocessing >> training 

    with Cluster("API & Serving"):
        api = Server("FastAPI / Flask")
        inference = Action("Inference Logic")
        # model_storage = registry

        # api >> inference >> model_storage

    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        inference >> prometheus >> grafana

    with Cluster("Background Tasks"):
        celery = Celery("Celery Workers")
        beat = Celery("Celery Beat")
        retrain_task = Action("Scheduled Retraining")
        health_check = Action("Daily Health Check")
        beat >> [retrain_task, health_check] >> celery

    with Cluster("CI/CD/CT Pipeline"):
        github = Github("GitHub Actions")
        jenkins = Jenkins("Build/Test/Deploy")
        docker = Docker("Containerize API")
        github >> jenkins >> docker >> api

    # Connexions générales
    user >> api
    inference >> prometheus
    retrain_task >> training
