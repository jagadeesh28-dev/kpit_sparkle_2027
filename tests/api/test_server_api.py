"""
tests/api/test_server_api.py
Comprehensive End-to-End Test Suite for AURA-Impact FastAPI Backend Server

Tests:
- /health: telemetry and dataset availability
- /scenarios: structured preset retrieval
- /analyze: happy path, semantic candidate separation (accepted vs rejected with reasons)
- /analyze: adversarial safety gate invariant retention
- /analyze: validation errors (empty fields, path traversal injection)
- /benchmarks: real CSV ingestion, verified figures manifest, scientific limitations
- /upload-diff: valid C/C++ unified diff parsing and artifact mapping
- /upload-diff: oversized payload and malformed input rejection
- /analysis/{id}: audit trace caching and retrieval
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.api.server import app, pipeline

@pytest.fixture(scope="module")
def client():
    # Ingest repo once for the test module
    demo_repo = REPO_ROOT / "data" / "demonstration_dataset"
    if not demo_repo.exists():
        demo_repo = REPO_ROOT / "examples" / "demo_repo"
    if demo_repo.exists() and len(pipeline.graph.graph.nodes) == 0:
        pipeline.ingest_repository(demo_repo)
    with TestClient(app) as test_client:
        yield test_client


# ── 1. Health Endpoint Tests ──────────────────────────────────────────────────

def test_health_endpoint(client):
    """Verifies that /health returns status 200, system telemetry, and dataset status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "architecture" in data
    assert "graph_telemetry" in data
    assert "datasets_available" in data
    assert data["graph_telemetry"]["node_count"] > 0
    assert data["graph_telemetry"]["edge_count"] > 0


# ── 2. Scenario Presets Tests ─────────────────────────────────────────────────

