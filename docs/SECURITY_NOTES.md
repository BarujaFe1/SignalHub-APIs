# Security notes

## Findings during portfolio quality pass (2026-07-13)

### Trigger endpoint was open

`POST /api/v1/runs/trigger/{slug}` had no authentication. On a public deploy this allows anyone to force outbound calls to third-party APIs and write to the database.

**Mitigation:** optional `TRIGGER_API_KEY`. When set, requests must send `X-API-Key`. When empty (local demo), the endpoint remains open by design — do not expose that mode publicly.

### No secrets committed

No live API keys or production credentials were found in the repository. `.env` remains gitignored. `.env.example` uses placeholder values only.

### Docker Compose Postgres password

`signalhub_dev` is a **local development** password in `docker-compose.yml`. Replace before any shared/staging environment.

### CORS

`allow_credentials=True` with explicit origins is acceptable for local demo. Tighten `CORS_ORIGINS` in production to the real frontend origin only.

### Browser-exposed trigger key

`NEXT_PUBLIC_TRIGGER_API_KEY` is visible to clients. Use only for demos with rate-limited upstream accounts — never reuse production secrets.

## Reporting

If you discover a secret in history or a new vulnerability, rotate the credential immediately and open a private report to the maintainer. Do not paste secret values into issues or docs.
