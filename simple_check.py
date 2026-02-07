#!/usr/bin/env python
"""
Simple script to check backend configuration and diagnose the signup issue.
"""

import os
import requests
from urllib.parse import urlparse

def check_environment_variables():
    """Check if required environment variables are set"""
    print("Checking environment variables...")

    required_vars = ['JWT_SECRET']
    optional_vars = ['DATABASE_URL', 'DEV_JWT_SECRET']

    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)

    if missing_required:
        print(f"Missing required environment variables: {missing_required}")
    else:
        print("All required environment variables are set")

    for var in optional_vars:
        if os.getenv(var):
            print(f"Optional variable {var} is set")
        else:
            print(f"Optional variable {var} is not set")

    # Check JWT_SECRET length
    jwt_secret = os.getenv('JWT_SECRET', os.getenv('DEV_JWT_SECRET', ''))
    if jwt_secret and len(jwt_secret) < 32:
        print(f"Warning: JWT_SECRET should be at least 32 characters long (current: {len(jwt_secret)})")

def check_api_endpoint(url):
    """Test the signup endpoint"""
    print(f"\nTesting signup endpoint: {url}")
    try:
        # Try a basic OPTIONS request first to check if the endpoint exists
        response = requests.options(url)
        print(f"OPTIONS request: {response.status_code}")

        if response.status_code == 200:
            print("Endpoint exists and accepts requests")
        else:
            print(f"Endpoint returned status: {response.status_code}")

        # Try a sample signup request with minimal data to trigger the error
        sample_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }

        response = requests.post(url, json=sample_data)
        print(f"POST request: {response.status_code}")

        if response.status_code == 500:
            print("500 Internal Server Error - this is the issue we're seeing")
            if response.text:
                print(f"Response: {response.text}")
        elif response.status_code == 409:
            print("409 Conflict - indicates the endpoint is working (email already exists)")
        elif response.status_code == 422:
            print("422 Unprocessable Entity - indicates the endpoint is working (validation error)")
        else:
            print(f"Response: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        print("Cannot connect to the endpoint")
    except Exception as e:
        print(f"Error testing endpoint: {e}")

def main():
    print("Backend Configuration Checker")
    print("=" * 40)

    # Check environment variables
    check_environment_variables()

    # Check the deployed endpoint
    deployed_url = "https://komal-agentic-ai-developer-hackathon-2.hf.space/auth/signup"
    check_api_endpoint(deployed_url)

    print("\nRecommendations:")
    print("- Make sure JWT_SECRET environment variable is set in the deployment")
    print("- Verify DATABASE_URL is properly configured for production")
    print("- Check the deployment logs for detailed error messages")
    print("- Ensure the database is accessible in the deployment environment")

if __name__ == "__main__":
    main()