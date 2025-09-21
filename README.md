# **RouterWise — ML-Powered Logistics Optimization for Art Handling**    
![Ray Serve](https://img.shields.io/badge/Ray_Serve-00AEEF?style=for-the-badge&logo=ray&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![MLflow](https://img.shields.io/badge/MLflow-FF4F00?style=for-the-badge&logo=mlflow&logoColor=white) ![BentoML](https://img.shields.io/badge/BentoML-FF6F61?style=for-the-badge&logo=bentoml&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white) ![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

*"Art logistics is not just about moving objects — it's about preserving legacy. RouterWise predicts optimal shipment paths, anticipates risks, and ensures precision in handling priceless artworks. Built for institutions that value both efficiency and integrity."*

---

## 🎯 Goal : Designed for high-value and highly constrained logistics workflows

- Predictive routing for fragile, high-value shipments  
- Risk-aware logistics decisions based on historical and real-time data  
- Modular backend for scalable deployment across art institutions and logistics partners  

---

## 🧠 Stack Used

- **Ray Serve**: distributed model serving → horizontal scalability without overhead  
- **FastAPI**: async-ready API layer → minimal latency, high throughput  
- **MLflow**: model lifecycle management → reproducibility, traceability  
- **BentoML**: fallback deployment → resilience in production  
- **Prometheus + Grafana**: telemetry and alerting → operational visibility  
- **Jenkins CI/CD**: automated build and deploy → zero-friction integration

  💡 Each tool was selected for **robustness, scalability, and maintainability**, not for decoration.

---

## ⚙️ Architecture
![Mlflow & BentoML](./statics/api.png)

---

## 📖 Backend Narrative

*"Shipment data is ingested and preprocessed using robust encoding strategies. Predictive models are trained and versioned via MLflow, then served through Ray Serve with BentoML fallback. FastAPI exposes endpoints for route scoring, risk estimation, and shipment classification. Monitoring is handled via Prometheus/Grafana, with CI/CD orchestrated by Jenkins. Retraining pipelines are modular and Airflow-compatible."*

---

## 💻 API Demonstration

![API Predictiver](./statics/postman.png)

---

## 📊 Monitoring
*"Real-time monitoring: API latency and uptime via Prometheus, request and error counts, drift detection, and data quality checks on incoming data streams."*

[![Dashboard Preview](./statics/grafana_preview.png)](https://drive.google.com/file/d/1uD0oQKDrmADOqS0NHQR6PEfOGW2Jhqwu/view?usp=drive_link)

---

## 📊 Operational Impact

- **97% accuracy** in route risk classification  
- **<100ms latency** per prediction under load  
- **Auto-fallback** to best-performing model in case of failure  
- **Live monitoring** of API health, model drift, and request volume  

---

## 🚀 Roadmap

- **Integration** of **real-time GPS signals** for dynamic rerouting  
- **Multi-agent simulation** for route stress testing  
- **Federated learning** across logistics partners  
- **Contractual risk scoring** based on shipment metadata  
- **Explainable AI** modules for compliance and transparency  

---

## 🏁 Final Note

*"RouterWise shows how a backend can be production-ready while staying modular and strategic. The code is here, the architecture is solid — how far you go next is up to you."*

---

👤 **Abdias Arsène**  
*Sr. AI Consultant — Architect of scalable intelligence* 🧠
