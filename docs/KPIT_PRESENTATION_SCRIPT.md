# KPIT Sparkle Round 2: Master Presentation Script & Mentor Walkthrough
**Project:** AURA-Impact (Automotive Unified Regression & Architecture Impact Intelligence)  
**Team:** THE GOAT  
**Event:** KPIT Sparkle Round 2 Online Mentor Session  
**Document Reference:** AURA-PRES-SCRIPT-2027  

---

## 🕒 Presentation Overview & Timing Strategy

- **Total Allocation:** 15 Minutes (10 Minutes Structured Presentation + 5 Minutes Mentor Q&A / Live Demo).
- **Core Narrative:** How AURA-Impact solves the fundamental tension between rapid SDV integration agility and strict ISO 26262 functional safety through a four-stage hybrid architecture: **PROVE $\to$ RECOVER $\to$ FILTER $\to$ PROTECT**.
- **Tone:** Technically authoritative, scientifically honest, evidence-grounded, zero hallucination.

---

## Slide 1: The SDV Integration Crisis (Problem & Motivation)

### Visual Content:
- Multi-tier automotive supply chain diagram: OEM $\leftrightarrow$ Tier-1 $\leftrightarrow$ Tier-2.
- The bottleneck: 100+ million lines of code, 5,000+ AUTOSAR SWCs, multi-day Hardware-in-the-Loop (HIL) regression cycles.
- The two failure modes:
  1. *Under-testing:* Escaped integration regressions in safety-critical software (ASIL-C/D).
  2. *Over-testing:* Re-running entire multi-day regression suites for minor interface tweaks.

### Speaking Notes:
> *"Respected mentors, in modern Software-Defined Vehicles, automotive software is evolving from static, isolated ECUs to dynamic, distributed software architectures. However, continuous integration in automotive development faces a crippling bottleneck: when an engineer modifies a low-level C driver or an AUTOSAR interface, running the entire regression test suite takes up to 48 hours on limited Hardware-in-the-Loop test rigs.*
> 
> *Current practices force engineers into a dangerous compromise: either run broad, unfocused test suites that delay continuous delivery, or manually guess which tests to run, risking escaped safety defects. Pure static call graphs miss unlinked semantic dependencies, while standalone AI language models hallucinate false dependencies across different vehicle domains. AURA-Impact was engineered to solve this dilemma."*

---

## Slide 2: The AURA-Impact Hybrid Architecture

### Visual Content:
- System Architecture Block Diagram:
  - Ingestion (Git Diff + ARXML + C Source) $\to$ Change Classifier.
  - Dual Engine: Bounded Deterministic Graph ($k \le 3$) + Dense Semantic Vectorizer (`AURA-DomainHashEmbedder-384`).
  - Context Filter (Subsystem Boundary Gate) $\to$ Strict Union Fusion ($S_{\text{final}} = S_{\text{struct}} \cup S_{\text{semantic}}$).
  - Regression Selector $\to$ Non-Bypassable Safety Gate ($T_{\text{safe}} \subseteq T_{\text{selected}}$).

### Speaking Notes:
> *"AURA-Impact is not another black-box AI model, nor is it a simple graph parser. It is a two-stage hybrid change-impact analysis engine. Stage 1 executes deterministic, depth-bounded breadth-first search across explicit architectural AST and ARXML call paths. When structural evidence is complete, it terminates with 100% confidence.*
> 
> *Only when explicit trace links are missing or broken does Stage 2 activate: our deterministic domain-concept hash embedder recovers latent dependencies without requiring multi-gigabyte neural weights. These candidates are then passed through hard automotive context filters—such as subsystem and ECU boundaries—before our non-bypassable safety gate guarantees that safety-critical tests are never omitted."*

---

## Slide 3: The Innovation: PROVE → RECOVER → FILTER → PROTECT

### Visual Content:
- 4-Quadrant Flowchart:
  1. **PROVE:** Deterministic structural evidence first ($1.0$ confidence).
  2. **RECOVER:** Dense semantic fallback for unlinked requirements & code.
  3. **FILTER:** Hard subsystem boundary isolation (rejecting 90%+ distractors).
  4. **PROTECT:** Mandatory ISO 26262 ASIL-C/D retention invariant ($100\%$).

### Speaking Notes:
> *"The heart of our innovation is the PROVE $\to$ RECOVER $\to$ FILTER $\to$ PROTECT methodology. Traditional tools make the mistake of either trusting AI completely or rejecting AI entirely. We establish that deterministic structural evidence must always be evaluated first.*
> 
> *When semantic recovery is needed, we filter retrieved candidates against hard engineering constraints. If a candidate passes lexical similarity but belongs to the Infotainment domain while the change occurred in Autonomous Emergency Braking, our filter immediately rejects it. Finally, our safety gate guarantees mathematically that any test tagged ASIL-C or ASIL-D is retained, regardless of any optimization heuristic."*

