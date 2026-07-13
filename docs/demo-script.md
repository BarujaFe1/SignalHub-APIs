# Demo script — 3 to 5 minutes

## Goal

Show that SignalHub makes API ingestion **auditable**: run → signals → quality → freshness.

## Setup (before the call)

SQLite path (no Docker):

```powershell
cd apps\api
.\.venv\Scripts\activate
$env:PYTHONPATH = "$PWD;$((Resolve-Path ..\..).Path)"
python ..\..\scripts\seed.py
uvicorn app.main:app --reload --port 8000
```

```powershell
cd apps\web
npm run dev
```

Optional: open [`docs/demo/signalhub.http`](demo/signalhub.http) in the editor.

## Minute-by-minute

| Time | Action | Say |
|------|--------|-----|
| 0:00–0:30 | Open overview `http://localhost:3000` | “Problem: integrations are invisible. SignalHub surfaces runs, freshness, and QC.” |
| 0:30–1:30 | Sources → Open-Meteo → **Run now** | “Manual trigger executes the same pipeline as the scheduler.” |
| 1:30–2:30 | Tabs: runs / signals / quality | “Duration, record counts, normalized keys, null/volume/range/schema checks.” |
| 2:30–3:30 | Swagger `/docs` → GET metrics + POST trigger | “OpenAPI is the contract; HTTP collection reproduces the demo.” |
| 3:30–4:30 | Mention trade-offs | “SQLite-first lab; optional API key + rate limit on triggers; not a multi-tenant platform.” |
| 4:30–5:00 | Close | “Shows analytics-engineering thinking: contracts, observability, honest scope.” |

## If upstream APIs fail

- Show the failed run + error message in the UI.
- Fall back to explaining `scripts/seed_mock_data.py` as an offline path (lab mode).

## Screenshots for the repo

Already under `docs/screenshots/` (01–05). Capture guide: [`docs/screenshots/README.md`](screenshots/README.md).
