# AURA-Impact: Dashboard Architectural Audit & Engineering Roadmap

**Document Version:** 1.0.0  
**Target Event:** KPIT Sparkle Round 2 — Online Mentor / Jury Evaluation  
**Author:** THE GOAT (Autonomous Engineering Architecture Team)  
**Date:** November 2026  

---

## 1. Executive Summary & Migration Status

In accordance with the project roadmap and team instructions:
1. **Repository Ingestion:** All dashboard deliverables from `https://github.com/Mogulkanna10/kpit_sparkle_2027` have been integrated into the repository.
2. **Streamlit Deprecation:** The legacy `dashboard/app.py` Streamlit visualizer has been removed.
3. **Backend Integration:** The high-throughput FastAPI server (`src/api/server.py`) has been linked with our canonical `AuraImpactPipeline`.
4. **Verification:** The test suite (`tests/dashboard/test_dashboard.py`) was updated, and all **256 unit/integration tests** pass.
5. **Git Synchronization:** All changes have been committed and pushed to `origin/main` (`commit 8c172d7`).

---

## 2. Ingested Dashboard Architecture

The pulled dashboard consists of **three complementary artifacts**:

```
kpit_sparkle_2027/
├── AURA-Impact — ISO 26262 Impact Analysis HMI.html # [Artifact 1] Standalone Zero-Dependency HMI
├── hmi_frontend/                                   # [Artifact 2] Modern React 19 + ReactFlow Workbench
│   ├── src/
│   │   ├── api.ts                                  # REST Client (Axios -> port 8000)
│   │   ├── App.tsx                                 # Main workbench state orchestration
│   │   └── components/
│   │       ├── CommandBar.tsx                      # Top action bar & artifact selector
│   │       ├── ProjectExplorer.tsx                 # Hierarchical artifact tree navigation
│   │       ├── Workspace.tsx                       # Tabbed view (Graph, Tests, Safety, Traceability)
│   │       ├── CustomNode.tsx                      # Domain-specific ReactFlow node rendering
│   │       ├── PropertiesInspector.tsx             # Node details & ASIL inspector
│   │       └── StatusBar.tsx                       # Latency, ISO 26262 & pipeline telemetry
└── src/api/server.py                               # [Artifact 3] FastAPI REST Backend
```

### Component Breakdown & Strengths

| Component | Technology | Key Capabilities & Strengths |
| :--- | :--- | :--- |
| **Standalone HTML HMI** | Single-file HTML5, CSS3, SVG, Vanilla JS | • **Zero external dependencies:** Opens instantly in any browser without Node or Python.<br>• **Executive-Ready Visuals:** IBM Plex typography, dark/light theme, ASIL badge color coding.<br>• **ISO 26262 Focus:** Native representation of ISO 26262-8 §8 change impact workflows.<br>• **Offline Fallback:** Contains built-in demonstration mock scenarios for offline pitch decks. |
| **React HMI Workbench (`hmi_frontend`)** | React 19, Vite 8, Tailwind CSS, `@xyflow/react` (React Flow 12), `elkjs` | • **Dynamic Graph Layout:** High-performance DAG layout with Elkjs.<br>• **Rich Engineering Views:** Multi-tab layout (Impact Graph, Impact Tree, Test Selection, Safety Matrix, Traceability Matrix, Reports).<br>• **Interactive Inspection:** Clicking any graph node highlights incoming/outgoing dependencies and displays metadata in `PropertiesInspector`.<br>• **Live Backend Hook:** Fully wired to send POST requests to `http://localhost:8000/analyze`. |
| **REST API Server (`src/api/server.py`)** | FastAPI, Uvicorn, NetworkX, Pydantic | • **Canonical Pipeline Binding:** Instantiates `AuraImpactPipeline()` and ingests the demonstration repository on startup.<br>• **CORS-Enabled:** Seamless local communication with Vite frontend on port 5173.<br>• **Structured Payload:** Returns `{ status, report, impacted_nodes, test_nodes, full_graph }`. |

---

## 3. Detailed Gap Analysis (What Needs to Be Added)

While the visual foundation is exceptional, the following critical engineering gaps must be addressed to make it **100% judge-ready** for KPIT Sparkle Round 2:

### Gap 1: Disconnected Empirical Public Dataset Evidence
- **Current State:** The React HMI only displays live single-artifact change scenarios.
- **The Problem:** The core breakthrough of our research is validation on **Dronology (CPS), Defects4J (Historical Bugs), Autoware (Autonomous Driving ROS 2), and Alexandria (Co-change)**. Judges will specifically ask: *"Where are your public dataset benchmark numbers?"*
- **Recommendation:** Add a dedicated **"🔬 Empirical Benchmark Evidence"** tab in `Workspace.tsx` that renders our 8 publication-grade plots (`results/plots/`) and summary tables (`results/tables/master_benchmark_summary.csv`).

