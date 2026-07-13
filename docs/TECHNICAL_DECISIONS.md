# Technical decisions

## SQLite by default, Postgres optional

**Decision:** Local development defaults to `sqlite+aiosqlite:///./signalhub.db`.  
**Why:** Zero infra friction for portfolio demos and CI. Postgres drivers remain installed for Docker Compose / production.  
**Trade-off:** SQLite concurrency limits; fine for demo scale.

## Synchronous trigger endpoint

**Decision:** `POST /runs/trigger/{slug}` runs the connector pipeline in-request and returns the final status.  
**Why:** Simpler demo UX (“Run now” shows real outcome).  
**Trade-off:** Long upstream calls block the request; production would enqueue a job and return `202` with polling.

## Optional `TRIGGER_API_KEY`

**Decision:** If set, require `X-API-Key`. If empty, allow open triggers (local demo).  
**Why:** Public demos must not let strangers hammer CoinGecko/Open-Meteo.  
**Trade-off:** Browser demos that need the key must expose `NEXT_PUBLIC_TRIGGER_API_KEY` — use throwaway demo keys only.

## Process-local trigger rate limit

**Decision:** Sliding-window limiter (default 10/min per source slug) on trigger.  
**Why:** Cheap abuse protection without Redis.  
**Trade-off:** Not shared across workers/instances; fine for lab/single process.

## Freshness computed on read

**Decision:** API recomputes `staleness_minutes` / `is_stale` from `last_success_at` + schedule interval.  
**Why:** Stored `staleness_minutes=0` after success was misleading minutes later.  
**Trade-off:** Slightly more CPU per request; negligible at V1 scale.

## Pydantic contracts + fallback validation

**Decision:** Connectors validate via contracts first, with a narrow dict fallback for partial fixtures.  
**Why:** Contracts become the living edge schema without breaking existing unit tests.  
**Trade-off:** Two validation paths until fixtures are fully contract-shaped.

## Schema drift = missing required keys

**Decision:** Warn when required fields disappear, not when APIs add extras.  
**Why:** Public APIs add fields constantly; missing required fields break normalization.  
**Trade-off:** Won’t detect “unexpected new required semantics”.

## Client-side Next.js data fetching

**Decision:** Pages are `"use client"` and fetch the API from the browser.  
**Why:** Matches current codebase; simplest path to a live ops UI.  
**Trade-off:** Weaker SSR/SEO story; acceptable for an authenticated ops dashboard style product.

## No Recharts in V1

**Decision:** Keep tabular/KPI UI without chart libraries.  
**Why:** Avoid fake README claims and dependency weight. Charts remain a roadmap item.
