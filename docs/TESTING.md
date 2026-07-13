# Testing

## What we test

| Layer | Location | Coverage |
|-------|----------|----------|
| Connectors | `packages/ingestion/tests/` | validate/normalize + quality helpers |
| API | `apps/api/tests/` | health, sources, auth gate, metrics, freshness helper |
| Frontend | CI lint + `tsc` + `next build` | static quality (no e2e yet) |

## Commands

From repo root (PowerShell):

```powershell
$env:PYTHONPATH = "$PWD\apps\api;$PWD"
$env:TRIGGER_API_KEY = "test-secret"
.\apps\api\.venv\Scripts\python.exe -m pytest packages\ingestion\tests apps\api\tests -v
```

Frontend:

```powershell
cd apps\web
npm run lint
npx tsc --noEmit
npm run build
```

Or with Make (Git Bash / WSL):

```bash
make test
make lint
make typecheck-web
```

## Conventions

- Prefer SQLite `:memory:` for API tests.
- Do not call live external APIs in unit/CI tests.
- When fixing a bug, add a regression test if practical (see `compute_freshness_age` tests).

## Gaps (known)

- No HTTP mocking for connector `fetch`
- No Playwright e2e against dashboard
- No load tests for scheduler fan-out
