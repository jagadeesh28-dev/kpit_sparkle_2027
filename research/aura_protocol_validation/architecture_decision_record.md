# Architecture Decision Record
## AURA Semantic Interoperability Protocol — Formal ADR
**Classification:** Architecture Decision Record (ADR-001)  
**Date:** 2026-10-01  
**Status:** FINAL  
**Deciders:** Research team — hostile review methodology

---

## The 23 Architecture Decision Questions

### Q1. Does the problem genuinely exist?

**YES.** Multi-vendor automotive software integration requires manual months-long ICD negotiation for every new supplier interface pair. ISO 23374 documents 3–6 months per deployment site. SAE studies confirm 4–8 weeks of manual parameter alignment per V2X configuration. Broy (2006) documents 30–50% of complex automotive system cost in integration engineering. The problem is economically documented, not theoretical.

---

### Q2. Why are existing standards insufficient?

| Standard | Why Insufficient |
|---------|-----------------|
| AUTOSAR Adaptive + SOME/IP | ServiceID is opaque numeric; no semantic meaning, ODD, safety class, or change-impact |
| DDS | TopicName is free string; same string can mean different things from different vendors |
| ROS2 | Inherits DDS limitations; freeform names have no semantic constraints |
| OPC UA | Closest existing approach; lacks automotive ODD, ASIL class, change-impact tracking |
| W3C WoT | No safety class model, no ODD, no change-impact; IoT-oriented, not safety-critical |
| ISO 23150 | Static sensor interface standard, not dynamic capability negotiation |
| COVESA VSS | Signal naming, not capability semantics; no safety, no ODD, no negotiation |
| V2X Standards | Fixed BSM/CAM message formats; no arbitrary capability description |

**No standard addresses the combination: semantic + ODD + safety + provenance + change-impact.**

---

### Q3. What exact gap remains?

**Six confirmed gaps:**
- **GAP A:** Semantic capability interoperability — same concept expressed with different names cannot be automatically matched cross-vendor
- **GAP B:** ODD-aware capability compatibility — no machine-readable cross-vendor ODD compatibility checking
- **GAP C:** Safety-bounded runtime negotiation — safety contracts verified at design-time only, not at runtime binding
- **GAP D:** Provenance-backed capability trust — no automotive capability provenance standard
- **GAP E:** Change-impact contract invalidation — NO PRIOR ART FOUND (strongest gap)
- **GAP F:** Autonomous cross-vendor composition — requires A–E as prerequisites

---

### Q4. Why is AURA needed?

1. It connects existing AURA-Impact dependency graph engine (proven technology) to cross-system capability binding management (novel application)
2. It provides the first mechanism for Gap E — change-impact-driven automatic contract invalidation
3. It implements safety-bounded semantic matching that no existing middleware provides
4. It reduces the 3–6 month manual integration effort per deployment to a structured, automatable process

---

### Q5. What is the minimum architecture?

Six stages in serial pipeline:
1. Semantic Embedding Filter (dense vector fast-reject)
2. Ontology Subsumption Check (conceptual correctness)
3. Symbolic Constraint Verification (units, frames, ODD, quality)
4. Safety Contract Gate (HARD GATE — ASIL comparison, fail-safe mode)
5. Provenance + Trust Verification (cryptographic + temporal)
6. Change Impact Check (dependency graph hash comparison)

Plus monitoring loop for active bindings (continuous).

---

### Q6. What is NOT part of AURA?

- Transport protocols (Ethernet, CAN-FD, V2X radio)
- Message serialization (DDS IDL, Protobuf, ARXML types)
- Security at transport layer (TLS, DTLS, IEEE 1609.2)
- Inner-loop real-time vehicle control
- Perception algorithm design
- Planning algorithm design
- Any function that requires execution latency < 10ms
- Closed proprietary autonomous stacks (Tesla FSD, Waymo internal pipeline)

---

### Q7. What existing standards does AURA reuse?

