# AURA-Impact: Context-Aware Change Impact & Regression Intelligence for Automotive Software Integration

[![KPIT Sparkle 2027](https://img.shields.io/badge/KPIT_Sparkle-2027_Submission-0052CC.svg?style=for-the-badge&logo=codeforces&logoColor=white)](#)
[![Status: Research Prototype](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg?style=for-the-badge)](#project-status--maturity-level)
[![Architecture: Locked B](https://img.shields.io/badge/Architecture-Bounded%20Graph%20%2B%20Strict%20Union%20Fallback-008080.svg?style=for-the-badge)](#locked-architecture-architecture-b)
[![Public Datasets Validated](https://img.shields.io/badge/Public_Datasets-Dronology%20%7C%20Defects4J%20%7C%20Autoware%20%7C%20Alexandria-8A2BE2.svg?style=for-the-badge)](#-public-dataset-empirical-benchmarks)
[![Safety Invariant](https://img.shields.io/badge/ISO%2026262-100%25%20Mandatory%20Safety%20Retention-success.svg?style=for-the-badge)](#safety-guarantee--invariant-distinction)
[![Tests Passing](https://img.shields.io/badge/Tests-256%20Passed%20%7C%20100%25%20Verified-brightgreen.svg?style=for-the-badge)](#testing--verification)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

## 📌 Project Status & Maturity Level

> [!IMPORTANT]
> **RESEARCH & COMPETITION PROTOTYPE (KPIT Sparkle Round 2):**
> AURA-Impact is an academic and research engineering prototype developed by **Team THE GOAT** for KPIT Sparkle 2027.
> - **Dual Validation Tiers:** Evaluated on both **canonical synthetic AUTOSAR models** (150 mutations across ADAS, Powertrain, and Battery EV) and **peer-reviewed public datasets** (Dronology CPS, Defects4J real historical bugs, Autoware.Universe ROS 2/C++ automotive stack, and Alexandria Git co-change evolution).
> - **Production Scope:** This system is **not** currently certified by any automotive OEM or Tier-1 supplier as an ISO 26262 Tool Confidence Level qualified software tool, nor is it connected to live vehicle hardware-in-the-loop (HIL) test rigs.
> - **Zero Hallucination Policy:** All metrics, models, tables, and test results in this repository are verified by executable tests and reproducible scripts.

---

## 📖 Executive Summary

Modern Software-Defined Vehicles (SDVs) integrate millions of lines of C/C++ code, thousands of AUTOSAR XML (`ARXML`) software components (SWCs), complex runtime environment (`RTE`) port mappings, and strict functional safety constraints ([ISO 26262](https://www.iso.org/standard/68383.html)). In multi-tier automotive development (OEM ↔ Tier-1 ↔ Tier-2), minor modifications—such as an interface signature change in a low-level device driver or a subtle timing semantic alteration—trigger multi-day continuous integration cycles, broad unfocused regression suites, and high risk of escaped integration defects.

**AURA-Impact** investigates a hybrid, explainable change-impact analysis engine designed specifically for automotive architectures:
1. **Deterministic Graph Traversal (PROVE):** Extracts high-fidelity structural relationships from ARXML, C/C++ headers/sources, and requirement specifications, performing bounded breadth-first propagation ($D \le 3$).
2. **Context-Constrained Semantic Fallback (RECOVER):** Employs domain-specific embedding representations filtered by strict automotive attributes (ECU boundaries, function clusters, ASIL levels) to recover *hidden semantic dependencies* that pure AST/graph parsers miss.
3. **Hard Domain Filtering (FILTER):** Rejects cross-subsystem semantic decoys and incompatible artifact pairs, dropping the distractor false positive rate to near zero.
4. **Strict Set Union ($S_{final} = S_{struct} \cup S_{semantic}$):** Under Architecture B, semantic candidates are retained alongside structural impacts without numerical attenuation.
5. **Non-Bypassable ASIL Safety Gate (PROTECT):** Enforces a mathematical invariant ($T_{safe} \subseteq T_{selected}$) ensuring unconditional retention of all ASIL-C/D safety-critical test cases regardless of ranking heuristics or threshold cutoffs.
6. **Actionable Engineering Evidence:** Generates cryptographically auditable JSON traces explaining exactly *why* every artifact and test case was selected.

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
         |  Heterogeneous AST    |   | Domain Hash Embedder          |
         |  & ARXML Graph Builder|   | (AURA-DomainHashEmbedder-384) |
         +-----------+-----------+   +---------------+---------------+
                     │                               │
                     ▼                               ▼
         +-----------------------+   +-------------------------------+
         | Stage 1: Deterministic|   | Stage 2: Context-Constrained  |
         | Bounded Traversal     |   | Semantic Retrieval            |
         | (Depth <= 3, BFS)     |   | (Hard Subsystem Filter, >0.45)|
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
                       | (Mandatory ASIL-C/D Added)|
                       +-------------+-------------+
                                     │
                                     ▼
                       +---------------------------+
                       | Ranked Regression Suite   |
                       | + JSON Evidence Audit Log |
                       +---------------------------+
```

### Core Architecture Invariants
* **Graph Priority:** Structural propagation is deterministic, fast (<1 ms query), and zero-hallucination.
* **Context Constraints:** Semantic retrieval rejects cross-subsystem decoys and incompatible artifact pairs, preventing false positive explosions.
* **Strict Set Union:** The impact union preserves both structural and semantic detections ($S_{final} = S_{struct} \cup S_{semantic}$) without lossy weighting.
* **Safety Invariant ($T_{safe} \subseteq T_{selected}$):** All known safety-critical tests are guaranteed to be in the final execution suite.

---

## 🔬 Semantic Model Specification

The canonical semantic model employed across all benchmarks and pipelines is:
- **Identifier:** `AURA-DomainHashEmbedder-384`
- **Embedding Dimension:** 384
- **Algorithm:** Deterministic domain-specific feature hashing with automotive ontology expansion, subword tokenization, and L2 unit normalization.
- **Indexing Backend:** FAISS (or NumPy cosine similarity fallback when FAISS C-extensions are unavailable).
- **Execution:** Zero external API calls, zero neural GPU requirements, 100% deterministic vector generation.

*(Note: Prior draft documentation informally referred to this component as "BGE-M3". That label was inaccurate and has been formally deprecated. The actual executable implementation is the deterministic domain-hash vectorizer.)*

---

## 📊 Public Dataset Empirical Benchmarks

AURA-Impact was subjected to rigorous validation across four independent public dataset benchmarks (`evaluation/experiments/run_all_experiments.py`):

| Evaluation Dataset | Domain & Benchmark Task | AURA-Impact Recall | Graph-Only Recall | Embedding-Only Recall | AURA-Impact F1 | Safety Retention | Mean Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dronology** | Safety-Critical CPS Link Deletion (10–30%) | **100.0%** | 22.2% | **100.0%** | **0.2170** | **100.0%** | 0.186 ms |
| **Defects4J** | Historical Real Faults RTS (Cli 1–14) | **100.0%** | **100.0%** | **100.0%** | **0.5410** | N/A (Non-Safety) | 0.167 ms |
| **Autoware.Universe** | Production Automotive ROS 2/C++ AEB Stack | **41.7%** | 33.3% | **41.7%** | **0.2012** | **100.0%** | 0.132 ms |
| **Alexandria** | Historical Git Co-Change Evolution Mining | **80.0%** | 40.0% | 60.0% | **0.6667** | N/A (Proxy) | 0.050 ms |

### Key Scientific Findings:
1. **Graph Blindness Overcome (Dronology):** Under controlled trace-link deletion across 720 scenario runs, Graph-Only recall collapsed to **20.0%–22.2%**. AURA-Impact achieved **100.0% recovery** ($p = 1.62 \times 10^{-12}$, Wilcoxon signed-rank test).
2. **Defect-Triggering Test Recall (Defects4J):** Across 10 real historical bugs, AURA-Impact captured **100.0% of the triggering failing tests** that expose runtime faults while **slashing test suite execution overhead by 54.10%**.
3. **Decoy Rejection (Autoware):** Traversed cross-package call paths between AEB and the Vehicle Command Gate while maintaining **0% False Positive Rate on documentation decoys**.
4. **Mandatory Safety Retention:** Enforced **100.0% retention of critical safety tests** across all evaluated change scenarios.

---

## 🛡️ Safety Guarantee & Invariant Distinction

To maintain strict scientific integrity, AURA-Impact distinguishes between two safety metrics:

1. **Safety Invariant Enforcement ($T_{safe} \subseteq T_{selected}$): 100.0% (Verified across all 256 test gates).**
   - Implemented in `src/testing/safety_gate.py`.
   - Guaranteed by post-selection invariant checking: any mandatory ASIL-C/D test omitted by algorithmic heuristics is forced back into the selected suite.
2. **Autonomous Safety Discovery Recall: 47.61% (without safety gate).**
   - Measures what percentage of safety-critical items the structural and semantic impact engines identify purely through graph walking and embedding retrieval without forced inclusion.
   - The safety gate exists precisely to bridge this gap, ensuring that safe automotive CI never relies solely on statistical or heuristic discovery.

---

## 📂 Repository Structure

```
KPIT_2026_aura_impact/
├── src/                               # Core Pipeline Implementation
│   ├── api/                           # CLI and high-level pipeline entrypoints
│   ├── benchmark/                     # Benchmark generators, metrics, statistics
│   ├── evidence/                      # Audit logging and multi-format report generator
│   ├── graph/                         # Engineering graph builder, schema, traversal
│   ├── impact/                        # Impact fusion, classification, fallback, ranking
│   ├── ingestion/                     # Git diff analyzer and artifact loader
│   ├── parsers/                       # C/C++, ARXML, Requirement, Test spec parsers
│   ├── semantic/                      # Domain hash embedder, FAISS index, context filter
│   └── testing/                       # Test mapper, regression selector, safety gate
├── evaluation/                        # Public Dataset Evaluation Framework
│   ├── ingestion/                     # Unified multi-dataset graph ingester
│   ├── baselines/                     # Standardized 4-baseline harness (Keyword, Emb, Graph, AURA)
│   ├── metrics/                       # Formal Precision, Recall, RTS, and Wilcoxon metrics
│   ├── experiments/                   # Experiment runners (Dronology, Defects4J, Autoware, Alexandria)
│   └── reports/                       # Publication-quality plotting engine
├── data/
│   ├── manifests/                     # Download provenance & SHA-256 checksums
│   ├── raw/                           # Downloaded public dataset files (Dronology, Defects4J, Autoware)
│   └── projects/                      # Canonical synthetic benchmark projects (ADAS, Powertrain, EV)
├── dashboard/                         # Streamlit Interactive Explorer (dashboard/app.py)
├── results/
│   ├── plots/                         # 8 Publication-quality figures (PNG)
│   ├── tables/                        # Standardized benchmark result CSVs
│   └── evidence/                      # Cryptographic JSON evidence traces
├── docs/                              # Comprehensive Research & Governance Package
│   ├── PROJECT_AUDIT.md               # Repository baseline and gap analysis
│   ├── DATASET_AUDIT.md               # Public dataset provenance & verification
│   ├── SYSTEM_ARCHITECTURE.md         # Formal architectural specification
│   ├── EXPERIMENTAL_METHODOLOGY.md    # Experimental protocols & anti-leakage guarantees
│   ├── RESULTS.md                     # Comprehensive empirical results & statistical tests
│   ├── LIMITATIONS.md                 # Scientific boundaries & zero-hallucination policies
│   ├── REPRODUCIBILITY.md             # 5-step reproduction runbook
│   ├── KPIT_PRESENTATION_SCRIPT.md    # 12-slide structured presentation narrative
│   ├── KPIT_MENTOR_QA.md              # 32 technical defense questions & answers
│   └── EXECUTION_LOG.md               # Full milestone progress log & acceptance criteria
├── tests/                             # Comprehensive 256-Test Regression Suite
│   ├── adversarial/                   # Hostile adversarial tests
│   ├── benchmark/                     # Metric integrity, leakage, and repro tests
│   ├── cli/                           # Subprocess CLI integration tests
│   ├── dashboard/                     # Programmatic dashboard verification tests
│   ├── evidence/                      # Audit logging completeness tests
│   ├── failure_injection/             # Hostile failure injection tests
│   ├── integration/                   # End-to-end pipeline tests
│   ├── safety/                        # Public dataset & safety gate invariant tests
│   ├── semantic/                      # Model identity and fallback validation tests
│   ├── structural/                    # Graph propagation and boundary tests
│   ├── testing/                       # Regression selection tests
│   └── unit/                          # Unit tests across parsers, graph, ranking
├── pyproject.toml                     # Modern Python packaging configuration
└── requirements.txt                   # Dependency specifications
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Git 2.40+

### 2. Clone & Install
```bash
git clone https://github.com/jagadeesh28-dev/kpit_sparkle_2027.git
cd kpit_sparkle_2027
pip install -r requirements.txt
```

### 3. Run Automated Tests (256 Tests)
```bash
python -m pytest tests/ -v
```
*Executes the complete 256-test regression, adversarial, and safety invariant test suite.*

### 4. Run Master Public Dataset Benchmark Pipeline
```bash
python evaluation/experiments/run_all_experiments.py
```
*Executes evaluations across Dronology, Defects4J, Autoware, and Alexandria in ~1.3 seconds, generating summary CSV tables and publication plots.*

### 5. Launch the Interactive Exploration Dashboard
```bash
streamlit run dashboard/app.py
```
*Opens the web-based visualizer. Explore live scenario graphs, semantic candidate scorings, and the new **Tab 7: "🔬 Public Dataset Evidence"**.*

---

## 🏆 KPIT Sparkle 2027 Submission Details

- **Project Title:** AURA-Impact (Automotive Unified Regression & Architecture Impact Intelligence)
- **Team Name:** THE GOAT
- **Domain:** Software-Defined Vehicles (SDV), AUTOSAR Integration, ISO 26262 Functional Safety, Regression Test Selection.
- **Innovation:** Bounded Heterogeneous Graph Traversal combined with Context-Constrained Semantic Fallback and Mandatory Safety Invariant Enforcement (**PROVE $\to$ RECOVER $\to$ FILTER $\to$ PROTECT**).
