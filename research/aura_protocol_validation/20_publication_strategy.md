# 20 — Publication Strategy
## Target Venues and Paper Positioning
**Classification:** Academic Publication Roadmap  
**Date:** 2026-10-01

---

## 1. Publication Tier Strategy

### Paper 1 (Short/Workshop): Semantic Gap Demonstration
**Target:** IEEE IV Workshop / ITSC Workshop / DAC Automotive Track  
**Timeline:** 6 months from prototype completion  
**Contribution:** Demonstrate benchmark dataset + baseline comparison showing semantic gap exists  
**Length:** 4-6 pages  
**Key Result:** Class B (synonym) recall gap between B0 (exact match) and AURA  
**Risk:** Low — demonstrating a gap is publishable even without full solution

### Paper 2 (Full Conference): AURA Semantic Gateway
**Target:** IEEE ITSC, IEEE IV, DATE (Design Automation and Test in Europe), ACM SAC  
**Timeline:** 12 months from prototype  
**Contribution:** Full AURA architecture, benchmark evaluation across all 14 classes, UAR = 0 on safety classes  
**Length:** 8 pages (IEEE format)  
**Key Result:** AURA achieves F1 > 87% while maintaining UAR = 0 on safety/malicious classes  
**Risk:** Medium — requires benchmark empirical results

### Paper 3 (Journal): Change-Impact Contract Invalidation
**Target:** IEEE Transactions on Intelligent Transportation Systems (T-ITS), IEEE Transactions on Vehicular Technology  
**Timeline:** 18-24 months from prototype  
**Contribution:** Formal model + experimental validation of Scenario 2 (change-impact invalidation)  
**Length:** 12-14 pages  
**Key Result:** Sub-500ms invalidation with zero missed invalidations in controlled experiments  
**Risk:** Medium-High — requires extensive empirical validation

---

## 2. Positioning Strategy

### Do NOT position AURA as:
- "The UPI of autonomous driving" (misleading, kills technical credibility)
- "A replacement for DDS/SOME/IP" (false, alienates the standards community)
- "The first semantic interoperability layer" (too broad, easily falsified)
- "An AI-first capability matching system" (safety reviewers will reject)

### DO position AURA as:
- "Change-impact-aware capability contract invalidation for multi-vendor autonomous systems"
- "Safety-bounded hybrid semantic-symbolic capability matching"
- "An engineering tool for automotive software integration teams"

### Recommended Abstract Opening:
> "Multi-vendor automotive software integration requires manual engineering effort to establish and maintain capability contracts between systems using different middleware, vocabularies, and safety standards. When provider software changes, existing capability assumptions silently become stale, potentially violating safety invariants. We present AURA Semantic Gateway, a protocol layer above existing middleware that automatically classifies capability compatibility, enforces safety contracts, and invalidates established bindings when software changes — with demonstrated Unsafe Acceptance Rate of 0% across safety-critical and adversarial test cases."

---

## 3. Related Work Positioning

**Must cite and differentiate from:**
1. OPC UA for Robotics (OPC 40010) — closest prior art, differentiate on automotive domain + change-impact
2. W3C WoT — differentiate on safety contracts + dynamic invalidation
3. Adler et al. DATE 2021 — differentiate on semantic matching + runtime vs. design-time
4. AURA-Impact (this team's prior work) — natural extension from internal to cross-system

**Avoid claiming to "solve" problems that others have "only partially addressed" without evidence.**

---

*Proceed to [21_kpit_strategy.md] for commercial strategy.*
