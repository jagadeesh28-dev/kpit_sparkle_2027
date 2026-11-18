# AURA-Impact System Architecture Specification
**Context-Aware Change Impact and Regression Intelligence for Automotive Software Engineering**  
**Document Reference:** AURA-ARCH-SPEC-2027  
**Architecture Specification:** Architecture B (Locked Canonical)  
**Authors:** THE GOAT (AURA-Impact Engineering Team for KPIT Sparkle 2027)  

---

## 1. Problem Statement & Motivation

Modern Software-Defined Vehicles (SDVs) integrate hundreds of millions of lines of C/C++ code, thousands of AUTOSAR XML (`ARXML`) software components (SWCs), intricate runtime environment (`RTE`) port connections, and stringent functional safety invariants ([ISO 26262](https://www.iso.org/standard/68383.html)).

In multi-tier automotive development (OEM $\leftrightarrow$ Tier-1 $\leftrightarrow$ Tier-2):
1. **Explicit Traceability Gaps:** Specifications, architecture models, and source implementations evolve asynchronously. Trace links between requirements, code, and test cases frequently break, creating "graph blindness."
2. **Regression Test Bloat:** Full integration regression test suites require days to execute on Hardware-in-the-Loop (HIL) test rigs. Existing test selection techniques either select too few tests (risking escaped safety-critical regressions) or too many tests (paralyzing continuous integration pipelines).
3. **Black-Box AI Flaws:** Unconstrained dense embedding models retrieve superficial lexical matches across disparate ECUs (e.g. searching for `"brake"` retrieves brake lights, brake pedal telemetry, and decelerating wiper routines), creating intolerable false alarm rates.

**AURA-Impact** resolves this dilemma through a hybrid, explainable architecture:

$$\text{\textbf{PROVE}} \longrightarrow \text{\textbf{RECOVER}} \longrightarrow \text{\textbf{FILTER}} \longrightarrow \text{\textbf{PROTECT}}$$

---

## 2. Core Operational Principles

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

### Principle A: Deterministic First (PROVE)
Structural dependency evidence must be evaluated prior to any AI/statistical model. Where static AST calls, port interfaces, and explicit requirement mappings exist, they receive deterministic confidence ($1.0$).

### Principle B: Context-Aware Semantic Recovery (RECOVER)
Dense vector retrieval activates only when structural evidence is incomplete or unlinked. Using `AURA-DomainHashEmbedder-384`, latent dependencies are recovered without external neural model weight dependencies.

### Principle C: Hard Contextual Filtering (FILTER)
All semantically retrieved candidates must satisfy hard engineering domain constraints:
1. **Subsystem Isolation:** Cross-subsystem links are strictly blocked unless explicit gateway interfaces exist.
2. **Artifact Type Compatibility:** Requirements only map to valid behavioral implementations (`C_Function`, `Runnable`, `SWC`, `Interface`).
3. **Proximity Bounds:** Candidates beyond acceptable structural or ontological distance are pruned.

### Principle D: Strict Set Union (FUSION)
Under Locked Architecture B, the final impact set $S_{\text{final}}$ is the mathematical strict union:
$$S_{\text{final}} = S_{\text{struct}} \cup S_{\text{semantic}}$$
Semantic candidates that survive context filtering are preserved alongside structural impacts without numerical attenuation.

### Principle E: Non-Bypassable Safety Gate (PROTECT)
The system asserts a mathematical invariant:
$$T_{\text{safe}} \subseteq T_{\text{selected}}$$
Every test classified as ASIL-C or ASIL-D is unconditionally retained in the selected test suite, guaranteeing 100% safety retention regardless of heuristic cutoffs.

---

## 3. Data Model & Graph Schema

The engineering dependency graph is modeled as a directed multi-graph $G = (V, E)$ using NetworkX:

### 3.1 Node Types ($V$)
- `Requirement`: System or functional requirement specification.
- `SafetyRequirement`: Safety goal, hazard mitigation, or FMECA critical item.
- `SoftwareComponent`: AUTOSAR SWC or ROS 2 package node.
- `Port`: AUTOSAR Provider/Requirer port or ROS 2 topic interface.
- `Interface`: Sender-Receiver, Client-Server, or service message definition.
- `DataElement`: Transmitted variable, signal, or payload structure.
- `Runnable`: Executable schedulable entity mapped to OS tasks.
- `Function`: C/C++ function implementation.
- `TestCase`: Unit, integration, or HIL test specification.
- `Defect`: Historical defect or issue report.

### 3.2 Edge Types ($E$)
- `IMPLEMENTS`: Source function/component fulfills requirement ($c \to r$).
- `CALLS`: Static function call invocation ($f_1 \to f_2$).
- `READS` / `WRITES`: Data-flow interaction with global variables or RTE signals.
- `DEPENDS_ON`: Build, package, or execution dependency.
- `INTERFACES_WITH`: Topic or Client-Server interface communication.
- `TESTS` / `VERIFIES`: Test case validates software component or requirement.
- `MODIFIES`: Change commit or patch alters component.
- `SAFETY_REQUIRES`: ASIL safety goal mandates functional mitigation.
- `CO_CHANGES_WITH`: Historical empirical co-modification relation (proxy evidence).

Every edge records `confidence`, `evidence_source`, `dataset_provenance`, and `is_verified`.

---

## 4. Semantic Engine: AURA-DomainHashEmbedder-384

Rather than relying on non-deterministic, multi-gigabyte neural transformer weights in restricted automotive CI environments, AURA-Impact employs **`AURA-DomainHashEmbedder-384`**:

1. **Text Normalization:** Lowercased and tokenized into alphanumeric terms $w \in W$.
2. **Primary Token Hashing:** MD5 hashed into 384 dimensions:
   $$h_1(w) = \text{MD5}(w) \pmod{384}, \quad \vec{v}[h_1(w)] \mathrel{+}= 1.0$$
3. **3-Gram Subwords:** SHA-256 hashed character n-grams handle abbreviations and compound tokens:
   $$h_{\text{sub}}(s) = \text{SHA256}(s) \pmod{384}, \quad \vec{v}[h_{\text{sub}}(s)] \mathrel{+}= 0.35$$
4. **Domain Concept Anchoring:** Reinforced weights for calibrated automotive clusters (AEB, ACC, BMS, Powertrain, Body, Safety):
   $$\vec{v}[h_c] \mathrel{+}= 1.50$$
5. **L2 Unit Hypersphere Normalization:**
   $$\vec{v}_{\text{norm}} = \frac{\vec{v}}{\|\vec{v}\|_2}$$

This provides exact bit-for-bit reproducibility across all operating systems, microsecond query latency, and true air-gapped execution.

---

## 5. Fail-Closed Safety Architecture

When an artifact has ambiguous classification or missing trace links:
1. It is flagged as `REVIEW_REQUIRED`.
2. The safety gate fails closed: if an artifact might be safety-critical, its associated tests are retained by default.
3. If an explicit bypass is attempted, the system raises a `SafetyInvariantViolationError` and halts continuous deployment.