| Standard | AURA Usage |
|---------|-----------|
| X.509 PKI (RFC 5280) | Provider certificate chain |
| Ed25519 signatures | Contract signing |
| OCSP (RFC 6960) | Certificate revocation |
| OWL-DL | Automotive capability ontology formalism |
| JSON-LD | Capability manifest serialization |
| ISO 26262 ASIL table | Safety class comparison logic |
| COVESA VSS | Seed vocabulary for capability ontology |
| AURA-Impact engine | Dependency graph for change-impact |

AURA does NOT define new transport, serialization, or authentication protocols.

---

### Q8. Where does AURA sit in the stack?

```
[Application / Mission Layer]
────────────────────────────────
[AURA Semantic Interoperability Layer]  ← HERE
  - Capability manifest management
  - Semantic matching
  - Safety contract verification
  - Change-impact monitoring
────────────────────────────────
[Existing Middleware]
  AUTOSAR Adaptive / DDS / ROS2 / OPC UA / SOME/IP
────────────────────────────────
[Transport]
  Ethernet / CAN-FD / V2X / IP
────────────────────────────────
[Physical]
  IEEE 802.3 / CAN / DSRC / 5G
```

---

### Q9. What is the protocol/message model?

**6 message types:**
1. `CapabilityDiscoverRequest` — consumer broadcasts requirement
2. `CapabilityDiscoverResponse` — provider returns capability contract list
3. `CapabilityBindingRequest` — consumer requests binding to specific contract
4. `CapabilityBindingAck` — provider confirms binding, returns session params
5. `CapabilityInvalidationNotice` — provider or AURA notifies consumer of contract invalidation
6. `CapabilityNegotiationProposal` — optional bilateral quality relaxation

**Capability Contract** (JSON format):
35 fields across: semantic identity, interface identity, operational context, quality, safety, trust, provenance, change-impact.

---

### Q10. How is semantic compatibility computed?

Two-stage hybrid:
1. Dense embedding cosine similarity (fast filter, probabilistic)
2. OWL-DL ontology subsumption check (definitive, deterministic)

Stage 1 output is NEVER the final decision. Stage 2 makes the semantic compatibility determination.

---

### Q11. How is context verified?

Deterministic set membership:
- `requester.current_domain ∈ provider.odd.domains`
- `provider.odd.speed_min ≤ requester.speed ≤ provider.odd.speed_max`
- `requester.weather ∈ provider.odd.weather_conditions`
- `requester.time_of_day ∈ provider.odd.time_of_day`

All checks are Boolean. No probabilistic components. Any FAIL → reject.

---

### Q12. How is safety verified?

Deterministic ASIL comparison:
- `ASIL_LEVEL[provider.asil] ≥ ASIL_LEVEL[requester.required_asil]`
- ASIL_LEVEL = {QM:0, A:1, B:2, C:3, D:4}
- Cross-standard (ISO26262 ↔ IEC61508): only with pre-approved mapping; otherwise REVIEW_REQUIRED
- Fail-safe behavior: `provider.fail_safe ∈ requester.acceptable_fail_modes`

**Safety gate is the ONLY non-bypassable component in the entire architecture.**

---

### Q13. How is trust established?

1. Provider certificate signed by trusted automotive CA (analogous to IEEE 1609.2 SCMS)
2. Capability contract signed with provider's private key (Ed25519)
3. Signature verified by consumer using provider's certificate
4. Certificate revocation checked via OCSP (or CRL for offline)
5. Hardware Security Modules (HSMs) hold private keys (production requirement)

---

### Q14. How are changes propagated?

1. AURA change-impact engine monitors provider's dependency graph hash continuously
2. On detection of hash change: analyze impact on published capabilities
3. For each affected capability: generate `CapabilityInvalidationNotice`
4. Send notice to all registered consumers via webhook
5. Consumer must: renegotiate, switch provider, or activate fail-safe
6. Consumer CANNOT continue operating on stale contract

---

### Q15. How is stale capability detected?

Three independent mechanisms:
- **Temporal expiry:** `valid_until < now` → contract expired
- **Software change:** `current_dep_graph_hash ≠ stored_dep_graph_hash` → invalidate
- **Certificate revocation:** OCSP check on provider certificate → revoke on REVOKED status

