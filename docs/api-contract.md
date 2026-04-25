# API Contracts

## Base URL

```
http://localhost:8000
```

## Endpoints

### GET /health

System health check.

**Response 200:**
```json
{
  "status": "healthy",
  "database": "connected",
  "scheduler": "running",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /api/v1/sources

List all sources with freshness summary.

**Response 200:**
```json
[
  {
    "id": "uuid",
    "slug": "open-meteo",
    "name": "Open-Meteo Weather",
    "description": "Current weather data for Berlin",
    "api_base_url": "https://api.open-meteo.com",
    "schedule_interval_minutes": 30,
    "is_active": true,
    "freshness": {
      "last_success_at": "2024-01-15T10:00:00Z",
      "is_stale": false,
      "staleness_minutes": 15
    },
    "last_run_status": "success"
  }
]
```

### GET /api/v1/sources/{slug}

Source detail with recent runs and signals.

**Response 200:**
```json
{
  "source": { "..." },
  "recent_runs": [ "..." ],
  "recent_signals": [ "..." ],
  "quality_summary": {
    "total_checks": 12,
    "passed": 10,
    "warnings": 2,
    "failures": 0
  }
}
```

### GET /api/v1/runs

List recent runs. Supports `?source=slug&status=success&limit=50&offset=0`.

**Response 200:**
```json
{
  "items": [
    {
      "id": "uuid",
      "source_slug": "open-meteo",
      "source_name": "Open-Meteo Weather",
      "status": "success",
      "started_at": "2024-01-15T10:00:00Z",
      "duration_ms": 1250,
      "records_fetched": 3,
      "records_stored": 3
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

### GET /api/v1/freshness

Freshness status per source.

**Response 200:**
```json
[
  {
    "source_slug": "open-meteo",
    "source_name": "Open-Meteo Weather",
    "last_success_at": "2024-01-15T10:00:00Z",
    "last_attempt_at": "2024-01-15T10:00:00Z",
    "is_stale": false,
    "staleness_minutes": 15
  }
]
```

### GET /api/v1/quality

Quality checks with optional filters: `?source=slug&status=fail&limit=50`.

**Response 200:**
```json
{
  "items": [
    {
      "id": "uuid",
      "source_slug": "open-meteo",
      "check_name": "null_check",
      "check_status": "pass",
      "expected_value": "non-null",
      "actual_value": "23.5",
      "message": "All critical fields present",
      "checked_at": "2024-01-15T10:00:00Z"
    }
  ],
  "summary": {
    "total": 36,
    "passed": 32,
    "warnings": 4,
    "failures": 0
  }
}
```

### GET /api/v1/signals

Recent normalized signals. Supports `?source=slug&type=weather&limit=50`.

**Response 200:**
```json
{
  "items": [
    {
      "id": "uuid",
      "source_slug": "open-meteo",
      "signal_type": "weather",
      "signal_key": "temperature_celsius",
      "signal_value": 23.5,
      "signal_unit": "°C",
      "observed_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 500,
  "limit": 50,
  "offset": 0
}
```

### GET /api/v1/metrics/summary

System-wide metrics.

**Response 200:**
```json
{
  "total_sources": 3,
  "active_sources": 3,
  "total_runs": 150,
  "successful_runs": 142,
  "failed_runs": 8,
  "total_signals": 1250,
  "total_quality_checks": 450,
  "quality_pass_rate": 0.95,
  "sources_stale": 0,
  "last_activity_at": "2024-01-15T10:00:00Z"
}
```

### POST /api/v1/runs/trigger/{slug}

Manually trigger a connector run.

**Response 202:**
```json
{
  "run_id": "uuid",
  "source_slug": "open-meteo",
  "status": "running",
  "message": "Run triggered successfully"
}
```
