import multiprocessing
import os

from dotenv import load_dotenv

load_dotenv()

bind = os.environ.get("BIND_WSGI", "0.0.0.0:5000")
workers = os.environ.get("WORKERS_WSGI", multiprocessing.cpu_count() * 2 + 1)
proc_name = "alejandria"
wsgi_app = "app:app"
timeout = os.environ.get("TIMEOUT_WSGI", 0)
