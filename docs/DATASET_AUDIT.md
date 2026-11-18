# AURA-Impact Dataset Audit & Verification Report
**KPIT Sparkle Round 2 — Phase 1 Dataset Audit**  
**Date:** November 2026  
**Auditors:** THE GOAT (AURA-Impact Engineering & Research Validation Team)  
**Status:** All Target Public Datasets Audited, Verified, and Ground-Truth Confirmed  

---

## 1. Dataset Strategy & Verification Overview

AURA-Impact evaluates four distinct public dataset targets to rigorously validate its hybrid architecture across diverse engineering conditions:

```
+----------------------------------------------------------------------------------------------------+
|                                    AURA-IMPACT DATASET STRATEGY                                    |
+----------------------------------------------------------------------------------------------------+
| 1. DRONOLOGY (Safety-Critical CPS)                                                                 |
|    - Grounding: Requirements-to-Code-to-Test Traceability & Failure Modes (FMECA)                  |
|    - Validation: Controlled 10%, 20%, 30% Link Deletion & Latent Dependency Recovery               |
+----------------------------------------------------------------------------------------------------+
| 2. DEFECTS4J (Historical Software Defects & RTS)                                                   |
|    - Grounding: Real Historical Software Bugs, Triggering Tests, and Relevant Regression Suites    |
|    - Validation: Bug-Triggering Test Recall, Regression Suite Reduction, and Defect Detection      |
+----------------------------------------------------------------------------------------------------+
| 3. AUTOWARE.UNIVERSE (Automotive Software Architecture)                                            |
|    - Grounding: ROS 2 / C++ Production Autonomous Driving Stack (AEB, Control, Planning, Sensing)  |
|    - Validation: Real-World Automotive Dependency Graph Traversal & Contextual Impact Scenarios    |
+----------------------------------------------------------------------------------------------------+
| 4. CO-CHANGE EVOLUTION (Alexandria Historical Co-Change Mining)                                    |
|    - Grounding: Git Historical Commit Logs Filtered for Untangled Co-Modifications                 |
|    - Validation: Historical Temporal Co-Change Prediction as Supplementary Proxy Evidence           |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Dataset 1: Dronology (Primary CPS Safety Dataset)

### 2.1 Metadata & Provenance
* **Official Source:** University of Notre Dame / SAREC Lab (Prof. Jane Cleland-Huang, et al.).
* **Canonical Repository:** `https://github.com/JaneClelandHuang/Dronology`
* **Dataset File:** `Artifacts_Version07.xlsx`
* **License:** MIT License (`LICENSE` confirmed in repository root)
* **Release Version:** Version 0.7 (Standard ICSE / RE / CoEST Benchmark)
* **Download Size:** ~23.5 KB (Traceability metadata) + ~886 KB (Full Java Source & Tests)

### 2.2 Available Artifact Types
1. **Requirements:** 53 explicit software requirements (e.g., flight safety, drone allocation, geofencing, collision avoidance).
2. **Safety & Hazard Metadata (FMECA):** 15 Failure Modes, Effects, and Criticality Analysis hazards with explicit criticalities (e.g. `Critical`, `High`, `Medium`).
3. **Design Decisions:** Architectural diversion algorithms and safety constraints.
4. **Assumptions:** 14 environmental and navigational assumptions.
5. **Java Classes:** 43 production Java classes (`controller`, `model`, `start`, `view`).
6. **Test Specifications:** Java JUnit test cases covering flight planning and controller routing.

### 2.3 Verified Ground Truth
* **Requirement-to-Code Links:** Column `Requirement Link` in Sheet `Classes` maps specific Java classes to requirement IDs (e.g., `FlightPlanner.java` $\to$ `R1, R2, R5`).
* **Requirement-to-Hazard Links:** FMECA hazards mapped to safety mitigations.
* **Controlled Link Deletion Protocol:** Ground-truth links are systematically masked at 10%, 20%, and 30% deletion rates across seeds to evaluate whether AURA-Impact recovers hidden trace links that graph-only traversal misses.

---

## 3. Dataset 2: Defects4J (Secondary Real Historical Defect Benchmark)

### 3.1 Metadata & Provenance
* **Official Source:** University of Washington & University of Massachusetts (René Just, et al., ISSTA).
* **Canonical Repository:** `https://github.com/rjust/defects4j`
* **License:** MIT License
* **Release Version:** Defects4J v2.0.0 (Master branch verified)
* **Download Size:** 150 MB (Metadata & Harness)
* **Target Project Evaluated:** `Commons-Cli` and `Commons-Lang` (compact, self-contained, reproducible test suites).

