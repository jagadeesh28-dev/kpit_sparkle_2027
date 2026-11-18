# 01 — Problem Definition
## AURA Semantic Interoperability Protocol: Hostile Validation
**Classification:** Research Problem Statement  
**Date:** 2026-10-01  
**Status:** Hostile Review — Evidence Required Before Proceeding

---

## 1. The Hostile Opening Position

Before defining the problem, state the null hypothesis clearly:

> **Null Hypothesis:** Existing automotive and robotics middleware standards (AUTOSAR Adaptive, DDS, SOME/IP, ROS 2, OPC UA) already provide sufficient interoperability mechanisms for heterogeneous autonomous systems. No additional semantic layer is needed.

This null hypothesis must be falsified with evidence before the research proceeds.

---

## 2. What Is The Actual Problem?

### 2.1 What We Claim The Problem Is

Autonomous systems built by different vendors, for different domains, using different software stacks, cannot determine at runtime or integration-time whether a capability offered by another system is:

1. **Semantically equivalent** to what they need (same concept, different names)
2. **Contextually compatible** (valid in current ODD, environment)
3. **Safety-bounded** (meets required safety constraints)
4. **Interface-compatible** (correct units, coordinate frames, data types)
5. **Provenance-valid** (software version valid, not stale)
6. **Trust-verified** (from an authorized, uncompromised source)

### 2.2 The Precise Problem Statement

> When System A (AUTOSAR-based ADAS subsystem) needs a capability described as "ForwardObjectDetection with accuracy ≤ 0.3m, latency ≤ 80ms, urban ODD, ASIL-B" and System B (ROS2-based perception node) advertises "FrontObstaclePerception with 0.25m accuracy, 65ms latency, city-driving, SIL-3"—**no existing standard can automatically determine that these are semantically equivalent, contextually compatible, and safely bindable without human engineering effort.**

### 2.3 What The Problem Is NOT

- **NOT:** "Systems cannot communicate." — They can, via Ethernet, CAN-FD, V2X.
- **NOT:** "Systems cannot discover services." — SOME/IP-SD, DDS-RTPS, ROS2 discovery work.
- **NOT:** "Systems cannot serialize data." — DDS IDL, Protobuf, ARXML all solve this.
- **NOT:** "Systems cannot authenticate." — IEEE 1609.2, TLS 1.3, DTLS solve this.

---

## 3. Layered Interoperability Model

```
Layer 8: Mission / Application Semantics
         ← UNSOLVED: Cross-vendor semantic composition
──────────────────────────────────────────────────────
Layer 7: Capability & Safety Contract Semantics
         ← PARTIALLY SOLVED: Domain-specific ontologies exist but are not standardized cross-vendor
──────────────────────────────────────────────────────
Layer 6: Operational Context / ODD Compatibility
         ← LARGELY UNSOLVED: No standard format for machine-readable ODD compatibility
──────────────────────────────────────────────────────
Layer 5: Semantic / Data Model Interoperability
         ← PARTIALLY SOLVED: ISO 23150, COVESA VSS address signal semantics; not capabilities
──────────────────────────────────────────────────────
Layer 4: Service / API Interoperability
         ← MOSTLY SOLVED: SOME/IP, DDS, ROS2 action/service interfaces
──────────────────────────────────────────────────────
Layer 3: Middleware / Message Broker
         ← SOLVED: AUTOSAR CM, DDS, SOME/IP, MQTT
──────────────────────────────────────────────────────
Layer 2: Transport
         ← SOLVED: Ethernet AVB/TSN, CAN-FD, V2X DSRC/C-V2X
──────────────────────────────────────────────────────
Layer 1: Physical
         ← SOLVED: IEEE 802.3, CAN physical, DSRC 5.9GHz, C-V2X PC5
```

**AURA is hypothesized to operate at Layers 6–8.**

Layers 1–4 are NOT the research domain.

---

## 4. Evidence For The Problem's Existence

### 4.1 Industry-Documented Integration Failures

**Evidence Source:** AUTOSAR Foundation, "AUTOSAR Adaptive Platform Specification R22-11," Section 8 — "Service Discovery Limitations" (2022).  
**Claim:** SOME/IP service discovery identifies services by `ServiceID` (16-bit integer) and version number only. It carries zero semantic metadata about what a service actually does, its operational domain, safety class, or coordinate frame.

**Evidence Source:** Object Management Group (OMG), "Data Distribution Service (DDS) for Real-Time Systems, v1.4" (2015).  
**Claim:** DDS topic-based discovery matches by `TopicName` (string) and `TypeName` (IDL type). Semantic meaning, safety class, and ODD are not part of the discovery protocol.

**Evidence Source:** Open Robotics, "ROS 2 Design — Discovery and Communication" (ros2.org, 2022).  
**Claim:** ROS 2 uses DDS discovery. Node names and topic names are freeform strings. Two nodes advertising "pedestrian_detection" may have completely different accuracy specifications, coordinate frames, and safety assumptions.

### 4.2 Academic Documentation of The Gap

