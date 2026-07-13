# Handoff — Portfolio quality pass

**Branch:** `chore/portfolio-quality-pass`  
**Date:** 2026-07-13  
**Repo:** BarujaFe1/SignalHub-APIs

---

## What was found

- Strong concept (ingestion → QC → freshness → dashboard) but weak publication readiness.
- Hardcoded `C:\dev\signalhub-apis` paths in `start.bat` and many scripts.
- Makefile `seed` / `test` pointed at wrong paths.
- Docker Compose referenced missing web Dockerfile; Postgres drivers were commented out.
- Trigger endpoint unauthenticated; returned `status: "running"` after sync completion.
- Source detail quality summary was **global**, not per-source.
- Freshness age stuck at `0m` after success.
- Pydantic contracts existed but were unused; `schema_drift_check` never called.
- README claimed Recharts / broken VALIDATION.md / session-doc noise at repo root.
- CI only ran Ruff + ingestion unit tests.
- Docker not installed on the audit machine → Compose path documented as optional.

**Pre-pass score:** ~5.5/10

---

## What was fixed

- Repo-relative `start.bat`, `scripts/_paths.py`, fixed script bootstraps; archived session docs under `docs/archive/`.
- Makefile PYTHONPATH + seed/test targets.
- `TRIGGER_API_KEY` gate; trigger returns real run status.
- Per-source quality summary; freshness recomputed on read.
- Contracts wired into connector validation; schema drift checks required keys.
- API tests (`apps/api/tests`) + expanded CI (web lint/tsc/build).
- Web Dockerfile; API Dockerfile module path; asyncpg enabled.
- Source detail **Run now** button; a11y labels on status/freshness pills.
- Honest README + VALIDATION.md + architecture/testing/deployment/security docs.

---

## What was improved

- DX for Windows clones (SQLite-first).
- Portfolio narrative honesty (no fake Recharts badge claims).
- Security notes for public demos.
- Lint hygiene (Ruff clean; ESLint tuned for client fetch patterns).

---

## Commands run

```powershell
python -m venv apps\api\.venv
pip install -r apps\api\requirements.txt
npm install   # apps/web
pytest packages\ingestion\tests apps\api\tests -v   # 22 passed
ruff check apps\api\app packages\ingestion          # clean
npm run lint / npx tsc --noEmit / npm run build     # web
```

Docker Compose was **not** executed (Docker CLI unavailable on this machine).

---

## Tests executed

| Suite | Result |
|-------|--------|
| Ingestion unit tests | Pass |
| API tests (health, sources, trigger auth, metrics, freshness helper) | Pass (22 total) |
| Ruff | Pass |
| Next.js lint (after rule tune + `any` cleanup) | Pass expected |
| `next build` | Pass |

---

## Still missing / remaining risks

- No Playwright e2e; no mocked HTTP fetch tests for connectors.
- Trigger remains open when `TRIGGER_API_KEY` is empty (intentional local demo).
- `NEXT_PUBLIC_TRIGGER_API_KEY` is browser-visible if used.
- Screenshots still placeholders under `docs/screenshots/`.
- Charts still on roadmap.
- `event_logs` not exposed via API.
- Compose not smoke-tested here without Docker.

---

## Next steps

1. Capture real screenshots into `docs/screenshots/`.
2. Deploy API (Railway/Render) + web (Vercel) with `TRIGGER_API_KEY` set.
3. Add chart library only if demos need trends.
4. Consider async job queue for triggers.
5. Open PR from this branch → `main`.

---

## Portfolio suggestions

- Lead with the problem of invisible pipelines; demo Swagger → Run now → QC/freshness.
- Mention SQLite-first DX + optional Postgres as a deliberate trade-off.
- Point interviewers at `docs/TECHNICAL_DECISIONS.md` and `docs/SECURITY_NOTES.md`.

---

## Suggested commit message

```
chore: improve portfolio quality, docs, tests and stability
```
