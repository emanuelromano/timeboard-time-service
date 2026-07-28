# TimeBoard Time Service (TBTS)

![Python](https://img.shields.io/badge/Python-3.11.9-blue)
![Version](https://img.shields.io/badge/version-1.0.2-green)
![License](https://img.shields.io/github/license/emanuelromano/timeboard-time-service)

TimeBoard Time Service (TBTS) is a lightweight HTTP time service API designed specifically for the **TimeBoard** and **TBTS** applications for Palm OS.

It provides accurate Coordinated Universal Time (UTC) through a simple API designed to remain compatible with legacy Palm OS networking libraries that only support plain HTTP connections.

## Features

- Lightweight JSON responses
- HTTP/1.0 compatible
- Compatible with legacy clients using plain HTTP
- Versioned REST API
- Designed for TimeBoard and TBTS on Palm OS
- Environment-based configuration
- Self-hostable using Python and Flask
- Reverse proxy friendly (Nginx + Gunicorn)
- Configurable per-client rate limiting

## Design Goals

TBTS was designed with the following goals in mind:

- Provide a dedicated time service for TimeBoard and TBTS.
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

Create the local environment configuration from the included example:

### Windows

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Adjust the values in `.env` if needed.

Start the development server:

```bash
python app.py
```

The service will start using the configuration defined in `.env`, with defaults provided by `config.py`.

## Configuration

TBTS uses environment variables for runtime configuration. A `.env.example` file is included as a reference and can be copied to `.env` for local use.

The `.env` file is excluded from version control.

Example:

```env
TBTS_HOST=127.0.0.1
TBTS_PORT=8000
TBTS_RATE_LIMIT=10 per minute
```

## Technology Stack

- Python
- Flask
- Flask-Limiter
- python-dotenv
- Gunicorn
- Nginx

## License

This project is licensed under the MIT License.