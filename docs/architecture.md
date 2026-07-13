# Architecture — SignalHub APIs

## Purpose

SignalHub makes backend analytics and public-API ingestion **visible, auditable, and explainable**. Heterogeneous external APIs are normalized into a common signal model, quality-checked, and exposed through FastAPI + a Next.js operations dashboard.

## High-level diagram

```text
┌──────────────┐   fetch    ┌─────────────────┐
│ Open-Meteo   │───────────▶│                 │
│ Frankfurter  │            │  Connectors     │
│ CoinGecko    │───────────▶│  (packages/)    │
└──────────────┘            └────────┬────────┘
                                     │ validate / normalize / QC
                                     ▼
                            ┌─────────────────┐
                            │  SQLite/Postgres│
                            │  7-table model  │
                            └────────┬────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                                 ▼
           ┌────────────────┐                ┌────────────────┐
           │ FastAPI :8000  │◀── REST ───────│ Next.js :3000  │
           │ OpenAPI /docs  │                │ Ops dashboard  │
           │ APScheduler    │                └────────────────┘
           └────────────────┘
```

## Monorepo layout

| Path | Role |
|------|------|
| `apps/api` | FastAPI app, SQLAlchemy models, Alembic, API tests |
| `apps/web` | Next.js 16 App Router dashboard |
| `packages/ingestion` | Connectors, Pydantic contracts, quality checks, job runner |
| `scripts/` | Seed, manual triggers, debug helpers |
| `docs/` | Architecture, testing, deployment, audit, handoff |

## Domain model (7 tables)

1. `sources` — connector definitions + schedule
2. `runs` — execution history + idempotency key
3. `raw_payloads` — original JSON responses
4. `normalized_signals` — unified numeric signals
5. `freshness_status` — last success / staleness
6. `quality_checks` — per-run quality gates
7. `event_logs` — operational events (write-heavy; not yet exposed via API)

## Request flow

1. Scheduler (or `POST /runs/trigger/{slug}`) calls `execute_connector`.
2. Connector `fetch` → Pydantic/contract `validate_raw` → `normalize`.
3. Persist raw + signals; run null/volume/range/schema checks; update freshness.
4. Dashboard reads `/api/v1/*` for KPIs, timelines, and source detail.

## Design principles

- **Explainability over black boxes** — every run has duration, counts, errors, QC.
- **Contracts at the edge** — Pydantic models validate upstream payloads.
- **SQLite-first DX** — clone and run without Docker; Postgres optional via Compose.
- **Optional trigger auth** — `TRIGGER_API_KEY` gates manual ingestion for public demos.

## Non-goals (V1)

- Multi-tenant auth / RBAC
- Stream processing / Kafka
- Real-time websocket push
- Horizontal worker fleet
