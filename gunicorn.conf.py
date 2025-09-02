import os

workers = int(os.getenv('GUNICORN_WORKERS', 4))
worker_class = 'sync'
threads = int(os.getenv('GUNICORN_THREADS', 1))

bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"
timeout = 120

accesslog = '-'
errorlog = '-'
loglevel = 'info'