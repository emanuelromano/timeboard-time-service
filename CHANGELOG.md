# Changelog

## [1.0.0] - 2026-07-14

### Added
- Initial public release.
- HTTP/1.0 compatible UTC endpoint.
- `/api/v1/utc` endpoint.
- Minimal JSON response.
- Designed for legacy Palm OS devices.


## [1.0.1] - 2026-07-17

### Added
- Added Flask-Limiter for per-client rate limiting.
- Added custom JSON response for HTTP 429 (Too Many Requests).
- Added ProxyFix support to correctly detect client IP addresses behind Nginx.

### Security
- Rate limiting is now applied per client IP instead of the reverse proxy address.

### Changed
- Improved production deployment behind Nginx.