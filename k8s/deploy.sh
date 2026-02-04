#!/bin/bash

# Phase 4: Kubernetes Deployment Script

echo "🚀 Starting Phase 4: Kubernetes Deployment"

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed. Please install helm first."
    exit 1
fi

if ! command -v minikube &> /dev/null; then
    echo "❌ minikube is not installed. Please install minikube first."
    exit 1
fi

echo "✅ All prerequisites are installed"

# Start Minikube
echo "🐳 Starting Minikube..."
minikube start
minikube status

# Create namespace
echo "🏷️ Creating namespace..."
kubectl apply -f k8s/namespaces/todo-app-namespace.yaml

# Build Docker images
echo "📦 Building Docker images..."

# Enable Docker in Minikube
eval $(minikube docker-env)

# Build frontend image
echo "🏗️ Building frontend image..."
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile .

# Build backend image
echo "🏗️ Building backend image..."
docker build -t todo-backend:latest -f docker/backend/Dockerfile .

# Build MCP server image
echo "🏗️ Building MCP server image..."
docker build -t todo-mcp-server:latest -f docker/mcp-server/Dockerfile .

echo "✅ Docker images built successfully"

# Create secrets
echo "🔒 Creating secrets..."
kubectl create secret generic database-secret \
  --from-literal=url="$DATABASE_URL" \
  --namespace=todo-app

kubectl create secret generic auth-secret \
  --from-literal=secret="$BETTER_AUTH_SECRET" \
  --namespace=todo-app

# Deploy using kubectl
echo "📡 Deploying applications using kubectl..."
kubectl apply -f k8s/deployments/ -n todo-app
kubectl apply -f k8s/services/ -n todo-app

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl rollout status deployment/frontend -n todo-app
kubectl rollout status deployment/backend -n todo-app
kubectl rollout status deployment/mcp-server -n todo-app

# Check pods
echo "📋 Checking pod status..."
kubectl get pods -n todo-app

# Check services
echo "🌐 Checking service status..."
kubectl get services -n todo-app

# Expose services using NodePort or Ingress
echo "🔌 Exposing services..."
kubectl expose deployment frontend --type=NodePort --port=80 --target-port=3000 --name=frontend-service-nodeport --namespace=todo-app
kubectl expose deployment backend --type=NodePort --port=8000 --target-port=8000 --name=backend-service-nodeport --namespace=todo-app
kubectl expose deployment mcp-server --type=NodePort --port=8001 --target-port=8001 --name=mcp-server-service-nodeport --namespace=todo-app

# Get service URLs
echo "🔗 Getting service URLs..."
echo "Frontend URL: $(minikube service frontend-service-nodeport -n todo-app --url)"
echo "Backend URL: $(minikube service backend-service-nodeport -n todo-app --url)"
echo "MCP Server URL: $(minikube service mcp-server-service-nodeport -n todo-app --url)"

echo "✅ Phase 4: Kubernetes Deployment completed successfully!"
echo "📊 You can now access your applications via the URLs above"
echo "🔧 To access the Kubernetes dashboard: minikube dashboard"