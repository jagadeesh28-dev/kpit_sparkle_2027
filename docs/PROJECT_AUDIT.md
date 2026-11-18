# AURA-Impact Project Audit & Architectural Baseline Report
**KPIT Sparkle Round 2 — Phase 0 Audit**  
**Date:** November 2026  
**Auditors:** THE GOAT (AURA-Impact Engineering & Research Validation Team)  
**System Status:** Production Prototype Passing 252/252 Unit & Regression Gates  

---

## 1. Executive Summary

This document establishes the comprehensive technical baseline of **AURA-Impact** (Context-Aware Change Impact and Regression Intelligence for Automotive Software Engineering) prior to public dataset expansion.

AURA-Impact investigates a hybrid, explainable change-impact analysis engine designed for complex automotive software integration (AUTOSAR, C/C++, and ISO 26262 functional safety). The core operational principle is:

$$\text{\textbf{PROVE}} \longrightarrow \text{\textbf{RECOVER}} \longrightarrow \text{\textbf{FILTER}} \longrightarrow \text{\textbf{PROTECT}}$$

1. **PROVE:** Deterministic engineering dependency graph traversal (BFS depth $k \le 3$) captures explicit call/data-flow links.
2. **RECOVER:** When structural links are missing or broken, dense semantic retrieval activates to identify latent dependencies.
3. **FILTER:** Hard automotive domain context filters (subsystem isolation, ECU boundaries, artifact type compatibility) suppress out-of-domain semantic decoys.
4. **PROTECT:** A non-bypassable safety gate unconditionally enforces $T_{\text{safe}} \subseteq T_{\text{selected}}$ (100% ASIL-C/D retention).

---

## 2. Technology Stack & Runtime Environment

| Category | Component / Tool | Version / Specification | Role in System |
| :--- | :--- | :--- | :--- |
| **Runtime** | Python | 3.14.0 (Windows x64) | Primary execution engine |
| **Packaging** | Setuptools / pip | `pyproject.toml` | Build & dependency management |
| **Graph Engine** | NetworkX | `>=3.0` | MultiDiGraph engineering dependency representation |
| **Numerical/Math** | NumPy / SciPy | `numpy>=1.24`, `scipy>=1.10` | Vector operations & statistical significance testing |
| **DataFrames** | Pandas | `>=2.0.0` | Tabular benchmark metrics, reporting & CSV export |
| **Semantic Index** | FAISS / NumPy Fallback | `faiss.IndexFlatIP` | Inner-product cosine search on L2-normalized vectors |
| **Embedder** | AURA-DomainHashEmbedder-384 | Custom ($d=384$) | Deterministic domain-concept hash vectorizer |
| **Parsers** | `lxml.etree` / Regex | `lxml>=4.9.0` | AUTOSAR ARXML & C code AST/token extraction |
| **Testing** | Pytest | `pytest>=7.3.0` | 252-test automated regression & safety test harness |
| **Dashboard** | Streamlit | `>=1.24.0` | Interactive mentor demonstrator & graph visualizer |
| **Visualization** | Matplotlib | `>=3.7.0` | Publication-quality radar charts, PR curves & histograms |

---

## 3. Existing Architecture & Implemented Components

