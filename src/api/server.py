"""
AURA-Impact Production REST API Backend Server
KPIT Sparkle 2027 — Engineering HMI Workbench Service

Provides:
- GET  /health: System health, graph telemetry, dataset availability
- GET  /scenarios: Structured automotive change presets
- POST /analyze: Canonical change impact analysis with two-stage resolution,
                 contextual candidate rejection tracking, and safety gate invariant
- GET  /benchmarks: Verified public dataset empirical evaluation metrics & plots
- POST /upload-diff: Safe Git diff and C/C++ patch parser and artifact mapper
- GET  /analysis/{analysis_id}: Historical analysis audit retrieval
"""
import sys
from pathlib import Path

# Ensure repository root is on sys.path regardless of execution method
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import csv
import json
import time
import uuid
import re
from typing import Dict, Any, List, Optional, Set
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, field_validator
import networkx as nx

from src.api.pipeline import AuraImpactPipeline
from src.ingestion.git_diff import ChangedArtifact
from src.testing.safety_gate import SafetyInvariantViolationError


# In-memory LRU ring buffer for audit traces
ANALYSIS_CACHE: Dict[str, Dict[str, Any]] = {}
MAX_CACHE_SIZE = 50

# Global canonical pipeline instance
pipeline = AuraImpactPipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern lifespan handler for FastAPI startup and shutdown."""
    default_repo = REPO_ROOT / "data" / "demonstration_dataset"
    if not default_repo.exists():
        default_repo = REPO_ROOT / "examples" / "demo_repo"
    if default_repo.exists():
        pipeline.ingest_repository(default_repo)
    yield
    # Cleanup on shutdown if needed
    ANALYSIS_CACHE.clear()


app = FastAPI(
    title="AURA-Impact Production REST API",
    description="Context-Aware Change Impact and Regression Intelligence for Automotive Software Engineering",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware for local Vite frontend and standalone HMI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount publication plots as static files if directory exists
plots_dir = REPO_ROOT / "results" / "plots"
if plots_dir.exists():
    app.mount("/plots", StaticFiles(directory=str(plots_dir)), name="plots")


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class ChangeRequest(BaseModel):
    artifact_id: str = Field(..., min_length=1, max_length=128, description="Target artifact identifier")
    artifact_type: str = Field("Requirement", min_length=1, max_length=64, description="Artifact type")
    subsystem: str = Field("ADAS", min_length=1, max_length=64, description="Vehicle subsystem (e.g. ADAS, POWERTRAIN, CHASSIS)")
    ecu: str = Field("VCU", min_length=1, max_length=64, description="Target ECU (e.g. VCU, BMS, ZONE_CONTROLLER)")
    change_type: str = Field("MODIFICATION", min_length=1, max_length=32, description="Change classification (MODIFICATION, DELETION, ADDITION)")
    after_content: str = Field(..., max_length=65536, description="Source code or specification content after modification")
    change_semantics: str = Field(..., max_length=4096, description="Natural language semantic description of the engineering change")
    force_semantic: bool = Field(False, description="Whether to bypass graph completeness check and force semantic retrieval")
    filter_subsystem: bool = Field(True, description="Enforce strict subsystem context isolation in semantic search")
    threshold_override: Optional[float] = Field(None, ge=0.0, le=1.0, description="Optional cosine similarity threshold override")

    @field_validator("artifact_id", "subsystem", "ecu")
    @classmethod
    def prevent_path_traversal(cls, v: str) -> str:
        if ".." in v or "/" in v or "\\" in v:
            raise ValueError("Identifier must not contain path traversal characters")
        return v.strip()


class DiffUploadRequest(BaseModel):
    diff_content: str = Field(..., min_length=5, max_length=262144, description="Unified Git diff or C/C++ patch (max 256 KB)")
    subsystem: Optional[str] = Field("ADAS", max_length=64)
    ecu: Optional[str] = Field("VCU", max_length=64)


# =============================================================================
# CURATED SCENARIOS
# =============================================================================

SCENARIO_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "scenario_braking_calibration",
        "name": "Scenario 1: Braking Threshold Calibration",
        "category": "Structural Traversal",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "artifact_id": "REQ_AEB_001",
        "artifact_type": "Requirement",
        "change_type": "MODIFICATION",
        "after_content": "void calibrate_aeb_threshold() {\n    aeb_decel_threshold = 7.5; // m/s^2\n    max_ttc = 1.8; // seconds\n}",
        "change_semantics": "Calibrated AEB autonomous emergency braking deceleration threshold to 7.5 m/s^2 and TTC to 1.8s.",
        "purpose": "Demonstrates deterministic structural impact propagation across call graph and ARXML ports without requiring semantic fallback.",
        "expected_behavior": "Structural graph coverage is complete; semantic fallback is not triggered; directly affected software components and tests are selected.",
        "force_semantic": False,
        "filter_subsystem": True
    },
    {
        "id": "scenario_latent_thermal_coupling",
        "name": "Scenario 2: Latent Thermal Coupling",
        "category": "Semantic Recovery",
        "subsystem": "POWERTRAIN",
        "ecu": "VCU",
        "artifact_id": "REQ_BMS_004",
        "artifact_type": "Requirement",
        "change_type": "MODIFICATION",
        "after_content": "void override_thermal_derating() {\n    cell_temp_ceiling = 95.0; // Celsius\n    coolant_pump_duty = 85.0; // Percent\n}",
        "change_semantics": "Increased battery cell maximum operating temperature ceiling to 95C and adjusted coolant pump duty cycle.",
        "purpose": "Demonstrates semantic dependency recovery when explicit static graph links are missing or undocumented.",
        "expected_behavior": "Graph traversal is incomplete; BGE-M3 semantic retrieval recovers related thermal mitigation runnables and requirements.",
        "force_semantic": True,
        "filter_subsystem": True
    },
    {
        "id": "scenario_decoy_attack",
        "name": "Scenario 3: Non-Automotive Decoy Attack",
        "category": "Contextual Rejection",
        "subsystem": "ADAS",
        "ecu": "VCU",
        "artifact_id": "REQ_AEB_014",
        "artifact_type": "Requirement",
        "change_type": "MODIFICATION",
        "after_content": "void process_passenger_infotainment() {\n    stream_audio();\n    render_spotify_playlist();\n}",
        "change_semantics": "Spotify infotainment multimedia playlist streaming service connected to cockpit audio bus.",
        "purpose": "Demonstrates contextual filtering of irrelevant non-automotive semantic candidates (0% False Positive Rate on decoys).",
        "expected_behavior": "Semantic retriever flags candidates, but ContextFilter rejects infotainment candidates with REJECT_SUBSYSTEM_MISMATCH.",
        "force_semantic": True,
        "filter_subsystem": True
    },
    {
        "id": "scenario_inverter_runaway",
        "name": "Scenario 4: High-Voltage Inverter Runaway",
        "category": "Safety Invariant Retention",
        "subsystem": "CHASSIS",
        "ecu": "BMS",
        "artifact_id": "SWC_InverterControl",
        "artifact_type": "SoftwareComponent",
        "change_type": "MODIFICATION",
        "after_content": "void emergency_inverter_shutdown() {\n    pwm_disable_all();\n    open_hv_contactor();\n    assert_safe_torque_off();\n}",
        "change_semantics": "High-voltage inverter safety-critical emergency shutdown procedure and contactor isolation routine.",
        "purpose": "Demonstrates non-bypassable mandatory ASIL-D safety test retention even under aggressive test suite optimization.",
        "expected_behavior": "Safety Gate activates fail-closed invariant; 100% of critical ASIL-D test cases are retained in the selected regression suite.",
        "force_semantic": False,
        "filter_subsystem": True
    }
]


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health", tags=["System"])
async def health_check():
    """Returns system status, loaded graph nodes, tests, and dataset availability."""
    node_count = len(pipeline.graph.graph.nodes) if pipeline.graph else 0
    edge_count = len(pipeline.graph.graph.edges) if pipeline.graph else 0
    test_count = len(pipeline.all_tests)

    # Check public dataset presence
    data_dir = REPO_ROOT / "data" / "raw"
    datasets_status = {
        "dronology": (data_dir / "dronology").exists(),
        "defects4j": (data_dir / "defects4j").exists(),
        "autoware": (data_dir / "autoware").exists(),
        "alexandria": (data_dir / "alexandria").exists()
    }

    return {
        "status": "healthy",
        "version": "2.0.0",
        "architecture": "Architecture B (Strict Union + Safety Gate)",
        "pipeline_ready": node_count > 0,
        "graph_telemetry": {
            "node_count": node_count,
            "edge_count": edge_count,
            "test_count": test_count,
            "indexed_artifacts": getattr(pipeline.index, "total_artifacts", 0)
        },
        "datasets_available": datasets_status,
        "timestamp": time.time()
    }


@app.get("/scenarios", tags=["Scenarios"])
async def get_scenarios():
    """Returns curated demonstration scenario presets with explicit payloads and expected behavior."""
    return {
        "status": "success",
        "count": len(SCENARIO_PRESETS),
        "scenarios": SCENARIO_PRESETS
    }


@app.post("/analyze", tags=["Analysis"])
async def analyze_change(request: ChangeRequest):
    """Executes change impact analysis, contextual semantic recovery, and safety-gated test selection."""
    try:
        change_obj = ChangedArtifact(
            artifact_id=request.artifact_id,
            artifact_type=request.artifact_type,
            subsystem=request.subsystem,
            ecu=request.ecu,
            change_type=request.change_type,
            after_content=request.after_content,
            change_semantics=request.change_semantics,
            metadata={
                "force_semantic": request.force_semantic,
                "filter_subsystem_in_index": request.filter_subsystem
            }
        )

        impact_res, test_res, report = pipeline.analyze_change(
            change=change_obj,
            threshold_override=request.threshold_override,
            force_semantic=request.force_semantic
        )

        # Separate accepted vs rejected vs review semantic candidates
        all_candidates = []
        accepted_candidates = []
        rejected_candidates = []
        review_required_candidates = []

        for cand in getattr(impact_res, "all_semantic_candidates", []):
            cand_dict = {
                "artifact_id": cand.artifact_id,
                "artifact_type": cand.artifact_type,
                "subsystem": cand.subsystem,
                "ecu": cand.ecu,
                "similarity_score": round(float(cand.similarity_score), 4),
                "context_score": round(float(cand.context_score), 4),
                "status": cand.status,
                "rejection_reason": cand.rejection_reason or "N/A",
                "source_file": cand.source_file
            }
            all_candidates.append(cand_dict)
            if cand.status == "ACCEPT":
                accepted_candidates.append(cand_dict)
            elif cand.status == "REJECT":
                rejected_candidates.append(cand_dict)
            elif cand.status == "REVIEW_REQUIRED":
                review_required_candidates.append(cand_dict)

        # Format selected tests
        formatted_tests = []
        for t in getattr(test_res, "selected_tests", []):
            formatted_tests.append({
                "test_id": t.test_id,
                "description": t.description,
                "safety_class": t.safety_class,
                "subsystem": t.subsystem,
                "mapped_from_artifact": t.mapped_from_artifact,
                "mapping_source": t.mapping_source,
                "source_file": t.source_file
            })

        formatted_safety_tests = []
        for t in getattr(test_res, "safety_tests", []):
            formatted_safety_tests.append({
                "test_id": t.test_id,
                "description": t.description,
                "safety_class": t.safety_class,
                "subsystem": t.subsystem,
                "mapped_from_artifact": t.mapped_from_artifact,
                "mapping_source": t.mapping_source
            })

        # Build full graph node-link payload
        graph_data = None
        if pipeline.graph and pipeline.graph.graph:
            g = pipeline.graph.graph
            impacted_set = set(i.artifact_id for i in getattr(impact_res, "final_impacts", []))
            nodes_payload = []
            for n_id, attrs in g.nodes(data=True):
                nodes_payload.append({
                    "id": str(n_id),
                    "type": str(attrs.get("type", "Unknown")),
                    "name": str(attrs.get("name", n_id)),
                    "subsystem": str(attrs.get("subsystem", "ADAS")),
                    "ecu": str(attrs.get("ecu", "VCU")),
                    "safety_level": str(attrs.get("safety_level", "QM")),
                    "isImpacted": n_id in impacted_set,
                    "isSeed": n_id == request.artifact_id
                })

            links_payload = []
            for u, v, attrs in g.edges(data=True):
                links_payload.append({
                    "source": str(u),
                    "target": str(v),
                    "relation": str(attrs.get("relation", "DEPENDS_ON")),
                    "provenance": str(attrs.get("provenance", "Static Analysis"))
                })
            graph_data = {"nodes": nodes_payload, "links": links_payload}

        analysis_id = str(uuid.uuid4())
        response_payload = {
            "status": "success",
            "analysis_id": analysis_id,
            "timestamp": time.time(),
            "changed_artifact": {
                "artifact_id": request.artifact_id,
                "artifact_type": request.artifact_type,
                "subsystem": request.subsystem,
                "ecu": request.ecu,
                "change_type": request.change_type
            },
            "impact_summary": {
                "total_impacts_count": len(getattr(impact_res, "final_impacts", [])),
                "structural_impacts_count": len(getattr(impact_res, "structural_impacts", [])),
                "semantic_recoveries_count": len(getattr(impact_res, "semantic_impacts", [])),
                "review_required_count": len(review_required_candidates),
                "structural_coverage_complete": getattr(impact_res, "structural_coverage_complete", True)
            },
            "test_summary": {
                "total_tests_available": getattr(test_res, "all_tests_count", len(pipeline.all_tests)),
                "selected_tests_count": len(formatted_tests),
                "mandatory_safety_tests_count": len(formatted_safety_tests),
                "removed_tests_count": getattr(test_res, "removed_tests_count", 0),
                "test_reduction_pct": round(float(getattr(test_res, "test_reduction_pct", 0.0)), 2),
                "safety_recall_pct": round(float(getattr(test_res, "safety_recall_pct", 100.0)), 2)
            },
            "safety_gate": {
                "status": "PASS_CLOSED_INVARIANT_SATISFIED",
                "retained_count": len(formatted_safety_tests),
                "invariant_asserted": True,
                "fail_closed_policy": "ISO-26262-STRICT-RETAIN"
            },
            "latencies": {
                "stage1_ms": round(float(getattr(impact_res, "stage1_latency_ms", 0.0)), 3),
                "stage2_ms": round(float(getattr(impact_res, "stage2_latency_ms", 0.0)), 3),
                "total_ms": round(float(getattr(impact_res, "total_latency_ms", 0.0)), 3)
            },
            "impacted_nodes": jsonable_encoder(getattr(impact_res, "final_impacts", [])),
            "all_semantic_candidates": all_candidates,
            "accepted_candidates": accepted_candidates,
            "rejected_candidates": rejected_candidates,
            "review_required_candidates": review_required_candidates,
            "selected_tests": formatted_tests,
            "safety_tests": formatted_safety_tests,
            "report": jsonable_encoder(report),
            "full_graph": graph_data
        }

        # Cache response in ring buffer
        if len(ANALYSIS_CACHE) >= MAX_CACHE_SIZE:
            oldest_key = next(iter(ANALYSIS_CACHE))
            del ANALYSIS_CACHE[oldest_key]
        ANALYSIS_CACHE[analysis_id] = response_payload

        return response_payload

    except SafetyInvariantViolationError as sve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Safety Gate Invariant Violation: {str(sve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline Analysis Failure: {str(e)}"
        )


@app.get("/benchmarks", tags=["Benchmarks"])
async def get_benchmarks():
    """Reads and returns real empirical benchmark summary tables and available publication figures."""
    pub_tables_dir = REPO_ROOT / "results" / "tables"
    master_sum_path = pub_tables_dir / "master_benchmark_summary.csv"

    summary_rows = []
    if master_sum_path.exists():
        with open(master_sum_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            summary_rows = list(reader)

    # Dataset-specific tables
    datasets_evidence: Dict[str, Any] = {}
    for ds_name, filename in [
        ("dronology", "dronology_link_deletion.csv"),
        ("defects4j", "defects4j_rts.csv"),
        ("autoware", "autoware_architecture.csv"),
        ("alexandria", "alexandria_co_change.csv")
    ]:
        p = pub_tables_dir / filename
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                datasets_evidence[ds_name] = list(csv.DictReader(f))
        else:
            datasets_evidence[ds_name] = []

    # Available publication figures
    figure_manifest = [
        {"id": "fig01", "name": "Precision, Recall, and F1 across Baselines", "file": "fig01_precision_recall_f1.png", "url": "/plots/fig01_precision_recall_f1.png"},
        {"id": "fig02", "name": "Traceability Recovery Under Controlled Link Deletion", "file": "fig02_hidden_dependency_recovery_by_rate.png", "url": "/plots/fig02_hidden_dependency_recovery_by_rate.png"},
        {"id": "fig03", "name": "Decoy False Positive Rate Suppression", "file": "fig03_false_positive_rate_comparison.png", "url": "/plots/fig03_false_positive_rate_comparison.png"},
        {"id": "fig04", "name": "Triggering Test Recall vs Test Suite Reduction on Defects4J", "file": "fig04_regression_test_selection_and_reduction.png", "url": "/plots/fig04_regression_test_selection_and_reduction.png"},
        {"id": "fig05", "name": "Safety-Critical Test Retention Invariant Verification", "file": "fig05_safety_test_retention_invariant.png", "url": "/plots/fig05_safety_test_retention_invariant.png"},
        {"id": "fig06", "name": "Execution Latency Comparison across Methods", "file": "fig06_execution_latency_comparison.png", "url": "/plots/fig06_execution_latency_comparison.png"},
        {"id": "fig07", "name": "Architectural Component Contribution Ablation", "file": "fig07_architecture_ablation_study.png", "url": "/plots/fig07_architecture_ablation_study.png"},
        {"id": "fig08", "name": "Cross-Dataset Empirical Comparison Matrix", "file": "fig08_dataset_cross_comparison.png", "url": "/plots/fig08_dataset_cross_comparison.png"}
    ]

    verified_figures = []
    for fig in figure_manifest:
        fig_path = REPO_ROOT / "results" / "plots" / fig["file"]
        if fig_path.exists():
            verified_figures.append(fig)

    # Master cryptographic evidence JSON
    ev_path = REPO_ROOT / "results" / "evidence" / "evaluation_master_evidence.json"
    ev_meta = {}
    if ev_path.exists():
        try:
            with open(ev_path, "r", encoding="utf-8") as f:
                full_ev = json.load(f)
                ev_meta = {
                    "evaluation_timestamp": full_ev.get("evaluation_timestamp"),
                    "git_commit": full_ev.get("git_commit"),
                    "sha256": full_ev.get("sha256_audit_hash")
                }
        except Exception:
            pass

    return {
        "status": "success",
        "summary_table": summary_rows,
        "datasets": datasets_evidence,
        "figures": verified_figures,
        "evidence_provenance": ev_meta,
        "limitations": [
            "Controlled trace-link deletions on Dronology are synthetic missing-link experiments, not organic undocumented links.",
            "Historical co-change mining on Alexandria is a statistical proxy for semantic relatedness, not proven call graph dependency.",
            "100% safety test retention verifies an architectural invariant enforcement check; it does not claim formal ISO 26262 certification.",
            "Autoware evaluation targets core ROS 2 AEB and Vehicle Command Gate control packages, not full autonomous driving stacks."
        ]
    }


@app.post("/upload-diff", tags=["Analysis"])
async def upload_diff(request: DiffUploadRequest):
    """Safely parses a submitted Git unified diff or C/C++ patch, identifies changed artifacts, and maps them to graph nodes."""
    raw = request.diff_content.strip()

    # Security: check for null bytes or excessive length
    if "\x00" in raw:
        raise HTTPException(status_code=400, detail="Malformed diff: null byte detected")
    if len(raw) > 262144:
        raise HTTPException(status_code=413, detail="Diff payload exceeds maximum allowable size (256 KB)")

    # Extract changed files from unified diff headers
    changed_files = re.findall(r'^(?:---|\+\+\+)\s+[ab]/(.+)$', raw, flags=re.MULTILINE)
    # Extract changed C function definitions
    changed_functions = re.findall(r'^[+\- ]*(?:void|int|bool|float|double|uint32_t|int32_t)\s+([A-Za-z0-9_]+)\s*\(', raw, flags=re.MULTILINE)
    # Extract requirement or component tokens
    artifact_tokens = re.findall(r'(REQ_[A-Za-z0-9_]+|SWC_[A-Za-z0-9_]+)', raw)

    candidates = list(dict.fromkeys(changed_functions + artifact_tokens))

    # Match against loaded graph nodes
    matched_artifact = None
    if pipeline.graph and pipeline.graph.graph:
        g = pipeline.graph.graph
        for c in candidates:
            if c in g:
                matched_artifact = c
                break

    if not matched_artifact:
        # Default to first candidate if found, else reject
        if candidates:
            matched_artifact = candidates[0]
        else:
            raise HTTPException(
                status_code=400,
                detail="Unable to safely parse a valid C/C++ function or requirement identifier from the provided diff."
            )

    node_type = "Requirement" if "REQ_" in matched_artifact else ("SoftwareComponent" if "SWC_" in matched_artifact else "C_Function")

    return {
        "status": "success",
        "parsed_summary": {
            "changed_files": list(set(changed_files)),
            "detected_identifiers": candidates,
            "mapped_artifact_id": matched_artifact,
            "inferred_type": node_type,
            "subsystem": request.subsystem or "ADAS",
            "ecu": request.ecu or "VCU"
        },
        "suggested_request": {
            "artifact_id": matched_artifact,
            "artifact_type": node_type,
            "subsystem": request.subsystem or "ADAS",
            "ecu": request.ecu or "VCU",
            "change_type": "MODIFICATION",
            "after_content": raw[:2000],
            "change_semantics": f"Engineering diff modification affecting {matched_artifact}",
            "force_semantic": False,
            "filter_subsystem": True
        }
    }


@app.get("/analysis/{analysis_id}", tags=["Analysis"])
async def get_analysis_by_id(analysis_id: str):
    """Retrieves previously computed analysis audit record from the in-memory cache."""
    if analysis_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail=f"Analysis ID {analysis_id} not found in audit cache")
    return ANALYSIS_CACHE[analysis_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
