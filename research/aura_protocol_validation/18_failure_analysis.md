# 18 — Failure Analysis
## Conditions That Would Kill The Research Direction
**Classification:** Hostile Failure Mode Analysis  
**Date:** 2026-10-01

---

## 1. The Kill Conditions

As stated in the research brief: the hypothesis must be killed if any of these conditions are met.

---

### Kill Condition 1: Existing Standards Already Solve The Problem

**Status:** EVALUATED  
**Finding:** No existing standard solves the combination of (A) cross-vendor semantic capability matching + (B) ODD-aware compatibility + (C) safety contract verification + (D) provenance-backed trust + (E) change-impact-driven invalidation.  
**Evidence:** See [03_standards_landscape.md] — full per-standard audit.  
**Most dangerous near-miss:** OPC UA for Robotics (PA-016) — solves capability description and semantic matching within OPC UA ecosystem. Does NOT solve ODD, ASIL, or change-impact.  
**Verdict:** **Kill Condition 1 NOT MET.**

---

### Kill Condition 2: No Meaningful Measurable Gap

**Status:** EVALUATED  
**Finding:** ISO 23374 documents 3-6 months integration time per deployment site; SAE papers document 4-8 weeks of manual parameter alignment per V2X configuration; Broy (2006) documents 30-50% of automotive system cost in integration.  
**Verdict:** **Kill Condition 2 NOT MET.** The gap is economically quantifiable.

---

### Kill Condition 3: Semantic Matching Cannot Achieve Acceptable Reliability

**Status:** PARTIALLY ASSESSED (requires empirical measurement)  
**Current evidence:**
- Dense embeddings (BGE-M3, which AURA-Impact already uses) achieve ~75-80% recall on technical synonym matching in domain-specific settings
- Ontology subsumption adds deterministic correction for false positives
- Safety gate provides hard backstop for safety-critical decisions
- Expected combined accuracy: 85-90% (Class A+B+C+D scenarios)

**Risk:** In the hybrid architecture, semantic matching only needs to succeed for the semantic layer. Hard constraints (safety, ODD, units) are verified deterministically regardless. The semantic layer only needs to distinguish "related concepts" from "completely different concepts" — a lower bar than general-purpose semantic matching.

**Scenario where this Kill Condition fires:** If embeddings produce > 20% false-positive rate for Class E (wrong ontology) — i.e., if "ObjectDetection (perception)" matches "ObjectDetection (database)" — the safety gate won't help because both have compatible safety classes.

**Current mitigation:** Ontology subsumption check (Stage 2) catches ontological domain mismatches that embeddings miss.

**Verdict:** **Kill Condition 3 CONDITIONAL — requires empirical benchmark to confirm.** If benchmark results show UAR > 0 due to semantic errors, the hypothesis is narrowed to: "AURA can solve Gaps C-E (units, safety, change-impact) but not Gap A (semantic) autonomously."

---

### Kill Condition 4: Safety Cannot Be Bounded

**Status:** EVALUATED  
**Finding:** Safety gate is deterministic. For Class I (safety mismatch) and Class K (malicious) instances, the deterministic ASIL comparison and cryptographic signature verification provide hard safety bounds.  
**Residual risk:** Cross-standard mapping (ISO 26262 ASIL ↔ IEC 61508 SIL) requires human-approved mapping table. Without this, cross-standard cases are routed to REVIEW_REQUIRED, never ACCEPT.  
**Verdict:** **Kill Condition 4 NOT MET.** Safety CAN be bounded. The mechanism is the deterministic safety gate.

---

### Kill Condition 5: Protocol Overhead Dominates Benefits

**Status:** ANALYTICALLY ASSESSED (requires empirical measurement)  
**Analysis:**
- Session establishment: 100–500ms (amortized over session duration of hours)
- Monitoring overhead: < 1% of CPU (periodic hash comparison)
- Change-impact notification: single webhook call
- Network overhead: capability manifests are ~5-10KB (one-time per capability)

**Risk scenario:** If sessions are very short-lived (< 1s), the 100-500ms establishment overhead is disproportionate. For AURA's target use cases (multi-minute to multi-hour capability bindings like valet parking sessions, logistics missions), the overhead is negligible.

**Quantitative break-even:** Session overhead is acceptable if session duration > 10× establishment time. At 200ms establishment, sessions > 2s are cost-justified.

**Verdict:** **Kill Condition 5 NOT MET for target use cases.** It WOULD fire for sub-second high-frequency capability switching — but that is explicitly OUT of scope.

---

### Kill Condition 6: Proprietary Systems Cannot Expose Sufficient Metadata

**Status:** EVALUATED — THIS IS A REAL RISK**

**Evidence:**
- Tesla architecture: no external interfaces for capability metadata. AURA cannot work with Tesla's internals.
- Waymo: no public service API.
- Most OEM proprietary systems: capability metadata is trade secret.

