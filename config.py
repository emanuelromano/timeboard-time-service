"""
TimeBoard Time Service (TBTS)

Application configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------
# Load .env
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------
# Network
# ---------------------------------------------------------

HOST = os.getenv("TBTS_HOST", "127.0.0.1")
PORT = int(os.getenv("TBTS_PORT", "8000"))

# ---------------------------------------------------------
# Service
# ---------------------------------------------------------

SERVICE_NAME = os.getenv(
    "TBTS_SERVICE_NAME",
    "TimeBoard Time Service"
)

SERVICE_SHORT_NAME = os.getenv(
    "TBTS_SERVICE_SHORT_NAME",
    "TBTS"
)

SERVICE_VERSION = os.getenv(
    "TBTS_SERVICE_VERSION",
    "1.0.1"
)

API_VERSION = os.getenv(
    "TBTS_API_VERSION",
    "v1"
)

SERVICE_DESCRIPTION = os.getenv(
    "TBTS_SERVICE_DESCRIPTION",
    "Lightweight HTTP time service for legacy Palm OS devices."
)

# ---------------------------------------------------------
# Repository
# ---------------------------------------------------------

PROJECT_URL = os.getenv(
    "TBTS_PROJECT_URL",
    "https://github.com/emanuelromano/timeboard-time-service"
)

LICENSE = os.getenv(
    "TBTS_LICENSE",
    "MIT"
)