### Gap 2: Hardcoded Change Scenario in `App.tsx`
- **Current State:** In `hmi_frontend/src/App.tsx`:
  ```typescript
  const handleRunAnalysis = async (aid?: string) => {
    const result = await runAnalysis({
      artifact_id: id,
      artifact_type: "requirement",
      subsystem: "ADAS",
      ecu: "VCU",
      change_type: "MODIFICATION",
      after_content: "void override_safety_limits() { max_temp = 90; }",
      change_semantics: "Increased maximum temperature limit to 90 degrees.",
      force_semantic: false,
      filter_subsystem: true,
    });
  ```
- **The Problem:** The `after_content` and `change_semantics` are static strings hardcoded in the frontend. When selecting different artifacts in `CommandBar.tsx`, the analysis always submits the same change payload.
- **Recommendation:** Implement a **Scenario Switcher** modal / dropdown in `CommandBar.tsx` that lets the user choose between curated test scenarios:
  1. *Scenario A: Braking Threshold Calibration (Direct Structural)*
  2. *Scenario B: Latent Thermal Coupling (Missing Link Recovered via BGE-M3 Semantic Retrieval)*
  3. *Scenario C: Decoy Injection Attack (Non-Automotive Candidate Filtered Out by Context Gate)*
  4. *Scenario D: Battery Thermal Runaway (Mandatory ASIL-D Safety Test Retention)*

### Gap 3: Missing Node Types in `CustomNode.tsx`
- **Current State:** `CustomNode.tsx` recognizes: `Requirement`, `SoftwareComponent`, `Port`, `Runnable`, `C_Function`, `C_Variable`, `Test`, `ChangeSeed`.
- **The Problem:** Our unified graph schema across public datasets uses additional node types: `SafetyRequirement`, `ECU`, `Subsystem`, `SourceFile`, `TestCase`, `Defect`, `Commit`. When these nodes arrive from the backend, they render with fallback styles.
- **Recommendation:** Expand `TYPE_CONFIG` in `CustomNode.tsx` to handle all unified schema node types with dedicated icons and ASIL color palettes.

### Gap 4: Decoy Rejection & Semantic Filtering Transparency
- **Current State:** The UI shows accepted impacts and selected tests, but does not display rejected candidates.
- **The Problem:** A key requirement of the KPIT Round 2 evaluation is proving that AURA-Impact avoids false positives by filtering out decoys (our Defined Decoy FPR = 0%).
- **Recommendation:** Add a **"Decoy & Semantic Inspector"** sub-panel showing candidates rejected by the Context Filter, explaining *why* they were rejected (e.g., `REJECT_SUBSYSTEM_MISMATCH`, `REJECT_BELOW_SIMILARITY_THRESHOLD < 0.45`).

### Gap 5: Standalone HTML HMI Backend Connectivity
- **Current State:** `"AURA-Impact — ISO 26262 Impact Analysis HMI.html"` uses static arrays (`var N = [...]`) and simulates execution with `setTimeout()`.
- **The Problem:** If judges ask to test a live custom artifact directly in the single-file HMI, it currently does not query `http://localhost:8000/analyze`.
- **Recommendation:** Add a simple `fetch()` call with graceful fallback to the embedded mock data if the backend is offline.

### Gap 6: Exportable Cryptographic Audit Bundle
- **Current State:** The "Export for audit" button does not generate a downloadable file.
- **The Problem:** ISO 26262-8 Clause 8 requires verifiable work products with cryptographic integrity.
- **Recommendation:** Add a one-click button that downloads `evaluation_master_evidence.json` and a formatted audit PDF/HTML report.

---

## 4. Implementation Roadmap for Round 2 Presentation

```mermaid
flowchart TD
    subgraph Phase 1 [Step 1: Backend API Enhancement]
        B1["Expose /scenarios Endpoint in server.py"]
        B2["Expose /benchmarks & /evidence Endpoints"]
        B3["Add /upload-diff Endpoint for live patches"]
    end

    subgraph Phase 2 [Step 2: React HMI Improvements]
        F1["Add Empirical Benchmark Tab in Workspace.tsx"]
        F2["Add Dynamic Scenario Selector in CommandBar.tsx"]
        F3["Add Decoy Rejection Inspector in PropertiesPanel"]
        F4["Add Unified Node Types to CustomNode.tsx"]
    end

    subgraph Phase 3 [Step 3: Standalone HMI & Export]
        H1["Wire Live fetch() into HTML HMI with Offline Fallback"]
        H2["Add 1-Click JSON/PDF Cryptographic Audit Export"]
    end

    Phase 1 --> Phase 2 --> Phase 3
```

---

## 5. Verification & Test Evidence

All 256 test cases in the test suite pass:
- **adversarial:** 47 passed
- **architecture:** 10 passed
- **benchmarks:** 11 passed
- **cli:** 10 passed
- **dashboard:** 8 passed (`tests/dashboard/test_dashboard.py`)
- **defects4j:** 10 passed
- **evaluation:** 5 passed
- **experiments:** 22 passed
- **graph:** 18 passed
- **ingestion:** 32 passed
- **metrics:** 17 passed
- **public_datasets:** 8 passed
- **reports:** 9 passed
- **safety:** 11 passed
- **semantic:** 38 passed
