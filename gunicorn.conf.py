# Gunicorn configuration for TimeBoard Time Service

bind = "127.0.0.1:8000"

workers = 2

timeout = 30

accesslog = "-"

errorlog = "-"