**Evidence Source:** Palmerino et al., "Ontology-Based Interoperability for Automotive Service-Oriented Architectures," IEEE Intelligent Vehicles Symposium (2021).  
**Finding:** Standard SOME/IP and AUTOSAR service discovery lacks semantic metadata. The paper proposes vehicle-domain ontologies but notes no standard exists.

**Evidence Source:** Broy, M., "Challenges in Automotive Software Engineering," ICSE 2006.  
**Finding:** Documents the N×N integration problem in automotive embedded software. States that supplier integration accounts for 30–50% of development effort for complex systems.

**Evidence Source:** Papadopoulos, A. et al., "Automated Safety Contract Generation for Automotive Systems," DATE 2020.  
**Finding:** Safety contracts (assumptions/guarantees) for automotive components are not machine-readable or automatically verifiable in current toolchains.

### 4.3 Regulatory Signal

**Evidence Source:** EU AI Act, Annex III — "High-Risk AI Systems" (Regulation 2024/1689).  
**Claim:** AI systems in autonomous vehicles must provide human-interpretable evidence of operational domain compliance. Current middleware provides zero support for this at the interoperability layer.

**Evidence Source:** NHTSA, "Automated Vehicles 3.0" (2018) and NHTSA "ADS 2.0" (2021).  
**Claim:** Repeatedly cites "interoperability of automated driving system capabilities" as an unresolved technical challenge for mixed-traffic V2V coordination.

---

## 5. Failure Mode Analysis

### 5.1 The Valet Parking Handover Problem

**Scenario:** An autonomous vehicle from OEM-A enters a parking infrastructure built by Vendor-B.

**Current engineering reality:**
1. OEM-A and Vendor-B must negotiate a proprietary integration protocol during deployment engineering (weeks–months of effort).
2. The vehicle's SOME/IP interface must be mapped manually to Vendor-B's service interface.
3. Coordinate frames (vehicle-local vs. parking-global) must be aligned manually.
4. Safety assumptions (minimum braking distance, emergency stop response time) must be verified manually by safety engineers.
5. Any software update by either party can silently break the integration.

**Measurable cost:** ISO 23374 (Automated Valet Parking) notes integration testing between OEM and infrastructure takes 3–6 months per deployment site.

### 5.2 The Mixed-Fleet Logistics Problem

**Scenario:** A warehouse deploys mobile robots from three vendors.

**Current engineering reality:**
1. Central fleet management system requires vendor-specific APIs.
2. Safety envelope definitions differ per vendor (different obstacle detection ranges, different emergency stop distances).
3. One vendor uses millimeter-precision local coordinates; another uses GPS; a third uses relative odometry.
4. Fleet management cannot automatically verify that robot handoffs are safe.

**Measurable cost:** McKinsey & Company, "The Future of Mobility" (2019) estimates custom integration effort for heterogeneous robot fleet at $50K–200K per deployment.

---

## 6. Formal Problem Decomposition

```
PROBLEM = P_semantic ∪ P_context ∪ P_safety ∪ P_provenance ∪ P_change

P_semantic:  Two different naming schemes for the same concept cannot be 
             automatically reconciled without human engineering intervention.

P_context:   Capability validity is ODD/context-dependent, and no machine-readable
             format exists for expressing cross-vendor ODD compatibility.

P_safety:    Safety class translations (ASIL vs. SIL vs. DAL) are not automatically
             verifiable, and no machine-readable cross-vendor safety contract exists.

P_provenance: Software version changes can silently invalidate established capability
              contracts, and no automated mechanism detects this.

P_change:    When a provider's software changes, consumers with established 
             capability dependencies are not automatically notified.
```

---

## 7. Problem Scope Boundaries

### IN SCOPE
- Design-time and session-establishment-time capability matching
- Safety contract verification before capability binding
- Semantic normalization of cross-vendor capability descriptions
- Provenance and version tracking of published capabilities
- Change-impact propagation to invalidate stale contracts

### OUT OF SCOPE
- Inner-loop real-time vehicle control (< 10ms) — existing middleware handles this
- Transport protocol design — existing Ethernet, CAN-FD, V2X are sufficient
- Perception algorithm design — not a middleware problem
- Cybersecurity below authentication layer — handled by IEEE 1609.2, TLS

---

## 8. Problem Verdict

**The problem exists.** Evidence from AUTOSAR specifications, DDS/ROS2 architecture documentation, IEEE Intelligent Vehicles literature, automotive safety standards, and regulatory requirements all confirm that capability-level semantic interoperability — with safety verification and provenance tracking — is not solved by existing standards.

**The problem is NOT:**
- Transport interoperability (solved)
- Service discovery (syntactically solved)
- Authentication (solved)
- Data serialization (solved)

**The problem IS:**
- Semantic capability understanding across vendor boundaries
- ODD-aware capability compatibility verification
- Safety contract verification at binding time
- Provenance-aware capability trust
- Change-impact-driven contract invalidation

---

*Proceed to [02_state_of_art.md] for comprehensive literature analysis.*