### 3.2 Available Artifact Types & Historical Versions
1. **Buggy & Fixed Revisions:** Source commits before and after defect fixes.
2. **Patch Diffs:** `patches/<bug_id>.src.patch` detailing exact line/token modifications.
3. **Modified Classes:** `modified_classes/<bug_id>.src` identifying root-cause source artifacts.
4. **Triggering Tests:** `trigger_tests/<bug_id>` containing the exact test cases that fail on the buggy version and pass on the fixed version.
5. **Relevant Regression Suites:** `relevant_tests/<bug_id>` providing the complete pool of candidate regression tests.

### 3.3 Verified Ground Truth
* **Defect Triggering Ground Truth:** A test is considered ground-truth relevant if it appears in `trigger_tests/<bug_id>`.
* **RTS Evaluation Protocol:**
  $$\text{Test Recall} = \frac{|T_{\text{selected}} \cap T_{\text{triggering}}|}{|T_{\text{triggering}}|}$$
  $$\text{Suite Reduction} = 1 - \frac{|T_{\text{selected}}|}{|T_{\text{relevant}}|}$$
* **Anti-Leakage Safeguard:** Only the pre-change code state and diff are provided to the impact engine. Target test execution results and fixing patches are strictly quarantined.

---

## 4. Dataset 3: Autoware (Automotive Architecture Validation)

### 4.1 Verification & Anti-Hallucination Audit
> [!IMPORTANT]
> **Repository Distinction Verification:**
> - `autowarefoundation/autoware`: A 2.4 MB meta-repository containing `.repos` YAML definitions and setup scripts. It does **not** contain the primary automotive algorithms.
> - `autowarefoundation/autoware.universe`: The **canonical 625 MB production software implementation** containing all core autonomous driving components.
> - **Audit Decision:** We specifically audit and ingest `autowarefoundation/autoware.universe`.

### 4.2 Metadata & Provenance
* **Official Source:** Autoware Foundation / Tier IV / OpenADx.
* **Canonical Repository:** `https://github.com/autowarefoundation/autoware.universe`
* **License:** Apache License 2.0
* **Release Version:** Main branch (ROS 2 Humble / Iron / Rolling target)
* **Target Automotive Subsystems:**
  - `control/autoware_autonomous_emergency_braking` (Autonomous Emergency Braking - AEB)
  - `control/autoware_vehicle_cmd_gate` (Safety command gate)
  - `control/autoware_collision_detector` (Collision detection node)
  - `control/autoware_mpc_lateral_controller` (Steering / trajectory control)
  - `planning/autoware_motion_velocity_planner` (Velocity & deceleration planning)

### 4.3 Available Artifact Types & Ground Truth
1. **Package Declarations:** `package.xml` specifying explicit ROS 2 package dependencies (`<depend>`, `<exec_depend>`, `<test_depend>`).
2. **Build Definitions:** `CMakeLists.txt` defining C++ executable and library targets.
3. **C++ Headers & Sources:** `include/` and `src/` declaring ROS 2 nodes, publishers, subscribers, and callbacks.
4. **Unit Tests:** `test/` directory containing `ament_cmake_gtest` test suites verifying trajectory safety and deceleration commands.
5. **Architectural Ground Truth:** Exact inter-package and component-level call graph topology verified by ROS 2 package manifests.

---

## 5. Dataset 4: Alexandria / Historical Co-Change Mining

### 5.1 Metadata & Provenance
* **Concept:** Mining Software Repositories (MSR) co-change analysis.
* **Extraction Source:** Historical Git commits from autonomous software repositories (`autoware.universe` / `dronology`).
* **Filtering Heuristics:**
  - Commits with $>10$ modified files are discarded (tangled commits).
  - Merge commits are discarded.
  - Pure documentation/formatting commits are excluded.
* **Evaluation Protocol:**
  - Evaluates whether two artifacts that frequently co-change historically, but lack an explicit static call link in the structural graph, can be recovered semantically by AURA-Impact.
  - Reported strictly as a **proxy supplementary metric**, not as absolute ground-truth dependencies.

---

## 6. Dataset Ingestion Manifest & Structure

```
data/
├── manifests/
│   └── dataset_manifest.json          # Checksums, URLs, licensing, artifact counts
├── raw/
│   ├── dronology/                     # Original Artifacts_Version07.xlsx & Java files
│   ├── defects4j/                     # Patches, triggering tests, modified classes
│   ├── autoware/                      # Package manifests & C++ source trees
│   └── alexandria/                    # Extracted clean co-change commit pairs
└── processed/
    ├── unified_graphs/                # Ingested MultiDiGraphs in canonical schema
    ├── ground_truth/                  # Standardized JSON ground-truth mappings
    └── change_scenarios/              # Standardized change contexts for benchmark execution
```

---
*Dataset Audit Approved for Phase 2: Ingestion Pipeline Implementation.*

