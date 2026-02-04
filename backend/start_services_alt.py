#!/usr/bin/env python3
"""
Start Script for Todo Chatbot - Alternative Version

This script starts both the main API server and the MCP server with different ports to avoid conflicts.
"""

import subprocess
import sys
import threading
import time
import signal
import os
import psutil

def is_port_in_use(port):
    """Check if a port is currently in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    print(f"Killing process {proc.info['pid']} ({proc.info['name']}) using port {port}")
                    proc.kill()
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            continue
    return False

def start_main_api():
    """Start the main API server"""
    print("Starting main API server on port 8000...")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start main API server: {e}")

def start_mcp_server():
    """Start the MCP server"""
    print("Starting MCP server on port 8002...")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "mcp_server.server:app", "--host", "0.0.0.0", "--port", "8002"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start MCP server: {e}")

def main():
    print("Starting Todo Chatbot services...")

    # Check and kill any processes on ports 8000 and 8002 (instead of 8001 to avoid conflict)
    if kill_process_on_port(8000):
        time.sleep(1)  # Wait a bit for the port to be released

    if kill_process_on_port(8002):
        time.sleep(1)  # Wait a bit for the port to be released

    # Start MCP server in a separate thread
    mcp_thread = threading.Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()

    # Give the MCP server a moment to start
    time.sleep(2)

    # Start main API server in the main thread
    start_main_api()

if __name__ == "__main__":
    main()