---

## Slide 4: Working Prototype & Codebase Maturity

### Visual Content:
- Codebase metrics callout:
  - 256 Automated Pytest Gates Passing ($100\%$).
  - Full pipeline implemented in Python with NetworkX, NumPy, and FAISS.
  - Interactive Streamlit Dashboard (`dashboard/app.py`).
  - Cryptographic JSON audit trails for every analysis decision.

### Speaking Notes:
> *"AURA-Impact is not a conceptual slide deck—it is a fully implemented, working engineering prototype. Our codebase includes 256 automated unit, integration, and adversarial tests passing with zero failures. We provide an interactive Streamlit demonstrator that visualizes graph propagation, semantic candidate scoring, and safety justifications in real time. Every decision is cryptographically logged into auditable JSON evidence reports suitable for OEM compliance audits."*

---

## Slide 5: Multi-Dataset Public Validation Strategy

### Visual Content:
- Matrix of 4 Public Datasets:
  - **Dronology (CPS):** 53 Requirements, 43 Classes, 15 Hazards, 101 Trace Links.
  - **Defects4J (Bugs):** Real historical defects in Commons-Cli, triggering tests vs. relevant pool.
  - **Autoware.Universe (Automotive):** Production C++ / ROS 2 Autonomous Emergency Braking stack.
  - **Alexandria (Evolution):** Real Git commit co-change evolution.

### Speaking Notes:
> *"To ensure scientific defensibility, we did not rely solely on synthetic models. We subjected AURA-Impact to four real-world public datasets across different software disciplines:*
> 
> *First, Dronology—a peer-reviewed cyber-physical safety benchmark from the University of Notre Dame. Second, Defects4J—evaluating real historical software defects and regression testing. Third, Autoware.Universe—verifying architectural compatibility against real C++ and ROS 2 autonomous driving stacks. And fourth, Alexandria—mining historical Git co-change patterns to evaluate evolutionary coupling."*

---

## Slide 6: Experimental Methodology & Anti-Leakage Safeguards

### Visual Content:
- Controlled trace-link deletion diagram (10%, 20%, 30% deletion across seeds 42, 101, 202).
- Data quarantine boundary: pre-change snapshot only; target test outcomes and fixing patches strictly quarantined.
- Standardized baselines: Keyword (TF-IDF), Embedding-Only, Graph-Only, AURA-Impact.

### Speaking Notes:
> *"Our experimental design adheres strictly to academic standards: all four baselines received identical graph snapshots and change inputs. In Dronology, we performed controlled trace-link deletion experiments at 10%, 20%, and 30% deletion rates across multiple random seeds, totaling 720 scenario evaluations.*
> 
> *Crucially, we enforced strict anti-leakage safeguards: our retrieval engine was only given access to pre-change code states. We never leaked fixing patches or test outcomes during prediction, ensuring that our results reflect genuine continuous integration conditions."*

---

## Slide 7: Benchmark Results Across Public Datasets

### Visual Content:
- Master Benchmark Summary Table:
  - Dronology: AURA Recall **100.0%** vs. Graph-Only **22.2%** ($p = 1.62 \times 10^{-12}$).
  - Defects4J: **100.0%** Bug-Triggering Test Recall with **54.10%** Suite Reduction.
  - Autoware: Cross-package AEB propagation with 0% decoy FPR.
  - Latency: **0.13 ms to 0.18 ms** per transaction.

### Speaking Notes:
> *"The empirical evidence confirms the power of our hybrid architecture. On Dronology, when trace links were intentionally deleted, Graph-Only traversal suffered severe blindness, achieving only 22.2% recall. AURA-Impact recovered 100.0% of the deleted target requirements, a statistically significant gain confirmed by Wilcoxon signed-rank tests ($p < 10^{-11}$).*
> 
> *On Defects4J, evaluating 10 real historical bugs, AURA-Impact achieved 100% recall of the exact triggering tests that expose the faults, while reducing test suite execution overhead by 54.10%. Furthermore, our execution latency averages under 0.2 milliseconds, making it instantaneous inside pre-commit hooks."*

---

## Slide 8: Safety Validation & The Non-Bypassable Invariant

### Visual Content:
- Mathematical Invariant Assertion: $T_{\text{safe}} \subseteq T_{\text{selected}}$.
- Fault Injection Results Table:
  - Stripped safety metadata $\to$ Fails closed (`REVIEW_REQUIRED`).
  - Empty candidate sets $\to$ Mandatory ASIL-D tests unconditionally retained.
  - Attempted exclusion attack $\to$ `SafetyInvariantViolationError` triggered.
  - Safety Retention: **100.0%** across all 720 iterations.

