# 10 — Negotiation Protocol
## AURA Capability Session Protocol: State Machine Design
**Classification:** Protocol Specification  
**Date:** 2026-10-01

---

## 1. Protocol Design Principles

Before defining states, the following principles eliminate unnecessary complexity:

### 1.1 What AURA Is NOT
- NOT a transport protocol (does not define how bytes are sent)
- NOT a real-time control protocol (does not operate in control loops)
- NOT a blockchain protocol (no distributed ledger required)
- NOT a replacement for SOME/IP, DDS, or ROS2 (they remain as transport bindings)

### 1.2 Protocol Timing Model

```
Deployment Phase (Hours/Days before operation):
  DISCOVER → DESCRIBE → NORMALIZE → VALIDATE

Session Establishment (Once per interaction, 100ms–5s budget):
  SEMANTIC MATCH → CONTEXT CHECK → SAFETY CHECK → PROVENANCE CHECK → BIND

Runtime Monitoring (Continuous, low overhead):
  MONITOR → INVALIDATE ON CHANGE

Negotiation (When compatibility is marginal, optional):
  NEGOTIATE → ACCEPT/REJECT/REVIEW
```

**IMPORTANT:** The entire negotiation pipeline is NOT in the real-time control path. It is in the session establishment path — analogous to TLS handshake (happens once, amortized over session duration).

---

## 2. Full Protocol State Machine

