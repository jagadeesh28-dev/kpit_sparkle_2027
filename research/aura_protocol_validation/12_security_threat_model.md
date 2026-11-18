# 12 — Security Threat Model
## AURA Protocol Adversarial Analysis
**Classification:** Security Architecture — Threat and Attack Analysis  
**Date:** 2026-10-01

---

## 1. Attacker Model

### 1.1 Attacker Types

| Attacker | Capabilities | Goal |
|---------|-------------|------|
| Malicious Provider | Can advertise capabilities, sign with valid cert | Get consumer to use unsafe capability |
| Compromised Provider | Legitimate cert, modified software | Undetected capability degradation |
| Network Attacker (MitM) | Can intercept/modify messages | Forge or corrupt capability contracts |
| Replay Attacker | Has captured valid capability contracts | Re-use stale contracts |
| Semantic Poisoner | Can inject into shared ontology | Cause semantic matching failures |
| Insider Attacker | Can modify provider's software | Silent capability degradation |
| OOD Capability Attacker | Constructs artificially similar capability | Pass semantic filter with wrong capability |

---

## 2. Attack Taxonomy and Mitigations

### Attack 01: Fake Capability Advertisement

**Description:** Attacker advertises a capability (e.g., ASIL-D pedestrian detection) that it cannot actually provide.

**Impact:** Consumer binds to incapable provider; safety function fails at runtime.

**Detection:**
- Cryptographic signature on capability contract: provider must sign with registered certificate
- Certificate authority (CA) verifies provider identity and minimum qualification
- Quality monitoring during EXECUTE state: if actual quality ≠ declared quality → INVALIDATE

**Mitigation:**
- Certificates issued only to verified providers by trusted CA
- Runtime quality monitoring with automatic invalidation on sustained violation
- Audit log of all bindings with quality evidence

**Residual Risk:** A legitimate but poorly-calibrated provider who genuinely believes their capability meets the declared spec. Mitigation: third-party capability certification (analogous to ISO 26262 supplier assessment).

---

### Attack 02: Stale Capability (Replay)

**Description:** Attacker replays a previously valid capability contract for a software version that is no longer current.

**Impact:** Consumer relies on capabilities of an older, potentially buggy or degraded software version.

**Detection:**
- `provenance.valid_until` field: contracts have explicit expiry
- `provenance.software_hash` verification: AURA checks against known current hash
- Change-impact engine: detects when dependency graph hash changes

**Mitigation:**
- Short-lived contracts (24h–7d default validity window)
- Change-impact invalidation triggered on any provider software change
- Consumer policy: re-validate all contracts after OTA update

**Residual Risk:** Attacker who can sign a new contract with a future `valid_until` date using a compromised certificate. Mitigation: certificate revocation.

---

### Attack 03: Semantic Poisoning

**Description:** Attacker gains write access to shared automotive capability ontology and introduces incorrect semantic equivalences (e.g., maps "steering_control" ⊑ "speed_control").

**Impact:** Semantic matching produces systematically wrong results; safety-critical mismatches accepted as equivalent.

**Detection:**
- Ontology is cryptographically signed by governing body
- Ontology version is pinned in AURA deployment configuration
- Semantic match results are audited by monitoring tools

**Mitigation:**
- Ontology distributed as signed, immutable artifact (like software package)
- Ontology updates require governance process (not runtime-mutable)
- Deterministic safety gate provides backstop: even a poisoned semantic match is rejected if safety class or ODD is incompatible

**Residual Risk:** An ontology attack that makes two semantically different but safety-equivalent capabilities appear equivalent. Extremely difficult to construct without insider access to ontology governance.

---

### Attack 04: Unit Mismatch (Adversarial)

**Description:** Provider declares accuracy in centimeters but the capability delivers results in meters (10x worse), with the unit field adversarially set to "cm" while outputs are in "m".

**Impact:** Consumer assumes sub-centimeter accuracy; makes planning decisions based on incorrect precision.

**Detection:**
- AURA performs runtime quality monitoring: statistical analysis of received values vs. declared unit range
- If declared spatial unit is "cm" but actual values cluster around 100× expected magnitude → ANOMALY_DETECTED → INVALIDATE

**Mitigation:**
- Normalization layer verifies unit declarations are internally consistent (e.g., accuracy in cm cannot exceed sensor wavelength limits)
- Sanity bounds: declared accuracy must be physically plausible given sensor type

**Residual Risk:** Subtle unit errors (e.g., radians vs. degrees for small angles) that pass plausibility checks. Mitigation: comprehensive unit normalization to SI before all comparisons.

---

### Attack 05: False Confidence Claim

**Description:** Provider declares confidence = 0.99 (high) for a capability that actually produces confidence = 0.60 on average.

**Impact:** Consumer fusion system over-weights provider's output; degrades overall system reliability.

**Detection:**
- Runtime monitoring of declared vs. observed confidence distributions
- Statistical hypothesis test: if observed ≪ declared → QUALITY_VIOLATION → INVALIDATE

**Mitigation:**
- Confidence field is declared as `typical` and `minimum_acceptable`
- AURA monitors minimum_acceptable; sustained violations trigger invalidation

**Residual Risk:** Adversary who can dynamically adjust output confidence to pass monitoring while degrading at critical moments. Defense: ensemble monitoring with multiple quality metrics.

---

### Attack 06: Capability Spoofing (Identity)

**Description:** Attacker impersonates a trusted provider (e.g., Bosch sensor node) by using a forged or stolen certificate.

**Impact:** Consumer trusts an untrusted provider.

