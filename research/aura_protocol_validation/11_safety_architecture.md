# 11 — Safety Architecture
## ISO 26262, SOTIF, and SAE 21434 Integration for AURA
**Classification:** Safety Architecture Specification  
**Date:** 2026-10-01

---

## 1. Applicable Safety Standards

| Standard | Scope | AURA Relevance |
|---------|-------|---------------|
| ISO 26262:2018 | Functional safety of road vehicles | Safety class verification, ASIL mapping |
| ISO 21448:2022 (SOTIF) | Safety of intended functionality | ODD verification, capability scope |
| ISO/SAE 21434:2021 | Automotive cybersecurity | Security of capability contracts |
| ISO 24089:2023 | Software updates in road vehicles | Change-impact and OTA capability invalidation |

---

## 2. The Core Safety Architecture Question

> **Can semantic negotiation itself be safety-critical?**

**Answer:** YES. If AURA accepts an incompatible capability contract, the consuming system may operate on incorrect assumptions, potentially causing hazardous situations.

**Therefore:** AURA's safety gate (Stage 4 of matching) is itself a safety-relevant function and must be designed accordingly.

### 2.1 What Is AURA's ASIL?

**Argument for ASIL-B minimum:**
- AURA makes binary binding decisions (ACCEPT/REJECT)
- A False Acceptance (Type I error) can propagate to ASIL-D functions downstream
- Therefore AURA must be at minimum ASIL-B (single-point fault detection)

**Argument against over-specifying ASIL-D:**
- AURA does not control vehicle actuators directly
- A False Acceptance does not immediately cause an accident — the consuming system's own safety mechanisms provide a layer of protection
- AURA is defense-in-depth, not the last line of defense

**Pragmatic position:** AURA's Safety Gate component should be designed to ASIL-B requirements. Other components (semantic matching, normalization) can be QM. The architecture enforces that QM components CANNOT override the ASIL-B Safety Gate.

---

## 3. Safety Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AURA SAFETY ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  LAYER 1: AI/SEMANTIC REASONING LAYER                    [QM]                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • Dense vector embedding similarity                                          │
│  • Ontology subsumption check                                                 │
│  • Semantic synonym resolution                                                │
│  • Output: CANDIDATE CONTRACTS + confidence scores                            │
│                                                                               │
│  ↓ Passes only candidates, never makes final decision                         │
│                                                                               │
│  LAYER 2: CONTEXT VERIFICATION LAYER                     [QM → ASIL-A]       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • ODD boundary checking (deterministic)                                      │
│  • Unit verification (deterministic)                                          │
│  • Coordinate frame verification (deterministic)                              │
│  • Output: CONTEXT_PASS / CONTEXT_FAIL with reason                            │
│                                                                               │
│  ↓ Context-failed contracts are eliminated before safety gate                 │
│                                                                               │
│  LAYER 3: SAFETY CONTRACT GATE                           [ASIL-B]            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • ASIL class comparison (ISO 26262 decomposition rules)                      │
│  • Fail-safe behavior compatibility                                           │
│  • Latency and accuracy hard limits                                           │
│  • RULE: If safety gate FAILS → REJECT. No override. No exception.            │
│  • Output: PASS or REJECT_SAFETY with reason code                             │
│                                                                               │
│  ↓ SAFETY GATE IS NON-BYPASSABLE                                              │
│                                                                               │
│  LAYER 4: TRUST AND PROVENANCE GATE                      [ASIL-A]            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • Cryptographic signature verification                                       │
│  • Certificate revocation check                                               │
│  • Contract temporal validity                                                 │
│  • Change impact verification                                                 │
│  • Output: TRUST_PASS or TRUST_FAIL with reason                               │
│                                                                               │
│  ↓ Trust-failed contracts are rejected                                        │
│                                                                               │
│  LAYER 5: FINAL BINDING AUTHORIZATION                    [ASIL-B]            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • Only reached if Layers 2, 3, 4 all PASS                                   │
│  • Generates CapabilityBinding record                                         │
│  • Activates transport binding                                                │
│  • Registers with change-impact monitor                                       │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Critical Design Invariant:**

> The output of Layer 1 (AI reasoning) is a CANDIDATE SET, not a decision.  
> The DECISION is made only by deterministic Layers 2–5.  
> AI reasoning CANNOT override deterministic safety checks.

---

## 4. ISO 26262 Integration Points

### 4.1 ASIL Comparison Logic

ASIL is defined in ISO 26262 as: ASIL A < ASIL B < ASIL C < ASIL D (QM < all)

