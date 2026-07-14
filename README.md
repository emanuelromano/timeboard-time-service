# TimeBoard Time Service (TBTS)

TimeBoard Time Service (TBTS) is a lightweight HTTP API that provides accurate Coordinated Universal Time (UTC) for legacy Palm OS devices.

Originally created as the backend for TimeBoard, it is designed to be simple, reliable and compatible with old Palm OS networking libraries that only support plain HTTP connections.

## Features

- Lightweight JSON responses
- HTTP/1.0 compatible
- No HTTPS required
- Versioned REST API
- Designed for legacy Palm OS devices
- Self-hostable using Python and Flask

## API

Current version:

GET /api/v1/utc

Example response:

```json
{
    "utc_datetime": "2026-07-14T16:45:00Z",
    "unixtime": 1784047500
}