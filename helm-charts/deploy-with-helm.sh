#!/bin/bash

# Phase 4: Helm Chart Deployment Script

echo "🚀 Starting Phase 4: Helm Chart Deployment"

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
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Enable Docker in Minikube
eval $(minikube docker-env)

# Build Docker images
echo "📦 Building Docker images..."

# Build frontend image
echo "🏗️ Building frontend image..."
docker build -t todo-frontend:latest -f ../docker/frontend/Dockerfile ../.

# Build backend image
echo "🏗️ Building backend image..."
docker build -t todo-backend:latest -f ../docker/backend/Dockerfile ../.

# Build MCP server image
echo "🏗️ Building MCP server image..."
docker build -t todo-mcp-server:latest -f ../docker/mcp-server/Dockerfile ../.

echo "✅ Docker images built successfully"

# Create secrets
echo "🔒 Creating secrets..."
kubectl create secret generic database-secret \
  --from-literal=url="${DATABASE_URL:-postgresql://user:password@host:5432/db}" \
  --namespace=todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic auth-secret \
  --from-literal=secret="${BETTER_AUTH_SECRET:-your-super-secret-key-at-least-32-characters-long}" \
  --namespace=todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy using Helm
echo "🚢 Deploying applications using Helm..."

# Package the chart
helm package todo-app

# Install the chart
helm install todo-app-release ./todo-app-0.1.0.tgz \
  --namespace todo-app \
  --set frontend.image.repository=todo-frontend \
  --set frontend.image.tag=latest \
  --set backend.image.repository=todo-backend \
  --set backend.image.tag=latest \
  --set mcpServer.image.repository=todo-mcp-server \
  --set mcpServer.image.tag=latest \
  --set database.url="${DATABASE_URL:-postgresql://user:password@host:5432/db}"

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl rollout status deployment/todo-app-release-frontend -n todo-app
kubectl rollout status deployment/todo-app-release-backend -n todo-app
kubectl rollout status deployment/todo-app-release-mcp-server -n todo-app

# Check pods
echo "📋 Checking pod status..."
kubectl get pods -n todo-app

# Check services
echo "🌐 Checking service status..."
kubectl get services -n todo-app

# Expose services using NodePort
echo "🔌 Exposing services..."
kubectl expose deployment todo-app-release-frontend --type=NodePort --port=80 --target-port=3000 --name=frontend-service-nodeport --namespace=todo-app
kubectl expose deployment todo-app-release-backend --type=NodePort --port=8000 --target-port=8000 --name=backend-service-nodeport --namespace=todo-app
kubectl expose deployment todo-app-release-mcp-server --type=NodePort --port=8001 --target-port=8001 --name=mcp-server-service-nodeport --namespace=todo-app

# Get service URLs
echo "🔗 Getting service URLs..."
FRONTEND_URL=$(minikube service frontend-service-nodeport -n todo-app --url 2>/dev/null || echo "Not available")
BACKEND_URL=$(minikube service backend-service-nodeport -n todo-app --url 2>/dev/null || echo "Not available")
MCP_URL=$(minikube service mcp-server-service-nodeport -n todo-app --url 2>/dev/null || echo "Not available")

echo "Frontend URL: $FRONTEND_URL"
echo "Backend URL: $BACKEND_URL"
echo "MCP Server URL: $MCP_URL"

echo "✅ Phase 4: Helm Chart Deployment completed successfully!"
echo "📊 You can now access your applications via the URLs above"
echo "🔧 To access the Kubernetes dashboard: minikube dashboard"
echo "📈 To view deployed resources: kubectl get all -n todo-app"