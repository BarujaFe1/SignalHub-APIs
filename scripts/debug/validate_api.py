"""Simple endpoint validation test."""
import sys
sys.path.insert(0, r"C:\dev\signalhub-apis\apps\api")
sys.path.insert(0, r"C:\dev\signalhub-apis")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("Testing SignalHub APIs Endpoints\n")
print("="*50)

# Test 1: Health
response = client.get("/health")
assert response.status_code == 200
data = response.json()
print(f"[PASS] /health - Status: {data['status']}, DB: {data['database']}")

# Test 2: Sources list
response = client.get("/api/v1/sources")
assert response.status_code == 200
sources = response.json()
print(f"[PASS] /api/v1/sources - Found {len(sources)} sources")

# Test 3: Source detail
response = client.get("/api/v1/sources/open-meteo")
assert response.status_code == 200
detail = response.json()
print(f"[PASS] /api/v1/sources/open-meteo - {detail['recent_runs'].__len__()} runs, {detail['recent_signals'].__len__()} signals")

# Test 4: Runs
response = client.get("/api/v1/runs?limit=5")
assert response.status_code == 200
runs = response.json()
print(f"[PASS] /api/v1/runs - Found {runs['total']} total runs")

# Test 5: Freshness
response = client.get("/api/v1/freshness")
assert response.status_code == 200
freshness = response.json()
print(f"[PASS] /api/v1/freshness - {len(freshness)} sources tracked")

# Test 6: Quality
response = client.get("/api/v1/quality?limit=5")
assert response.status_code == 200
quality = response.json()
print(f"[PASS] /api/v1/quality - {quality['summary']['total']} total checks")

# Test 7: Signals
response = client.get("/api/v1/signals?limit=5")
assert response.status_code == 200
signals = response.json()
print(f"[PASS] /api/v1/signals - {signals['total']} total signals")

# Test 8: Metrics
response = client.get("/api/v1/metrics/summary")
assert response.status_code == 200
metrics = response.json()
print(f"[PASS] /api/v1/metrics/summary - {metrics['total_sources']} sources, {metrics['total_runs']} runs")

print("="*50)
print("\n[SUCCESS] All 8 endpoints validated successfully!")
print(f"\nSummary:")
print(f"  - Sources: {len(sources)}")
print(f"  - Total Runs: {metrics['total_runs']}")
print(f"  - Total Signals: {metrics['total_signals']}")
print(f"  - Quality Checks: {metrics['total_quality_checks']}")
print(f"  - Pass Rate: {metrics['quality_pass_rate']:.1%}")
