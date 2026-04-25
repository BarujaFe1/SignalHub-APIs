# Demo Script

## Setup (2 minutes)

1. Clone the repository
2. Run `cp .env.example .env`
3. Run `make db` to start PostgreSQL
4. Run `make migrate` to set up the schema
5. Run `make seed` to seed initial sources
6. Run `make api` in one terminal
7. Run `make web` in another terminal

## Walkthrough (5 minutes)

### 1. Overview Page
Open `http://localhost:3000`. Show:
- System pulse: all 3 sources healthy
- Source cards with freshness indicators
- Recent activity timeline
- Quality summary

### 2. Trigger a Run
- Use the API: `POST http://localhost:8000/api/v1/runs/trigger/open-meteo`
- Switch to the Runs page and show the new run appearing
- Point out: status, duration, records fetched

### 3. Source Detail
- Click on "Open-Meteo" source
- Show the freshness indicator
- Show recent runs list
- Show normalized signals (temperature, humidity, wind speed)
- Show quality checks (all passing)

### 4. Quality Page
- Navigate to Quality
- Show the global health bar
- Filter by status to show any warnings
- Explain what each check validates

### 5. API Explorer
- Open `http://localhost:8000/docs` (Swagger)
- Show the structured endpoints
- Execute a `/api/v1/signals` request live
- Show the normalized response format

### 6. Architecture Page
- Navigate to Docs in the frontend
- Show the Mermaid architecture diagram
- Explain the data flow briefly

## Key Talking Points

- "This isn't about consuming APIs. It's about making the integration work visible and reliable."
- "Every run is tracked. Every quality check is logged. Freshness is computed automatically."
- "The frontend exists to dignify the backend work — not as decoration, but as operational clarity."
- "This is a single-process architecture. No Kafka, no Airflow, no distributed complexity. Just clean engineering."