```
                                  GIT DIFF / ARTIFACT CHANGE
                                              │
                                              ▼
                                 INGESTION & DIFF ANALYZER
                                 (src/ingestion/diff_analyzer.py)
                                              │
                                              ▼
                                   CHANGE CLASSIFIER
                               (src/impact/classifier.py)
                                  /                   \
                                 /                     \
       [Structural / Explicit]  ▼                       ▼  [Semantic / Implicit]
          DETERMINISTIC GRAPH TRAVERSAL             AURA DOMAIN HASH EMBEDDER (384-d)
          (src/graph/traversal.py)                  (src/semantic/embedder.py)
          - Bounded BFS (Depth <= 3)                - Deterministic MD5 / SHA-256
          - Structural confidence = 1.0             - Concept ontology anchors
                 │                                      │
                 │                                      ▼
                 │                          CONTEXT-CONSTRAINED FILTER
                 │                          (src/semantic/context_filter.py)
                 │                          - Subsystem isolation gate
                 │                          - Artifact type compatibility
                 │                          - Cosine threshold (tau = 0.45)
                 │                                      │
                 └───────────────────────┬──────────────┘
                                         ▼
                               IMPACT FUSION ENGINE
                             (src/impact/fusion.py)
                     Strict Set Union: S_final = S_struct ∪ S_semantic
                                         │
                                         ▼
                           REGRESSION TEST SELECTOR
                       (src/testing/regression_selector.py)
                                         │
                                         ▼
                            NON-BYPASSABLE SAFETY GATE
                           (src/testing/safety_gate.py)
                     Invariant Enforcement: T_safe ⊆ T_final (100%)
                                         │
                                         ▼
                           EXPLAINABLE EVIDENCE EXPORT
                        (src/evidence/evidence_logger.py)
```

### Detailed Component Inventory:

1. **Graph Construction & Ingestion (`src/graph/`, `src/parsers/`):**
   - `schema.py`: Formal typed data models for `GraphNode`, `GraphEdge`, `NodeType` (Requirement, SoftwareComponent, Port, Interface, DataElement, Runnable, C_Function, C_Variable, Test, DiagnosticEvent), `RelationType`, and `SafetyLevel` (QM, ASIL_A through ASIL_D).
   - `engineering_graph.py` & `builder.py`: MultiDiGraph wrapper managing node stores, edge relations, adjacency caches, cycle detection, and upstream/downstream lookups.
   - `arxml_parser.py`: Fast XML parser extracting AUTOSAR components, ports, and interfaces.
   - `c_parser.py`: Extracts C function definitions, function calls, global variable read/writes.
   - `requirement_parser.py`: Ingests requirement IDs, text, ASIL classifications, and trace matrices.
   - `test_parser.py`: Extracts test cases, execution constraints, and ASIL classifications.

2. **Semantic Retrieval Engine (`src/semantic/`):**
   - `embedder.py`: `AURA-DomainHashEmbedder-384`. Produces 384-dimensional unit-norm dense embeddings using token hashing, 3-gram subwords, and automotive concept projections (AEB, ACC, BMS, Powertrain, Body, Safety). It achieves zero external weight dependencies and microsecond latency.
   - `index.py`: `FAISSSemanticIndex` implementing top-$K$ cosine similarity search via `IndexFlatIP` (with pure NumPy dot-product fallback when FAISS binaries are absent).
   - `context_filter.py`: Evaluates hard subsystem boundaries, artifact type compatibility, and contextual proximity.
   - `retrieval.py` & `retriever.py`: Bridges change diffs with index querying, applying candidate thresholding ($\tau = 0.45$).

3. **Impact Analysis & Fusion (`src/impact/`):**
   - `classifier.py`: Routes changes into `STRUCTURAL`, `SEMANTIC`, `MIXED`, or `NO_IMPACT`.
   - `fusion.py`: Implements Locked Architecture B's Strict Set Union:
     $$S_{\text{final}} = S_{\text{struct}} \cup S_{\text{semantic}}$$
     Structural evidence retains full certainty ($1.0$); semantic evidence retains similarity score without attenuation.
   - `ranking.py`: Ranks impacts, determines `REVIEW_REQUIRED` status on ambiguous edges, and generates human-readable rationales.

4. **Regression Test Selection & Safety Invariants (`src/testing/`):**
   - `test_mapper.py`: Maps impacted nodes to test cases via `TESTS` and `VERIFIES` relations.
   - `safety_gate.py`: Asserts non-bypassable post-selection invariant. Forces any omitted ASIL-C/D test back into the selected set. Raises `SafetyInvariantViolationError` if $T_{\text{safe}} \not\subseteq T_{\text{selected}}$.
   - `regression_selector.py`: Computes test suite reduction while maintaining 100% safety test retention.

