"""
Your Flask Application Entry Point

This module serves as the entry point for your Flask application.
It initializes and runs the Flask app, sets up routes, and handles other
configuration related to running the application.
"""
from app import create_app
import socket

# Get the current ip address to run the server with IP address
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Initializing application 
app = create_app()

if __name__ == "__main__":
    app.run(host=ip_address)