```
┌─────────────────────────────────────────────────────────┐
│                   AURA PROTOCOL STATE MACHINE            │
└─────────────────────────────────────────────────────────┘

STATE: IDLE
  No active capability request
  System monitors for incoming DISCOVER requests
  
  TRIGGER: CapabilityDiscoverRequest received
  NEXT STATE: DISCOVER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: DISCOVER
  Consumer broadcasts CapabilityDiscoverRequest containing:
  - Required semantic_type (URI)
  - Required ODD parameters
  - Required quality bounds
  - Required safety class
  - Consumer identity + certificate
  
  Providers respond with:
  - CapabilityDiscoverResponse (list of CapabilityContracts)
  
  Timeouts:
  - Discovery window: configurable (default 500ms, max 5s)
  - If no response: → STATE: NO_PROVIDER_FOUND (terminal)
  
  NEXT STATE: NORMALIZE (on response received)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: NORMALIZE
  For each received CapabilityContract:
  1. Parse semantic_type URI
  2. Map to shared automotive capability ontology
  3. Resolve unit declarations to canonical units (SI)
  4. Resolve coordinate frames to canonical reference (WGS84 or ENU)
  5. Normalize safety class to common comparison scale
  
  Inputs: Raw CapabilityContracts
  Outputs: Normalized CapabilityContracts
  
  Failure: Unresolvable semantic_type → UNKNOWN_CAPABILITY (routed to REVIEW)
  Timeout: 50ms per contract normalization
  
  NEXT STATE: SEMANTIC_MATCH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: SEMANTIC_MATCH
  Run hybrid semantic matching (see 09_semantic_matching_architecture.md):
  
  Stage 1: Embedding similarity filter
    similarity_score = cosine_similarity(request_embedding, contract_embedding)
    if score < LOW_THRESHOLD: → REJECT this contract
    if score > HIGH_THRESHOLD: → advance
    if score in middle: → flag for REVIEW
  
  Stage 2: Ontology subsumption check
    if semantic_type_request ⊑ semantic_type_contract: → advance
    else: → REJECT this contract
  
  Inputs: Normalized contracts
  Outputs: Semantically filtered contract list + confidence scores
  
  Failure: All contracts rejected → NO_MATCH_FOUND (terminal)
  
  NEXT STATE: CONTEXT_CHECK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: CONTEXT_CHECK
  Deterministic ODD compatibility verification:
  
  For each candidate contract:
  1. Check: requester.current_environment ⊆ contract.odd
     - Domain type compatible?
     - Current speed within provider speed range?
     - Current weather within provider weather conditions?
     - Current time_of_day within provider time conditions?
  2. Check: coordinate frame compatible or convertible?
  3. Check: all units fully resolved (no unit ambiguity)?
  
  This check is DETERMINISTIC. No probabilistic components.
  
  Failure: ODD mismatch → CONTEXT_INCOMPATIBLE
           Unresolvable unit → REVIEW_REQUIRED
           Unresolvable coordinate frame → REVIEW_REQUIRED
  
  NEXT STATE: SAFETY_CHECK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: SAFETY_CHECK  ← HARD GATE: CANNOT BE BYPASSED
  Deterministic safety constraint verification:
  
  1. Safety class check:
     provider.safety.classification ≥ requester.required_safety_class
     (using ISO 26262 decomposition table for ASIL comparison)
  
  2. Fail-safe behavior compatibility:
     provider.fail_safe_behavior ∈ requester.acceptable_fail_modes
  
  3. Quality bounds:
     provider.accuracy ≤ requester.required_accuracy
     provider.latency_worst_case ≤ requester.latency_budget
  
  RULE: If safety check fails, contract is REJECTED. 
        No negotiation. No override. No exception.
  
  This rule is non-negotiable.
  
  Output: PASS or REJECT with specific reason code
  
  NEXT STATE: PROVENANCE_CHECK (if PASS)
              REJECT (if FAIL)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: PROVENANCE_CHECK
  Trust and freshness verification:
  
  1. Verify cryptographic signature on CapabilityContract
     (using provider's X.509 certificate)
  
  2. Check certificate against revocation list
     (OCSP or CRL endpoint)
  
  3. Check temporal validity:
     valid_from ≤ now ≤ valid_until
  
  4. Check software version vs. known change impact database:
     if dependency_graph_hash changed since contract_published:
       → INVALIDATED (trigger contract invalidation flow)
  
  Failure modes:
  - Invalid signature → REJECT (potential tampering)
  - Certificate revoked → REJECT (provider compromised)
  - Contract expired → REJECT (stale)
  - Software changed → INVALIDATED (change impact trigger)
  
  NEXT STATE: COMPATIBILITY_SCORE (if PASS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: COMPATIBILITY_SCORE
  Compute final compatibility score:
  
  Score = w1 × semantic_similarity
        + w2 × odd_coverage_ratio
        + w3 × quality_margin_ratio
        + w4 × provenance_freshness_score
  
  Where weights are configurable by consumer policy.
  
  If multiple contracts pass, rank by Score.
  
  NEXT STATE: NEGOTIATE (if multiple candidates and consumer policy allows)
              BIND (if single winner or consumer policy = first-pass)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: NEGOTIATE (OPTIONAL)
  Consumer and provider exchange CapabilityNegotiationProposals:
  
  Allowed negotiation parameters:
  - Latency budget relaxation (consumer relaxes requirement)
  - Accuracy bound relaxation (consumer accepts lower accuracy)
  - ODD subset restriction (provider offers subset of its ODD)
  
  NOT ALLOWED in negotiation:
  - Safety class downgrade (never negotiable)
  - Provenance relaxation (never negotiable)
  - Trust bypass (never negotiable)
  
  Negotiation timeout: 2 seconds
  Maximum rounds: 3
  
  NEXT STATE: BIND (if agreement reached)
              REJECT (if no agreement or timeout)
              REVIEW_REQUIRED (if human approval needed per policy)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: BIND
  Establish capability session:
  
  1. Generate CapabilityBinding:
     - binding_id: UUID
     - consumer_id + provider_id
     - capability_contract_id
     - bound_interface_endpoint
     - session_start_time
     - invalidation_webhook registered
  
  2. Register binding with change-impact engine
     (provider subscribes to notifying consumer on software changes)
  
  3. Activate underlying transport binding
     (SOME/IP service subscribe / DDS topic subscribe / ROS2 subscriber)
  
  NEXT STATE: EXECUTE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: EXECUTE
  Normal operation:
  - Provider delivers capability via bound transport
  - AURA monitors for:
    a. Contract expiry (valid_until approached)
    b. Invalidation signal from change-impact engine
    c. Consumer-side quality violations (latency exceeded)
    d. Provider certificate revocation
  
  NEXT STATE: MONITOR (continuous)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: MONITOR
  Background monitoring loop:
  - Poll change-impact engine for dependency_graph_hash changes
  - Poll PKI revocation status every T_revocation_check
  - Check contract expiry vs. current time
  - Monitor quality metrics from transport layer
  
  NEXT STATE: INVALIDATE (on trigger)
              EXECUTE (continue if no trigger)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATE: INVALIDATE
  Contract invalidation:
  
  Trigger conditions:
  - Provider software change affecting capability (change impact)
  - Contract expiry
  - Certificate revocation
  - Quality violation exceeding threshold
  - Explicit revocation by provider
  
  Actions:
  1. Terminate transport binding
  2. Notify consumer with CapabilityInvalidationNotice
     (includes: binding_id, reason, provider_id, change_summary)
  3. Log to audit log
  4. If consumer policy = AUTOMATIC_RENEGOTIATE → DISCOVER
     If consumer policy = FAIL_SAFE → execute consumer's MRM
     If consumer policy = HUMAN_APPROVAL → REVIEW_REQUIRED
  
  NEXT STATE: IDLE or DISCOVER or REVIEW_REQUIRED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TERMINAL STATES:
  NO_PROVIDER_FOUND  — no provider responded
  NO_MATCH_FOUND     — semantic match failed for all providers
  REJECT             — deterministic gate failed
  REVIEW_REQUIRED    — human approval needed
```

