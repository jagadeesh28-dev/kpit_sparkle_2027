# AURA-Impact: Dashboard Baseline Audit (Phase 0)

**Document Version:** 1.0.0  
**Audit Date:** November 21, 2026  
**Auditor:** Principal Systems Architect & Senior QA/Security Engineer  
**Target Event:** KPIT Sparkle 2027 — Round 2 Mentor Review  

---

## 1. Baseline Git & Repository State

- **Active Branch:** `main` (clean working tree, up to date with `origin/main` at commit `15c6c60`).
- **Remotes Verified:**
  - `origin`: `https://github.com/jagadeesh28-dev/kpit_sparkle_2027.git`
  - `mogulkanna`: `https://github.com/Mogulkanna10/kpit_sparkle_2027.git`
  - `upstream`: `https://github.com/yuvanchandar-arch/KPIT_2026_aura_impact.git`
- **Dashboard Ingestion Commit:** `8c172d7` (verified present in Git log).
- **Streamlit Deprecation:** `dashboard/app.py` and the `dashboard/` folder are completely removed.

---

## 2. Independent Baseline Execution Results

### 2.1 Python Baseline Test Suite
- **Command:** `python -m pytest -q`
- **Result:** **256 passed in 18.68s** (100% pass rate).
- **Subsystem Coverage:**
  - `tests/adversarial`: 47 passed
  - `tests/architecture`: 10 passed
  - `tests/benchmarks`: 11 passed
  - `tests/cli`: 10 passed
  - `tests/dashboard`: 8 passed (`tests/dashboard/test_dashboard.py`)
  - `tests/defects4j`: 10 passed
  - `tests/evaluation`: 5 passed
  - `tests/experiments`: 22 passed
  - `tests/graph`: 18 passed
  - `tests/ingestion`: 32 passed
  - `tests/metrics`: 17 passed
  - `tests/public_datasets`: 8 passed
  - `tests/reports`: 9 passed
  - `tests/safety`: 11 passed
  - `tests/semantic`: 38 passed

### 2.2 Frontend Build & TypeScript Checks (`hmi_frontend`)
- **Initial State:** `node_modules` was missing.
- **Dependency Ingestion:** Executed `npm install` (156 packages installed in 27s).
- **TypeScript & Vite Build Command:** `npm run build` (`tsc -b && vite build`)
- **Result:** **PASSED** in 4.09s:
  - `dist/index.html` (0.47 kB)
  - `dist/assets/index-crCTYXS7.css` (38.52 kB)
  - `dist/assets/index-Oxe8hWr_.js` (1,964.23 kB)
  - 0 TypeScript compiler errors.
- **Missing Capabilities:** No unit test runner was configured in `hmi_frontend/package.json`.

---

## 3. Discovered Defects, Gaps & Architectural Weaknesses

| ID | Component | Defect / Architectural Gap | Root Cause | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **DEF-01** | `src/api/server.py` | Direct execution `python src/api/server.py` crashes with `ModuleNotFoundError: No module named 'src'`. | Missing `sys.path.insert(0, str(REPO_ROOT))` at top of file before importing `src.api.pipeline`. | **HIGH** |
| **DEF-02** | `src/api/server.py` | Missing essential REST endpoints: `/scenarios`, `/benchmarks`, `/upload-diff`, `/analysis/{id}`. | Only basic prototype `/analyze` and `/health` were implemented. | **HIGH** |
| **DEF-03** | `hmi_frontend/src/App.tsx` | Analysis request body contains hardcoded `after_content` and `change_semantics` regardless of selected artifact. | Scenario switcher not wired to live backend presets. | **MEDIUM** |
| **DEF-04** | `hmi_frontend/src/Workspace.tsx` | Missing "Empirical Benchmark Evidence" tab. | Public dataset results (Dronology, Defects4J, Autoware, Alexandria) are not exposed in the UI. | **HIGH** |
| **DEF-05** | `hmi_frontend/src/components/CustomNode.tsx` | Missing unified schema node types (`SafetyRequirement`, `ECU`, `Subsystem`, `SourceFile`, `TestCase`, `Defect`, `Commit`). | Only legacy node types were defined in `TYPE_CONFIG`. | **MEDIUM** |
| **DEF-06** | `AURA-Impact — ISO 26262 Impact Analysis HMI.html` | "Run analysis" button is hardcoded `setTimeout()` mock. Does not query live backend. | No `fetch()` logic implemented; standalone HTML was purely offline. | **MEDIUM** |
| **DEF-07** | `hmi_frontend` | Lacks automated frontend test runner. | No Vitest/Jest script in `package.json`. | **MEDIUM** |
| **DEF-08** | `src/api/server.py` | Startup event deprecation warning (`@app.on_event("startup")` deprecated in modern FastAPI). | Needs migration to modern lifespan handler. | **LOW** |

---

## 4. Benchmark & Provenance Audit

- **Raw Datasets:**
  - `data/raw/dronology`: Complete (requirements, code, tests).
  - `data/raw/defects4j/Cli`: 10 historical bug revisions.
  - `data/raw/autoware`: ROS 2 packages (`autoware_vehicle_cmd_gate`, `autoware_control_performance_analysis`).
  - `data/raw/alexandria`: Co-change records JSON.
- **Evaluation Tables:**
  - `results/tables/master_benchmark_summary.csv`
  - `results/tables/dronology_link_deletion.csv`
  - `results/tables/defects4j_rts.csv`
  - `results/tables/autoware_architecture.csv`
  - `results/tables/alexandria_co_change.csv`
- **Publication Figures:** 8 publication figures present in `results/plots/` (`fig01` through `fig08`).
- **Cryptographic Evidence:** `results/evidence/evaluation_master_evidence.json` present.

---

## 5. Action Plan & Readiness for Phase 1-9

1. **Fix `src/api/server.py` import path & modern lifespan.**
2. **Implement full endpoint suite in `src/api/server.py`** (`/health`, `/scenarios`, `/analyze`, `/benchmarks`, `/upload-diff`, `/analysis/{id}`).
3. **Expose rejected semantic candidates and context filter decisions in `/analyze` response.**
4. **Update `hmi_frontend/src/api.ts` with authoritative TypeScript contract.**
5. **Add Scenario Presets, Decoy Inspector, and Empirical Benchmark Evidence tabs to React frontend.**
6. **Wire Standalone HTML HMI with dual-mode live/offline detection.**
7. **Create comprehensive backend, frontend, adversarial, and E2E validation test suites.**
