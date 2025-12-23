"""
Task Management System - Main Application Runner
Launches all services: Flask, FastAPI, Streamlit, and NiceGUI
"""
# python runr.py
import threading
import time
import sys
import subprocess

def print_banner():
    """Display application banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║           TASK MANAGEMENT SYSTEM - ALL SERVICES                    ║
    ║                                                                    ║
    ║  Comprehensive Python Application Integration:                    ║
    ║  • Flask      - Web Dashboard                                      ║
    ║  • FastAPI    - RESTful API                                        ║
    ║  • Streamlit  - Analytics Dashboard                                ║
    ║  • NiceGUI    - Desktop Interface                                  ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_flask():
    """Launch Flask application"""
    from flask_app import run_flask as flask_runner
    flask_runner()

def run_fastapi():
    """Launch FastAPI application"""
    from fastapi_app import run_fastapi as fastapi_runner
    fastapi_runner()

def run_streamlit():
    """Launch Streamlit application"""
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 
        'streamlit_app.py',
        '--server.port', '8501',
        '--server.headless', 'true',
        '--server.runOnSave', 'false',
        '--browser.gatherUsageStats', 'false'
    ])

def run_nicegui():
    """Launch NiceGUI application"""
    from nicegui_app import run_nicegui as nicegui_runner
    nicegui_runner()

def main():
    """Main launcher function"""
    print_banner()
    print("\n🚀 Starting all services...\n")
    
    # Start Flask in separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True, name="Flask-Thread")
    flask_thread.start()
    time.sleep(1)
    print("✅ Flask Dashboard:      http://localhost:5000")
    
    # Start FastAPI in separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True, name="FastAPI-Thread")
    fastapi_thread.start()
    time.sleep(1)
    print("✅ FastAPI:              http://localhost:8000")
    print("   📚 API Documentation:  http://localhost:8000/docs")
    print("   📖 ReDoc:              http://localhost:8000/redoc")
    
    # Start Streamlit in separate thread
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True, name="Streamlit-Thread")
    streamlit_thread.start()
    time.sleep(2)
    print("✅ Streamlit Analytics:  http://localhost:8501")
    
    # Small delay before starting NiceGUI
    time.sleep(1)
    print("✅ NiceGUI Interface:    http://localhost:8084")
    
    print("\n" + "="*70)
    print("🎉 ALL SERVICES ARE NOW RUNNING!")
    print("="*70)
    print("\n📋 Quick Guide:")
    print("   • Flask:     Visual dashboard with task cards and statistics")
    print("   • FastAPI:   RESTful API for programmatic access (check /docs)")
    print("   • Streamlit: Interactive analytics with filters and charts")
    print("   • NiceGUI:   Desktop-style GUI for task management")
    print("\n💡 All services share the same in-memory database")
    print("⚠️  Press Ctrl+C to stop all services\n")
    
    # Start NiceGUI (blocking call - keeps main thread alive)
    try:
        run_nicegui()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all services...")
        print("✅ All services stopped successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()