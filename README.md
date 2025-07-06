# Lugx Gaming Microservices Deployment Runbook

This project contains containerised microservices for a fictional gaming platform: `frontend`, `game-service`, `order-service`, and `analytics-service`. These services are built with Flask and deployed on **Google Kubernetes Engine (GKE)**. The pipeline is automated via **GitHub Actions**, and observability is set up with **Google Cloud Monitoring dashboards**.

---

## Prerequisites

| Tool | Purpose |
| ---- | ------- |
| Google Cloud Platform (GCP) | Hosting Kubernetes cluster and Artifact Registry |
| Docker | Building container images locally |
| Kubectl | Kubernetes CLI tool |
| Python 3 | Running test scripts |
| GitHub Actions | CI/CD automation |

Ensure you have a **GCP Project with billing enabled** and **service account JSON key** set as `GCP_SA_KEY` secret in GitHub Actions.

---

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/seyed-ruzaik/Lugx-GKE
```

---

### 2. Authenticate kubectl with cluster

Ensure your `kubectl` context points to your cluster:

```bash
gcloud container clusters get-credentials lugx-cluster --region asia-south1 --project lugx-gaming-465010
```
Verify

```bash
kubectl get nodes

```

### 3. Build Docker images with GCR tags

```bash
docker build -t gcr.io/lugx-gaming-465010/lugx-frontend ./ 
docker build -t gcr.io/lugx-gaming-465010/game-service ./lugx-microservices/game-service
docker build -t gcr.io/lugx-gaming-465010/order-service ./lugx-microservices/order-service
docker build -t gcr.io/lugx-gaming-465010/analytics-service ./lugx-microservices/analytics-service
```

---

### 4. Push images to Google Container Registry

*(Handled automatically by CI/CD, but can be done locally for testing)*

First, authenticate Docker to GCR:

```bash
gcloud auth configure-docker gcr.io
```
Then push:
```bash
docker push gcr.io/lugx-gaming-465010/lugx-frontend
docker push gcr.io/lugx-gaming-465010/game-service
docker push gcr.io/lugx-gaming-465010/order-service
docker push gcr.io/lugx-gaming-465010/analytics-service
```

---

### 5. Set up Secrets (ClickHouse and Supabase) and Apply deployments to GKE

```bash
kubectl create secret generic clickhouse-secret --from-literal=CLICKHOUSE_HOST=your-host   --from-literal=CLICKHOUSE_USERNAME=your-username   --from-literal=CLICKHOUSE_PASSWORD=your-password
```

```bash
kubectl create secret generic supabase-secret --from-literal=SUPABASE_URL=your-host --from-literal=SUPABASE_KEY=your-key
```


Apply Kubernetes manifests:

```bash
kubectl apply -f k8s-frontend.yaml
kubectl apply -f ./lugx-microservices/game-service/k8s-game-service.yaml
kubectl apply -f ./lugx-microservices/order-service/k8s-order-service.yaml
kubectl apply -f ./lugx-microservices/analytics-service/k8s-analytics-service.yaml
```


---

Apply ServiceMonitors
```bash
kubectl apply -f lugx-microservices/game-service/game-service-monitor.yaml
kubectl apply -f lugx-microservices/order-service/order-service-monitor.yaml
kubectl apply -f lugx-microservices/analytics-service/analytics-service-monitor.yaml
```

---

### 6. Observability

Monitoring is integrated using **Google Cloud Monitoring dashboards**:

- Pod CPU & Memory usage
- Pod restarts
- Uptime status
- (Optional) Network I/O metrics

---

### 7. CI/CD Pipeline

GitHub Actions pipeline (`.github/workflows/ci.yml`) is configured to:

1. **Build** Docker images
2. **Push** to Artifact Registry
3. **Deploy** updated manifests to GKE
4. **Run integration tests** against deployed services

Triggers on every push, PR, and nightly schedule.

---

### 8. Integration Tests

Run locally:

```bash
python tests/integration_tests.py
```

Or automatically via GitHub Actions.

---

### 9. Cleaning Up

```bash
gcloud container clusters delete lugx-cluster --region asia-south1
```

*(This will delete your GKE cluster to avoid billing charges.)*

---

## Notes

- **Load Balancer IPs** can be found via:

```bash
kubectl get services
```

- Ensure all pods are in `Running` state to validate successful deployment:

```bash
kubectl get pods
```

---

### 10. Updating a Microservice

1. Make code changes (e.g., `app.py`).
2. Commit and push to `main`.
3. CI/CD pipeline redeploys automatically.

---

**End of Runbook**
