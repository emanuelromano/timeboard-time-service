"""
TimeBoard Time Service (TBTS)

Application configuration.
"""

import os

# ---------------------------------------------------------
# Network
# ---------------------------------------------------------

HOST = os.getenv("TBTS_HOST", "127.0.0.1")
PORT = int(os.getenv("TBTS_PORT", "8000"))

# ---------------------------------------------------------
# Service
# ---------------------------------------------------------

SERVICE_NAME = "TimeBoard Time Service"
SERVICE_SHORT_NAME = "TBTS"
SERVICE_VERSION = "1.0.0"
API_VERSION = "v1"

SERVICE_DESCRIPTION = (
    "Lightweight HTTP time service for legacy Palm OS devices."
)

# ---------------------------------------------------------
# Repository
# ---------------------------------------------------------

PROJECT_URL = "https://github.com/emanuelromano/timeboard-time-service"

LICENSE = "MIT"