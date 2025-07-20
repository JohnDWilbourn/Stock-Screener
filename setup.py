#!/usr/bin/env python3
"""
Setup script for Stock Screener application
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Set up the environment for the stock screener"""
    print("🚀 Setting up Stock Screener...")
    
    # Check if virtual environment exists
    venv_path = Path("stock_screener_env")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "stock_screener_env"], check=True)
    
    # Activate virtual environment and install packages
    if sys.platform.startswith("win"):
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_path = venv_path / "Scripts" / "pip"
    else:
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    print("Installing required packages...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists() or env_file.read_text().strip() == "POLYGON_API_KEY=your_polygon_api_key_here":
        print("\n⚠️  Please set up your Polygon.io API key:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and replace 'your_polygon_api_key_here' with your actual API key")
        print("3. You can get your API key from: https://polygon.io/dashboard")
        return False
    
    print("✅ Setup complete!")
    return True

def run_application():
    """Run the stock screener application"""
    if not setup_environment():
        return
    
    print("\n🌟 Starting Stock Screener...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    # Run the Flask application
    if sys.platform.startswith("win"):
        python_path = Path("stock_screener_env") / "Scripts" / "python"
    else:
        python_path = Path("stock_screener_env") / "bin" / "python"
    
    try:
        subprocess.run([str(python_path), "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Stock Screener stopped")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup-only":
        setup_environment()
    else:
        run_application()