#!/usr/bin/env python3
"""
Test script to verify the authentication endpoints are properly working
"""
import asyncio
import httpx
import json

async def test_auth_endpoints():
    """Test the authentication endpoints"""

    # Replace with your actual backend URL when deployed
    base_url = "http://localhost:8000"  # Change this when testing on HuggingFace Spaces

    print("Testing authentication endpoints...")

    # Test the available routes
    try:
        # Test GET / to confirm API is running
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/")
            print(f"Root endpoint: {response.status_code} - {response.json()}")

            # Test /api-docs
            response = await client.get(f"{base_url}/api-docs")
            print(f"API Docs endpoint: {response.status_code}")

            # Test the auth routes by checking OPTIONS
            response = await client.options(f"{base_url}/auth/signup")
            print(f"OPTIONS /auth/signup: {response.status_code}")

            # Print the OpenAPI schema to see all routes
            response = await client.get(f"{base_url}/openapi.json")
            if response.status_code == 200:
                schema = response.json()
                auth_paths = {path: methods for path, methods in schema.get('paths', {}).items() if '/auth' in path}
                print(f"\nAuthentication routes found: {len(auth_paths)}")
                for path, methods in auth_paths.items():
                    print(f"  {path}: {list(methods.keys())}")

    except Exception as e:
        print(f"Error testing endpoints: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_auth_endpoints())