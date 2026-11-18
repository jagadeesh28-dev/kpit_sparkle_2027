# 13 — Formal Compatibility Model
## Mathematical Formalization of Cross-System Capability Compatibility
**Classification:** Formal Methods Specification  
**Date:** 2026-10-01

---

## 1. Formal Definitions

### 1.1 Capability Contract

Let a **Capability Contract** C be a tuple:

```
C = ⟨id, stype, provider, iface, odd, qual, safety, trust, prov, ci⟩

Where:
  id      ∈ UUID
  stype   ∈ CapabilityOntology (OWL class URI)
  provider ∈ ProviderIdentity
  iface   = ⟨binding_type, endpoint, message_type, units, coord_frame⟩
  odd     = ⟨domains, speed_range, weather_conds, time_of_day⟩
  qual    = ⟨accuracy, latency_typical, latency_wcet, availability⟩
  safety  = ⟨asil_class, safety_standard, fail_safe_behavior⟩
  trust   = ⟨certificate, signature, revocation_uri⟩
  prov    = ⟨sw_version, sw_hash, valid_from, valid_until⟩
  ci      = ⟨dep_graph_hash, last_commit, invalidation_condition⟩
```

### 1.2 Capability Request

A **Capability Request** R is a tuple:

```
R = ⟨r_stype, r_odd, r_qual, r_safety, r_trust_scope, r_context⟩

Where:
  r_stype        ∈ CapabilityOntology
  r_odd          = current operating environment
  r_qual         = minimum required quality bounds
  r_safety       = minimum required safety class
  r_trust_scope  ∈ {PUBLIC, FLEET, BILATERAL, PRIVATE}
  r_context      = current runtime context
```

---

## 2. Compatibility Predicate

**Definition: Compatible(R, C)**

```
Compatible(R, C) ≡ S(R,C) ∧ I(R,C) ∧ O(R,C) ∧ Q(R,C) ∧ F(R,C) ∧ T(R,C) ∧ P(R,C)

Where:
  S(R,C) = Semantic Compatibility
  I(R,C) = Interface Compatibility
  O(R,C) = Operational Context Compatibility
  Q(R,C) = Quality-of-Service Compatibility
  F(R,C) = Safety (Functional) Compatibility
  T(R,C) = Trust Compatibility
  P(R,C) = Provenance Validity
```

This is a **conjunctive** predicate — ALL sub-predicates must be true. Any false sub-predicate makes Compatible(R,C) = false.

This is NOT a weighted average. Not a probabilistic threshold. It is a strict logical conjunction.

---

## 3. Sub-Predicate Formal Definitions

### 3.1 Semantic Compatibility S(R, C)

```
S(R, C) ≡ r_stype ⊑_Ω c.stype

Where:
  ⊑_Ω = subsumption in automotive capability ontology Ω
  r_stype ⊑_Ω c.stype means "requested type is a subclass of provided type"

Example:
  r_stype = "PedestrianDetection"
  c.stype = "ObjectDetection"
  PedestrianDetection ⊑_Ω ObjectDetection → S = TRUE

  r_stype = "PedestrianDetection"
  c.stype = "LaneDetection"
  PedestrianDetection ⊄_Ω LaneDetection → S = FALSE

Note: The subsumption direction is important.
  The provider must offer a type that is AT LEAST as general as requested,
  or exactly the requested type.
  A provider of "VehicleDetection" cannot satisfy "PedestrianDetection" 
  unless PedestrianDetection ⊑ VehicleDetection in the ontology.
```

**Embedding assist (not final decision):**

```
SemScore(R, C) = cosine_similarity(embed(r_stype), embed(c.stype))

If SemScore < θ_low:  S is likely FALSE → fast-path REJECT (preliminary)
If SemScore > θ_high: advance to ontology subsumption check
If θ_low ≤ SemScore ≤ θ_high: route to REVIEW_REQUIRED (uncertain)

Final S(R,C) is determined by ontology subsumption, not by SemScore alone.
```

---

### 3.2 Interface Compatibility I(R, C)

```
I(R, C) ≡ units_compatible(r_iface, c.iface) 
         ∧ frame_compatible(r_iface, c.iface)
         ∧ type_compatible(r_iface.message_type, c.iface.message_type)

units_compatible(r, c) ≡ ∀ parameter p: 
  SI_normalize(r.units[p]) = SI_normalize(c.iface.units[p])
  OR exists_unit_converter(r.units[p], c.iface.units[p])

frame_compatible(r, c) ≡ 
  r.coord_frame = c.iface.coord_frame
  OR exists_frame_transform(r.coord_frame, c.iface.coord_frame)

type_compatible(r_type, c_type) ≡ 
  r_type = c_type (exact) 
  OR r_type ⊑ c_type (structural subtyping)
```

**Strict rules:**
- Unit mismatch with no available converter → I = FALSE (REJECT)
- Coordinate frame mismatch with no computable transform → I = FALSE (REJECT)
- If transform exists but introduces error > r_qual.accuracy → I = FALSE (REJECT)

---

### 3.3 Operational Context Compatibility O(R, C)

```
O(R, C) ≡ r_context ⊆_env c.odd

r_context ⊆_env c.odd ≡ 
  r_context.domain ∈ c.odd.domains
  ∧ c.odd.speed_range.min ≤ r_context.speed ≤ c.odd.speed_range.max
  ∧ r_context.weather ∈ c.odd.weather_conditions
  ∧ r_context.time_of_day ∈ c.odd.time_of_day

All conditions are deterministic Boolean checks.
```

