# SignalHub APIs - Developer Guide

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- npm or yarn

### Start Everything
```bash
# Windows
start.bat

# Manual start
# Terminal 1 - Backend
cd apps/api
venv\Scripts\activate
set PYTHONPATH=C:\dev\signalhub-apis\apps\api;C:\dev\signalhub-apis
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd apps/web
npm run dev
```

### Access
- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Project Structure

```
signalhub-apis/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── app/
│   │   │   ├── db/            # Models, engine, base
│   │   │   ├── routers/       # API endpoints
│   │   │   ├── schemas/       # Pydantic schemas
│   │   │   ├── services/      # Business logic
│   │   │   ├── config.py      # Configuration
│   │   │   └── main.py        # FastAPI app
│   │   ├── alembic/           # Database migrations
│   │   ├── venv/              # Python virtual environment
│   │   ├── signalhub.db       # SQLite database
│   │   └── requirements.txt   # Python dependencies
│   │
│   └── web/                   # Next.js frontend
│       ├── src/
│       │   ├── app/           # App router pages
│       │   ├── components/    # React components
│       │   └── lib/           # Utilities
│       └── package.json       # Node dependencies
│
├── packages/
│   └── ingestion/             # Data pipeline
│       ├── connectors/        # API connectors
│       ├── jobs/              # Job runner
│       ├── quality/           # Quality checks
│       └── transforms/        # Data transforms
│
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── PLAN.md                    # Development plan
├── SUMMARY.md                 # Project summary
└── VALIDATION.md              # Validation report
```

---

## Common Tasks

### Trigger Connectors Manually
```bash
cd apps/api
venv\Scripts\activate
python trigger_connectors.py
```

### Validate API Endpoints
```bash
cd apps/api
venv\Scripts\activate
python validate_api.py
```

### Inspect Database
```bash
cd apps/api
venv\Scripts\activate
python inspect_db.py
python inspect_data.py
```

### Run Migrations
```bash
cd apps/api
venv\Scripts\activate
set PYTHONPATH=C:\dev\signalhub-apis\apps\api;C:\dev\signalhub-apis
alembic upgrade head
```

### Create New Migration
```bash
cd apps/api
venv\Scripts\activate
set PYTHONPATH=C:\dev\signalhub-apis\apps\api;C:\dev\signalhub-apis
alembic revision --autogenerate -m "description"
```

---

## Database Schema

### Tables
1. **sources** - Data source definitions
2. **runs** - Execution history
3. **raw_payloads** - Raw API responses
4. **normalized_signals** - Normalized data points
5. **freshness_status** - Data freshness tracking
6. **quality_checks** - Quality validation results
7. **event_logs** - System events

### Relationships
- Source → Runs (1:N)
- Source → FreshnessStatus (1:1)
- Run → RawPayloads (1:N)
- Run → NormalizedSignals (1:N)
- Run → QualityChecks (1:N)

---

## API Endpoints

### Health
- `GET /health` - System health check

### Sources
- `GET /api/v1/sources` - List all sources
- `GET /api/v1/sources/{slug}` - Get source detail

### Runs
- `GET /api/v1/runs` - List runs (paginated)
- `GET /api/v1/runs/{id}` - Get run detail

### Data
- `GET /api/v1/signals` - List signals (paginated)
- `GET /api/v1/freshness` - Get freshness status
- `GET /api/v1/quality` - List quality checks

### Metrics
- `GET /api/v1/metrics/summary` - System metrics

### Actions
- `POST /api/v1/runs/trigger/{slug}` - Trigger manual run

---

## Configuration

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///C:/dev/signalhub-apis/apps/api/signalhub.db
DATABASE_URL_SYNC=sqlite:///C:/dev/signalhub-apis/apps/api/signalhub.db

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Connectors
COINGECKO_API_KEY=

# Open-Meteo
OPEN_METEO_LATITUDE=52.52
OPEN_METEO_LONGITUDE=13.41
```

---

## Connectors

### Open-Meteo (Weather)
- **Endpoint**: https://api.open-meteo.com/v1/forecast
- **Schedule**: Every 30 minutes
- **Signals**: temperature, humidity, wind_speed
- **Auth**: None required

### Frankfurter (Currency)
- **Endpoint**: https://api.frankfurter.app/latest
- **Schedule**: Every 60 minutes
- **Signals**: EUR exchange rates (USD, GBP, BRL, etc.)
- **Auth**: None required

### CoinGecko (Crypto)
- **Endpoint**: https://api.coingecko.com/api/v3/simple/price
- **Schedule**: Every 15 minutes
- **Signals**: BTC, ETH prices in USD
- **Auth**: Optional API key

---

## Troubleshooting

### Backend won't start
1. Check if venv is activated
2. Verify PYTHONPATH is set correctly
3. Check if port 8000 is available
4. Review logs for errors

### Frontend won't start
1. Run `npm install` in apps/web
2. Check if port 3000/3001 is available
3. Verify NEXT_PUBLIC_API_URL in .env

### Connectors failing
1. Check internet connection
2. Verify API endpoints are accessible
3. Check rate limits
4. Review error logs in database

### Database issues
1. Check if signalhub.db exists
2. Verify file permissions
3. Run migrations if needed
4. Check SQLite version

---

## Testing

### Backend Tests
```bash
cd apps/api
venv\Scripts\activate
pytest
```

### Frontend Tests
```bash
cd apps/web
npm test
```

---

## Deployment

### Production Checklist
- [ ] Switch to PostgreSQL
- [ ] Set API_DEBUG=false
- [ ] Configure CORS for production domain
- [ ] Add rate limiting
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure SSL/TLS
- [ ] Set up CI/CD pipeline
- [ ] Add authentication
- [ ] Configure backup strategy
- [ ] Set up logging aggregation

---

## Support

For issues or questions:
1. Check VALIDATION.md for known issues
2. Review PLAN.md for development status
3. Check SUMMARY.md for project overview
4. Create issue on GitHub

---

## License

MIT
