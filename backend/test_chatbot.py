import asyncio
import httpx
import json

async def test_chatbot():
    """
    Test script to verify the chatbot functionality with authentication
    """
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000", timeout=30.0) as client:

        # First, try to register a test user (or sign in if already exists)
        print("Creating or signing in test user...")

        # Try to sign in first, if fails then sign up
        signin_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        # Try sign in first
        signin_response = await client.post("/auth/signin", json=signin_data)
        auth_data = None

        if signin_response.status_code == 200:
            auth_data = signin_response.json()
            print("User signed in successfully")
        else:
            # If sign in fails, try to sign up
            signup_data = {
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }

            signup_response = await client.post("/auth/signup", json=signup_data)
            print(f"Signup status: {signup_response.status_code}")

            if signup_response.status_code == 201:
                auth_data = signup_response.json()
                print("User created successfully")
            elif signup_response.status_code == 409:
                # User already exists, try sign in again
                signin_response = await client.post("/auth/signin", json=signin_data)
                if signin_response.status_code == 200:
                    auth_data = signin_response.json()
                    print("User signed in successfully (after conflict)")

        if auth_data:
            token = auth_data["token"]
            user_id = auth_data["user"]["id"]

            print(f"User ID: {user_id}")
            print(f"Token: {token[:20]}...")  # Show first 20 chars of token

            # Set the token in headers for subsequent requests
            headers = {"Authorization": f"Bearer {token}"}

            # Test messages for the chatbot
            test_messages = [
                "Hello",
                "Add a task to buy groceries",
                "Show me my tasks",
                "Add another task to call mom",
                "Show me my tasks again"
            ]

            conversation_id = None

            for i, message in enumerate(test_messages):
                print(f"\n--- Test {i+1}: Sending message '{message}' ---")

                try:
                    # Send chat request with authentication
                    response = await client.post(
                        f"/api/{user_id}/chat",
                        json={
                            "message": message,
                            "conversation_id": conversation_id
                        },
                        headers=headers
                    )

                    print(f"Status Code: {response.status_code}")

                    if response.status_code == 200:
                        result = response.json()
                        print(f"Response: {result.get('response', 'No response text')}")

                        # Update conversation ID for subsequent messages
                        if 'conversation_id' in result and not conversation_id:
                            conversation_id = result['conversation_id']
                            print(f"Assigned conversation ID: {conversation_id}")

                        if 'tool_calls' in result and result['tool_calls']:
                            print(f"Tool calls made: {len(result['tool_calls'])}")
                    else:
                        print(f"Error: {response.text}")

                except httpx.RequestError as e:
                    print(f"Request error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
        else:
            print("Failed to authenticate user")

if __name__ == "__main__":
    print("Testing Chatbot API with authentication...")
    asyncio.run(test_chatbot())