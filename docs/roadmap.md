# Roadmap

## V1 — Foundation ✓

Core platform with 3 connectors, scheduler, quality checks, and status page.

- [x] Repository structure
- [x] 3 connectors: Open-Meteo, Frankfurter, CoinGecko
- [x] Pydantic contracts per connector
- [x] APScheduler with idempotency
- [x] Raw + normalized persistence
- [x] Execution history (runs)
- [x] Freshness tracking
- [x] Quality checks (null, volume, range, schema drift)
- [x] FastAPI read endpoints
- [x] Next.js status page
- [x] Docker Compose
- [x] Documentation
- [x] CI/CD

## V1.1 — Refinement

- [ ] New connector (e.g., NewsAPI or GitHub API)
- [ ] Additional quality checks
- [ ] Smarter retry with exponential backoff
- [ ] Simple temporal comparison (value vs. previous run)
- [ ] Timeline filtering by date range
- [ ] Source detail page enhancements
- [ ] Swagger documentation improvements

## V2 — Depth

- [ ] Notification system (webhook or email on failures)
- [ ] Schema drift detection with diff view
- [ ] Contract governance improvements
- [ ] Historical analytics and trends
- [ ] Comparative views across sources
- [ ] Performance optimization
- [ ] Deployment guide for cloud platforms
