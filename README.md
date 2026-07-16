<div align="center">
  <img src="./icon.png" alt="SignalHub APIs Logo" width="120" height="120" />

  <h1>SignalHub APIs</h1>

  <p><strong>Lab de observabilidade para ingestão de APIs públicas — contratos, qualidade, frescor e dashboard ops.</strong></p>
  <p><strong>Observability lab for public API ingestion — contracts, quality, freshness and an ops dashboard.</strong></p>

  <p>
    <a href="#pt-br">PT-BR</a>
     · 
    <a href="#english">English</a>
     · 
    <a href="#stack">Stack</a>
     · 
    <a href="#architecture">Architecture</a>
     · 
    <a href="#quick-start">Quick Start</a>
     · 
    <a href="#author">Author</a>
  </p>

  <p>
    <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge" />
    <img alt="Status-Lab" src="https://img.shields.io/badge/Status-Lab-22C55E?style=for-the-badge" />
    <img alt="License-MIT" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
  </p>

  <p>
    <a href="https://github.com/BarujaFe1/SignalHub-APIs"><strong>Repo</strong></a>
     · 
    <a href="https://barujafe.vercel.app/"><strong>Portfolio</strong></a>
     · 
    <a href="https://www.linkedin.com/in/barujafe/"><strong>LinkedIn</strong></a>
  </p>
</div>


> **Lab notice:** local observability cockpit for API ingestion. No public homepage is set on GitHub — run with `start.bat` / Docker Compose. Not a SaaS status-page product.

---

## PT-BR

### Visão geral
O **SignalHub** torna analytics de backend visível: integração de fontes, processamento, checagens de contrato/qualidade/frescor e dashboard Next.js sobre API FastAPI.

### Problema
Ingestões de APIs públicas quebram em silêncio — sem contrato, SLA de frescor nem painel ops para explicar falhas.

### Para quem
Data/backend engineers que querem um **lab de observabilidade** de ingestão antes de um data platform pesado.

### Funcionalidades
- Integração / jobs de ingestão (scheduler APScheduler no backend)
- Processamento e persistência (SQLAlchemy, SQLite/Postgres)
- Sinais de qualidade, frescor e saúde
- Dashboard web (Next.js + Recharts)
- `docker-compose.yml` + `start.bat`

### Escopo e limites (honestos)
- Lab local — **sem** demo Vercel configurada no homepage
- Não substitui Datadog/New Relic enterprise
- Fontes públicas: respeite rate limits e termos

---

## English

### Overview
**SignalHub** makes backend analytics visible: source integration, processing, contract/quality/freshness checks and a Next.js dashboard on a FastAPI API.

### Problem
Public API ingest fails silently — no contract, freshness SLO or ops view to explain breakage.

### Who it is for
Data/backend engineers who want an ingestion **observability lab** before a heavy platform.

### Features
- Integration / ingest jobs (APScheduler on the API)
- Processing + persistence (SQLAlchemy, SQLite/Postgres)
- Quality, freshness and health signals
- Web dashboard (Next.js + Recharts)
- `docker-compose.yml` + `start.bat`

### Scope and honest limits
- Local lab — **no** Vercel homepage configured
- Not a Datadog/New Relic replacement
- Respect public API rate limits and terms

---

## Stack

| Layer | Technology |
|---|---|
| Web | Next.js (`apps/web`) |
| API | FastAPI, SQLAlchemy, APScheduler, httpx (`apps/api`) |
| Ops | Docker Compose, Makefile, `start.bat` |

---

## Architecture

```txt
apps/web      ops dashboard
apps/api      ingest + quality services
packages/     shared bits (if present)
scripts/      helpers
```

Flow: schedule/pull → validate contract → store → freshness/quality signals → dashboard.

---

## Quick Start

```bash
.\start.bat
```

Or `docker compose up` and open the ports documented in `DEVELOPER.md` / README history (commonly web `:3001`, API `:8000`).

---

## Technical decisions

- **Contract + freshness** as first-class signals, not only “job success”
- SQLite for lab speed; Postgres optional
- Separate web/API apps for clear ownership

---

## Roadmap

- More source connectors and contract fixtures
- Stronger alerting rules
- Optional public demo deploy

---

## Author

**Felipe Alirio Baruja** — data / product / full-stack portfolio.

- Portfolio: [https://barujafe.vercel.app/](https://barujafe.vercel.app/)
- GitHub: [https://github.com/BarujaFe1](https://github.com/BarujaFe1)
- LinkedIn: [https://www.linkedin.com/in/barujafe/](https://www.linkedin.com/in/barujafe/)


## License

MIT — see [`LICENSE`](./LICENSE).