def test_scenarios_endpoint(client):
    """Verifies that /scenarios returns the 4 distinct automotive scenario presets."""
    response = client.get("/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 4
    scenarios = data["scenarios"]
    scenario_ids = [s["id"] for s in scenarios]
    assert "scenario_braking_calibration" in scenario_ids
    assert "scenario_latent_thermal_coupling" in scenario_ids
    assert "scenario_decoy_attack" in scenario_ids
    assert "scenario_inverter_runaway" in scenario_ids

    # Verify each scenario has distinct non-empty payload
    for s in scenarios:
        assert s["artifact_id"]
        assert s["subsystem"]
        assert s["ecu"]
        assert s["after_content"]
        assert s["change_semantics"]
        assert s["purpose"]


# ── 3. Analysis Pipeline Execution Tests ──────────────────────────────────────

def test_analyze_structural_scenario(client):
    """Verifies /analyze executes scenario 1 (Braking Calibration) with structural propagation."""
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void calibrate_aeb_threshold() { aeb_decel_threshold = 7.5; max_ttc = 1.8; }",
        "change_semantics": "Calibrated AEB autonomous emergency braking deceleration threshold to 7.5 m/s^2 and TTC to 1.8s.",
        "force_semantic": False,
        "filter_subsystem": True
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "analysis_id" in data
    assert data["changed_artifact"]["artifact_id"] == "REQ_AEB_001"
    assert data["impact_summary"]["structural_impacts_count"] > 0
    assert len(data["selected_tests"]) > 0
    assert data["safety_gate"]["status"] == "PASS_CLOSED_INVARIANT_SATISFIED"
    assert data["full_graph"] is not None
    assert len(data["full_graph"]["nodes"]) > 0


def test_analyze_semantic_and_rejected_candidates(client):
    """Verifies /analyze exposes accepted vs rejected semantic candidates with explicit rejection reasons."""
    payload = {
        "artifact_id": "REQ_AEB_014",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void process_passenger_infotainment() { stream_audio(); render_spotify_playlist(); }",
        "change_semantics": "Spotify infotainment multimedia playlist streaming service connected to cockpit audio bus.",
        "force_semantic": True,
        "filter_subsystem": True
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "all_semantic_candidates" in data
    assert "accepted_candidates" in data
    assert "rejected_candidates" in data

    # For candidates that are rejected, ensure an explicit rejection_reason is recorded
    for rej in data["rejected_candidates"]:
        assert rej["status"] == "REJECT"
        assert rej["rejection_reason"] != "N/A"
        assert len(rej["rejection_reason"]) > 0


def test_analyze_safety_retention_invariant(client):
    """Verifies that mandatory safety-critical tests are retained unconditionally."""
    payload = {
        "artifact_id": "SWC_InverterControl",
        "artifact_type": "SoftwareComponent",
        "subsystem": "CHASSIS",
        "ecu": "BMS",
        "change_type": "MODIFICATION",
        "after_content": "void emergency_inverter_shutdown() { pwm_disable_all(); open_hv_contactor(); }",
        "change_semantics": "High-voltage inverter safety-critical emergency shutdown procedure.",
        "force_semantic": False,
        "filter_subsystem": True
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["safety_gate"]["invariant_asserted"] is True
    assert data["safety_gate"]["status"] == "PASS_CLOSED_INVARIANT_SATISFIED"
    assert data["test_summary"]["safety_recall_pct"] == 100.0


# ── 4. Validation & Adversarial Input Tests ────────────────────────────────────

def test_analyze_path_traversal_rejection(client):
    """Verifies that path traversal attempts in identifiers are rejected with HTTP 422."""
    payload = {
        "artifact_id": "../../../etc/passwd",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "test",
        "change_semantics": "malicious path injection"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422


def test_analyze_empty_payload_rejection(client):
    """Verifies that empty artifact ID is rejected with HTTP 422."""
    payload = {
        "artifact_id": "",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "test",
        "change_semantics": "empty id"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422


# ── 5. Empirical Benchmarks Endpoint Tests ────────────────────────────────────

def test_benchmarks_endpoint(client):
    """Verifies that /benchmarks returns real CSV evaluation data, verified figures, and limitations."""
    response = client.get("/benchmarks")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["summary_table"]) > 0
    assert "dronology" in data["datasets"]
    assert "defects4j" in data["datasets"]
    assert "autoware" in data["datasets"]
    assert len(data["figures"]) > 0
    assert len(data["limitations"]) > 0

    # Ensure all returned figure URLs start with /plots/
    for fig in data["figures"]:
        assert fig["url"].startswith("/plots/")


# ── 6. Diff Upload and Parser Tests ───────────────────────────────────────────

def test_upload_diff_valid_c_patch(client):
    """Verifies that /upload-diff safely parses a unified C diff and maps to an artifact."""
    diff_text = """
--- a/src/aeb_controller.c
+++ b/src/aeb_controller.c
@@ -45,3 +45,5 @@
 void calibrate_aeb_threshold() {
+    aeb_decel_threshold = 8.0;
+    max_ttc = 2.0;
 }
"""
    response = client.post("/upload-diff", json={"diff_content": diff_text})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "calibrate_aeb_threshold" in data["parsed_summary"]["detected_identifiers"]
    assert data["suggested_request"]["artifact_id"]


def test_upload_diff_malformed_rejection(client):
    """Verifies that an unparseable diff returns HTTP 400."""
    response = client.post("/upload-diff", json={"diff_content": "random noise without functions or files"})
    assert response.status_code == 400


def test_upload_diff_null_byte_rejection(client):
    """Verifies that null byte injection is rejected with HTTP 400."""
    response = client.post("/upload-diff", json={"diff_content": "void test()\x00malicious"})
    assert response.status_code == 400


# ── 7. Audit Cache Retrieval Tests ────────────────────────────────────────────

def test_get_analysis_by_id(client):
    """Verifies that /analysis/{id} retrieves the cached analysis record."""
    # First run an analysis
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "test content",
        "change_semantics": "test semantics"
    }
    post_res = client.post("/analyze", json=payload)
    assert post_res.status_code == 200
    analysis_id = post_res.json()["analysis_id"]

    # Now retrieve via GET
    get_res = client.get(f"/analysis/{analysis_id}")
    assert get_res.status_code == 200
    assert get_res.json()["analysis_id"] == analysis_id


def test_get_analysis_by_id_not_found(client):
    """Verifies that unknown analysis ID returns HTTP 404."""
    response = client.get("/analysis/non_existent_uuid_12345")
    assert response.status_code == 404
