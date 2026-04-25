.PHONY: help dev db api web migrate seed test lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Infrastructure ──────────────────────────

db: ## Start PostgreSQL
	docker compose up -d db

db-stop: ## Stop PostgreSQL
	docker compose stop db

dev: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

# ─── Backend ─────────────────────────────────

api: ## Start FastAPI dev server
	cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate: ## Run Alembic migrations
	cd apps/api && alembic upgrade head

migrate-new: ## Create new migration (usage: make migrate-new MSG="description")
	cd apps/api && alembic revision --autogenerate -m "$(MSG)"

seed: ## Seed database with initial data
	cd apps/api && python -m scripts.seed

# ─── Frontend ────────────────────────────────

web: ## Start Next.js dev server
	cd apps/web && npm run dev

web-build: ## Build frontend
	cd apps/web && npm run build

# ─── Quality ─────────────────────────────────

test: ## Run backend tests
	cd apps/api && python -m pytest packages/ingestion/tests/ -v

lint-api: ## Lint backend
	cd apps/api && ruff check .

lint-web: ## Lint frontend
	cd apps/web && npm run lint

lint: lint-api lint-web ## Lint everything

# ─── Utilities ───────────────────────────────

clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; true
	rm -rf apps/web/.next
