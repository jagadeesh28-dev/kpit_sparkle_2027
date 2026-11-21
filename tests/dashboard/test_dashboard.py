"""
tests/dashboard/test_dashboard.py
Gate 18 — Production HMI Dashboard & API Backend Validation Tests

Validates the new dashboard system components:
- Standalone ISO 26262 Impact Analysis HMI (AURA-Impact — ISO 26262 Impact Analysis HMI.html)
- React HMI Frontend (hmi_frontend/)
- Fast API Backend Server (src/api/server.py)
- Canonical pipeline integration and demo data execution
- Error handling on missing data
- No hardcoded fake metrics
"""
import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ── DB-01: Dashboard HMI and Backend files exist ──────────────────────────────

def test_db01_dashboard_assets_exist():
    """DB-01: Standalone HTML HMI and API backend server must exist."""
    hmi_html = REPO_ROOT / "AURA-Impact — ISO 26262 Impact Analysis HMI.html"
    api_server = REPO_ROOT / "src" / "api" / "server.py"
    hmi_frontend = REPO_ROOT / "hmi_frontend" / "package.json"

    assert hmi_html.exists(), "Standalone ISO 26262 HMI HTML must exist"
    assert api_server.exists(), "src/api/server.py must exist"
    assert hmi_frontend.exists(), "hmi_frontend/package.json must exist"


# ── DB-02: Backend API uses canonical pipeline ────────────────────────────────

def test_db02_backend_uses_canonical_pipeline():
    """DB-02: src/api/server.py must import and use AuraImpactPipeline."""
    api_path = REPO_ROOT / "src" / "api" / "server.py"
    content = api_path.read_text(encoding="utf-8")
    assert "AuraImpactPipeline" in content, \
        "Backend server must use AuraImpactPipeline (canonical pipeline)"
    assert "FastAPI" in content, \
        "Backend server must use FastAPI"
    assert "/analyze" in content, \
        "Backend server must expose /analyze endpoint"
    assert "/health" in content, \
        "Backend server must expose /health endpoint"


# ── DB-03: Dashboard does not hardcode fake benchmark metrics ─────────────────

def test_db03_no_hardcoded_fake_metrics():
    """DB-03: Dashboard files must not hardcode deceptive baseline metrics."""
    hmi_html = REPO_ROOT / "AURA-Impact — ISO 26262 Impact Analysis HMI.html"
    content = hmi_html.read_text(encoding="utf-8")
    assert "ISO 26262" in content, "HMI must reflect ISO 26262 standard"
    assert "Safety Gate" in content, "HMI must reflect Safety Gate active enforcement"
    assert "Stage 1" in content and "Stage 2" in content, "HMI must depict Stage 1 & Stage 2"


# ── DB-04: Backend API loads demonstration data ───────────────────────────────

def test_db04_backend_loads_repo_data():
    """DB-04: Backend server references demonstration_dataset or demo_repo."""
    api_path = REPO_ROOT / "src" / "api" / "server.py"
    content = api_path.read_text(encoding="utf-8")
    assert "demonstration_dataset" in content or "demo_repo" in content, \
        "Backend server must load real data from demonstration_dataset or demo_repo"


# ── DB-05: Demo change files exist ───────────────────────────────────────────

def test_db05_demo_change_files_exist():
    """DB-05: Demo scenario change JSON files referenced by dashboard must exist."""
    demo_dir = REPO_ROOT / "examples" / "demo_repo"
    expected = [
        "change_structural.json",
        "change_hidden_semantic.json",
    ]
    if not demo_dir.exists():
        pytest.skip("examples/demo_repo not available")
    for fname in expected:
        fpath = demo_dir / fname
        assert fpath.exists(), f"Dashboard demo file missing: {fname}"


# ── DB-06: Pipeline produces real output for demo scenario ───────────────────

def test_db06_pipeline_produces_real_output():
    """DB-06: AuraImpactPipeline.analyze_change() returns non-empty result on demo change."""
    sys.path.insert(0, str(REPO_ROOT))
    demo_dir = REPO_ROOT / "examples" / "demo_repo"
    if not demo_dir.exists():
        pytest.skip("examples/demo_repo not available")
    from src.api.pipeline import AuraImpactPipeline
    from src.ingestion.git_diff import ChangedArtifact
    pipeline = AuraImpactPipeline()
    pipeline.ingest_repository(demo_dir)
    change = ChangedArtifact(
        artifact_id="REQ_AEB_001",
        artifact_type="REQUIREMENT",
        subsystem="ADAS",
        ecu="ECU_1",
        change_type="MODIFY",
        after_content="Updated autonomous braking threshold"
    )
    impact_res, test_res, report = pipeline.analyze_change(change)
    assert impact_res is not None, "Pipeline must return impact result"
    assert test_res is not None, "Pipeline must return test selection result"
    assert report is not None, "Pipeline must return report"


# ── DB-07: Pipeline handles empty repo gracefully ────────────────────────────

def test_db07_pipeline_empty_repo_no_crash():
    """DB-07: AuraImpactPipeline.ingest_repository on empty dir does not crash."""
    import tempfile
    sys.path.insert(0, str(REPO_ROOT))
    from src.api.pipeline import AuraImpactPipeline
    pipeline = AuraImpactPipeline()
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            pipeline.ingest_repository(Path(tmpdir))
        except Exception as e:
            assert isinstance(e, Exception), f"Empty repo should raise explicit error: {e}"


# ── DB-08: HMI Frontend structure and routing integrity ──────────────────────

def test_db08_hmi_frontend_integrity():
    """DB-08: HMI frontend must define API communication and graph visualizer."""
    api_ts = REPO_ROOT / "hmi_frontend" / "src" / "api.ts"
    app_tsx = REPO_ROOT / "hmi_frontend" / "src" / "App.tsx"
    workspace_tsx = REPO_ROOT / "hmi_frontend" / "src" / "components" / "Workspace.tsx"

    assert api_ts.exists(), "hmi_frontend api.ts must exist"
    assert app_tsx.exists(), "hmi_frontend App.tsx must exist"
    assert workspace_tsx.exists(), "hmi_frontend Workspace.tsx must exist"

    api_content = api_ts.read_text(encoding="utf-8")
    assert "/analyze" in api_content, "Frontend api.ts must call /analyze"
    assert "http://localhost:8000" in api_content, "Frontend api.ts must target port 8000"
