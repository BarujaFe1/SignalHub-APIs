# Changelog

## Unreleased / `chore/portfolio-quality-pass`

### Added
- Problem statement (`docs/PROBLEM_STATEMENT.md`)
- Reproducible HTTP demo collection (`docs/demo/signalhub.http`)
- Contract tests for OpenAPI paths + trigger rate limiting
- Process-local sliding-window rate limiter on `POST /runs/trigger/{slug}`
- Portfolio handoff (`docs/PORTFOLIO_HANDOFF.md`)
- Optional `TRIGGER_RATE_LIMIT_PER_MINUTE`

### Fixed / improved
- API contract docs aligned with real schemas (`quality_summary.total`, trigger final status)
- Demo script updated for SQLite-first (no Docker required)
- README uses real screenshots; removes inflated claims
- Removed unused frontend `mock-data.ts`
- OpenAPI tags and richer trigger endpoint documentation

### Previously on this branch
- Path/DX fixes, trigger API key, per-source quality summary, freshness on read
- Contracts wired into connectors; schema drift checks
- Expanded CI; Dockerfiles; session docs archived
