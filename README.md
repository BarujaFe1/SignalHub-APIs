<div align="center">

# SignalHub APIs

**Make public-API ingestion visible, auditable, and explainable**

Lab de observabilidade para integrações: conectores → contratos → qualidade → frescor → dashboard operacional.

[Problem statement](docs/PROBLEM_STATEMENT.md) · [Architecture](docs/architecture.md) · [API contract](docs/api-contract.md) · [Demo HTTP](docs/demo/signalhub.http) · [Interview demo](docs/demo-script.md)

![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

</div>

---

## Screenshots

![Overview](docs/screenshots/01-overview-dashboard.png)

![Runs](docs/screenshots/02-runs-timeline.png)

![Source detail](docs/screenshots/03-source-detail.png)

![Quality](docs/screenshots/04-quality-checks.png)

![Swagger / OpenAPI](docs/screenshots/05-swagger-ui.png)

---

## Problem & audience

**Audience:** analytics engineers, data engineers, and full-stack builders who integrate heterogeneous APIs and need to *trust* the results.

**Problem:** pipelines fail quietly, schemas drift, data goes stale, and run history lives only in logs — so nobody can answer “is this source healthy right now?”

**What SignalHub enables:** an explainable loop — ingest → validate → normalize → persist → observe freshness/QC → decide whether to trust the data.

Full write-up: [docs/PROBLEM_STATEMENT.md](docs/PROBLEM_STATEMENT.md)

---

## Solution (flow)

```text
Open-Meteo / Frankfurter / CoinGecko
        │
        ▼
 packages/ingestion  (contracts + normalize + quality)
        │
        ▼
 SQLite (local) or Postgres
        │
        ├─► FastAPI /api/v1 + OpenAPI (/docs)
        └─► Next.js ops dashboard (:3000)
```

## What this project demonstrates

- Domain modeling for **data observability** (runs, freshness, quality, signals)
- **Pydantic contracts** at the edge of third-party APIs
- Idempotent scheduled jobs + manual trigger with optional API key and rate limit
- Typed REST API with OpenAPI as the source of truth
- TypeScript ops UI that consumes the same contract
- Honest lab scope: clone → seed → demo in minutes (SQLite-first)

## Architecture & stack

| Layer | Tech |
|-------|------|
| API | Python 3.12, FastAPI, SQLAlchemy async, Alembic, APScheduler, httpx |
| Ingestion | Connectors + contracts + QC in `packages/ingestion` |
| Web | Next.js 16, React 19, TypeScript, Tailwind 4 |
| Data | SQLite local / Postgres optional (Compose) |
| Quality gates | GitHub Actions: Ruff, pytest, ESLint, `tsc`, `next build` |

Details: [docs/architecture.md](docs/architecture.md) · [docs/TECHNICAL_DECISIONS.md](docs/TECHNICAL_DECISIONS.md)

## Quick start (Windows / PowerShell)

Requires Python 3.12+ and Node 22+.

```powershell
cd apps\api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH = "$PWD;$((Resolve-Path ..\..).Path)"
python ..\..\scripts\seed.py
uvicorn app.main:app --reload --port 8000
```

```powershell
cd apps\web
npm install
npm run dev
```

Or `.\start.bat` from the repo root.

| Surface | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| Swagger | http://localhost:8000/docs |
| HTTP collection | [docs/demo/signalhub.http](docs/demo/signalhub.http) |

Then: **Sources → open-meteo → Run now**.

## Environment

Copy [`.env.example`](.env.example) → `.env`.

| Variable | Default | Notes |
|----------|---------|-------|
| `DATABASE_URL` | SQLite | Postgres optional |
| `TRIGGER_API_KEY` | empty | Set for public demos |
| `TRIGGER_RATE_LIMIT_PER_MINUTE` | `10` | Per source slug, process-local |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Web → API |

Security notes: [docs/SECURITY_NOTES.md](docs/SECURITY_NOTES.md)

## Tests & gates

```powershell
$env:PYTHONPATH = "$PWD\apps\api;$PWD"
$env:TRIGGER_API_KEY = "test-secret"
.\apps\api\.venv\Scripts\python.exe -m pytest packages\ingestion\tests apps\api\tests -v

cd apps\web
npm run lint
npx tsc --noEmit
npm run build
```

Includes OpenAPI path/contract tests and trigger rate-limit regression.

## Decisions & trade-offs

- SQLite-first DX vs Postgres for shared deploy
- Synchronous trigger (great for demos; queue later for scale)
- Freshness recomputed on read
- No chart library in V1 (tables/KPIs only)
- Read endpoints open locally; write path gated + rate-limited

## Status & limitations

**Status:** local lab demo is reproducible; CI covers lint/test/build.  
**No public production deploy is claimed** in this pass — host API (always-on) + Vercel for web when you need a URL ([docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)).

Limitations: no multi-tenant auth, no job queue, no Playwright e2e, Compose not required for the happy path.

## Interview script (3–5 min)

See [docs/demo-script.md](docs/demo-script.md).

1. Problem of invisible pipelines  
2. Run now → runs / signals / QC / freshness  
3. OpenAPI + HTTP collection as evidence of contracts  
4. Trade-offs and next steps  

## License

MIT · Felipe Alírio Baruja
