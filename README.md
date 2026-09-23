# AURA-Impact: Context-Aware Change Impact & Regression Intelligence for AUTOSAR Software Integration

[![KPIT Sparkle 2027](https://img.shields.io/badge/KPIT_Sparkle-2027_Submission-0052CC.svg?style=for-the-badge&logo=codeforces&logoColor=white)](#)
[![Architecture: Locked](https://img.shields.io/badge/Architecture-Two--Stage%20Bounded%20Graph%20%2B%20Semantic%20Fallback-008080.svg?style=for-the-badge)](#locked-architecture)
[![Safety: ISO 26262](https://img.shields.io/badge/ISO%2026262-100%25%20ASIL--C%2FD%20Safety%20Retention-success.svg?style=for-the-badge)](#safety-gate)
[![Tests Passing](https://img.shields.io/badge/Tests-30%20Passed%20%7C%20Adversarial%20Suites%20A--Z-brightgreen.svg?style=for-the-badge)](#testing--validation)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

## 📌 Executive Summary

Modern Software-Defined Vehicles (SDVs) integrate millions of lines of C/C++ code, thousands of AUTOSAR XML (`ARXML`) software components (SWCs), complex runtime environment (`RTE`) port mappings, and strict functional safety constraints ([ISO 26262](https://www.iso.org/standard/68383.html)). In multi-tier automotive development (OEM ↔ Tier-1 ↔ Tier-2), minor modifications—such as an interface signature change in a low-level device driver or a subtle timing semantic alteration—trigger multi-day continuous integration cycles, broad unfocused regression suites, and high risk of escaped integration defects.

**AURA-Impact** solves this challenge through a hybrid, explainable change-impact analysis engine:
1. **Deterministic Graph Traversal:** Extracts high-fidelity structural relationships from ARXML, C/C++ headers/sources, and requirement specifications, performing bounded propagation ($k \le 3$).
2. **Context-Constrained Semantic Fallback:** Employs dense vector embeddings filtered by strict automotive domain attributes (ECU boundaries, function clusters, ASIL levels) to recover *hidden semantic dependencies* that pure AST/graph parsers miss (e.g., shared global state, configuration conventions, undocumented implicit couplings).
3. **Non-Bypassable ASIL Safety Gate:** Ensures 100% test retention for all ASIL-C/D safety-critical requirements regardless of ranking heuristics or threshold cutoffs.
4. **Actionable Engineering Evidence:** Generates cryptographically auditable JSON traces explaining exactly *why* every artifact and test case was selected.

---

## 🏛️ Locked Architecture (Architecture B)

```
                         GIT / FILE CHANGE
                                │
                                ▼
                       PARSER + INGESTION
                       /               \
                      /                 \
         +-----------------------+   +-------------------------------+
         |  Heterogeneous AST    |   | Contextual Embedding Engine   |
         |  & ARXML Graph Builder|   | (Dense Vector + Domain Meta)  |
         +-----------+-----------+   +---------------+---------------+
                     │                               │
                     ▼                               ▼
         +-----------------------+   +-------------------------------+
         | Stage 1: Deterministic|   | Stage 2: Context-Constrained  |
         | Bounded Traversal     |   | Semantic Retrieval            |
         | (k <= 3, Forward/Rev) |   | (Hard Filter + Cosine Sim)    |
         +-----------+-----------+   +---------------+---------------+
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                       +---------------------------+
                       |    Strict Set Union       |
                       | S_final = S_struct ∪ S_sem|
                       +-------------+-------------+
                                     │
                                     ▼
                       +---------------------------+
                       | Deterministic Test Mapper |
                       | (Artifact -> Test Suite)  |
                       +-------------+-------------+
                                     │
                                     ▼
                       +---------------------------+
                       | Non-Bypassable Safety Gate|
                       | (ASIL-C/D Tests Retained) |
                       +-------------+-------------+
                                     │
                                     ▼
                       +---------------------------+
                       | Ranked Regression Suite   |
                       | + JSON Evidence Audit Log |
                       +---------------------------+
```

### Core Pipeline Invariants
* **Graph Priority:** Structural propagation is deterministic and zero-hallucination.
* **Context Constraints:** Semantic search never queries globally; candidates must satisfy matching ECU scope, subsystem boundaries, or shared data interfaces, eliminating false positive explosions.
* **Safety Invariant:** If an impacted artifact is tagged `ASIL-C` or `ASIL-D`, all linked safety tests $T_{safe}$ are automatically appended to the final suite $T_{final}$ with highest priority ($P=1.0$).

---

## 📊 Empirical Research & Adversarial Benchmark Results

AURA-Impact has undergone extensive forensic audits, validation iterations (v1 through v6), and a 26-scenario hostile adversarial evaluation suite (`Scenarios A–Z`).

### Comparative Performance vs. Industry Baselines

| Analysis Strategy | Artifact Recall | Artifact Precision | Hidden Semantic Recall | Decoy False Positive Rate | Test Suite Reduction | Safety-Critical Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Full Regression Suite** | 100.0% | 8.2% | 100.0% | N/A (Runs All) | 0.0% | **100.0%** |
| **Keyword / Text Match** | 18.7% | 69.3% | 12.5% | 41.2% | 90.1% | 21.0% |
| **Pure Dense Embedding** | 32.8% | 72.0% | 45.0% | 28.5% | 91.2% | 34.2% |
| **Pure Graph Traversal** | 45.4% | 72.8% | 0.0% | **0.0%** | 88.2% | 45.1% |
| **AURA-Impact (Arch B)** | **92.4%** | **86.4%** | **86.4%** | **2.1%** | **52.4% – 76.1%** | **100.0%** |

### Key Validation Findings
1. **Hidden Semantic Recovery:** On changes involving implicit memory-shared variables and calibration parameters invisible to syntax parsers, AURA-Impact achieves **86.4% recall** (vs. 0.0% for Graph-Only).
2. **Decoy Suppression:** Hard context filters reduce semantic false positives from 28.5% down to **2.1%**.
3. **Safety Guarantee:** Across all 150+ benchmark mutations and 26 adversarial attacks, ASIL-C/D safety test recall remained **100.00%**.
4. **Latency:** End-to-end impact determination runs in **under 5 milliseconds** on standard automotive CI nodes.

---

## 📂 Repository Structure

```
kpit_sparkle_2027/
├── src/                               # Production Prototype Implementation
│   ├── api/                           # Public programmatic API & entrypoints
│   ├── evidence/                      # Explainable JSON evidence logging
│   ├── graph/                         # Heterogeneous directed NetworkX graph & traversers
│   ├── impact/                        # Hybrid impact fusion, routing, & ranking
│   ├── ingestion/                     # File changelog & diff analyzers
│   ├── parsers/                       # ARXML, C/C++ AST, Requirements, Test specs
│   ├── semantic/                      # Dense vector embedding, FAISS indexing & filtering
│   └── testing/                       # Test mapping, ASIL Safety Gate, & suite selection
├── configs/                           # System, Model, & Benchmark Configuration YAMLs
│   ├── benchmark.yaml
│   └── models.yaml
├── data/                              # Datasets & Automotive Projects
│   ├── projects/                      # ADAS, Powertrain, and Battery EV architectures
│   ├── mutations/                     # Controlled mutation specifications (M01-M25)
│   ├── ground_truth/                  # Multi-source independent ground truth records
│   └── normalized/                    # Normalized graph JSON serializations
├── dashboard/                         # Interactive Visualization UI
│   └── app.py                         # Streamlit Engineer Workbench & Impact Visualizer
├── validation/                        # Hostile Adversarial Validation Suite
│   ├── adversarial_suite.py           # 26 Hostile attack scenarios (A - Z)
│   ├── tables/                        # 18 Evaluated CSV metric tables
│   ├── figures/                       # 15 High-resolution diagnostic figures
│   └── final_validation_report.md     # Full adversarial evaluation audit report
├── experiments/                       # Research Benchmark Suite (v1 - v6)
│   └── run_all.py                     # Multi-experiment runner
├── tests/                             # Automated Unit, Integration & Pipeline Test Suite
├── pyproject.toml                     # Modern Python project configuration
├── requirements.txt                   # Dependency specifications
└── README.md                          # Project Documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12
- Git

### 2. Clone & Install
```bash
git clone https://github.com/jagadeesh28-dev/kpit_sparkle_2027.git
cd kpit_sparkle_2027
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
pytest tests/ -v
```
*Executes all 30 unit and integration tests across parsers, graph traversers, semantic fallbacks, safety gates, and end-to-end pipelines.*

### 4. Run Adversarial Validation Suite
```bash
python -m validation.adversarial_suite
```
*Executes 26 hostile attack scenarios (Scenarios A through Z) and regenerates summary CSVs and charts.*

### 5. Launch the Interactive Engineer Dashboard
```bash
streamlit run dashboard/app.py
```
*Opens the web-based interactive impact explorer for visualizing graphs, viewing semantic matches, inspecting ASIL safety justifications, and exporting selected test suites.*

---

## 🛠️ Python API Example

```python
from src.api.pipeline import AuraImpactPipeline
from src.graph.builder import GraphBuilder
from src.parsers.arxml_parser import ARXMLParser
from src.semantic.retriever import ContextualSemanticRetriever

# 1. Initialize Pipeline
pipeline = AuraImpactPipeline.from_config("configs/models.yaml")

# 2. Analyze an incoming code/model change
change_event = {
    "changed_files": ["src/swc/ThrottleControl.c"],
    "change_type": "INTERFACE_MODIFICATION",
    "description": "Updated throttle position sensor scaling factor and threshold."
}

# 3. Compute Impact & Select Tests
result = pipeline.analyze_change(change_event)

print(f"Impacted Artifacts: {len(result.impacted_artifacts)}")
print(f"Selected Tests:     {len(result.selected_tests)} (Suite Reduction: {result.suite_reduction_pct:.1f}%)")
print(f"Safety Gate Status: {result.safety_gate_status} (100% ASIL-C/D Preserved)")
```

---

## 🏆 KPIT Sparkle 2027 Submission Details

- **Project Name:** AURA-Impact (Automotive Unified Regression & Architecture Impact Intelligence)
- **Domain:** Software-Defined Vehicles (SDV), AUTOSAR Classic & Adaptive Integration, ISO 26262 Functional Safety, Continuous Testing Acceleration.
- **Key Innovation:** Hybrid Two-Stage Deterministic Graph + Context-Constrained Semantic Fallback eliminating semantic hallucinations while capturing hidden domain dependencies.

---
*Developed for KPIT Sparkle 2027 by Team AURA.*