5. **Evidence Logging & Dashboard (`src/evidence/`, `dashboard/`):**
   - `evidence_logger.py`: Writes JSON audit traces recording every decision, match score, and safety reason.
   - `app.py`: Streamlit-based interactive dashboard supporting interactive scenario selection, graph visual inspection, and test selection reviews.

---

## 4. Current Experimental Results & Provenance of Historical Claims

The repository currently contains two distinct tiers of experimental results:

### Tier 1: Canonical 150-Mutation Synthetic Benchmark (Gate 11 / Gate 14)
*Executed via `python benchmark/final/runner.py` on synthetic automotive models (`ADAS`, `POWERTRAIN`, `BATTERY_EV`):*
- **Overall Artifact Recall:** 57.73% (across all 150 mutations)
- **Mean Test Suite Reduction:** 89.1% (test split) / 82.29% (average benchmark suite)
- **Safety Invariant Enforcement:** 100.0% (150/150 mutations, zero safety test omissions)
- **Semantic Top-$K$ Retrieval:** Recall@1 = 3.3%, Recall@5 = 13.3%, MRR = 0.0665

### Tier 2: Historical Prototype Claims (Found in Research Logs & Scripts)
The metrics cited in previous prototype summaries originate from specific controlled validation experiments:
- **Hidden-Dependency Recall (40.67%):** Measured in `experiments/run_v4_final_validation.py` and `scripts/run_v6_hostile_audit.py` on controlled synthetic unlinked semantic mutations (Generator A).
- **Graph-Only Hidden-Dependency Recall (0.0%):** In scenarios where explicit graph trace links were deleted, graph traversal alone exhibited complete blindness (0% recall), demonstrating the necessity of the semantic fallback.
- **Defined Decoy FPR (0.0% / 2.1%):** In `validation/tables/decoy_analysis.csv` and `validation/final_validation_report.md`, hard subsystem boundary filtering dropped the raw embedding distractor false positive rate from 28.0% down to 2.1% (and 0.0% in specific closed decoy tests).
- **Regression Reduction (82.29%):** Documented in `README.md`, `artifacts/final_release_evidence_integrity.json`, and `ROUND2_ARCHITECTURE_AUDIT.md` as the mean test suite reduction across synthetic benchmark suites.
- **Test-Suite Recall (90.07%):** Historical test selection recall across the 150-mutation suite.
- **Safety-Test Retention (100%):** Enforced by `SafetyGate.enforce()`.
- **Execution Latency (0.79 ms):** Single-thread CPU in-memory latency per mutation scenario.

> [!CAUTION]
> **Scientific Integrity Notice:** These historical prototype results were evaluated exclusively on **synthetic AUTOSAR models and controlled mutations**. They are **NOT** public-dataset results. They must never be conflated with evaluations on external real-world benchmarks.

---

## 5. Incomplete Components & Critical Gaps

To meet the rigorous standards of KPIT Sparkle Round 2, the following critical gaps must be resolved:

