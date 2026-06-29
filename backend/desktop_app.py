import sys
import os
import threading
import time
import webbrowser
from pathlib import Path

import uvicorn
import webview

from app.main import app


def get_resource_path(relative_path):
    if getattr(sys, '_MEIPASS', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path


class Api:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window


def start_server(host="127.0.0.1", port=8000):
    config = uvicorn.Config(app, host=host, port=port, log_level="error")
    server = uvicorn.Server(config)
    server.run()


def wait_for_server(url, timeout=30):
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"

    server_thread = threading.Thread(target=start_server, args=(host, port), daemon=True)
    server_thread.start()

    if not wait_for_server(url):
        print("Server failed to start")
        sys.exit(1)

    api = Api()
    window = webview.create_window(
        "齿轮系统设计", url, width=1200, height=800, resizable=True)
    api.set_window(window)
    webview.start()


if __name__ == "__main__":
    main()
