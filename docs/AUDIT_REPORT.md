# SignalHub APIs — Audit Report

**Date:** 2026-07-13  
**Branch:** `chore/portfolio-quality-pass`  
**Auditor role:** senior architecture + portfolio readiness

---

## Executive summary

SignalHub is a strong portfolio *concept*: public API connectors → validation → normalization → persistence → quality/freshness → FastAPI + Next.js observability dashboard. The core pipeline and domain model are coherent.

Publication readiness was undermined by broken Windows paths (`C:\dev\...`), incorrect Makefile targets, Docker/Postgres mismatches, thin tests/CI, unused contracts, incorrect per-source quality summary, unauthenticated trigger endpoint, and a pile of outdated session docs with broken README links.

**Current score (pre-pass): 5.5 / 10**  
**Target after this pass: ~8 / 10** for a public engineering portfolio piece.

---

## Current score: 5.5 / 10

| Area | Score | Notes |
|------|------:|-------|
| Concept / narrative | 8.5 | Clear “make pipelines visible” story |
| Backend core | 7.5 | Clean models/runner; a few semantic bugs |
| Ingestion | 7.0 | Solid pipeline; contracts underused |
| Frontend | 6.5 | Usable dashboard; incomplete trigger UX |
| Tests | 3.5 | Thin unit tests only |
| CI | 4.0 | Python lint + ingestion tests |
| Docs hygiene | 3.0 | Session dumps + broken links |
| Deploy story | 3.0 | Compose/Dockerfile gaps; no Docker locally |
| Security (public demo) | 2.0 | Open trigger endpoint |

---

## Main risks

1. **Unauthenticated `POST /runs/trigger/{slug}`** — abuse of upstream APIs / DoS if deployed publicly.
2. **Docker Compose broken** — web Dockerfile missing; Postgres drivers commented out; API module path fragile.
3. **Hardcoded `C:\dev\signalhub-apis` paths** — clone-and-run fails on any other machine.
4. **Makefile seed/test wrong cwd** — documented DX commands fail.
5. **Source detail quality summary is global** — wrong product semantics.
6. **README claims Recharts / schema drift / VALIDATION.md / icon** — credibility damage for recruiters.
7. **Freshness shows `0m ago` after success** — stale metric never recomputed on read.

---

## Quick wins

- Fix Makefile / `start.bat` / script `sys.path` to be repo-relative.
- Protect trigger with optional API key; return real run status.
- Scope quality summary by source; recompute freshness age on read.
- Wire `schema_drift_check` + Pydantic contracts into validation path.
- Archive session markdown; rewrite README to match reality.
- Expand CI: frontend lint/build + API tests.
- Add web Dockerfile; enable `asyncpg` for compose path.
- SQLite-first local demo (Docker optional / not required).

---

## Structural improvements

- Treat SQLite as default local DX; Postgres as optional production path.
- Keep contracts as the validation source of truth for connectors.
- Separate portfolio docs (`README`, `docs/*`) from session artifacts (`docs/archive/*`).
- Add minimal API integration tests with in-memory/SQLite.
- Document deploy as API (Render/Railway/Fly) + web (Vercel).

---

## Bugs found

| Bug | Severity | Status |
|-----|----------|--------|
| `start.bat` / scripts hardcode `C:\dev\...` | Critical | Fix in this pass |
| Compose web Dockerfile missing | Critical | Fix |
| Compose Postgres without asyncpg | Critical | Fix |
| Makefile `seed` / `test` wrong paths | High | Fix |
| Source quality summary global | High | Fix |
| Trigger returns `status: "running"` after sync completion | Medium | Fix |
| Freshness age stuck at 0 after success | Medium | Fix |
| Contracts unused by connectors | High | Fix |
| `schema_drift_check` defined but never run | Medium | Fix |
| README Recharts claim false | High | Fix (docs) |
| Missing `VALIDATION.md` / broken links | High | Fix |
| Health scheduler always `"running"` | Low | Fix |
| Quality list summary ignores `source` filter | Medium | Fix |

---

## Execution plan

1. Diagnose & write this audit.
2. Install deps; run lint/test/build; document Docker absence.
3. Fix backend semantics, security gate, freshness, contracts, quality.
4. Fix DX (Makefile, start scripts, seed path, Dockerfiles).
5. Add API tests; expand CI.
6. Frontend: trigger run UX, freshness display, a11y labels.
7. Docs: ARCHITECTURE, TECHNICAL_DECISIONS, TESTING, DEPLOYMENT, SECURITY_NOTES, README, HANDOFF.
8. Archive obsolete root session files.
9. Commit + push branch.

---

## Final checklist

- [x] Project installs (Python venv + npm)
- [x] Tests pass
- [x] Frontend lint/build pass (or documented)
- [x] API runs on SQLite locally
- [x] Bugs above fixed or documented
- [x] README portfolio-ready
- [x] Docs created/updated
- [x] CI expanded
- [x] `.env.example` accurate
- [x] `.gitignore` protects secrets
- [x] `docs/HANDOFF.md` complete
- [x] Branch pushed