**Detection:**
- Cryptographic signature verification using provider's X.509 certificate
- Certificate authority validates provider identity

**Mitigation:**
- Use Hardware Security Modules (HSMs) for certificate storage (private key cannot be extracted)
- Short-lived certificates (max 90 days) minimize stolen certificate exposure window
- OCSP stapling for real-time revocation checks

**Residual Risk:** CA compromise. Mitigation: Certificate Transparency logging; cross-signing.

---

### Attack 07: Semantic Collision

**Description:** Two capabilities with completely different functions happen to have very similar semantic embeddings (adversarially constructed).

**Example:** Attacker crafts "VehicleSpeedMonitor" to have high embedding similarity to "VehicleSpeedControl." Consumer accepts monitoring capability believing it's control.

**Impact:** Consumer attempts to use a monitoring capability as a control capability.

**Detection:**
- Ontology subsumption check (Stage 2): "VehicleSpeedMonitor" is NOT a subclass of "VehicleSpeedControl"
- Interface binding check: monitoring outputs (read-only) vs. control inputs (write) are structurally different

**Mitigation:**
- Semantic matching alone does NOT determine compatibility
- Ontology subsumption (deterministic) verifies conceptual hierarchy
- Interface type compatibility verifies structural compatibility
- Two independent gates must both pass

**Residual Risk:** An ontology that is insufficiently precise to distinguish monitoring from control. Mitigation: ontology quality assurance in governance process.

---

### Attack 08: Context Manipulation (ODD Claim)

**Description:** Provider declares ODD = {URBAN, HIGHWAY, FOG, NIGHT, SNOW} (all conditions) when it only reliably works in {URBAN, CLEAR, DAY}.

**Impact:** Consumer uses capability in fog or night conditions where it performs unreliably.

**Detection:**
- Certificate authority requires third-party validation of declared ODD (analogous to sensor qualification testing)
- Runtime monitoring: if consumer operates in declared ODD subset where quality degrades → ANOMALY

**Mitigation:**
- ODD claims must be backed by validation evidence (linked via `provenance.validation_evidence_uri`)
- Third-party ODD certification process (analogous to ISO 21448 validation)

**Residual Risk:** Inadequate third-party testing. No perfect mitigation without comprehensive operational testing.

---

### Attack 09: Provenance Forgery

**Description:** Attacker forges `provenance.software_hash` to claim a known-good version when the actual binary is malicious.

**Impact:** AURA's change-impact check passes because hash matches declared value; actual binary is different.

**Detection:**
- Change-impact engine maintains independent record of provider's software hash (computed from binary, not from declaration)
- Hash is independently computed, not trusted from the contract itself

**Mitigation:**
- AURA never trusts the `software_hash` field from the contract as the source of truth
- AURA independently fetches and computes the hash from the provider's build artifacts (if accessible)
- Alternatively: third-party software attestation (TPM-based remote attestation)

**Residual Risk:** If AURA cannot independently verify the hash (e.g., proprietary binary), it falls back to checking the dependency graph hash which is computed from observable behavior.

---

### Attack 10: Downgrade Attack

**Description:** Attacker exploits NEGOTIATE state to convince consumer to accept lower safety class capability by repeatedly proposing marginal compromises.

**Impact:** Consumer ends up with ASIL-A capability for a function that needs ASIL-B.

**Detection:**
- Safety Gate is NON-NEGOTIABLE (by design)
- Negotiation only allows: latency relaxation, accuracy relaxation, ODD subset
- Safety class is explicitly excluded from negotiation parameters

**Mitigation:**
- Protocol enforces that NEGOTIATE state cannot modify safety-related fields
- Consumer's minimum safety requirement is a hard constraint, not an initial preference

**Residual Risk:** Zero for safety class downgrade (structural prevention). Residual for accuracy/latency: consumer must carefully set their minimum acceptable bounds.

---

## 3. Summary Threat Matrix

| Attack | Severity | Detectability | Mitigation Quality | Residual Risk |
|--------|---------|--------------|-------------------|--------------|
| Fake Capability | CRITICAL | MEDIUM | HIGH | LOW |
| Stale Capability | HIGH | HIGH | HIGH | LOW |
| Semantic Poisoning | HIGH | HIGH (offline) | HIGH | VERY LOW |
| Unit Mismatch | HIGH | MEDIUM | HIGH | LOW |
| False Confidence | MEDIUM | HIGH | MEDIUM | MEDIUM |
| Capability Spoofing | CRITICAL | HIGH | HIGH (HSM) | LOW |
| Semantic Collision | HIGH | HIGH (ontology) | HIGH | LOW |
| Context Manipulation | HIGH | MEDIUM | MEDIUM | MEDIUM |
| Provenance Forgery | HIGH | MEDIUM | MEDIUM | MEDIUM |
| Downgrade Attack | CRITICAL | VERY HIGH | VERY HIGH | VERY LOW |

---

## 4. Security Architecture Principles

1. **Fail Closed:** Any security check failure → REJECT. Never ACCEPT on error.
2. **Cryptographic Trust Root:** All provider identities must be cryptographically verifiable.
3. **Freshness:** All contracts must have explicit expiry; stale contracts are treated as invalid.
4. **Defense in Depth:** No single mechanism is the only protection for any critical attack.
5. **Hardware Root of Trust:** HSMs for certificate storage; TPM for remote attestation where available.
6. **Separation of AI and Security:** The semantic matching AI component CANNOT override security checks. Security checks are implemented in the deterministic layer only.

---

*Proceed to [13_formal_compatibility_model.md] for mathematical formalization.*
