"""
Phishing Detection System - One-Click Web Application Launcher
MCA Research Project

Starts the Flask backend API and opens the web application in your default browser.
"""

import os
import sys
import time
import webbrowser
import threading

import socket

def open_browser():
    """Opens default browser to the web app URL after server startup is complete."""
    url = "http://127.0.0.1:5000"
    # Wait until Flask server is actively listening on port 5000
    for _ in range(20):
        time.sleep(0.5)
        try:
            with socket.create_connection(("127.0.0.1", 5000), timeout=0.5):
                break
        except (OSError, ConnectionRefusedError):
            pass
    print(f"\n🌐 Opening web application in default browser: {url}\n")
    webbrowser.open(url)

def main():
    print("=" * 65)
    print("🚀 PHISHING DETECTION SYSTEM - WEB APPLICATION LAUNCHER")
    print("   MCA Research Project - Real-Time Machine Learning Classifier")
    print("=" * 65)

    MODEL_FILE = "random_forest_model.pkl"
    if not os.path.exists(MODEL_FILE):
        print(f"❌ Error: Model file '{MODEL_FILE}' missing!")
        print("Please run main.py to train and save the model before starting.")
        sys.exit(1)

    print("✅ Model file verified: 'random_forest_model.pkl'")
    print("✅ Starting Flask web server on http://127.0.0.1:5000...")
    print("   Press Ctrl+C in terminal to stop server.\n")

    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Import and run Flask app
    from app import app
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == "__main__":
    main()
