# run.py
"""
Startup script for the Watchmaker API
This script will:
1. Check environment setup
2. Setup initial data
3. Start the API server
"""
import subprocess
import sys
import os
from setup_database import setup_database

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting Watchmaker API setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Creating one with default settings...")
        with open('.env', 'w') as f:
            f.write("DATABASE_URL=postgresql://user:password@localhost/watchmaker_db\n")
            f.write("SECRET_KEY=your-secret-key-here\n")
            f.write("DEBUG=True\n")
        print("✅ Created .env file. Please update it with your database credentials.")
    
    # Setup initial data
    print("🔄 Setting up initial database data...")
    try:
        setup_database()
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        print("💡 Make sure PostgreSQL is running and your .env file has correct database credentials")
        sys.exit(1)
    
    # Start the API server
    print("🔄 Starting API server...")
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()