#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading
import os
import sys

PORT = 8089

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server():
    global PORT
    for port in range(8089, 8100):
        try:
            with ReusableTCPServer(("", port), Handler) as httpd:
                PORT = port
                print(f"[+] Arcade Game Hub Sunucusu Başlatıldı: http://localhost:{PORT}/index.html")
                httpd.serve_forever()
                break
        except OSError:
            continue

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    
    import time
    time.sleep(0.5)
    url = f"http://localhost:{PORT}/index.html"
    print(f"[*] Tarayıcı açılıyor: {url}")
    webbrowser.open(url)
    
    try:
        input("\n[!] Sunucuyu kapatmak için ENTER tuşuna basın...\n")
    except KeyboardInterrupt:
        pass
    print("Sunucu kapatıldı.")
