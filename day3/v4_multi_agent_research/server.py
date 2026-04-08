import http.server
import socketserver
import os
import webbrowser
import threading
import time
import json
import urllib.request
import urllib.error

PORT = 8504
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging

    def do_POST(self):
        # Native proxy endpoint to circumvent browser CORS restrictions and pure environments!
        if self.path == "/api/groq":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=post_data,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
            )
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                err = e.read()
                print(f"[API ERROR] {err}")
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(err)
            return

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n--- Starting Multi-Agent Pipeline Simulator ---")
    if not GROQ_API_KEY:
        print("\n[WARNING] GROQ_API_KEY is missing! Set via: $env:GROQ_API_KEY='your_key'")
    print(f"Loaded Native Localhost Proxy! Engine LLM: Groq.")
    print(f"Live at http://localhost:{PORT}/dashboard.html")
    print("Press CTRL+C to stop.")
    
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        def open_browser():
            time.sleep(1)
            webbrowser.open(f"http://localhost:{PORT}/dashboard.html")
            
        threading.Thread(target=open_browser, daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Server...")