---

## 3. Message Types

| Message | Direction | Key Fields |
|---------|-----------|-----------|
| CapabilityDiscoverRequest | Consumer → Network | required_semantic_type, odd_constraints, quality_bounds, safety_class, consumer_cert |
| CapabilityDiscoverResponse | Provider → Consumer | capability_contracts[] |
| CapabilityBindingRequest | Consumer → Provider | contract_id, consumer_id, consumer_cert |
| CapabilityBindingAck | Provider → Consumer | binding_id, session_params |
| CapabilityInvalidationNotice | Provider/AURA → Consumer | binding_id, reason, change_summary |
| CapabilityNegotiationProposal | Consumer ↔ Provider | relaxed_parameters, round_number |
| AuditLogEntry | Internal | all state transitions |

---

## 4. State Machine Necessity Analysis

| State | Necessary? | Reason |
|-------|-----------|--------|
| IDLE | YES | Starting state |
| DISCOVER | YES | Find providers |
| NORMALIZE | YES | Cross-vendor unit/frame reconciliation |
| SEMANTIC_MATCH | YES | Core problem |
| CONTEXT_CHECK | YES | ODD compatibility |
| SAFETY_CHECK | YES | Non-negotiable safety gate |
| PROVENANCE_CHECK | YES | Trust verification |
| COMPATIBILITY_SCORE | OPTIONAL | Only needed for multi-provider selection |
| NEGOTIATE | OPTIONAL | Only for quality relaxation cases |
| BIND | YES | Transport activation |
| EXECUTE | YES | Operating state |
| MONITOR | YES | Stale detection |
| INVALIDATE | YES | Change impact response |
| REVIEW_REQUIRED | YES | Escape hatch for human |

**States that are NOT necessary (eliminated):**
- A separate "ADVERTISE" state — providers respond to DISCOVER requests on-demand
- A "REGISTER" state — capability contracts are published independently, not part of protocol flow

---

## 5. Timeout and Failure Behavior

| Phase | Timeout | Failure Action |
|-------|---------|---------------|
| Discovery | 500ms (default, configurable) | Try next provider or FAIL_SAFE |
| Normalization per contract | 50ms | Skip contract, log warning |
| Semantic matching | 100ms | Conservative → REVIEW_REQUIRED |
| Safety check | 5ms | Must be deterministic, fast |
| Provenance check | 200ms (includes OCSP) | On OCSP timeout → REJECT (safe default) |
| Negotiation round | 2s | REJECT after max 3 rounds |
| Binding establishment | 1s | REJECT |

**Failure Policy:**
> **Default to safe failure.** Any timeout or error in the protocol pipeline defaults to REJECT or REVIEW_REQUIRED, never to ACCEPT. This is the fundamental safety design principle.

---

*Proceed to [11_safety_architecture.md] for safety model.*