All three are checked before binding and continuously during monitoring.

---

### Q16. How is malicious capability handled?

Defense-in-depth:
1. Cryptographic signature fails → REJECT at Stage 5 (certificate not trusted)
2. Certificate revoked → REJECT at Stage 5
3. Safety class declared high but interface has unit mismatch → REJECT at Stage 3
4. Semantic embedding crafted to be similar → caught by ontology subsumption (Stage 2)
5. Replay of expired contract → REJECT at Stage 5 (temporal validity check)

No single attack vector can pass all stages simultaneously without a compromised CA.

---

### Q17. How is interoperability measured?

Primary metrics:
- **UAR** (Unsafe Acceptance Rate) = unsafe accepted / total unsafe — TARGET: 0
- **SAR** (Safe Acceptance Rate) = correctly accepted / total compatible — TARGET: >85%
- **FRR** (False Rejection Rate) = incorrectly rejected / total compatible — TARGET: <15%
- **P99 Latency** (session establishment) — TARGET: <500ms
- **Change-Impact Detection Latency** — TARGET: <500ms

---

### Q18. What benchmark proves the hypothesis?

The 14-class benchmark (1,850 instances, 7 baselines) with the key constraint:
- UAR = 0 for Class I (safety mismatch) and Class K (malicious) instances is a BINARY PASS/FAIL
- If UAR > 0 on any run: hypothesis is falsified for safety claims

---

### Q19. What would falsify the hypothesis?

```
FALSIFICATION CONDITIONS:
(a) UAR > 0 for Class I or K: safety claim falsified
(b) Semantic recall (Class B) < 60%: semantic matching fails fundamentally
(c) AUTOSAR R24/25 publishes equivalent capability manifest standard: novelty eliminated
(d) Protocol overhead > session duration for target use cases: efficiency claim fails
(e) Expert panel cannot establish ground truth consensus for Class B (synonym) cases: benchmark validity fails
```

---

### Q20. What is genuinely novel?

**NOVEL (zero prior art):**
- Change-impact-driven capability contract invalidation (Gap E)
- ODD-aware cross-vendor capability compatibility reasoning (Gap B)

**NOVEL IN AUTOMOTIVE (no prior automotive standard/paper):**
- Safety-bounded semantic capability negotiation with ASIL-class enforcement at runtime
- Combined: semantic + ODD + safety + provenance + change-impact in single automotive framework

**EXTENSION (existing techniques in new domain):**
- Hybrid semantic-symbolic matching architecture
- Provenance-aware capability trust (extending PKI concepts to capability contracts)

---

### Q21. What is merely integration?

- Dense vector embeddings for similarity: KNOWN (SentenceTransformers)
- OWL ontology for concept hierarchy: KNOWN
- X.509 PKI: KNOWN
- State machine protocol: KNOWN
- Unit conversion: KNOWN

These are implementation technologies, not research contributions.

---

### Q22. What is the MVP?

AURA Semantic Gateway — Python prototype:
- 10 components (parser, normalizer, context engine, safety gate, provenance verifier, change-impact engine, compatibility scorer, negotiation manager, middleware adapter, audit log)
- Three-system synthetic testbed (Systems A/B/C)
- CLI interface
- Benchmark runner
- Integration with existing AURA-Impact dependency graph engine

Estimated implementation: 6–8 person-weeks with existing AURA-Impact infrastructure.

---

### Q23. What is the 3-year research roadmap?

| Phase | Timeline | Key Milestone |
|-------|---------|--------------|
| Phase 0 | 0–3 months | MVP + benchmark dataset + KPIT Sparkle demo |
| Phase 1 | 3–9 months | Empirical validation + Paper 2 submission |
| Phase 2 | 9–18 months | Domain expansion + AUTOSAR integration + Paper 3 |
| Phase 3 | 18–36 months | Standardization contribution + KPIT pilot |

**The critical path:** Safety gate empirical validation (UAR = 0) must come before any other publication claim.

---

*End of Architecture Decision Record*
