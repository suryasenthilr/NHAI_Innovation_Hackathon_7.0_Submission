import http.server
import socketserver
import threading
import subprocess
import time
import os
import socket

# Find a free port dynamically
def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

PORT = find_free_port()

class DelayedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files relative to workspace root
        return os.path.join("c:/bharatverify-antigravity", path.lstrip('/'))

    def log_message(self, format, *args):
        # Suppress request logs to keep terminal output clean
        pass

    def do_GET(self):
        if self.path == '/delay.js':
            print("[Server] Delay script requested. Sleeping 4 seconds for MathJax...")
            time.sleep(4)
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            self.wfile.write(b"console.log('Delayed load event fired!');")
            print("[Server] Delay script sent.")
            return
            
        if self.path in ['/technical_documentation_print.html', '/judges_presentation_print.html']:
            # Read original print HTML
            file_path = self.translate_path(self.path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Inject delay script right before </body> to hold load event
            injected_content = content.replace("</body>", '<script src="/delay.js"></script></body>')
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(injected_content.encode('utf-8'))
            return
            
        super().do_GET()

def run_server():
    handler = DelayedHTTPRequestHandler
    # Threading server to handle concurrent requests (e.g. stylesheet and delays)
    class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass
        
    with ThreadingHTTPServer(("", PORT), handler) as httpd:
        print(f"[Server] Started on port {PORT}")
        httpd.serve_forever()

# Start HTTP server in background thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Give server a second to bind
time.sleep(1)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1. Compile Spec PDF
print("[PDF] Printing Spec PDF (technical_documentation.pdf)...")
spec_url = f"http://localhost:{PORT}/technical_documentation_print.html"
spec_pdf = r"C:\bharatverify-antigravity\technical_documentation.pdf"

# Remove old PDF if exists
if os.path.exists(spec_pdf):
    os.remove(spec_pdf)

cmd_spec = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={spec_pdf}",
    "--include-background",
    spec_url
]
res1 = subprocess.run(cmd_spec, capture_output=True, text=True)
print("[PDF] Spec Print completed. Exit code:", res1.returncode)
print("[PDF] Spec PDF exists:", os.path.exists(spec_pdf))
if os.path.exists(spec_pdf):
    print("[PDF] Spec size:", os.path.getsize(spec_pdf), "bytes")

# 2. Compile Slides PDF
print("[PDF] Printing Slides PDF (judges_presentation.pdf)...")
slides_url = f"http://localhost:{PORT}/judges_presentation_print.html"
slides_pdf = r"C:\bharatverify-antigravity\judges_presentation.pdf"

# Remove old PDF if exists
if os.path.exists(slides_pdf):
    os.remove(slides_pdf)

cmd_slides = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={slides_pdf}",
    "--include-background",
    slides_url
]
res2 = subprocess.run(cmd_slides, capture_output=True, text=True)
print("[PDF] Slides Print completed. Exit code:", res2.returncode)
print("[PDF] Slides PDF exists:", os.path.exists(slides_pdf))
if os.path.exists(slides_pdf):
    print("[PDF] Slides size:", os.path.getsize(slides_pdf), "bytes")

print("[PDF] All prints completed successfully!")
