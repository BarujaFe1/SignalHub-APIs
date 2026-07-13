# Portfolio handoff — SignalHub APIs

**Date:** 2026-07-13  
**Branch:** `chore/portfolio-quality-pass`  
**Recommendation:** **selecionado** (strong analytics-engineering lab; not “enterprise production”)

---

## Summary

SignalHub is a monorepo lab that turns public API ingestion into an explainable ops loop: connectors, Pydantic contracts, quality gates, freshness, FastAPI/OpenAPI, and a Next.js dashboard. This pass closed remaining portfolio gaps: problem statement, contract docs, reproducible HTTP demo, rate limiting, contract tests, honest README with real screenshots, and a consolidation supermegaprompt outside the repo.

## Before → after

| Area | Before (main / early audit) | After |
|------|-----------------------------|-------|
| DX | Broken `C:\dev\...` paths | Repo-relative scripts + `start.bat` |
| Trigger | Open + lied `running` | Optional API key + final status + rate limit |
| Quality | Global summary on source detail | Scoped per source |
| Freshness | Stuck at 0m | Recomputed on read |
| Contracts | Docs drift / unused models | Wired validation + OpenAPI tests + HTTP collection |
| README | Inflated / placeholder screenshots | Honest claims + real PNGs |
| GitHub meta | Empty description | Should be updated (see below) |
| Tests | Thin unit only | + API + contract/rate-limit tests |

## Commands (validation)

```powershell
$env:PYTHONPATH = "$PWD\apps\api;$PWD"
$env:TRIGGER_API_KEY = "test-secret"
.\apps\api\.venv\Scripts\python.exe -m pytest packages\ingestion\tests apps\api\tests -v
.\apps\api\.venv\Scripts\ruff.exe check apps\api\app packages\ingestion
cd apps\web; npm run lint; npx tsc --noEmit; npm run build
```

Docker Compose was not smoke-tested on the audit machine (Docker unavailable).

## Visual / deploy evidence

- Screenshots: `docs/screenshots/01-*.png` … `05-*.png`
- Public deploy: **not claimed** — local demo is the evidence path
- Open API locally: `http://localhost:8000/docs`

## Limitations

- Lab/MVP scope, not multi-tenant SaaS
- Trigger rate limit is process-local (not Redis)
- No Playwright e2e
- GitHub description historically empty / misleading “TypeScript APIs” — correct to bilingual FastAPI + Next.js wording

## Next steps

1. Merge PR `chore/portfolio-quality-pass` → `main`
2. Set GitHub description + topics (`fastapi`, `nextjs`, `data-observability`, `openapi`, `portfolio`)
3. Optional: deploy API + Vercel web with `TRIGGER_API_KEY` set
4. Optional: Playwright smoke for Run now path

## Supermegaprompt path

`C:\dev\prompts_para_port\signalhub-apis-supermegaprompt-portfolio.md`
