# Validation checklist

Use this after cloning to confirm the portfolio demo works.

## Environment

- [ ] Python 3.12+ available (`python --version`)
- [ ] Node 22+ available (`node --version`)
- [ ] `.env` copied from `.env.example` (optional if using SQLite defaults)

## Backend

- [ ] `pip install -r apps/api/requirements.txt` succeeds
- [ ] `python scripts/seed.py` creates 3 sources
- [ ] `uvicorn app.main:app --reload --port 8000` starts
- [ ] `GET http://localhost:8000/health` returns `healthy`
- [ ] `GET http://localhost:8000/docs` opens Swagger
- [ ] `GET /api/v1/sources` lists `open-meteo`, `frankfurter`, `coingecko`

## Ingestion

- [ ] Trigger via Swagger `POST /api/v1/runs/trigger/open-meteo` (or UI **Run now**)
- [ ] Run appears in `/api/v1/runs` with `success` or a clear error
- [ ] Quality checks appear in `/api/v1/quality`
- [ ] Freshness updates on `/api/v1/freshness`

## Frontend

- [ ] `npm install` + `npm run dev` in `apps/web`
- [ ] Overview loads KPIs
- [ ] Source detail **Run now** works
- [ ] Dark/light theme toggle works

## Quality gates

- [ ] `pytest packages/ingestion/tests apps/api/tests -v` passes
- [ ] `npm run lint` + `npx tsc --noEmit` + `npm run build` pass in `apps/web`

## Security

- [ ] No `.env` committed
- [ ] If deploying publicly, `TRIGGER_API_KEY` is set
