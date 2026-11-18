# 06 — Gap Analysis
## Definitive Research Gap: Where Exactly The Problem Begins
**Classification:** Research Gap Formalization  
**Date:** 2026-10-01  
**Method:** Eliminating each interoperability layer from the bottom up; finding the precise stratum where standards fail

---

## 1. The Elimination Methodology

To locate the precise gap, systematically eliminate layers that ARE already solved:

```
TRANSPORT INTEROPERABILITY
        ↓ 
        STATUS: SOLVED
        EVIDENCE: IEEE 802.3, CAN-FD, C-V2X PC5, DSRC 5.9GHz
        STANDARD: ISO 11898 (CAN), IEEE 802.3, SAE J2945/1
        VERDICT: Do NOT propose a new transport. This is NOT the gap.
        ─────────────────────────────────────────────────────────────

PROTOCOL/ENCODING INTEROPERABILITY  
        ↓
        STATUS: SOLVED
        EVIDENCE: DDS, SOME/IP, Protobuf, MQTT, OPC UA
        STANDARD: OMG DDS v1.4, AUTOSAR SOME/IP, RFC 1459
        VERDICT: Do NOT propose a new encoding. This is NOT the gap.
        ─────────────────────────────────────────────────────────────

SERVICE DISCOVERY (SYNTACTIC)
        ↓
        STATUS: MOSTLY SOLVED
        EVIDENCE: SOME/IP-SD, DDS-RTPS, ROS2 discovery, mDNS
        STANDARD: AUTOSAR SOME/IP-SD, OMG RTPS 2.5
        LIMITATION: Discovery is by opaque ID/name; no semantic content
        VERDICT: Syntactic discovery is solved; semantic discovery is NOT.
        ─────────────────────────────────────────────────────────────

DATA MODEL / SIGNAL INTEROPERABILITY
        ↓
        STATUS: PARTIALLY SOLVED
        EVIDENCE: ISO 23150, COVESA VSS, ASAM OpenDRIVE, DDS IDL
        STANDARD: ISO 23150:2023, COVESA VSS v3.0
        LIMITATION: Signal naming is standardized; capability MEANING is not
        VERDICT: Signal names are partially standardized; capability semantics are NOT.
        ─────────────────────────────────────────────────────────────

SERVICE-LEVEL INTEROPERABILITY (SOA)
        ↓
        STATUS: PARTIALLY SOLVED
        EVIDENCE: AUTOSAR Adaptive SOA, SOME/IP, DDS
        LIMITATION: Service interfaces are defined but semantic equivalence between 
                    different naming conventions is not discoverable
        VERDICT: Interface type-matching is solved; semantic equivalence is NOT.
        ─────────────────────────────────────────────────────────────

──────────────────────────────────────────────────────────────────────────
GAP BEGINS HERE:
──────────────────────────────────────────────────────────────────────────

SEMANTIC CAPABILITY INTEROPERABILITY          ← GAP A (Confirmed)
        ↓
        STATUS: RESEARCH PROTOTYPE STAGE ONLY
        EVIDENCE: No published, deployed automotive standard
        CLOSEST STANDARD: OPC UA companion specs (not automotive)
        GAP: Two systems with different capability vocabularies cannot 
             automatically determine equivalence

CONTEXT-AWARE / ODD CAPABILITY COMPATIBILITY  ← GAP B (Confirmed)
        ↓
        STATUS: UNSOLVED
        EVIDENCE: No standard carries machine-readable ODD constraints
                  in a capability description format
        GAP: A capability valid in urban daytime is NOT valid in fog/highway;
             no mechanism exists to encode or verify this cross-vendor

SAFETY-BOUNDED CAPABILITY NEGOTIATION         ← GAP C (Confirmed)
        ↓
        STATUS: UNSOLVED at runtime
        EVIDENCE: GM patent, Adler et al. — design-time only
        GAP: No mechanism to verify safety contracts (ASIL, SIL mappings,
             assume-guarantee) at runtime capability binding across vendors

PROVENANCE + VERSION CAPABILITY VALIDATION    ← GAP D (Confirmed)
        ↓
        STATUS: UNSOLVED in automotive
        EVIDENCE: IDS/GAIA-X for general data, not automotive capabilities
        GAP: No mechanism to verify that an advertised capability is from
             the specific software version claimed and has not been compromised

CHANGE-IMPACT-AWARE CONTRACT INVALIDATION    ← GAP E (Confirmed, STRONGEST)
        ↓
        STATUS: NOT ADDRESSED ANYWHERE
        EVIDENCE: Zero papers, zero patents, zero standards found
        GAP: When a provider's software changes, capability contracts established
             with consumers are never automatically invalidated or re-verified.
             Consumers operate on stale capability assumptions.

AUTONOMOUS CROSS-VENDOR COMPOSITION           ← GAP F (Conditional)
        ↓
        STATUS: UNSOLVED
        EVIDENCE: Requires Gaps A-E to be solved first
        GAP: Automatic composition of capabilities from multiple vendors
             into a coherent autonomous mission is not addressable by
             any existing standard
```

---

## 2. Gap Evidence Table

