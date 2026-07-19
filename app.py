"""
TimeBoard Time Service (TBTS)

A lightweight HTTP time service designed for legacy Palm OS devices.

Author: Emanuel Romano
API: v1
License: MIT
"""

from datetime import datetime, timezone, UTC
from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

from config import (
    HOST,
    PORT,
    SERVICE_NAME,
    SERVICE_SHORT_NAME,
    SERVICE_VERSION,
    API_VERSION,
    SERVICE_DESCRIPTION,
    PROJECT_URL,
)

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1
)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)

limiter.init_app(app)


# ---------------------------------------------------------
# API v1 response builders
# ---------------------------------------------------------

def build_v1_utc_response(now):

    return {
        "utc_datetime": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "unixtime": int(now.timestamp())
    }


# ---------------------------------------------------------
# Customize HTTP headers
# ---------------------------------------------------------

@app.after_request
def customize_headers(response):

    # Hide Werkzeug/Python version
    response.headers["Server"] = f"{SERVICE_SHORT_NAME}/{SERVICE_VERSION}"
    response.headers["Cache-Control"] = "no-store"

    return response


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.route("/")
def index():
    current_utc = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    return render_template(
        "index.html",
        service_name=SERVICE_NAME,
        version=SERVICE_VERSION,
        description=SERVICE_DESCRIPTION,
        api_version=API_VERSION,
        project_url=PROJECT_URL,
        current_utc=current_utc
    )


# ---------------------------------------------------------
# API information
# ---------------------------------------------------------

@app.route("/api")
@limiter.limit("10 per minute")
def api():

    return jsonify({
        "latest": API_VERSION,
        "health": "/api/health",
        "versions": {
        "v1": {
            "utc": "/api/v1/utc"
            }
        }
    })


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.route("/api/health")
@limiter.limit("10 per minute")
def health():

    return jsonify({
        "status": "ok",
        "service": SERVICE_SHORT_NAME,
        "version": SERVICE_VERSION,
        "utc_datetime": datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
    })


# ---------------------------------------------------------
# API v1 - UTC time
# ---------------------------------------------------------

@app.route("/api/v1/utc")
@limiter.limit("20 per minute")
def api_v1_utc():

    now = datetime.now(timezone.utc)

    return jsonify(build_v1_utc_response(now))


# ---------------------------------------------------------
# ERROR Handler - Error 429
# ---------------------------------------------------------

@app.errorhandler(429)
def ratelimit_handler(e):

    return jsonify({
        "error": "rate_limit_exceeded",
        "message": "Too many requests.",
        "status": 429
    }), 429


# ---------------------------------------------------------
# DEBUG ENDPOINT
# ---------------------------------------------------------

# @app.route("/debug/ip")
# def debug_ip():

#     return jsonify({
#         "remote_addr": request.remote_addr,
#         "x_real_ip": request.headers.get("X-Real-IP"),
#         "x_forwarded_for": request.headers.get("X-Forwarded-For")
#     })


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)