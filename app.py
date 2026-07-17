"""
TimeBoard Time Service (TBTS)

A lightweight HTTP time service designed for legacy Palm OS devices.

Author: @coloraturip
API: v1
License: MIT
"""

import os
from flask import Flask, jsonify
from datetime import datetime, UTC
from flask import render_template

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


# ---------------------------------------------------------
# API v1 response builders
# ---------------------------------------------------------

def build_v1_utc_response(now):
    """Builds the UTC response for API v1."""

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

# @app.route("/")
# def index():
#     return jsonify({
#         "service": SERVICE_NAME,
#         "short_name": SERVICE_SHORT_NAME,
#         "version": SERVICE_VERSION,
#         "status": "online",
#         "description": SERVICE_DESCRIPTION,
#         "documentation": "/api",
#         "repository": PROJECT_URL
#     })

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
def api_v1_utc():

    now = datetime.now(timezone.utc)

    return jsonify(build_v1_utc_response(now))


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)