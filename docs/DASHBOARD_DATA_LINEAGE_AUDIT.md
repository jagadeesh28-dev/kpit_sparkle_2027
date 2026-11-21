# AURA-Impact — Dashboard Data Lineage Audit

**Evaluation Date:** November 21, 2026  
**Auditor Mode:** Full-Stack Data Lineage & Traceability Audit  
**Scope:** Backend Engine → REST API → TypeScript Client → React State → UI DOM  
**Project:** AURA-Impact — Context-Aware Change Impact and Regression Intelligence  
**Team:** THE GOAT (KPIT Sparkle 2027 Round 2)

---

## 1. Lineage Architecture

The AURA-Impact dashboard enforces strict data provenance. No UI component is permitted to fabricate impact relationships, ASIL ratings, test counts, or performance figures.

```
┌────────────────────────────────────────────────────────┐
│             CORE ENGINE COMPUTATION (PYTHON)           │
│  - EngineeringGraph (NetworkX DiGraph)                │
│  - FAISSSemanticIndex (Cosine L2 Index)                │
│  - ContextFilter (Subsystem / Type Constraints)        │
│  - TestMapper & SafetyGate (ASIL Invariant)            │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│              FASTAPI REST LAYER (PYTHON)               │
│  - Serialization to Pydantic & jsonable_encoder        │
│  - Endpoint: POST /analyze, GET /benchmarks            │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│             TYPESCRIPT API CLIENT (VITE)               │
│  - hmi_frontend/src/api.ts                             │
│  - Strongly-typed interfaces (AnalysisResponse, etc.)  │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                REACT APPLICATION STATE                 │
│  - hmi_frontend/src/App.tsx                            │
│  - State: analysisData, selectedScenario, selectedNode │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│             UI PRESENTATION & VISUALIZATION            │
│  - Workspace.tsx (ReactFlow & ELK Graph, Tabs)         │
│  - PropertiesInspector.tsx (Node Metadata & Links)     │
│  - CommandBar.tsx (HUD & Presets)                      │
│  - StatusBar.tsx (Execution Telemetry)                 │
└────────────────────────────────────────────────────────┘
```

---

## 2. Field-by-Field Data Lineage Mapping Table

The following table traces each primary dashboard UI element back to its authoritative backend computation source:

| UI Component | Dashboard Display Element | Frontend State / Prop | API Response Key | Core Engine Source |
| :--- | :--- | :--- | :--- | :--- |
| **CommandBar** | Scenario Dropdown | `selectedScenario.name` | `scenarios[i].name` | `src/api/server.py:SCENARIO_PRESETS` |
| **CommandBar** | Target Badge | `selectedScenario.artifact_id` | `changed_artifact.artifact_id` | `GitDiffParser` / `ChangedArtifact.artifact_id` |
| **CommandBar** | Backend Status Pill | `isBackendConnected` | HTTP 200 on `GET /health` | FastAPI health check & graph node count > 0 |
| **Workspace (Graph)** | Node Identifier | `node.data.label` | `full_graph.nodes[i].id` | `EngineeringGraph.graph.nodes[n_id]` |
| **Workspace (Graph)** | Node ASIL Badge | `node.data.safety_level` | `full_graph.nodes[i].safety_level` | `GraphNode.safety_level` |
| **Workspace (Graph)** | Impact Highlighting | `node.data.isImpacted` | `full_graph.nodes[i].isImpacted` | `TwoStageImpactEngine.final_impacts` |
| **Workspace (Graph)** | Directed Edge / Arrow | `edge.label` (Relation) | `full_graph.links[i].relation` | `EngineeringGraph.graph.edges[u,v]['relation']` |
| **Workspace (Tabs)** | Selected Tests Table | `selected_tests[i].test_id` | `selected_tests[i].test_id` | `RegressionSelector.selected_tests` |
| **Workspace (Tabs)** | Test Safety Class | `selected_tests[i].safety_class` | `selected_tests[i].safety_class` | `TestRecord.safety_class` |
| **Workspace (Tabs)** | Test Suite Reduction | `test_summary.test_reduction_pct` | `test_summary.test_reduction_pct` | `((T_all - T_sel) / T_all) * 100` |
| **Workspace (Tabs)** | Safety Invariant Badge | `safety_gate.status` | `safety_gate.status` | `SafetyGate.enforce()` invariant check |
| **Workspace (Tabs)** | Decoy Rejection Table | `rejected_candidates[i]` | `rejected_candidates[i]` | `ContextFilter.evaluate()` rejection log |
| **Workspace (Tabs)** | Rejection Reason | `cand.rejection_reason` | `rejected_candidates[i].rejection_reason` | `ContextFilter.REJECT_SUBSYSTEM_MISMATCH`, etc. |
| **Workspace (Tabs)** | Benchmark Summary | `summary_table[i]` | `summary_table[i]` | `results/tables/master_benchmark_summary.csv` |
| **Workspace (Tabs)** | Publication Figures | `figures[i].url` | `figures[i].url` | `results/plots/*.png` served via `/plots/` |
| **Inspector** | Node Metadata Details | `selectedNode.data.*` | `full_graph.nodes[i].*` | `EngineeringGraph.get_node(id)` attributes |
| **StatusBar** | Pipeline Latency | `latencies.total_ms` | `latencies.total_ms` | `time.perf_counter()` stage 1 + stage 2 |

---

## 3. Strict Separation of Live vs Offline Fallback

To prevent data ambiguity during mentor demonstrations, `hmi_frontend/src/App.tsx` maintains strict separation between live backend telemetry and offline fallback data:

1. **Live Mode:**
   - Active when `isBackendConnected === true`.
   - All graphs, test mappings, candidate rejections, and latency stats are directly populated from `POST /analyze`.
   - CommandBar displays a green pulsing badge: `LIVE BACKEND`.
2. **Offline Fallback Mode:**
   - Active only if the FastAPI backend is offline or network fails.
   - CommandBar immediately displays an amber badge: `OFFLINE DEMO`.
   - Response payload explicitly sets `status: "offline_demo"`, preventing any false claim of live execution.

---

## 4. Lineage Audit Verdict

The data lineage of AURA-Impact is **100% closed, traceable, and grounded in empirical computation**. No mocked or fabricated metrics leak into the live analysis views.
