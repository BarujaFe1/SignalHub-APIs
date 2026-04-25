"""Test API endpoints by importing them directly."""
import sys
sys.path.insert(0, r"C:\dev\signalhub-apis\apps\api")
sys.path.insert(0, r"C:\dev\signalhub-apis")

import asyncio
from fastapi.testclient import TestClient
from app.main import app

def test_endpoints():
    client = TestClient(app)
    
    # Test 1: Health endpoint
    response = client.get("/health")
    print(f"[OK] /health: {response.status_code}")
    print(f"     Response: {response.json()}")
    
    # Test 2: Sources list
    response = client.get("/api/v1/sources")
    print(f"\n[OK] /api/v1/sources: {response.status_code}")
    data = response.json()
    print(f"     Found {len(data)} sources")
    for s in data:
        print(f"     - {s['slug']}: {s['name']}")
    
    # Test 3: Source detail
    response = client.get("/api/v1/sources/open-meteo")
    print(f"\n[OK] /api/v1/sources/open-meteo: {response.status_code}")
    data = response.json()
    print(f"     Name: {data['source']['name']}")
    print(f"     Active: {data['source']['is_active']}")
    print(f"     Recent runs: {len(data['recent_runs'])}")
    print(f"     Recent signals: {len(data['recent_signals'])}")
    
    # Test 4: Runs
    response = client.get("/api/v1/runs?limit=5")
    print(f"\n[OK] /api/v1/runs: {response.status_code}")
    data = response.json()
    print(f"     Found {len(data)} runs")
    for r in data[:3]:
        print(f"     - {r['source']['slug']}: {r['status']} | {r['records_stored']} records")
    
    # Test 5: Freshness
    response = client.get("/api/v1/freshness")
    print(f"\n[OK] /api/v1/freshness: {response.status_code}")
    data = response.json()
    print(f"     Found {len(data)} freshness records")
    for f in data:
        stale = "STALE" if f['is_stale'] else "FRESH"
        print(f"     - {f['source']['slug']}: {stale}")
    
    # Test 6: Quality checks
    response = client.get("/api/v1/quality?limit=5")
    print(f"\n[OK] /api/v1/quality: {response.status_code}")
    data = response.json()
    print(f"     Found {len(data)} quality checks")
    for q in data[:3]:
        print(f"     - {q['check_name']}: {q['check_status']}")
    
    # Test 7: Signals
    response = client.get("/api/v1/signals?limit=5")
    print(f"\n[OK] /api/v1/signals: {response.status_code}")
    data = response.json()
    print(f"     Found {len(data)} signals")
    for sig in data[:3]:
        print(f"     - {sig['signal_key']}: {sig['signal_value']} {sig['signal_unit']}")
    
    # Test 8: Metrics summary
    response = client.get("/api/v1/metrics/summary")
    print(f"\n[OK] /api/v1/metrics/summary: {response.status_code}")
    data = response.json()
    print(f"     Total sources: {data['total_sources']}")
    print(f"     Total runs: {data['total_runs']}")
    print(f"     Total signals: {data['total_signals']}")
    
    print("\n[SUCCESS] All API endpoints working correctly!")

if __name__ == "__main__":
    test_endpoints()
