# API contracts — SignalHub

**Base URL (local):** `http://localhost:8000`  
**Interactive:** `/docs` (Swagger) · `/redoc` · `/openapi.json`  
**Reproducible requests:** [`docs/demo/signalhub.http`](demo/signalhub.http)

## Consumers and guarantees

| Consumer | Contract surface | Guarantee (V1) |
|----------|------------------|----------------|
| Next.js dashboard | `/api/v1/*` JSON | Field names match `apps/web/src/lib/types.ts` |
| Humans / interviewers | OpenAPI + HTTP collection | Paths and status codes documented |
| Upstream APIs | Pydantic contracts in `packages/ingestion/contracts` | Validate before normalize |

## Auth & rate limits

| Endpoint class | Auth | Rate limit |
|----------------|------|------------|
| `GET /*` (read) | None (local demo) | None |
| `POST /api/v1/runs/trigger/{slug}` | Optional `X-API-Key` when `TRIGGER_API_KEY` is set | Process-local sliding window (`TRIGGER_RATE_LIMIT_PER_MINUTE`, default 10) |

`429` responses include `Retry-After`.

## Endpoints

### `GET /health`

```json
{
  "status": "healthy",
  "database": "connected",
  "scheduler": "running",
  "timestamp": "2026-07-13T18:00:00Z"
}
```

### `GET /api/v1/sources`

List sources with recomputed freshness and last run status.

### `GET /api/v1/sources/{slug}`

Detail payload:

```json
{
  "source": { "slug": "open-meteo", "freshness": { "is_stale": false, "staleness_minutes": 12 } },
  "recent_runs": [],
  "recent_signals": [],
  "recent_checks": [],
  "quality_summary": { "total": 12, "passed": 10, "warnings": 2, "failures": 0 }
}
```

Note: `quality_summary.total` (not `total_checks`).

### `GET /api/v1/runs`

Query: `source`, `status` (`success|failed|running|partial`), `limit`, `offset`.

### `GET /api/v1/runs/{run_id}`

Single run by UUID.

### `GET /api/v1/freshness`

Per-source freshness with age recomputed on read from `last_success_at`.

### `GET /api/v1/quality`

Query: `source`, `status` (`pass|warn|fail`), `limit`.  
`summary` respects the same `source` filter as `items`.

### `GET /api/v1/signals`

Query: `source`, `limit`, `offset`.

### `GET /api/v1/metrics/summary`

Aggregate KPIs for the overview page.

### `POST /api/v1/runs/trigger/{slug}`

Synchronous pipeline execution. Response reflects final status:

```json
{
  "run_id": "uuid",
  "source_slug": "open-meteo",
  "status": "success",
  "message": "Run completed successfully"
}
```

## Canonical signal shape

Normalized rows stored in `normalized_signals`:

| Field | Meaning |
|-------|---------|
| `signal_type` | Domain bucket (`weather`, `exchange_rate`, `crypto_price`) |
| `signal_key` | Stable metric id (`temperature_celsius`, `EUR_USD`, `bitcoin_usd`) |
| `signal_value` | Numeric value |
| `signal_unit` | Display unit |
| `observed_at` | Observation timestamp (UTC) |

## Drift policy

Quality check `schema_drift` warns when **required** keys are missing from the raw payload. Extra upstream fields are allowed.

## Export OpenAPI

With the API running:

```powershell
Invoke-RestMethod http://localhost:8000/openapi.json | ConvertTo-Json -Depth 40 |
  Set-Content docs/demo/openapi.snapshot.json
```

Or in CI/tests: `app.openapi()` (see `apps/api/tests/test_contracts.py`).
