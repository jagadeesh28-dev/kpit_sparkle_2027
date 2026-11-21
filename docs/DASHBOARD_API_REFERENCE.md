# AURA-Impact: Dashboard REST API Reference

**Service Version:** 2.0.0  
**Host:** `http://localhost:8000` (or configured host)  
**Protocol:** HTTP/1.1 REST (JSON)  

---

## 1. System Health

### `GET /health`
Returns system status, loaded graph nodes, total tests, and public dataset availability.

#### Response `200 OK`
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "architecture": "Architecture B (Strict Union + Safety Gate)",
  "pipeline_ready": true,
  "graph_telemetry": {
    "node_count": 217,
    "edge_count": 314,
    "test_count": 120,
    "indexed_artifacts": 156
  },
  "datasets_available": {
    "dronology": true,
    "defects4j": true,
    "autoware": true,
    "alexandria": true
  },
  "timestamp": 1732204500.12
}
```

---

## 2. Scenario Presets

### `GET /scenarios`
Returns curated automotive demonstration scenario presets.

#### Response `200 OK`
```json
{
  "status": "success",
  "count": 4,
  "scenarios": [
    {
      "id": "scenario_braking_calibration",
      "name": "Scenario 1: Braking Threshold Calibration",
      "category": "Structural Traversal",
      "subsystem": "ADAS",
      "ecu": "VCU",
      "artifact_id": "REQ_AEB_001",
      "artifact_type": "Requirement",
      "change_type": "MODIFICATION",
      "after_content": "void calibrate_aeb_threshold() { ... }",
      "change_semantics": "Calibrated AEB deceleration threshold to 7.5 m/s^2",
      "purpose": "Demonstrates deterministic structural impact propagation...",
      "expected_behavior": "Structural graph coverage complete; directly affected tests selected.",
      "force_semantic": false,
      "filter_subsystem": true
    }
  ]
}
```

---

## 3. Change Impact Analysis

### `POST /analyze`
Executes change impact analysis, contextual semantic recovery, and safety-gated test selection.

#### Request Body
```json
{
  "artifact_id": "REQ_AEB_001",
  "artifact_type": "Requirement",
  "subsystem": "ADAS",
  "ecu": "VCU",
  "change_type": "MODIFICATION",
  "after_content": "void calibrate_aeb_threshold() { aeb_decel_threshold = 7.5; }",
  "change_semantics": "Calibrated AEB deceleration threshold to 7.5 m/s^2",
  "force_semantic": false,
  "filter_subsystem": true,
  "threshold_override": null
}
```

#### Response `200 OK`
```json
{
  "status": "success",
  "analysis_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "timestamp": 1732204505.5,
  "changed_artifact": { ... },
  "impact_summary": {
    "total_impacts_count": 4,
    "structural_impacts_count": 4,
    "semantic_recoveries_count": 0,
    "review_required_count": 0,
    "structural_coverage_complete": true
  },
  "test_summary": {
    "total_tests_available": 120,
    "selected_tests_count": 1,
    "mandatory_safety_tests_count": 1,
    "removed_tests_count": 119,
    "test_reduction_pct": 99.0,
    "safety_recall_pct": 100.0
  },
  "safety_gate": {
    "status": "PASS_CLOSED_INVARIANT_SATISFIED",
    "retained_count": 1,
    "invariant_asserted": true,
    "fail_closed_policy": "ISO-26262-STRICT-RETAIN"
  },
  "latencies": {
    "stage1_ms": 0.045,
    "stage2_ms": 0.046,
    "total_ms": 0.091
  },
  "impacted_nodes": [ ... ],
  "all_semantic_candidates": [ ... ],
  "accepted_candidates": [ ... ],
  "rejected_candidates": [ ... ],
  "selected_tests": [ ... ],
  "safety_tests": [ ... ],
  "full_graph": { "nodes": [ ... ], "links": [ ... ] }
}
```

#### Error Responses
- `422 Unprocessable Entity`: Input validation failure (empty artifact ID, path traversal attempt, threshold out of bounds).
- `500 Internal Server Error`: Pipeline execution failure.

---

## 4. Empirical Benchmarks

### `GET /benchmarks`
Reads and returns real empirical benchmark summary tables and verified publication figures.

#### Response `200 OK`
```json
{
  "status": "success",
  "summary_table": [
    {
      "Dataset": "Dronology (CPS Traceability)",
      "Evaluation_Task": "Controlled Link Deletion (10-30%)",
      "AURA_Impact_Recall": "1.0",
      "Graph_Only_Recall": "0.2222",
      "Embedding_Only_Recall": "1.0",
      "AURA_F1": "0.217",
      "Safety_Retention": "100.0%",
      "Mean_Latency_ms": "0.186"
    }
  ],
  "datasets": { ... },
  "figures": [
    {
      "id": "fig01",
      "name": "Precision, Recall, and F1 across Baselines",
      "file": "fig01_precision_recall_f1.png",
      "url": "/plots/fig01_precision_recall_f1.png"
    }
  ],
  "evidence_provenance": {
    "evaluation_timestamp": "...",
    "git_commit": "...",
    "sha256": "..."
  },
  "limitations": [ ... ]
}
```

---

## 5. Diff Upload & Parser

### `POST /upload-diff`
Parses a submitted Git diff or C/C++ patch and maps it to a repository graph node.

#### Request Body
```json
{
  "diff_content": "--- a/src/aeb.c\n+++ b/src/aeb.c\n@@ -10,3 +10,4 @@\n void calibrate_aeb_threshold() {\n+ aeb_threshold = 8.0;\n }",
  "subsystem": "ADAS",
  "ecu": "VCU"
}
```

#### Response `200 OK`
```json
{
  "status": "success",
  "parsed_summary": {
    "changed_files": ["src/aeb.c"],
    "detected_identifiers": ["calibrate_aeb_threshold"],
    "mapped_artifact_id": "calibrate_aeb_threshold",
    "inferred_type": "C_Function",
    "subsystem": "ADAS",
    "ecu": "VCU"
  },
  "suggested_request": { ... }
}
```

---

## 6. Historical Analysis Retrieval

### `GET /analysis/{analysis_id}`
Retrieves a previously executed analysis trace by UUID.

- `200 OK`: Returns cached analysis record.
- `404 Not Found`: Analysis ID expired or not found.
