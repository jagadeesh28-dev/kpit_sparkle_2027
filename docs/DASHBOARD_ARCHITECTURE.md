# AURA-Impact: Dashboard Architecture & Data Flow Specification

**Document Version:** 2.0.0  
**Target:** KPIT Sparkle 2027 — Round 2 Engineering Demonstrator  
**Authors:** THE GOAT (Systems Architecture & Software Engineering Team)  
**Date:** November 2026  

---

## 1. Architectural Philosophy

The AURA-Impact dashboard is an automotive engineering workbench built around the core research tenet:
$$\text{PROVE} \longrightarrow \text{RECOVER} \longrightarrow \text{FILTER} \longrightarrow \text{PROTECT}$$

The dashboard represents the end-to-end pipeline:

```
[ Engineering Change Input ]
             │
             ▼
[ Git Diff / ARXML Change Parser ]
             │
             ▼
[ Stage 1: Deterministic Call Graph & Port Traversal ] ─── (Coverage Complete?) ──► YES ──┐
             │                                                                             │
            NO                                                                             │
             ▼                                                                             │
[ Stage 2: Context-Constrained Semantic Retrieval ]                                        │
             │                                                                             │
             ▼                                                                             │
[ Context Filter Gate: Subsystem & Artifact Compatibility ]                                 │
             │                                                                             │
             ├────────► [ Decoy Rejection (FPR = 0%) ]                                    │
             │                                                                             │
             ▼                                                                             │
[ Impact Fusion & Candidate Aggregation ] ◄────────────────────────────────────────────────┘
             │
             ▼
[ Safety-Aware Regression Test Selection (RTS) ]
             │
             ▼
[ Non-Bypassable Fail-Closed Safety Gate ]
             │
             ├────────► [ Mandatory ASIL-C/D Test Retention (100% Invariant) ]
             │
             ▼
[ Cryptographic Evidence Audit Report & HMI Visualization ]
```

---

## 2. Dual-Tier Dashboard Topology

The system provides two distinct, interoperable user interfaces:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AURA-Impact System                               │
├──────────────────────────────────────┬──────────────────────────────────────┤
│  Tier 1: Standalone HTML HMI         │  Tier 2: Full-Stack React Workbench  │
│  (AURA-Impact — ISO 26262 HMI.html) │  (hmi_frontend/)                     │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Zero external dependencies         │ • React 19 + TypeScript + Vite 8     │
│ • Runs directly in any web browser   │ • @xyflow/react (React Flow 12) DAG  │
│ • Probes localhost:8000 on load      │ • elkjs automated layered layout     │
│ • Dual Mode: Live Backend or Offline │ • Tailwind CSS dark engineering UI   │
│ • Instant presentation fallback      │ • Multi-tabbed diagnostic workbench  │
└──────────────────────────────────────┴──────────────────────────────────────┘
                                  │
                                  ▼
                 ┌─────────────────────────────────┐
                 │  FastAPI REST API Service       │
                 │  (src/api/server.py on :8000)   │
                 └─────────────────────────────────┘
                                  │
                                  ▼
                 ┌─────────────────────────────────┐
                 │  Canonical Pipeline Orchestrator │
                 │  (AuraImpactPipeline)           │
                 └─────────────────────────────────┘
```

---

## 3. Component Details & Interactions

### 3.1 Command Bar (`CommandBar.tsx`)
- Orchestrates preset scenarios:
  1. **Braking Threshold Calibration:** Direct call graph propagation.
  2. **Latent Thermal Coupling:** Semantic recovery of missing links.
  3. **Non-Automotive Decoy Attack:** Contextual filtering of multimedia/Spotify decoys.
  4. **High-Voltage Inverter Runaway:** Mandatory ASIL-D safety retention.
- Displays connection indicator: `LIVE BACKEND` (green) vs `OFFLINE DEMO` (amber).
- Handles arbitrary patch upload via modal dialog calling `POST /upload-diff`.

### 3.2 Impact Graph (`Workspace.tsx` + `CustomNode.tsx`)
- Renders directed acyclic graphs (DAGs) using `elkjs` layered layout.
- Solid red/teal edges indicate Stage 1 deterministic graph traversal.
- Dashed purple edges indicate Stage 2 contextual semantic fallback recoveries.
- Displays ASIL badges: **ASIL-D** (red), **ASIL-C** (orange), **ASIL-B** (amber), **ASIL-A** (yellow), **QM** (gray).

### 3.3 Decoy & Semantic Inspector
- Exposes raw vector similarity candidates.
- Categorizes each candidate as `ACCEPT`, `REJECT`, or `REVIEW_REQUIRED`.
- Exposes exact backend rejection reasons (`REJECT_SUBSYSTEM_MISMATCH`, `REJECT_BELOW_SIMILARITY_THRESHOLD`).

### 3.4 Mandatory Safety Matrix
- Displays locked safety tests.
- Proves fail-closed invariant: $T_{\text{safe}} \subseteq T_{\text{selected}}$.
- Explicitly disclaims certification claims while confirming rigorous prototype invariant retention.

### 3.5 Empirical Benchmark Evidence Tab
- Directly loads and displays real data from `GET /benchmarks`:
  - `master_benchmark_summary.csv`
  - Dataset tables for Dronology, Defects4J, Autoware.Universe, and Alexandria.
  - Interactive gallery of 8 verified publication figures from `results/plots/`.
  - Cryptographic evidence SHA-256 hash.
