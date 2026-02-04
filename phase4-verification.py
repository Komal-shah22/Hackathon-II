#!/usr/bin/env python3
"""
Phase 4 Verification Script
Verifies that all Phase 4 Kubernetes deployment files were created correctly
"""

import os
import yaml
from pathlib import Path

def verify_phase4_deployment():
    print("=" * 60)
    print("Phase 4: Local Kubernetes Deployment - Verification Report")
    print("=" * 60)

    # Expected files and directories
    expected_files = {
        # Documentation
        'README-phase4.md': 'Documentation',

        # Kubernetes manifests
        'k8s/namespaces/todo-app-namespace.yaml': 'Kubernetes Namespaces',
        'k8s/deployments/frontend-deployment.yaml': 'Kubernetes Deployments',
        'k8s/deployments/backend-deployment.yaml': 'Kubernetes Deployments',
        'k8s/deployments/mcp-server-deployment.yaml': 'Kubernetes Deployments',
        'k8s/services/frontend-service.yaml': 'Kubernetes Services',
        'k8s/services/backend-service.yaml': 'Kubernetes Services',
        'k8s/services/mcp-server-service.yaml': 'Kubernetes Services',
        'k8s/ingress/app-ingress.yaml': 'Kubernetes Ingress',
        'k8s/secrets/database-secret.yaml': 'Kubernetes Secrets',
        'k8s/secrets/auth-secret.yaml': 'Kubernetes Secrets',

        # Docker files
        'docker/frontend/Dockerfile': 'Docker Configuration',
        'docker/backend/Dockerfile': 'Docker Configuration',
        'docker/mcp-server/Dockerfile': 'Docker Configuration',

        # Helm chart
        'helm-charts/todo-app/Chart.yaml': 'Helm Chart',
        'helm-charts/todo-app/values.yaml': 'Helm Chart',
        'helm-charts/todo-app/templates/_helpers.tpl': 'Helm Templates',
        'helm-charts/todo-app/templates/frontend-deployment.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/backend-deployment.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/mcp-server-deployment.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/frontend-service.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/backend-service.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/mcp-server-service.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/auth-secret.yaml': 'Helm Templates',
        'helm-charts/todo-app/templates/namespace.yaml': 'Helm Templates',

        # Specs
        'specs/004-k8s-deployment/specification.md': 'Specifications',
        'specs/004-k8s-deployment/plan.md': 'Specifications',
        'specs/004-k8s-deployment/tasks.md': 'Specifications',

        # Scripts
        'k8s/deploy.sh': 'Deployment Scripts'
    }

    missing_files = []
    found_files = []

    for file_path, category in expected_files.items():
        if os.path.exists(file_path):
            found_files.append((file_path, category))
        else:
            missing_files.append((file_path, category))

    # Print results
    print(f"\n📁 Total Files Expected: {len(expected_files)}")
    print(f"✅ Files Found: {len(found_files)}")
    print(f"❌ Files Missing: {len(missing_files)}")

    if missing_files:
        print("\n❌ MISSING FILES:")
        for file_path, category in missing_files:
            print(f"  - {file_path} [{category}]")

    if found_files:
        print("\n✅ FOUND FILES BY CATEGORY:")
        categories = {}
        for file_path, category in found_files:
            if category not in categories:
                categories[category] = []
            categories[category].append(file_path)

        for category, files in categories.items():
            print(f"\n  {category}:")
            for file in files:
                print(f"    - {file}")

    # Verify YAML syntax for Kubernetes manifests
    print("\n🔍 YAML Syntax Verification:")
    yaml_files = [f for f, _ in found_files if f.endswith('.yaml')]
    yaml_errors = []

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
            print(f"  ✅ {yaml_file}")
        except Exception as e:
            print(f"  ❌ {yaml_file}: {str(e)}")
            yaml_errors.append((yaml_file, str(e)))

    print(f"\n📊 YAML Verification: {len(yaml_files) - len(yaml_errors)} OK, {len(yaml_errors)} ERRORS")

    # Summary
    print("\n" + "=" * 60)
    if len(missing_files) == 0 and len(yaml_errors) == 0:
        print("🎉 PHASE 4 VERIFICATION: COMPLETE SUCCESS!")
        print("All Kubernetes deployment files created successfully.")
        print("Ready for deployment to Minikube cluster.")
    else:
        print("⚠️  PHASE 4 VERIFICATION: ISSUES FOUND")
        print(f"- Missing files: {len(missing_files)}")
        print(f"- YAML syntax errors: {len(yaml_errors)}")
    print("=" * 60)

if __name__ == "__main__":
    verify_phase4_deployment()