| # | Gap Area | Current State | Required Public Validation State |
| :--- | :--- | :--- | :--- |
| **G1** | **Dataset Grounding** | 100% synthetic models (`data/projects/*`). | Real-world validation on **Dronology**, **Defects4J**, **Autoware**, and **Alexandria**. |
| **G2** | **Unified Graph Ingestion** | Parsers tightly coupled to synthetic ARXML/JSON. | Generalized multi-dataset ingestion producing unified `NodeType` and `RelationType` schemas. |
| **G3** | **Baseline Standardization** | Baselines in `baselines/` exist but are evaluated only on synthetic mutations. | Unified evaluation framework running Keyword (TF-IDF/BM25), Embedding-Only, Graph-Only, and AURA-Impact on identical real dataset slices. |
| **G4** | **Data Leakage Safeguards** | Synthetic ground truth evaluated in memory. | Strict temporal and causal isolation: pre-change snapshot indexing only; no future commit/patch leakage. |
| **G5** | **Controlled Link Deletion** | Evaluated on fixed hand-crafted unlinked mutations. | Systematic trace-link deletion experiments at 10%, 20%, 30% deletion rates across multiple random seeds. |
| **G6** | **Real Defect Prediction** | Evaluated on synthetic injected defects. | Evaluation against actual historical bugs and failing test executions in Defects4J. |
| **G7** | **Automotive C++ / ROS 2** | Evaluated on small synthetic C files. | Real automotive architecture graph extraction from Autoware package/component hierarchies. |
| **G8** | **Dashboard Public Mode** | Dashboard only exposes synthetic projects. | Integration of public dataset evaluation tab displaying real-world benchmarks, PR curves, and evidence traces. |

---

## 6. Known Bugs & Performance Bottlenecks

1. **Lack of Ingestion Generalization:** Current parsers assume fixed directory layouts (`arxml/`, `requirements/`, `src/`, `tests/`) and specific JSON keys. Real-world datasets (e.g. Dronology XML, Defects4J patch diffs, Autoware CMake/package.xml) fail without dedicated adapters.
2. **Deterministic Hash Vocabulary Drift:** While `AURA-DomainHashEmbedder-384` is microsecond-fast and deterministic, out-of-distribution vocabularies (e.g., aerospace terms in Dronology or Java method signatures in Defects4J) do not match automotive concept clusters unless concept mappings are generalized.
3. **Keyword Baseline Parameter Sensitivity:** In `baselines/keyword_baseline.py`, the default TF-IDF threshold ($0.15$) produces variable recall depending on document length. BM25 with length normalization is needed for fair comparison.
4. **Memory Profiling in Benchmarks:** Current memory scaling estimates in `benchmark/final/runner.py` use simulated node graphs rather than streaming real project graphs.

---

## 7. Recommended Action Plan (Phased Roadmap)

1. **Phase 1: Dataset Verification & Audit:**
   - Verify official sources, URLs, licenses, download sizes, artifact types, and ground truth for Dronology, Defects4J, Autoware, and Alexandria.
   - Document findings in `docs/DATASET_AUDIT.md`.
2. **Phase 2: Unified Ingestion Architecture:**
   - Establish `data/raw/`, `data/processed/`, and `data/manifests/`.
   - Implement unified graph ingestion mapping all datasets to the common canonical graph schema.
3. **Phase 3: Multi-Baseline Evaluation Framework:**
   - Standardize Keyword (BM25/TF-IDF), Embedding-Only (384-d), Graph-Only (Deterministic BFS), and full AURA-Impact.
   - Implement strict anti-leakage guards (pre-change snapshots only).
4. **Phase 4: Dataset-Specific Experiments:**
   - *Dronology:* Traceability recovery under 10%, 20%, 30% link deletion; safety requirement retention.
   - *Defects4J:* Real historical defect test selection (triggering vs failing tests).
   - *Autoware:* Automotive ROS 2 / C++ architecture graph traversal and impact scenarios.
   - *Alexandria:* Historical co-change relationship evaluation as proxy evidence.
5. **Phase 5: Safety Invariant & Adversarial Verification:**
   - Automated unit tests asserting $T_{\text{safe}} \subseteq T_{\text{selected}}$ under failure injection.
6. **Phase 6: Visualizations & Reporting:**
   - Generate publication-quality figures, machine-readable CSV/JSON results.
7. **Phase 7: Dashboard Enhancement & Presentation:**
   - Update Streamlit UI with public dataset demonstration modes.
   - Create `docs/KPIT_PRESENTATION_SCRIPT.md` and `docs/KPIT_MENTOR_QA.md`.

---
*Audit Completed & Approved for Phase 1 Progression.*

