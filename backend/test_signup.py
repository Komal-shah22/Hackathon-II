#!/usr/bin/env python3
"""
Test script to verify the signup endpoint is working properly
"""
import asyncio
import httpx
import json
import random
import string

async def test_signup_endpoint():
    """Test the signup endpoint functionality"""

    # Base URL - adjust this when testing with the actual deployed backend
    base_url = "http://localhost:8000"  # Change this to your HuggingFace Space URL when deployed

    print("Testing signup endpoint functionality...")

    # Generate a random email for testing to avoid conflicts
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_email = f"testuser_{random_suffix}@example.com"
    test_password = "securepassword123"
    test_name = "Test User"

    print(f"Using test email: {test_email}")

    # Define the signup payload
    signup_payload = {
        "email": test_email,
        "password": test_password,
        "name": test_name
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("\n1. Testing POST /auth/signup with valid data...")

            # Test the signup endpoint
            response = await client.post(
                f"{base_url}/auth/signup",
                json=signup_payload,
                headers=headers
            )

            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")

            try:
                response_data = response.json()
                print(f"Response Body: {json.dumps(response_data, indent=2)}")

                if response.status_code == 201:
                    print("[v] SUCCESS: Signup completed successfully!")
                    print(f"  - User ID: {response_data['user']['id']}")
                    print(f"  - User Email: {response_data['user']['email']}")
                    print(f"  - User Name: {response_data['user'].get('name', 'N/A')}")
                    print(f"  - Token received (length: {len(response_data['token'])})")

                    # Test the returned token by accessing /auth/me
                    print("\n2. Testing /auth/me with the returned token...")
                    headers_with_auth = {
                        "Authorization": f"Bearer {response_data['token']}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }

                    me_response = await client.get(
                        f"{base_url}/auth/me",
                        headers=headers_with_auth
                    )

                    print(f"/auth/me Response Status: {me_response.status_code}")
                    if me_response.status_code == 200:
                        me_data = me_response.json()
                        print("[v] SUCCESS: Token authentication works!")
                        print(f"  - Retrieved user: {me_data['email']}")
                    else:
                        print(f"[x] FAILED: Token authentication failed - {me_response.status_code}")
                        if me_response.content:
                            print(f"  - Error: {me_response.text}")

                    return True, response_data

                elif response.status_code == 409:
                    print("[!] CONFLICT: Email already exists (this may be expected if test ran before)")
                    return False, None
                elif response.status_code == 400:
                    print(f"[x] VALIDATION ERROR: {response_data.get('detail', 'Unknown validation error')}")
                    return False, None
                else:
                    print(f"[x] UNEXPECTED STATUS: {response.status_code}")
                    print(f"  - Response: {response_data}")
                    return False, None

            except json.JSONDecodeError:
                print(f"[x] ERROR: Could not parse JSON response: {response.text}")
                return False, None

    except httpx.ConnectError:
        print(f"[x] ERROR: Cannot connect to {base_url}. Is the server running?")
        print("  - If testing locally, make sure to start the backend with: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        print("  - If testing remotely, check that the URL is correct")
        return False, None
    except httpx.TimeoutException:
        print(f"[x] ERROR: Request timed out after 30 seconds")
        return False, None
    except Exception as e:
        print(f"[x] ERROR: Unexpected error occurred: {str(e)}")
        return False, None

async def test_invalid_signups():
    """Test various invalid signup scenarios"""

    base_url = "http://localhost:8000"  # Change this to your HuggingFace Space URL when deployed

    print("\n3. Testing invalid signup scenarios...")

    invalid_cases = [
        {
            "name": "Missing email",
            "payload": {"password": "password123", "name": "Test User"},
            "expected_status": 422  # Validation error
        },
        {
            "name": "Invalid email format",
            "payload": {"email": "invalid-email", "password": "password123", "name": "Test User"},
            "expected_status": 400
        },
        {
            "name": "Short password",
            "payload": {"email": "test@example.com", "password": "123", "name": "Test User"},
            "expected_status": 400
        },
        {
            "name": "Empty password",
            "payload": {"email": "test@example.com", "password": "", "name": "Test User"},
            "expected_status": 400
        }
    ]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        for case in invalid_cases:
            print(f"  Testing: {case['name']}")
            try:
                response = await client.post(
                    f"{base_url}/auth/signup",
                    json=case['payload'],
                    headers=headers
                )

                print(f"    Status: {response.status_code} (Expected: {case['expected_status']})")

                if response.content:
                    try:
                        response_data = response.json()
                        print(f"    Response: {response_data.get('detail', 'N/A')}")
                    except:
                        print(f"    Raw response: {response.text[:200]}...")

            except Exception as e:
                print(f"    Error: {str(e)}")

async def main():
    """Main test function"""
    print("=" * 60)
    print("SIGNUP ENDPOINT TEST")
    print("=" * 60)

    # Test the signup endpoint
    success, signup_data = await test_signup_endpoint()

    # Test invalid cases regardless of signup success
    await test_invalid_signups()

    print("\n" + "=" * 60)
    if success:
        print("OVERALL RESULT: [v] SIGNUP ENDPOINT IS WORKING PROPERLY")
    else:
        print("OVERALL RESULT: [x] SIGNUP ENDPOINT NEEDS ATTENTION")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())