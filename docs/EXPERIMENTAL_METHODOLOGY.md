# AURA-Impact Experimental Methodology & Benchmark Specification
**KPIT Sparkle Round 2 Research Validation**  
**Document Reference:** AURA-METH-SPEC-2027  
**Auditor:** THE GOAT (AURA-Impact Research Engineering)  

---

## 1. Experimental Objectives

This benchmark evaluates whether combining deterministic engineering graphs with context-constrained semantic retrieval provides measurable, statistically verified advantages over conventional impact analysis and regression testing baselines.

The evaluation answers five core research questions:
- **RQ1 (Latent Recovery):** Can AURA-Impact recover missing trace links when explicit structural edges are deleted?
- **RQ2 (Decoy Suppression):** Does hard engineering context filtering eliminate semantic false alarms?
- **RQ3 (Real Defect RTS):** Can the system select tests that expose real historical software bugs while reducing test suite execution overhead?
- **RQ4 (Automotive Compatibility):** Does the architecture scale and apply accurately to production autonomous driving software (ROS 2 / C++)?
- **RQ5 (Safety Invariant):** Is the 100% safety test retention invariant strictly maintained under hostile fault injection?

---

## 2. The Four Standardized Baselines

All evaluation approaches operate on identical graph snapshots and change inputs to ensure completely fair, unconfounded comparisons:

| Baseline | Traversal Mechanism | Semantic Recovery | Context Filtering | Safety Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline 1: Keyword** | None | TF-IDF (sublinear TF scaling) | None | Standard Mapping |
| **Baseline 2: Embedding-Only** | None | 384-d Dense Cosine Retrieval ($\tau=0.45$) | None | Standard Mapping |
| **Baseline 3: Graph-Only** | Deterministic BFS ($k \le 3$) | None (0% recovery on missing links) | None | Standard Mapping |
| **Baseline 4: AURA-Impact** | Deterministic BFS ($k \le 3$) | AURA-DomainHashEmbedder-384 ($\tau=0.45$) | Hard Subsystem Isolation Gate | Non-Bypassable Invariant ($T_{\text{safe}} \subseteq T_{\text{selected}}$) |

---

## 3. Dataset-Specific Experimental Protocols

### 3.1 Experiment A: Dronology (Controlled Link Deletion)
- **Dataset:** University of Notre Dame Dronology CPS Benchmark (53 requirements, 43 Java classes, 15 FMECA hazards, 101 verified trace links).
- **Protocol:**
  1. Ingest full ground-truth graph.
  2. Extract all verified $(Class \to Requirement)$ `IMPLEMENTS` edges.
  3. Systematically delete trace links at three controlled deletion rates: **10%**, **20%**, and **30%**.
  4. Repeat each deletion rate across three independent random seeds (**42, 101, 202**), yielding 720 total scenario evaluations.
  5. Feed only the masked graph (with deleted links hidden) to each baseline.
  6. Measure whether each baseline recovers the artificially deleted target requirement from code change queries.
  7. *Scientific Integrity:* Clearly reported as **synthetic missing-link experiments**, not organically discovered undocumented dependencies.

### 3.2 Experiment B: Defects4J (Real Historical Faults RTS)
- **Dataset:** Apache Commons-Cli historical faults (Bugs 1, 2, 3, 4, 5, 8, 11, 12, 13, 14).
- **Protocol:**
  1. For each bug, retrieve buggy source class and historical bug intent (strictly pre-change).
  2. Ground Truth: Target triggering tests identified in `trigger_tests/<bug_id>` that fail on the buggy version and pass on the fixed version.
  3. Pool: Full candidate regression suite from `relevant_tests/<bug_id>`.
  4. Measure:
     $$\text{Test Recall} = \frac{|T_{\text{selected}} \cap T_{\text{triggering}}|}{|T_{\text{triggering}}|}$$
     $$\text{Test Precision} = \frac{|T_{\text{selected}} \cap T_{\text{triggering}}|}{|T_{\text{selected}}|}$$
     $$\text{Suite Reduction} = 1 - \frac{|T_{\text{selected}}|}{|T_{\text{relevant}}|}$$

### 3.3 Experiment C: Autoware.Universe (Automotive Architecture)
- **Dataset:** Tier IV / Autoware Foundation `autoware.universe` (Autonomous Emergency Braking `control/autoware_autonomous_emergency_braking` and Vehicle Command Gate `control/autoware_vehicle_cmd_gate`).
- **Protocol:**
  1. Ingest ROS 2 `package.xml` dependencies, `CMakeLists.txt`, and C++ node implementations.
  2. Execute 4 representative automotive scenarios:
     - Scenario 1: AEB Deceleration Parameter Calibration (ASIL-D)
     - Scenario 2: Vehicle Command Gate Emergency Stop Actuation (ASIL-D)
     - Scenario 3: Motion Velocity Trajectory Planning (QM)
     - Scenario 4: Markdown Documentation Decoy (No-impact)
  3. Measure Precision, Recall, F1, Decoy Rejection, and Safety Test Retention.

### 3.4 Experiment D: Alexandria (Co-Change Evolution)
- **Dataset:** Historical Git commit co-change pairs extracted across repository evolution.
- **Protocol:**
  1. Filter tangled commits ($>10$ files modified) and merge commits.
  2. Evaluate semantic similarity on file pairs that historically co-change but have no direct static call graph edge.
  3. Report co-change prediction strictly as **supplementary proxy evidence**.

---

## 4. Anti-Leakage & Data Quarantine Safeguards

To prevent subtle research validation leakage, the experimental pipeline enforces:
1. **Temporal Isolation:** All baseline features, graphs, and vector indexes are constructed strictly from the pre-change software snapshot.
2. **Quarantine of Target Outcomes:** No baseline has access to bug-fixing commits, target patches, or future execution logs during prediction.
3. **Synthetic Edge Masking:** In link deletion experiments, masked edges are physically removed from the graph data structure, preventing graph traversers from accessing edge stubs or residual metadata.

---

## 5. Formal Evaluation Metrics

### A. Dependency Recovery Metrics
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
$$\text{F1} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}, \quad \text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$

### B. Regression Test Selection Metrics
$$\text{Test Selection Recall} = \frac{|T_{\text{selected}} \cap T_{\text{triggering}}|}{|T_{\text{triggering}}|}$$
$$\text{Test Selection Precision} = \frac{|T_{\text{selected}} \cap T_{\text{triggering}}|}{|T_{\text{selected}}|}$$
$$\text{Test Suite Reduction} = 1 - \frac{|T_{\text{selected}}|}{|T_{\text{pool}}|}$$

### C. Safety Gate Retention Metric
$$\text{Safety Retention} = \frac{|T_{\text{selected}} \cap T_{\text{safe}}|}{|T_{\text{safe}}|} = 100.0\% \quad (\text{Target: Non-Bypassable Invariant})$$

### D. Statistical Validation
Paired **Wilcoxon Signed-Rank Test** across paired scenario observations:
$$W = \min(W^+, W^-), \quad \alpha = 0.05$$
Results are considered statistically significant if $p < 0.05$.

