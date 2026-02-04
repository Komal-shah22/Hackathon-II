# Phase 4: Local Kubernetes Deployment

## Overview
Deployment of the Todo Chatbot application on local Kubernetes cluster using Minikube and Helm Charts with AI-assisted operations using kubectl-ai and Kagent.

## Tech Stack
- **Orchestration**: Kubernetes (Minikube)
- **Package Manager**: Helm Charts
- **Containerization**: Docker (with Gordon AI Agent)
- **AI DevOps**: kubectl-ai, Kagent
- **Application**: Phase 2+3 Todo Chatbot (Next.js + FastAPI + MCP Server)

## Features to Implement
- Containerize frontend and backend applications using Docker
- Create Kubernetes manifests for all services
- Deploy on local Minikube cluster
- Create Helm charts for deployment
- Use kubectl-ai and Kagent for AI-assisted Kubernetes operations
- Configure service discovery and networking
- Set up persistent storage for database
- Configure ingress for external access
- MCP server deployment alongside main API

## Architecture
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

## Services to Deploy
1. **Frontend Service**: Next.js application
2. **Backend API Service**: FastAPI application
3. **MCP Server Service**: Model Context Protocol server
4. **Database**: External Neon PostgreSQL
5. **Load Balancer/Ingress**: External access

## Directory Structure
```
phase-2/
├── docker/              # Docker configurations
│   ├── frontend/
│   │   └── Dockerfile
│   ├── backend/
│   │   └── Dockerfile
│   └── mcp-server/
│       └── Dockerfile
├── k8s/                 # Kubernetes manifests
│   ├── namespaces/
│   ├── configmaps/
│   ├── secrets/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── persistent-volumes/
├── helm-charts/         # Helm chart templates
│   └── todo-app/
│       ├── templates/
│       └── values.yaml
├── specs/004-k8s-deployment/ # Phase 4 specifications
└── README-phase4.md     # Phase 4 documentation
```

## Prerequisites
- Docker Desktop (with Gordon AI Agent enabled)
- Minikube
- kubectl
- Helm
- kubectl-ai (AI-assisted kubectl)
- Kagent (AI operations agent)

## Deployment Steps
1. Containerize frontend and backend applications
2. Set up Minikube cluster
3. Create Kubernetes secrets for environment variables
4. Deploy database (Neon - external)
5. Deploy MCP server service
6. Deploy backend services
7. Deploy frontend
8. Configure ingress and load balancing
9. Test deployment with AI-assisted tools
10. Optimize resources using Kagent