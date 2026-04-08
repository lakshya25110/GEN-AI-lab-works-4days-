import http.server
import socketserver
import os
import webbrowser
import threading
import time

PORT = 8503

class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n--- Starting HITL Sub-System ---")
    print(f"Simulator Live at http://localhost:{PORT}/dashboard.html")
    print("Press CTRL+C to stop.")
    
    with socketserver.TCPServer(("", PORT), StaticHandler) as httpd:
        def open_browser():
            time.sleep(1)
            webbrowser.open(f"http://localhost:{PORT}/dashboard.html")
            
        threading.Thread(target=open_browser, daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")
