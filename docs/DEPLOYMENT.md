# Deployment

## Local demo (recommended)

No Docker required.

```powershell
# API
cd apps\api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH = "$PWD;$((Resolve-Path ..\..).Path)"
python ..\..\scripts\seed.py
uvicorn app.main:app --reload --port 8000

# Web (second terminal)
cd apps\web
npm install
npm run dev
```

Or run `start.bat` from the repo root on Windows.

- API: http://localhost:8000/docs  
- Dashboard: http://localhost:3000  

## Docker Compose (optional)

Requires Docker Desktop.

```bash
docker compose up --build
```

Services: Postgres `5432`, API `8000`, Web `3000`.

**Note:** On machines without Docker (common for portfolio clones), use the SQLite path above.

## Production split

| Piece | Suggested host | Notes |
|-------|----------------|-------|
| FastAPI + scheduler | Railway / Render / Fly.io | Needs always-on process |
| Next.js | Vercel | Set `NEXT_PUBLIC_API_URL` to public API |
| Database | Managed Postgres | Set `DATABASE_URL` + `DATABASE_URL_SYNC` |

### Required production env

```env
DATABASE_URL=postgresql+asyncpg://...
DATABASE_URL_SYNC=postgresql://...
CORS_ORIGINS=["https://your-frontend.vercel.app"]
TRIGGER_API_KEY=<strong-random>
NEXT_PUBLIC_API_URL=https://your-api.example.com
# Prefer not exposing trigger key in the browser for real prod
```

### Vercel (frontend only)

1. Import `apps/web` as the project root (or set Root Directory to `apps/web`).
2. Set `NEXT_PUBLIC_API_URL`.
3. Deploy. Backend is **not** suitable for Vercel serverless (scheduler + long jobs).

## Health checks

- `GET /health` — DB connectivity + scheduler state  
- OpenAPI: `/docs`