---

### 3.4 Quality-of-Service Compatibility Q(R, C)

```
Q(R, C) ≡ c.qual.accuracy ≤ r_qual.required_accuracy
         ∧ c.qual.latency_wcet ≤ r_qual.latency_budget

Note: smaller accuracy value = better (e.g., 0.25m < 0.5m means more precise)
Note: WCET (worst-case execution time) must satisfy budget, not just typical

Additional quality predicates (optional, consumer-configurable):
  q_avail: c.qual.availability ≥ r_qual.min_availability
  q_conf:  c.qual.confidence ≥ r_qual.min_confidence
```

---

### 3.5 Safety (Functional) Compatibility F(R, C)

**This is the HARD GATE. No exceptions.**

```
F(R, C) ≡ asil_compare(c.safety.asil_class, r_safety.required_asil)
         ∧ failsafe_compatible(c.safety.fail_safe_behavior, r_safety.acceptable_fail_modes)
         ∧ standard_compatible(c.safety.safety_standard, r_safety.required_standard)

asil_compare(c_asil, r_asil) ≡ ASIL_LEVEL[c_asil] ≥ ASIL_LEVEL[r_asil]

ASIL_LEVEL = {QM: 0, A: 1, B: 2, C: 3, D: 4}

failsafe_compatible(c_behavior, r_acceptable) ≡ c_behavior ∈ r_acceptable

standard_compatible(c_std, r_std) ≡ c_std = r_std 
  OR (c_std, r_std) ∈ APPROVED_CROSS_STANDARD_MAPPINGS
```

**Cross-standard mapping:**
```
APPROVED_CROSS_STANDARD_MAPPINGS = {
  (ISO_26262_ASIL_D, IEC_61508_SIL_3): when deployment-verified,
  (ISO_26262_ASIL_B, IEC_61508_SIL_2): when deployment-verified,
  ... (requires explicit human-approved table per deployment context)
}
```

---

### 3.6 Trust Compatibility T(R, C)

```
T(R, C) ≡ sig_valid(c) ∧ cert_valid(c.trust.certificate, now) 
         ∧ ¬revoked(c.trust.certificate, now)
         ∧ c.trust.authorization_scope ≥ r_trust_scope

sig_valid(c) ≡ verify_signature(c.trust.signature, c, c.trust.certificate)
cert_valid(cert, t) ≡ cert.valid_from ≤ t ≤ cert.valid_until
revoked(cert, t) ≡ OCSP_check(cert, t) = REVOKED
```

---

### 3.7 Provenance Validity P(R, C)

```
P(R, C) ≡ c.prov.valid_from ≤ now ≤ c.prov.valid_until
         ∧ ¬changed(c, now)

changed(c, now) ≡ 
  current_dep_graph_hash(c.provider) ≠ c.ci.dep_graph_hash
  ∨ current_sw_hash(c.provider) ≠ c.prov.sw_hash

Where:
  current_dep_graph_hash(p): queries AURA change-impact engine for provider p
  current_sw_hash(p):        queries provider's software attestation endpoint
```

---

## 4. Complete Compatibility Theorem

```
THEOREM: AURA_ACCEPT(R, C) ↔ Compatible(R, C)

PROOF OBLIGATION:
  (a) AURA must not accept (R, C) when ¬Compatible(R, C)  [Safety requirement: UAR = 0]
  (b) AURA should accept (R, C) when Compatible(R, C)      [Performance requirement: SAR > 85%]
  
  (a) is enforced by the hard gates in Stages 2, 3, 4 of the matching pipeline.
  (b) is an empirical property to be measured in experiments.
```

---

## 5. Change-Impact Extension

```
DEFINITION: ContractInvalidated(C, t)

ContractInvalidated(C, t) ≡ 
  ¬P(R, C)  [provenance no longer valid]
  ∨ c.prov.valid_until < t  [contract expired]
  ∨ revoked(c.trust.certificate, t)  [certificate revoked]
  ∨ changed(c, t)  [software changed]

INVARIANT:
  ∀ C in active_bindings, t > binding_time:
    ContractInvalidated(C, t) → CapabilityInvalidationNotice(C) sent to consumer
```

This invariant is the formal expression of **Gap E** — the core AURA contribution with no prior art.

---

## 6. Complexity Analysis of Compatibility Check

For a single (R, C) pair:

| Sub-predicate | Complexity | Notes |
|--------------|-----------|-------|
| S: Semantic | O(E) embedding + O(log N) ontology | E = embedding dimension, N = ontology size |
| I: Interface | O(P) where P = parameter count | Typically P < 20 |
| O: Context | O(W + D) where W = weather conditions, D = domains | O(1) in practice |
| Q: Quality | O(1) | Direct comparison |
| F: Safety | O(1) | Table lookup |
| T: Trust | O(1) signature + O(1) OCSP cache | OCSP is network call, cached |
| P: Provenance | O(1) + O(dep_graph) | Dep graph query amortized |

**Total complexity per pair:** O(E + log N) dominated by semantic stage.

For N providers, complexity is O(N × (E + log Ω)) where Ω = ontology size.

For realistic N < 100 and Ω < 10,000 terms, this is well within 200ms latency budget.

---

*Proceed to [14_complexity_analysis.md] for N×N integration complexity model.*