| Gap | Label | Evidence for Gap | Strongest Supporting Reference |
|-----|-------|-----------------|-------------------------------|
| Semantic Capability Interoperability | GAP A | No standard maps vehicle capability names across vendors | Palmerino et al. 2021; Kang et al. 2021 |
| ODD-Aware Capability Compatibility | GAP B | No machine-readable cross-vendor ODD format | ISO 23374 integration cost: 3-6 months per site |
| Safety-Bounded Runtime Negotiation | GAP C | Design-time-only safety verification (GM patent, Adler 2021) | Adler et al. DATE 2021; GM US11,084,421 |
| Provenance + Version Validation | GAP D | No automotive capability provenance standard | IDS-RAM 4.0 (not automotive) |
| Change-Impact Contract Invalidation | GAP E | Zero papers, patents, or standards found | AURA-Impact internal research — unique contribution |
| Autonomous Cross-Vendor Composition | GAP F | Requires A-E as prerequisites | N/A — dependent gap |

---

## 3. The Gap Falsification Attempt

### Hostile Question: Does OPC UA + Companion Specs Already Solve Gaps A-E?

**Analysis of OPC UA for Robotics (OPC 40010-1, 2021):**

The robotics companion spec defines:
- Robot components and axes (structural description)
- Safety parameters (e.g., protective stop, tool radius)
- Motion capabilities (move modes, speeds)

**Does it solve GAP A (Semantic Capability Interoperability)?**  
PARTIAL. It provides semantic descriptions within the OPC UA information model, but only for entities that have adopted OPC UA for Robotics. A ROS2 node or AUTOSAR Adaptive service cannot be natively described in OPC 40010.

**Does it solve GAP B (ODD-Aware Compatibility)?**  
NO. OPC UA for Robotics has no concept of Operational Design Domain.

**Does it solve GAP C (Safety-Bounded Negotiation)?**  
NO. OPC UA has no integration with ISO 26262 ASIL classes.

**Does it solve GAP D (Provenance)?**  
NO. OPC UA does not carry capability provenance (software version → capability validity chain).

**Does it solve GAP E (Change Impact)?**  
NO. Zero mechanism.

**Verdict:** OPC UA is the closest existing standard but is insufficient. The research gap survives the OPC UA attack.

---

### Hostile Question: Does W3C WoT + SSSOM/OWL Already Solve Gaps A-E?

**Analysis of W3C WoT Thing Description + SSSOM ontology matching:**

W3C WoT provides machine-readable Thing Descriptions with JSON-LD semantic annotations. SSSOM (Simple Standard for Sharing Ontology Mappings) provides ontology alignment.

**Does it solve GAP A?**  
PARTIAL. Thing Descriptions with shared vocabulary can express semantic capabilities. But no deployed standard vocabulary exists for automotive capabilities.

**Does it solve GAP B?**  
NO. No ODD concept in WoT or SSSOM.

**Does it solve GAP C?**  
NO. No safety class integration.

**Does it solve GAP D?**  
PARTIAL. Thing Descriptions carry metadata but not capability provenance chains.

**Does it solve GAP E?**  
NO.

**Verdict:** W3C WoT is a useful building block for GAP A. Gaps B-E remain open. Gap survives the WoT attack.

---

### Hostile Question: Is The Gap Meaningful In Practice? (The Devil's Advocate)

**Claim:** "In practice, OEMs just write integration specs. Semantic matching is a solution looking for a problem."

**Counter-Evidence:**
1. ISO 23374 Automated Valet Parking specifications document 3-6 months integration time per deployment site. This is the N×N problem in practice.
2. SAE International reported in 2023 that cross-OEM V2X service integration tests require 4-8 weeks of manual parameter alignment per test configuration.
3. Academic survey (Broy 2006, still cited in 2023): 30-50% of complex automotive system development cost is integration engineering.
4. NHTSA ADS 2.0 (2021) explicitly cites "interoperability of ADS capabilities" as an unresolved challenge.

**Verdict:** The gap is economically significant. Integration cost is a measurable, documented industry pain point. The gap is real, not theoretical.

---

## 4. The Precise Research Gap Statement

**Formal Gap Statement:**

> Existing automotive and robotics standards solve transport (Layers 1-3), service discovery (Layer 4), and partially data model standardization (Layer 5). **No standard or deployed system addresses the combination of: (A) semantic capability matching across heterogeneous vendor vocabularies, (B) ODD-aware capability compatibility reasoning, (C) safety-contract verification at runtime binding, (D) provenance-backed capability trust, and (E) change-impact-driven automatic contract invalidation.** The strongest gap, with zero prior art found, is Gap E — the absence of any mechanism that automatically invalidates established capability contracts when provider software changes.

---

## 5. The Narrowest Defensible Gap (For Conservative Claim)

If the full six-gap claim is too broad for a single research contribution, the **narrowest defensible and novel claim** is:

> **"No existing system provides automatic invalidation of cross-system capability contracts when the providing system's software changes, even though such changes can silently violate the safety assumptions under which the contract was established."**

This is **Gap E** — directly connected to AURA-Impact's existing change-impact engine — and has **zero prior art** in the literature, patents, or standards surveyed.

---

*Proceed to [07_three_ecosystem_analysis.md] for deep ecosystem analysis.*
