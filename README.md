# TimeBoard Time Service (TBTS)

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Version](https://img.shields.io/badge/version-1.0.1-green)
![License](https://img.shields.io/github/license/emanuelromano/timeboard-time-service)

TimeBoard Time Service (TBTS) is a lightweight HTTP API that provides accurate Coordinated Universal Time (UTC) for legacy Palm OS devices.

Originally created as the backend service for **TimeBoard**, it is designed to be simple, reliable, and compatible with legacy Palm OS networking libraries that only support plain HTTP connections.

## Features

- Lightweight JSON responses
- HTTP/1.0 compatible
- Compatible with legacy clients using plain HTTP
- Versioned REST API
- Designed for legacy Palm OS devices
- Self-hostable using Python and Flask
- Reverse proxy friendly (Nginx + Gunicorn)
- Per-client rate limiting

## Design Goals

TBTS was designed with the following goals in mind:

- Keep the API simple and lightweight.
- Maximize compatibility with legacy Palm OS devices.
- Minimize resource usage.
- Be easy to self-host and maintain.

## Endpoints

| Method | Endpoint | Description |
| :----: | -------- | ----------- |
| `GET` | `/` | HTML landing page with service information |
| `GET` | `/api` | API information and available versions |
| `GET` | `/api/health` | Health check endpoint |
| `GET` | `/api/v1/utc` | Returns the current UTC date and Unix timestamp |

## API Discovery

Retrieve general information about the service and discover available API versions.

### Request

```http
GET /api
```

### Example Response

```json
{
    "latest": "v1",
    "health": "/api/health",
    "versions": {
        "v1": {
            "utc": "/api/v1/utc"
        }
    }
}
```

## UTC Endpoint

Returns the current Coordinated Universal Time (UTC) in ISO 8601 format, along with its corresponding Unix timestamp.

### Request

```http
GET /api/v1/utc
```

### Example Response

```json
{
    "utc_datetime": "2026-07-14T16:45:00Z",
    "unixtime": 1784047500
}
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/emanuelromano/timeboard-time-service.git
cd timeboard-time-service
```

Create a virtual environment.

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
python app.py
```

The service will start using the host and port configured in `config.py`.

## Technology Stack

- Python
- Flask
- Flask-Limiter
- Gunicorn
- Nginx

## License

This project is licensed under the MIT License.