**Assessment:** This kill condition applies to CLOSED, MONOLITHIC, PROPRIETARY autonomous stacks. It does NOT apply to:
- AUTOSAR Adaptive systems (capability manifests can be generated from ARXML)
- ROS2 systems (capability information available from message type definitions)
- OPC UA systems (information models are accessible)
- Multi-supplier integration environments (suppliers can be required to provide manifests as a procurement condition)

**The research direction must explicitly exclude** closed monolithic systems (Tesla, Waymo as-is) from its applicability claims.

**Verdict:** **Kill Condition 6 PARTIALLY MET for closed proprietary systems.** The research direction is NARROWED but not killed. Target market is explicitly multi-vendor integration environments, not closed monolithic stacks.

---

### Kill Condition 7: Deployment Requires Unrealistic Standard Changes

**Status:** EVALUATED — SIGNIFICANT RISK

**Analysis:**
- AURA does not require changing SOME/IP, DDS, ROS2, or existing transport standards
- AURA requires: (a) an automotive capability manifest format, and (b) a shared capability ontology
- (a) can be a voluntary industry standard (like COVESA VSS was adopted voluntarily)
- (b) requires governance — but the robotics community has done this (ROS Industrial capability descriptions)

**Timeline risk:** Industry standard adoption typically takes 5-10 years. AURA cannot be commercially deployed until this happens.

**Research-level reframing:** For the research prototype, AURA does not require industry standardization. It requires only that participating systems adopt the manifest format — which is a bilateral agreement, not a standard.

**Verdict:** **Kill Condition 7 NOT MET for research.** It IS a risk for commercial deployment, which is correctly characterized as a long-term roadmap item, not a near-term deliverable.

---

### Kill Condition 8: Evaluation Cannot Produce Independent Ground Truth

**Status:** ADDRESSED IN DESIGN

**Mitigation:** Ground truth is established by expert panel before AURA results are generated. Benchmark is separate from AURA internals. Baselines are evaluated on identical data.

**Risk:** Expert disagreement on Class B (synonym) and Class L (ambiguous) cases. Mitigation: require unanimous agreement for ACCEPT/REJECT labels; route disagreements to REVIEW_REQUIRED.

**Verdict:** **Kill Condition 8 NOT MET** — benchmark design provides independent ground truth methodology.

---

## 2. Summary Kill Condition Assessment

| Kill Condition | Status | Action |
|---------------|--------|--------|
| 1. Already solved by standards | NOT MET | Proceed |
| 2. No measurable gap | NOT MET | Proceed |
| 3. Semantic matching unreliable | CONDITIONAL | Empirical validation required |
| 4. Safety not boundable | NOT MET | Proceed |
| 5. Protocol overhead dominates | NOT MET (for target use cases) | Clarify scope |
| 6. Proprietary metadata inaccessible | PARTIALLY MET | Narrow scope to multi-vendor environments |
| 7. Requires unrealistic standards | NOT MET (for research) | Note deployment risk |
| 8. No independent ground truth | NOT MET | Proceed |

**Overall Verdict:** The research direction survives. However, the scope must be NARROWED to:
- Explicitly exclude closed monolithic proprietary stacks (Tesla FSD, Waymo as-is)
- Focus on multi-vendor AUTOSAR Adaptive + ROS2 + OPC UA integration environments
- Acknowledge that deployment at scale requires industry adoption of manifest standard

---

## 3. Failure Modes in Deployment

Even if the research succeeds, deployment failure modes include:

| Failure Mode | Probability | Impact | Mitigation |
|-------------|------------|--------|-----------|
| Ontology governance failure (no consortium formed) | HIGH | CRITICAL — no shared vocabulary | Academic contribution → industry consortium pitch |
| Patent thicket blocking open standard | MEDIUM | HIGH | File provisional patents; license openly |
| Industry fragmentation (two competing manifest formats) | MEDIUM | HIGH | Early standardization engagement |
| ASIL certification cost prohibitive | HIGH | HIGH | Target non-safety-critical use cases first |
| Latency unacceptable in specific deployment context | LOW | MEDIUM | Cache and precompute |
| Security vulnerability in semantic layer exploited | LOW | HIGH | Defense-in-depth; deterministic gates |

---

## 4. Recommended Narrowing Actions

Based on the failure analysis, the research direction should be narrowed with these explicit scope statements:

### SCOPE IN:
1. Multi-vendor automotive software integration (AUTOSAR Adaptive + ROS2 + OPC UA)
2. Design-time capability compatibility analysis
3. CI/CD-integrated change-impact capability contract validation
4. Automated valet parking infrastructure integration (ISO 23374 use case)
5. Mixed logistics robot fleet integration

### SCOPE OUT:
1. Closed monolithic autonomous stacks (Tesla FSD, Waymo internal pipeline)
2. Real-time inner-loop control protocols
3. Consumer-vehicle perception pipeline integration
4. Blockchain/DLT-based distributed registry (technically disqualified)
5. Internet-of-Things sensor integration (different domain with different standards)

---

*Proceed to [19_novelty_analysis.md] for novelty classification.*
