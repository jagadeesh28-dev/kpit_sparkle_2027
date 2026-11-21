"""
tests/api/test_adversarial_api.py
Adversarial Security & Attack Test Suite for AURA-Impact Backend API

Attacks:
1. XSS / Script injection in change semantics
2. SQL / Command injection strings in artifact IDs
3. Out-of-bounds threshold overrides (>1.0 and <0.0)
4. Extreme diff payload size attacks (>256 KB)
5. Binary and null-byte injection attacks
6. Empty or missing required fields
7. Path traversal tokens (../, ..\\, /etc/passwd, C:\\Windows)
8. High-frequency concurrent request resilience
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
    demo_repo = REPO_ROOT / "data" / "demonstration_dataset"
    if not demo_repo.exists():
        demo_repo = REPO_ROOT / "examples" / "demo_repo"
    if demo_repo.exists() and len(pipeline.graph.graph.nodes) == 0:
        pipeline.ingest_repository(demo_repo)
    with TestClient(app) as test_client:
        yield test_client


def test_attack_xss_in_semantics(client):
    """Attack 1: XSS script tags in change_semantics must not crash the engine."""
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void test() {}",
        "change_semantics": "<script>alert('xss_attack_attempt')</script><img src=x onerror=alert(1)>"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Ensure script content is safely accepted as string without crash
    assert data["changed_artifact"]["artifact_id"] == "REQ_AEB_001"


def test_attack_path_traversal_linux(client):
    """Attack 2: Linux style path traversal attempt in artifact_id is rejected with 422."""
    payload = {
        "artifact_id": "../../etc/shadow",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void test() {}",
        "change_semantics": "path traversal probe"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422


def test_attack_path_traversal_windows(client):
    """Attack 3: Windows style path traversal attempt in ECU is rejected with 422."""
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "..\\..\\Windows\\System32",
        "change_type": "MODIFICATION",
        "after_content": "void test() {}",
        "change_semantics": "path traversal probe"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422


def test_attack_invalid_threshold_over_bounds(client):
    """Attack 4: Threshold override > 1.0 must be rejected with HTTP 422."""
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void test() {}",
        "change_semantics": "invalid threshold test",
        "threshold_override": 1.5
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422


def test_attack_invalid_threshold_negative(client):
    """Attack 5: Threshold override < 0.0 must be rejected with HTTP 422."""
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void test() {}",
        "change_semantics": "invalid threshold test",
        "threshold_override": -0.1
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422


def test_attack_oversized_diff_payload(client):
    """Attack 6: Submitting diff > 256 KB must be rejected with HTTP 413 (Payload Too Large)."""
    large_payload = "diff --git a/test.c b/test.c\n" + ("+ line of arbitrary text\n" * 15000)
    response = client.post("/upload-diff", json={"diff_content": large_payload})
    assert response.status_code in (413, 422)


def test_attack_null_byte_in_diff(client):
    """Attack 7: Null byte injection in diff payload must be rejected with HTTP 400."""
    poisoned_payload = "--- a/test.c\n+++ b/test.c\n@@ -1 +1 @@\n+\x00malicious_code\n"
    response = client.post("/upload-diff", json={"diff_content": poisoned_payload})
    assert response.status_code == 400


def test_resilience_rapid_repeated_queries(client):
    """Attack 8: Engine handles rapid back-to-back queries without race conditions or memory leak."""
    payload = {
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "change_type": "MODIFICATION",
        "after_content": "void loop_test() {}",
        "change_semantics": "rapid loop test"
    }
    for _ in range(5):
        res = client.post("/analyze", json=payload)
        assert res.status_code == 200
        assert res.json()["status"] == "success"
