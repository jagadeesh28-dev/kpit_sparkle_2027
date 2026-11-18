# 22 — Future Roadmap
## 3-Year Research and Engineering Roadmap
**Classification:** Strategic Technology Roadmap  
**Date:** 2026-10-01

---

## Phase 0 (Months 0-3): Foundation

### Research
- Complete benchmark dataset (1,850 instances) with expert ground truth
- Develop automotive capability ontology prototype (v0.1, ~200 terms)
- Document formal capability manifest schema (JSON Schema + Pydantic)

### Engineering
- Implement AURA Semantic Gateway MVP (Python prototype)
- Integrate with existing AURA-Impact graph engine for change-impact
- Three-system synthetic testbed (Systems A, B, C)

### Deliverable
- Paper 1 draft: benchmark dataset + baseline comparison
- KPIT Sparkle submission: system demonstration

---

## Phase 1 (Months 3-9): Empirical Validation

### Research
- Execute full benchmark evaluation (all 14 classes, all 7 baselines)
- Validate UAR = 0 across Class I and K
- Validate Scenario 2 (change-impact invalidation) timing
- Statistical analysis and ablation study

### Engineering
- Harden MVP: test PKI, Ed25519 signing, unit test coverage > 90%
- Integrate with real AUTOSAR Adaptive simulator (ISOLAR-EVE or equivalent)
- Real DDS discovery integration (CycloneDDS)

### Deliverable
- Paper 2 (full conference paper) submission to IEEE ITSC or IV
- Open-source benchmark dataset release

---

## Phase 2 (Months 9-18): Domain Expansion

### Research
- Expand automotive capability ontology (v1.0, ~500 terms)
- Safety gate formal verification (TLA+ specification)
- Cross-standard safety class mapping study (ISO 26262 ↔ IEC 61508)

### Engineering
- Real AUTOSAR Adaptive integration (production-quality interface)
- Production PKI integration (automotive-grade CA)
- Change-impact monitoring at real CI/CD integration

### Deliverable
- Paper 3 (journal) submission to IEEE T-ITS
- KPIT pilot project initiation

---

## Phase 3 (Months 18-36): Standardization and Commercialization

### Research
- Contribute automotive capability manifest format to COVESA working group
- Propose AUTOSAR Adaptive companion specification

### Engineering
- Safety certification of AURA Safety Gate to ASIL-B (ISO 26262 part 4/5/6)
- Multi-tenant capability registry (federated deployment)

### Deliverable
- AUTOSAR companion specification proposal
- KPIT commercial integration intelligence product

---

## The Critical Path

The **single most important near-term deliverable** is the empirical validation of UAR = 0 for safety-critical cases. Without this, all other claims are unverifiable.

Priority order:
1. Implement safety gate (deterministic ASIL comparison)
2. Build Class I and K benchmark instances with ground truth
3. Run benchmark → confirm UAR = 0
4. Everything else is secondary

---

*Proceed to [FINAL_RESEARCH_VERDICT.md] for the final verdict.*
