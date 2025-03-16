from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import signal
import sys

STORAGE_DIR = "storage"
DATA_FILE = os.path.join(STORAGE_DIR, "data.json")
messages_store = {}


class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        self.store_message(data_dict)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            self.show_messages()
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def store_message(self, data_dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        messages_store[timestamp] = data_dict

    def show_messages(self):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("messages_template.html")

        html_content = template.render(
            messages=messages_store,
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def load_messages_from_disk():
    global messages_store
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            messages_store = json.load(file)


def save_messages_to_disk():
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(messages_store, file, indent=2, ensure_ascii=False)


def signal_handler(sig, frame):
    save_messages_to_disk()
    sys.exit(0)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    load_messages_from_disk()
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        save_messages_to_disk()


if __name__ == "__main__":
    run()