### Speaking Notes:
> *"In automotive engineering, safety is non-negotiable. Standard AI optimization algorithms will readily discard a safety test if it reduces test suite size. AURA-Impact makes this mathematically impossible.*
> 
> *Our safety gate acts as a non-bypassable post-selection filter. In our fault-injection tests, when we intentionally stripped safety metadata or attempted to force deselect ASIL-D tests, the system failed closed and raised a SafetyInvariantViolationError. Across all 720 Dronology iterations and all Autoware emergency braking scenarios, our safety retention was exactly 100.0%."*

---

## Slide 9: Live Demonstrator Walkthrough

### Visual Content:
- Live Demo sequence in Streamlit:
  1. Select Dronology / Autoware dataset.
  2. Select change scenario: AEB Deceleration Parameter Modification.
  3. Inspect Stage 1 Graph: shows call propagation to `vehicle_cmd_gate`.
  4. Inspect Stage 2 Semantic: shows recovered latent interface.
  5. Inspect Safety Gate: verifies `test_autonomous_emergency_braking` retention.
  6. Export auditable JSON trace.

### Speaking Notes:
> *"(Transition to live screen): Let me demonstrate this in our live dashboard. Here we select Autoware.Universe and simulate a modification to the autonomous emergency braking deceleration threshold in node.cpp.*
> 
> *In the impact graph, we see Stage 1 deterministically traverse the ROS 2 interface to the Vehicle Command Gate. In the semantic tab, latent concept matching identifies the emergency stop actuation routine. And in the safety gate tab, the system verifies that our ASIL-D braking test is unconditionally locked into the execution suite, completing the analysis in 0.13 milliseconds."*

---

## Slide 10: Scientific Limitations & Research Boundaries

### Visual Content:
- Transparent boundaries callout:
  - Prototype Status: Academic engineering demonstrator, not TÜV-certified tool qualification.
  - Synthetic deletion vs. real-world specification decay.
  - Java (Defects4J) vs. Embedded C/AUTOSAR memory models.
  - Deliberate trade-off: High Recall (safety-first) over aggressive precision.

### Speaking Notes:
> *"To be completely honest with our mentors: we recognize the boundaries of our current research. AURA-Impact is an engineering prototype, not a commercially certified ISO 26262 Tool Confidence Level tool. Controlled link deletion in Dronology uses synthetic masking, which has higher lexical congruence than fragmented industrial specs.*
> 
> *Furthermore, our 54.10% test reduction on real bugs reflects a deliberate engineering choice: we prioritize safety-critical recall over aggressive test pruning. In automotive systems, running a few extra tests costs minutes; missing a safety defect costs lives."*

---

## Slide 11: Industrial Relevance & KPIT Alignment

### Visual Content:
- Integration Architecture Diagram:
  - Git / Gerrit Pre-Commit Hook $\to$ AURA-Impact Microservice.
  - ALM Integration: PTC Windchill, IBM DOORS, Siemens Polarion.
  - HIL Test Harness: Vector CANoe, dSPACE, Jenkins CI.
  - Direct value: Slashes HIL bench queue times by 50%+, prevents escaped integration defects.

### Speaking Notes:
> *"How does this create direct commercial value for KPIT and Tier-1 automotive suppliers? In an OEM software factory, hundreds of pull requests are submitted daily. AURA-Impact integrates directly as a pre-commit GitHub Action or Gerrit hook.*
> 
> *By cutting regression test suites in half while guaranteeing 100% safety test coverage, Tier-1 suppliers can double their daily CI throughput on multi-million-dollar HIL test benches. Furthermore, our cryptographic JSON evidence reports provide automated compliance trails for ISO 26262 and ASPICE audits."*

---

## Slide 12: Conclusion & Summary of Contributions

### Visual Content:
- Summary Highlights:
  - Hybrid Architecture: Bounded Graph + Deterministic 384-d Domain Hash Embedder.
  - Multi-Dataset Grounding: Dronology, Defects4J, Autoware.Universe, Alexandria.
  - 100% Safety Invariant Verified ($T_{\text{safe}} \subseteq T_{\text{selected}}$).
  - 256 Passing Tests | 0.13–0.18 ms Execution Latency.
- Team closing quote.

### Speaking Notes:
> *"To conclude: traditional dependency graphs provide deterministic evidence but suffer from graph blindness when links break. Pure semantic AI retrieves plausible but dangerous false positives. AURA-Impact unites deterministic engineering graphs, context-constrained semantic recovery, and mandatory safety gates.*
> 
> *We have proven its efficacy across real-world CPS traceability, real historical software faults, and production automotive architectures. Thank you, mentors. We are now eager to take your questions."*