**AURA Safety Gate Rule:**
```
def asil_compatible(provider_asil, required_asil):
    ASIL_ORDER = {"QM": 0, "A": 1, "B": 2, "C": 3, "D": 4}
    return ASIL_ORDER[provider_asil] >= ASIL_ORDER[required_asil]
```

**Cross-Standard Translation:** SIL (IEC 61508) and ASIL (ISO 26262) are not directly comparable without standard-specific mapping. AURA requires `safety.integrity_level_standard` to be specified. Cross-standard mapping requires explicit human-approved mapping table per deployment.

### 4.2 SOTIF Integration

ISO 21448 addresses "performance limitations" in the operating domain. AURA's ODD verification (Layer 2) directly implements SOTIF requirements:

- **SOTIF Requirement:** System must not operate outside its intended use case.
- **AURA Implementation:** ODD check verifies current operating environment is within provider's declared ODD before accepting capability binding.

### 4.3 ISO 24089 (Software Updates)

AURA's change-impact engine directly implements ISO 24089 principles:

- **ISO 24089 Requirement:** Software updates must not invalidate existing safety properties without re-validation.
- **AURA Implementation:** When provider software changes, change-impact engine detects affected capabilities and triggers CapabilityInvalidationNotice to consumers. Consumer is forced to re-negotiate or activate fail-safe.

---

## 5. What Must NEVER Be Decided by AI/ML

| Decision | Allowed AI Input? | Final Decision By |
|---------|-------------------|------------------|
| Is safety class sufficient? | NO | Deterministic rule (ASIL table) |
| Is ODD compatible? | NO | Deterministic boundary check |
| Is unit correct? | NO | Deterministic unit comparison |
| Is certificate valid? | NO | Cryptographic verification |
| Is contract expired? | NO | Timestamp comparison |
| Is semantic meaning similar? | YES (stage 1 only) | Human-approved ontology (stage 2) |
| Should contract be ACCEPTED? | NO | All deterministic gates must pass |
| Should contract be REJECTED? | NO | Deterministic gate failure |

---

## 6. Fail-Safe Default Principle

```
AURA SAFETY INVARIANT:
    ∀ capability_contract c:
        AURA_ACCEPT(c) → (
            semantic_match(c) ∧
            context_compatible(c) ∧
            safety_class_compatible(c) ∧
            trust_valid(c) ∧
            provenance_fresh(c)
        )
    
    Equivalently:
        ¬semantic_match(c) → AURA_REJECT(c)
        ¬context_compatible(c) → AURA_REJECT(c)
        ¬safety_class_compatible(c) → AURA_REJECT(c)     ← HARD GATE
        ¬trust_valid(c) → AURA_REJECT(c)
        ¬provenance_fresh(c) → AURA_REJECT(c)
        
    Any uncertainty → REVIEW_REQUIRED (never ACCEPT under uncertainty)
```

---

## 7. Safety Metric: Unsafe Acceptance Rate (UAR)

**Definition:**
```
UAR = |{contracts c : AURA_ACCEPT(c) ∧ ¬truly_compatible(c)}|
      ─────────────────────────────────────────────────────────
      |{contracts c : ¬truly_compatible(c)}|
```

**Target:** UAR = 0 (zero unsafe acceptances)

This target is achievable for the HARD constraints (safety class, ODD, units, trust) because these checks are deterministic. The residual risk is in the semantic matching layer — where a semantically wrong but ASIL-correct capability could be accepted. This residual risk is bounded by:

1. The ontology subsumption check (semantic)
2. The quality attribute checks (accuracy, latency)
3. The human review escape hatch for uncertain cases

**Complementary Metrics:**

```
SAR (Safe Acceptance Rate) = accepted truly compatible / total truly compatible
FRR (False Rejection Rate) = rejected truly compatible / total truly compatible  
RR  (Review Rate) = routed to review / total requests

UAR target: 0
SAR target: > 85%
FRR acceptable: < 15% (false rejections cause human review, not unsafe operation)
RR target: < 10% (minimize human burden)
```

---

## 8. Safety Certification Strategy

**Current AURA-Impact:** Not safety-certified (research prototype).  
**AURA SIP Safety Gate:** Should be certifiable to ASIL-B if implemented in:
- Deterministic language (C, Ada, or certified-safe subset of C++)
- With verified MISRA compliance
- With formal verification of safety gate logic (TLA+ or similar)
- With hardware redundancy for safety-critical deployment

This is a significant engineering effort beyond the current research scope. For the research prototype, the safety gate is implemented in Python for demonstration purposes, with explicit disclaimers about production certification requirements.

---

*Proceed to [12_security_threat_model.md] for adversarial analysis.*
