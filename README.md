# Lugx Gaming Microservices Deployment Runbook

This project contains a set of containerized microservices for a fictional gaming platform: `frontend`, `game-service`, `order-service`, and `analytics-service`. These services are built with Flask and deployed on a Kubernetes cluster using Minikube. The pipeline is automated using GitHub Actions and includes monitoring with Prometheus and Grafana.

---

## Prerequisites

Before starting, ensure the following are installed and set up on your machine:

| Tool           | Purpose                                |
| -------------- | -------------------------------------- |
| Docker Desktop | Build and run container images locally |
| Minikube       | Local Kubernetes cluster               |
| Kubectl        | Kubernetes command-line tool           |
| Python 3       | Running services and test scripts      |
| Helm           | For installing Prometheus & Grafana    |
| AWS QuickSight | Data visualization for analytics       |
| ClickHouse     | Storing analytics data                 |
| GitHub Actions | CI/CD automation                       |


> Ensure Docker and Minikube are correctly configured on your system.

---

##  Setup Steps

### 1. Clone the Repository

```bash
https://github.com/seyed-ruzaik/lugx-gaming.git
```

### 2. Start Minikube (Docker driver)

####  On Windows (PowerShell)
```bash
minikube start --driver=docker
```

####  On macOS/Linux
```bash
minikube start --driver=docker
```

---

### 3. Create Secrets for Supabase and ClickHouse

#### On macOS/Linux:
```bash
kubectl create secret generic supabase-secret \
  --from-literal=SUPABASE_URL=https://your-project.supabase.co \
  --from-literal=SUPABASE_KEY=your-secret-key

kubectl create secret generic clickhouse-secret \
  --from-literal=CLICKHOUSE_HOST=your-host \
  --from-literal=CLICKHOUSE_USERNAME=your-username \
  --from-literal=CLICKHOUSE_PASSWORD=your-password
```

#### On Windows (PowerShell):
```powershell
kubectl create secret generic supabase-secret `
  --from-literal=SUPABASE_URL=https://your-project.supabase.co `
  --from-literal=SUPABASE_KEY=your-secret-key

kubectl create secret generic clickhouse-secret `
  --from-literal=CLICKHOUSE_HOST=your-host `
  --from-literal=CLICKHOUSE_USERNAME=your-username `
  --from-literal=CLICKHOUSE_PASSWORD=your-password
```

---

### 4. Build Docker Images inside Minikube

```bash
Mac: eval $(minikube docker-env)
Windows: & minikube -p minikube docker-env | Invoke-Expression

docker build -t lugx-frontend ./
docker build -t game-service ./lugx-microservices/game-service
docker build -t order-service ./lugx-microservices/order-service
docker build -t analytics-service ./lugx-microservices/analytics-service
```

---

### 5. Deploy to Kubernetes Cluster (Including Monitoring Setup)

Apply the following for each service:

#### Game Service:
```bash
kubectl apply -f ./lugx-microservices/game-service/k8s-game-service.yaml
kubectl apply -f ./lugx-microservices/game-service/game-service.yaml
kubectl apply -f ./lugx-microservices/game-service/game-servicemonitor.yaml
```

#### Order Service:
```bash
kubectl apply -f ./lugx-microservices/order-service/k8s-order-service.yaml
kubectl apply -f ./lugx-microservices/order-service/order-service.yaml
kubectl apply -f ./lugx-microservices/order-service/order-servicemonitor.yaml
```

#### Analytics Service:
```bash
kubectl apply -f ./lugx-microservices/analytics-service/k8s-analytics-service.yaml
kubectl apply -f ./lugx-microservices/analytics-service/analytics-service.yaml
kubectl apply -f ./lugx-microservices/analytics-service/analytics-servicemonitor.yaml
```

>  All `ServiceMonitor` YAMLs are required for Prometheus to scrape `/metrics` from services.

---


### 6. Port Forward Services for Local Access

Open separate terminals for each:

```bash
kubectl port-forward svc/lugx-service 8080:80
kubectl port-forward svc/order-service 5001:5001
kubectl port-forward svc/game-service 5000:5000
kubectl port-forward svc/analytics-service 5002:5002
```

---

### 7. Run Integration Tests (Locally)
Run integration tests:

```bash
python tests/integration_tests.py
```

Or test manually in browser/Postman:

- `GET http://localhost:5000/games`
- `POST http://localhost:5000/add-game` (with JSON payload)
- `GET http://localhost:5001/orders`
- `POST http://localhost:5001/place-order` (with JSON payload)
- `POST http://localhost:5002/track` (with JSON payload)

---


### 8. Set Up Monitoring Stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

---

### 9. Port-Forward Grafana UI

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```
Visit [http://localhost:3000](http://localhost:3000) (default login: admin/admin)

> Create dashboards using the metrics: `order_requests_total`, `get_orders_total`, `track_requests_total`, etc.

---

### 10. Visualize Analytics in AWS QuickSight

Since QuickSight doesn’t support ClickHouse directly:

1. ClickHouse is deployed and stores tracked events (`web_analytics` table).
2. We connect via MySQL-compatible port.
3. In QuickSight, create a new **MySQL connection** using:
   - Host: Your Host
   - Port: 3306 (ClickHouse MySQL port)
   - User: `default`
   - Password: `mypassword`
4. Build interactive dashboards on the table.

---
### 11. CI/CD Pipeline (GitHub Actions)

Every commit or push triggers:

- Docker builds for all services
- Deploys to Kubernetes (Rolling strategy used)
- Runs integration tests automatically

\*Script is located at: \**`.github/workflows/ci.yml`*

---

### 12. Updating a Microservice

If you change `app.py`, follow:

```bash
Windows: & minikube -p minikube docker-env | Invoke-Expression
Mac: eval $(minikube docker-env)

docker build -t lugx-frontend ./
docker build -t game-service ./lugx-microservices/game-service
docker build -t order-service ./lugx-microservices/order-service
docker build -t analytics-service ./lugx-microservices/analytics-service

kubectl rollout restart deployment game-service
kubectl rollout restart deployment order-service
kubectl rollout restart deployment analytics-service
kubectl rollout restart deployment lugx-frontend
 
kubectl delete pod -l app=game-service
kubectl delete pod -l app=order-service
kubectl delete pod -l app=analytics-service
kubectl delete pod -l app=lugx-frontend

```

---

### 13. Shutting Down and Cleanup

```bash
kubectl delete -f ./lugx-microservices/analytics-service/k8s-clickhouse.yaml
kubectl delete -f ./lugx-microservices/order-service/k8s-order-service.yaml
kubectl delete -f ./lugx-microservices/game-service/k8s-game-service.yaml
kubectl delete -f ./lugx-microservices/analytics-service/k8s-analytics-service.yaml
kubectl delete -f ./k8s-frontend.yaml
minikube stop
```

---

  **End of Runbook**

