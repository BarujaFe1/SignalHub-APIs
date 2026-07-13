<div align="center">

# SignalHub APIs

**Backend analytics made visible, reliable, and explainable**

Integrates public APIs → normalizes signals → tracks runs, freshness & quality → exposes an ops dashboard.

[PT-BR below](#pt-br) · [Architecture](docs/architecture.md) · [API contract](docs/api-contract.md) · [Deployment](docs/DEPLOYMENT.md) · [Testing](docs/TESTING.md)

![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

</div>

---

## Screenshot placeholder

> Add PNGs under `docs/screenshots/` (see that folder’s README). Until then, open the live UI locally:

| Surface | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| OpenAPI / Swagger | http://localhost:8000/docs |

```text
┌─────────────────────────────────────────────────────────────┐
│  SignalHub · Overview                                       │
│  Sources active · Runs · Quality pass rate · Freshness      │
│  ─────────────────────────────────────────────────────────  │
│  open-meteo │ frankfurter │ coingecko   [Run now]           │
└─────────────────────────────────────────────────────────────┘
```

---

<a id="pt-br"></a>

## Problema real

Pipelines e integrações costumam ser caixas-pretas: falham sem aviso claro, dados envelhecem sem indicador, qualidade degrada sem gate, e o histórico de execução some em logs. Times de produto e engenharia não conseguem responder rápido: *a fonte está viva? a última run falhou? os dados ainda estão frescos?*

## Solução

**SignalHub** transforma APIs públicas heterogêneas em uma camada observável de sinais:

1. **Ingestão** via conectores (Open-Meteo, Frankfurter, CoinGecko)
2. **Validação** com contratos Pydantic + checks de qualidade
3. **Normalização** para um modelo canônico de sinais
4. **Persistência** com histórico de runs, payload bruto e eventos
5. **Frescor** recalculado na leitura a partir do último sucesso
6. **Dashboard** Next.js para operação e storytelling técnico

## Principais funcionalidades

- 3 conectores reais com agendamento (APScheduler) e trigger manual
- Idempotência por janela horária
- Quality gates: null, volume, range, schema (campos obrigatórios)
- API REST versionada (`/api/v1`) com OpenAPI automático
- Dashboard: overview, sources, detalhe com **Run now**, runs, quality
- SQLite out-of-the-box; Postgres opcional via Docker Compose
- Gate opcional `TRIGGER_API_KEY` para demos públicas

## Arquitetura

```text
Public APIs → packages/ingestion → SQLite/Postgres → FastAPI → Next.js
                 contracts + QC         7 tables      /docs      ops UI
```

Detalhes: [docs/architecture.md](docs/architecture.md) · decisões: [docs/TECHNICAL_DECISIONS.md](docs/TECHNICAL_DECISIONS.md)

## Stack

| Camada | Tecnologias |
|--------|-------------|
| API | Python 3.12, FastAPI, SQLAlchemy 2 (async), Alembic, APScheduler, httpx, Pydantic v2 |
| Ingestion | Conectores + contracts + quality checks |
| Web | Next.js 16, React 19, TypeScript, Tailwind 4, shadcn/ui |
| Data | SQLite (local) / PostgreSQL (Compose/prod) |
| CI | GitHub Actions — Ruff, pytest, ESLint, `tsc`, `next build` |

## Demo local (Windows / PowerShell)

Pré-requisitos: Python 3.12+, Node 22+, npm.

```powershell
# 1) Backend
cd apps\api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH = "$PWD;$((Resolve-Path ..\..).Path)"
python ..\..\scripts\seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2) Frontend (outro terminal)
cd apps\web
npm install
npm run dev
```

Atalho Windows: `.\start.bat` na raiz do repositório.

| Serviço | URL |
|---------|-----|
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Dashboard | http://localhost:3000 |

Depois abra **Sources → detalhe → Run now** para ingerir dados ao vivo.

### Make (Git Bash / WSL / macOS)

```bash
make seed && make api   # terminal 1
make web                # terminal 2
make test
make lint
```

## Variáveis de ambiente

Copie [`.env.example`](.env.example) → `.env`.

| Variável | Padrão | Notas |
|----------|--------|-------|
| `DATABASE_URL` | SQLite async | Postgres opcional |
| `CORS_ORIGINS` | localhost:3000 | Ajuste no deploy |
| `TRIGGER_API_KEY` | vazio | Defina em demos públicas |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | URL da API para o web |
| `COINGECKO_API_KEY` | vazio | Opcional (rate limit) |

Segurança: [docs/SECURITY_NOTES.md](docs/SECURITY_NOTES.md)

## Testes

```powershell
$env:PYTHONPATH = "$PWD\apps\api;$PWD"
$env:TRIGGER_API_KEY = "test-secret"
.\apps\api\.venv\Scripts\python.exe -m pytest packages\ingestion\tests apps\api\tests -v

cd apps\web
npm run lint
npx tsc --noEmit
npm run build
```

Guia: [docs/TESTING.md](docs/TESTING.md)

## Decisões técnicas e trade-offs

- **SQLite-first** para DX de portfólio; Postgres quando precisar de deploy real.
- **Trigger síncrono** simplifica a demo; produção deveria enfileirar jobs.
- **Freshness na leitura** evita “Fresh (0m ago)” mentiroso.
- **Sem Recharts no V1** — KPIs e tabelas primeiro; charts no roadmap.
- **Auth mínima** — só no trigger; leitura aberta para demo local.

Mais: [docs/TECHNICAL_DECISIONS.md](docs/TECHNICAL_DECISIONS.md)

## Roadmap

- [ ] Charts de tendência (runs / freshness)
- [ ] Expor `event_logs` na API
- [ ] Fila assíncrona para triggers
- [ ] Auth de leitura para demos públicas
- [ ] Playwright smoke tests

## Status atual

**Portfolio-ready local demo.** Core pipeline operacional com SQLite. Docker Compose disponível se Docker estiver instalado. CI cobre lint/test/build. Deploy: API em host always-on + web na Vercel — ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## O que este projeto demonstra

- Modelagem de domínio para observabilidade de dados
- Contratos Pydantic na borda de APIs externas
- Pipelines com qualidade, idempotência e frescor
- API FastAPI bem tipada + OpenAPI
- Frontend TypeScript operacional (não só marketing page)
- DX: seed, scripts portáveis, CI, docs honestas
- Conciência de segurança em demos públicas

## Como eu apresentaria em entrevista

1. **Problema (30s):** integrações invisíveis e dados velhos sem sinal.
2. **Demo (2 min):** Swagger → trigger → dashboard (status, duração, QC, freshness).
3. **Arquitetura (2 min):** monorepo `apps/` + `packages/ingestion`, 7 tabelas, scheduler.
4. **Trade-offs (1 min):** SQLite vs Postgres; trigger síncrono; auth só no write path.
5. **Próximo passo (30s):** fila + charts + testes e2e.

---

## English summary

SignalHub is a portfolio-grade observability layer for public API ingestion: connectors normalize weather, FX, and crypto into signals; FastAPI exposes runs/freshness/quality; Next.js makes the pipeline explainable. Clone, seed SQLite, run API + web, hit **Run now**.

## License

MIT · Felipe Alirio Baruja
