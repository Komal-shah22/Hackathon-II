#!/usr/bin/env python3
"""
Test script to verify chatbot functionality
"""

import asyncio
import httpx
import json

async def test_chatbot():
    """
    Test the chatbot endpoint to verify it's working properly
    """
    print("Testing chatbot functionality...")

    # Assuming the backend is running on localhost:8000
    base_url = "http://localhost:8000"

    # Sample token - in real usage, you'd need a valid JWT token
    # This is just for testing purposes
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer fake-token-for-testing"
    }

    # Test data - this would normally come from an authenticated user
    user_id = "test-user-id"
    test_message = "Hello, how are you?"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{base_url}/api/{user_id}/chat",
                json={"message": test_message},
                headers=headers
            )

            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response data: {json.dumps(data, indent=2)}")
            else:
                print(f"Response error: {response.text}")

    except httpx.ConnectError:
        print("Could not connect to the backend server. Please make sure:")
        print("1. The main API server is running on port 8000")
        print("2. The MCP server is running on port 8001")
        print("3. Both servers are started using: python start_services.py")
    except Exception as e:
        print(f"Error testing chatbot: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_chatbot())