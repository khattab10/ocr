"""Minimal webhook receiver — stdlib only, no pip install needed.

    python server/receiver.py

Then insert a row in documents; the Oracle trigger POSTs here.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        print(f"\n>>> WEBHOOK on {self.path}")
        print(f"    body: {body}\n")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, *_):
        pass  # quiet; we print in do_POST instead


if __name__ == "__main__":
    port = 8000
    print(f"Listening on http://0.0.0.0:{port}/webhook")
    HTTPServer(("0.0.0.0", port), WebhookHandler).serve_forever()
