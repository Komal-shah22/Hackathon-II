# Phase 4: Local Kubernetes Deployment Specification

## Overview
This specification outlines the deployment of the Todo Chatbot application on a local Kubernetes cluster using Minikube and Helm Charts, with AI-assisted operations using kubectl-ai and Kagent.

## Objectives
- Deploy the Todo Chatbot application (Phase 2+3) on local Kubernetes
- Use Minikube for local Kubernetes cluster
- Create and use Helm Charts for deployment
- Implement AI-assisted Kubernetes operations with kubectl-ai and Kagent
- Ensure scalable, resilient, and maintainable deployment

## Architecture

### Current Application Architecture
```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              Kubernetes Cluster              │     │                 │
│  User Browser   │────▶│  ┌─────────────┐   ┌─────────────┐         │     │    Neon DB      │
│                 │     │  │   Frontend  │   │   Backend   │         │     │  (External)     │
│                 │     │  │   Service   │   │   Service   │         │     │                 │
│                 │     │  └─────────────┘   └─────────────┘         │     │  - tasks        │
│                 │     │        │                   │                │     │  - conversations│
│                 │     │        └───────────────────┼────────────────┘     │  - messages     │
│                 │     │                            │                      │                 │
│                 │     │                   ┌─────────────┐               │     │                 │
│                 │     │                   │ MCP Server  │               │────▶│                 │
│                 │     │                   │   Service   │               │     │                 │
│                 │     │                   └─────────────┘               │     │                 │
└─────────────────┘     └────────────────────────────────────────────────┘     └─────────────────┘
```

### Kubernetes Services
1. **Frontend Service**: Next.js application (Node.js)
2. **Backend API Service**: FastAPI application (Python)
3. **MCP Server Service**: Model Context Protocol server (Python)
4. **Database**: External Neon PostgreSQL
5. **Load Balancer/Ingress**: External access via Ingress Controller

## Deployment Strategy

### 1. Containerization
- Containerize frontend, backend, and MCP server using Docker
- Use multi-stage builds for optimized images
- Implement proper resource limits and requests

### 2. Kubernetes Manifests
- Create deployments for each service
- Define services for internal communication
- Configure ingress for external access
- Set up secrets for sensitive data
- Configure configmaps for configuration

### 3. Helm Charts
- Package deployment as Helm chart
- Parameterize configuration values
- Support for different environments
- Versioned releases

### 4. AI-Assisted Operations
- Use kubectl-ai for intelligent Kubernetes operations
- Implement Kagent for advanced operations
- Leverage AI for troubleshooting and optimization

## Technical Specifications

### Docker Images
- **Frontend**: Node.js 18-alpine with Next.js build
- **Backend**: Python 3.11-slim with FastAPI
- **MCP Server**: Python 3.11-slim with MCP server
- **Multi-stage builds**: Optimized for production

### Kubernetes Resources
- **Namespace**: `todo-app`
- **Deployments**: frontend, backend, mcp-server
- **Services**: ClusterIP for internal communication
- **Ingress**: External access with path-based routing
- **Secrets**: Database credentials, auth secrets
- **Resource Limits**: Memory and CPU requests/limits

### Helm Chart Structure
```
todo-app/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── secret.yaml
│   ├── configmap.yaml
│   └── _helpers.tpl
└── charts/
```

## Deployment Steps

### Pre-deployment
1. Set up Minikube cluster
2. Build Docker images
3. Create namespace
4. Configure secrets

### Deployment
1. Deploy MCP server first (dependency)
2. Deploy backend API
3. Deploy frontend
4. Configure ingress
5. Set up monitoring and logging

### Post-deployment
1. Verify deployments
2. Test service connectivity
3. Validate external access
4. Performance testing

## Environment Variables

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Authentication secret
- `NEXT_PUBLIC_API_URL`: API URL for frontend

### Kubernetes Secrets
- `database-secret`: Contains database connection details
- `auth-secret`: Contains authentication secrets

## Scaling Configuration

### Horizontal Pod Autoscaling
- CPU-based autoscaling for backend
- Memory-based alerts for all services
- Minimum/maximum replica configuration

### Resource Requirements
- **Frontend**: 128Mi memory, 100m CPU (requests); 256Mi memory, 200m CPU (limits)
- **Backend**: 256Mi memory, 200m CPU (requests); 512Mi memory, 500m CPU (limits)
- **MCP Server**: 128Mi memory, 100m CPU (requests); 256Mi memory, 200m CPU (limits)

## Monitoring and Logging
- Kubernetes native monitoring
- Container logs aggregation
- Health check endpoints
- Liveness and readiness probes

## Security Considerations
- Network policies (if needed)
- RBAC configuration
- Secret encryption
- Image scanning
- Least privilege principle

## AI-Assisted Operations

### kubectl-ai Commands
- `kubectl-ai "deploy the todo frontend with 2 replicas"`
- `kubectl-ai "scale the backend to handle more load"`
- `kubectl-ai "check why the pods are failing"`

### Kagent Operations
- `kagent "analyze the cluster health"`
- `kagent "optimize resource allocation"`

## Rollback Strategy
- Helm rollback for configuration changes
- Deployment rollback for application issues
- Database migration rollback procedures

## Success Criteria
- All services running and healthy
- External access working via ingress
- Internal service communication established
- Proper scaling configuration
- AI-assisted operations functional
- Performance benchmarks met
- Security compliance verified

## Next Steps
- Phase 5: Advanced Cloud Deployment with Kafka and Dapr
- Production deployment preparation
- Monitoring and alerting setup
- Backup and disaster recovery planning