# TimeBoard Time Service (TBTS) API

This document describes the HTTP endpoints provided by the TimeBoard Time Service.

The API is intentionally lightweight and designed to be compatible with legacy Palm OS devices.

Base URL

```
http://<server>
```

---

# API Overview

| Endpoint | Description |
|----------|-------------|
| `/` | Service information |
| `/api` | API information |
| `/api/health` | Health check |
| `/api/v1/utc` | Current UTC date and time |

---

# GET /

Returns general information about the service.

Example request:

```http
GET /
```

Example response:

```json
{
    "service": "TimeBoard Time Service",
    "short_name": "TBTS",
    "version": "1.0.0",
    "status": "online",
    "description": "Lightweight HTTP time service for legacy Palm OS devices.",
    "documentation": "/api",
    "repository": "https://github.com/emanuelromano/timeboard-time-service"
}
```

---

# GET /api

Returns information about the available API versions.

Example request:

```http
GET /api
```

Example response:

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

---

# GET /api/health

Returns the service status.

This endpoint can be used by monitoring systems to verify that the service is available.

Example request:

```http
GET /api/health
```

Example response:

```json
{
    "status": "ok",
    "service": "TBTS",
    "version": "1.0.0",
    "utc_datetime": "2026-07-14T20:15:18Z"
}
```

---

# GET /api/v1/utc

Returns the current Coordinated Universal Time (UTC).

Example request:

```http
GET /api/v1/utc
```

Example response:

```json
{
    "utc_datetime": "2026-07-14T20:15:18Z",
    "unixtime": 1784060118
}
```

---

# Response Fields

## utc_datetime

Current UTC date and time.

Format:

```
YYYY-MM-DDTHH:MM:SSZ
```

Example:

```
2026-07-14T20:15:18Z
```

---

## unixtime

Unix timestamp expressed in seconds since January 1st, 1970 (UTC).

Example:

```
1784060118
```

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Request completed successfully |
| 404 | Resource not found |
| 500 | Internal server error |

---

# Compatibility

TBTS is intentionally implemented over plain HTTP to maximize compatibility with legacy Palm OS devices that cannot reliably communicate using modern HTTPS/TLS protocols.

---

# Versioning

The API uses URL versioning.

Current version:

```
v1
```

Future incompatible changes will be published under a new version (for example, `/api/v2/...`) while preserving compatibility with existing clients whenever possible.

---

# License

This project is released under the MIT License.

---

# Design Goals

The primary goal of TBTS is not to provide a full-featured time service, but to offer a simple, reliable and long-term stable HTTP API that can be consumed by legacy Palm OS devices.

The service intentionally avoids unnecessary dependencies, authentication mechanisms and modern web technologies that could reduce compatibility with older hardware.