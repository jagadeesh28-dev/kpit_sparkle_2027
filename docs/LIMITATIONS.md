# AURA-Impact Scientific Limitations & Research Boundaries
**KPIT Sparkle Round 2 — Technical Integrity Statement**  
**Document Reference:** AURA-LIMIT-2027  
**Auditor:** THE GOAT (AURA-Impact Research Engineering)  

---

## 1. Zero-Hallucination & Scientific Integrity Policy

To uphold the highest academic and professional standards for KPIT Sparkle Round 2, this document explicitly states the empirical boundaries, known limitations, and non-certified status of **AURA-Impact**.

---

## 2. Research Prototype vs. Production Certification

> [!WARNING]
> **NO ISO 26262 TOOL QUALIFICATION CERTIFICATION:**
> AURA-Impact is an advanced **academic and engineering research prototype**. It is **not** currently certified by TÜV SÜD or any automotive body as an ISO 26262 Tool Confidence Level (TCL3 / TCL2) qualified software tool.
> - The safety gate implements the *principles* of ISO 26262 mandatory ASIL retention.
> - It must not be deployed as an autonomous, unmonitored safety filter in live vehicle manufacturing without formal safety manual qualification and independent auditor verification.

---

## 3. Dataset-Specific Scientific Boundaries

### 3.1 Dronology (Controlled Link Deletion vs. Real Omissions)
- In Experiment A, trace links between Java classes and requirements were **artificially deleted** at 10%, 20%, and 30% rates to benchmark recovery capabilities.
- While this methodology is the standard software engineering research protocol (CoEST / ICSE), artificially masked links have perfect historical semantic congruence. Real-world missing links in multi-tier OEM software often involve fragmented, informal, or poorly written specifications where lexical alignment is substantially lower.

### 3.2 Defects4J (Enterprise Java vs. Embedded C/AUTOSAR)
- Defects4J evaluates real historical software defects from open-source Java projects (`Commons-Cli`).
- While this provides definitive proof that AURA-Impact selects tests that expose real runtime faults, Java reflection, dynamic classloading, and object-oriented polymorphism differ from MISRA-C static memory allocation, AUTOSAR RTE macro generation, and synchronous periodic OS tasks.
- Regression test reduction on Defects4J was **54.10%**, whereas synthetic AUTOSAR benchmarks achieved 82.29%. We report both transparently.

### 3.3 Autoware.Universe (ROS 2 / C++ vs. Classic AUTOSAR)
- Autoware.Universe demonstrates real-world autonomous driving architecture in C++ and ROS 2 package manifests.
- However, our evaluation was performed on static package dependency graphs, CMake target configurations, and C++ source code ASTs. It was **not executed on physical vehicle CAN bus test benches or live hardware-in-the-loop (HIL) simulators**.

### 3.4 Alexandria (Co-Change Coupling as a Proxy Metric)
- Historical co-change relationships mined from Git commit logs reflect files that developers frequently committed together.
- Co-change is a **statistical proxy metric**, not a proven physical runtime dependency. A developer may commit two files together due to organizational habits or build updates rather than genuine functional coupling. AURA-Impact treats co-change strictly as secondary supporting evidence.

---

## 4. Algorithmic & Model Boundaries

### 4.1 Vocabulary Shift & Domain Adaptation
- `AURA-DomainHashEmbedder-384` uses deterministic concept clustering calibrated to automotive domains (AEB, ACC, BMS, Powertrain, Body, Safety).
- When applied to completely foreign domains (e.g., aerospace telecommand protocols or database query engines), subword hash collisions increase, causing lower semantic precision unless the domain concept cluster dictionary is updated.

### 4.2 Precision vs. Recall Trade-Off
- In automotive functional safety, **missing a true dependency is catastrophic**, whereas including a redundant test merely increases execution time.
- AURA-Impact is deliberately tuned to maximize **Recall** at the cost of modest Precision (precision ranges from 11% to 26% during recovery). This behavior is an intentional safety engineering design decision.

---

## 5. Summary of Truthful Commitments

1. We do not claim 100% full-system integration test reduction; we claim **54.10% on real historical defects** and **82.29% on synthetic models**.
2. We do not claim complete replacement of manual integration engineers; we provide an **explainable evidence assistant**.
3. We do not claim that synthetic link deletion equals real-world software decay; we report it as a reproducible controlled benchmark.
4. When evidence is ambiguous, the system halts with `REVIEW_REQUIRED` and fails closed.
