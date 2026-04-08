import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 8501
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    # Suppress verbose logging to keep terminal clean like Streamlit
    def log_message(self, format, *args):
        pass

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    print("\n  You can now view your FinTech LangGraph Dashboard in your browser.")
    print(f"\n  Local URL: http://localhost:{PORT}/dashboard.html")
    print("  (Press CTRL+C to quit)\n")
    
    # Start server in a background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a tiny bit and pop open the browser automatically!
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}/dashboard.html")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
