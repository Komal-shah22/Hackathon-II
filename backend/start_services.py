#!/usr/bin/env python3
"""
Start Script for Todo Chatbot

This script starts both the main API server and the MCP server.
"""

import subprocess
import sys
import threading
import time
import signal
import os

def start_main_api():
    """Start the main API server"""
    print("Starting main API server...")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def start_mcp_server():
    """Start the MCP server"""
    print("Starting MCP server...")
    subprocess.run([sys.executable, "-m", "uvicorn", "mcp_server.server:app", "--host", "0.0.0.0", "--port", "8001"])

def main():
    print("Starting Todo Chatbot services...")

    # Start MCP server in a separate thread
    mcp_thread = threading.Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()

    # Give the MCP server a moment to start
    time.sleep(2)

    # Start main API server in the main thread
    start_main_api()

if __name__ == "__main__":
    main()