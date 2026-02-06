#!/usr/bin/env python3
"""
Quick connectivity test to check if the backend server is running
"""
import subprocess
import sys
import threading
import time
import requests
import json

def start_backend_server():
    """Start the backend server in a separate thread"""
    def run_server():
        try:
            # Start the uvicorn server
            subprocess.run([
                sys.executable, "-m", "uvicorn",
                "main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"  # Enable auto-reload for development
            ], cwd=".", check=False)
        except Exception as e:
            print(f"Error starting server: {e}")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return server_thread

def test_connectivity():
    """Test if the backend server is accessible"""
    base_url = "http://localhost:8000"

    print("Checking backend server connectivity...")

    try:
        # Try to reach the root endpoint
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Root endpoint: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Server info: {data}")

            # Check if auth routes are available
            openapi_resp = requests.get(f"{base_url}/openapi.json", timeout=10)
            if openapi_resp.status_code == 200:
                schema = openapi_resp.json()
                auth_paths = [path for path in schema.get('paths', {}).keys() if '/auth' in path]
                print(f"Found auth routes: {auth_paths}")

                return True

    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible at http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing connectivity: {e}")
        return False

    return False

def main():
    print("Backend Connectivity Test")
    print("-" * 30)

    # Check if server is already running
    is_running = test_connectivity()

    if not is_running:
        print("\nThe server is not running. Would you like me to start it?")
        print("(Note: This will start the server in the background)")
        response = input("Start server? (y/n): ").lower().strip()

        if response in ['y', 'yes']:
            print("\nStarting backend server on port 8000...")
            server_thread = start_backend_server()

            print("Server started. Waiting for it to initialize...")
            time.sleep(5)  # Wait for server to start

            # Test connectivity again
            is_running = test_connectivity()

            if is_running:
                print("\n✅ Server is now running and accessible!")
                print("You can now run the signup tests.")
                print("\nPress Ctrl+C to stop the server when done testing.")

                try:
                    # Keep the server running
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nStopping server...")
                    return
            else:
                print("\n❌ Failed to start server or server is not accessible")
        else:
            print("Skipping server startup. Make sure your backend is running before testing.")
    else:
        print("✅ Server is already running and accessible!")

if __name__ == "__main__":
    main()