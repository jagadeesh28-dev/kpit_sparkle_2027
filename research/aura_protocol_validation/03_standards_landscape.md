# 03 — Standards Landscape
## Rigorous Per-Standard Capability Analysis
**Classification:** Standards Technical Audit  
**Date:** 2026-10-01

---

## Evaluation Methodology

For each standard, answer these exact questions with YES/NO/PARTIAL:
1. What does it standardize?
2. What does it discover?
3. What does it describe?
4. What does it semantically understand?
5. What does it verify?
6. Does it understand capability meaning?
7. Does it understand operational context/ODD?
8. Does it validate safety constraints?
9. Does it carry provenance?
10. Does it reason over dependencies?
11. Does it reason about software change impact?
12. Does it negotiate compatibility?
13. Does it support heterogeneous vendor semantics?
14. Does it support runtime autonomous capability composition?

---

## Standard 1: AUTOSAR Classic Platform (R22-11)

**Organization:** AUTOSAR  
**Scope:** Safety-critical automotive embedded software in static ECU configurations

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | RTOS, BSW, RTE, COM stack | AUTOSAR Classic Spec R22-11 |
| Discovers | Nothing — static configuration | SWC descriptions are compile-time |
| Describes | SWC port interfaces in ARXML | AUTOSAR Schema |
| Semantically understands | NO | Only syntactic port types |
| Verifies | Static compilation — no runtime verification | AUTOSAR Methodology |
| Understands capability meaning | NO | Port = data flow type, not semantic capability |
| Understands ODD | NO | Not part of AUTOSAR Classic |
| Validates safety constraints | PARTIAL — static ASIL annotation only | ISO 26262 mapping in ARXML |
| Carries provenance | NO | Version in ARXML but not capability provenance |
| Reasons over dependencies | NO | Port connections only |
| Reasons about change impact | NO | No change-impact mechanism |
| Negotiates compatibility | NO | Static, no runtime negotiation |
| Supports heterogeneous vendor semantics | NO | Monolithic per-vehicle |
| Runtime capability composition | NO | Static configuration only |

**Verdict:** AUTOSAR Classic solves intra-ECU interface typing. It does not touch cross-system semantic capability matching. **Not a gap-killer.**

---

## Standard 2: AUTOSAR Adaptive Platform (R22-11)

**Organization:** AUTOSAR  
**Scope:** Service-oriented architecture for high-compute automotive systems

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | ara::com, service-oriented middleware, manifest | AUTOSAR Adaptive Spec R22-11 |
| Discovers | SOME/IP-SD: service by ID + version | ara::com SWS_CM |
| Describes | Service interfaces in manifest (ARXML) | Service manifest spec |
| Semantically understands | NO | ServiceID is opaque 16-bit integer |
| Verifies | Interface type compatibility only | ara::com type matching |
| Understands capability meaning | NO | Service discovery has no semantic layer |
| Understands ODD | NO | ODD not in AUTOSAR scope |
| Validates safety constraints | NO — ASIL tagging is static metadata | AUTOSAR safety analysis |
| Carries provenance | NO | Version field exists but not capability provenance |
| Reasons over dependencies | NO | No dependency graph |
| Reasons about change impact | NO | No mechanism |
| Negotiates compatibility | NO | Binary: found/not-found |
| Supports heterogeneous vendor semantics | NO | Within one vehicle/platform |
| Runtime capability composition | LIMITED — service binding only | ara::com |

**Verdict:** AUTOSAR Adaptive adds SOA-style discovery but semantic capability understanding is completely absent. **Not a gap-killer.** The ServiceID problem is explicit: a service named "0x1234" tells a consumer nothing about what it does.

---

## Standard 3: SOME/IP (Service-Oriented Middleware over IP)

**Organization:** AUTOSAR  
**Scope:** Transport binding for automotive SOA

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Message framing, service discovery (SD), RPCs, events | AUTOSAR SOME/IP Spec |
| Discovers | Service by: ServiceID, InstanceID, MajorVersion, MinorVersion | SOME/IP-SD spec |
| Describes | Nothing beyond numeric IDs | No semantic description |
| Semantically understands | NO | Pure numeric identifier space |
| Verifies | NO | No verification in protocol |
| Understands capability meaning | NO | ServiceID is opaque |
| Understands ODD | NO | |
| Validates safety constraints | NO | |
| Carries provenance | NO | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO | Version check only |
| Supports heterogeneous vendor semantics | NO | |
| Runtime capability composition | NO | |

**Verdict:** SOME/IP is a transport binding. ServiceID is semantically empty. Discovering "Service 0x0301 v2.1" tells you nothing about what that service does. **Completely irrelevant to semantic capability matching.**

---

## Standard 4: DDS (Data Distribution Service, v1.4)

**Organization:** OMG  
**Scope:** Real-time publish-subscribe data middleware

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Pub-sub, topics, QoS, discovery (RTPS) | OMG DDS v1.4 |
| Discovers | Topic by name + data type name | RTPS discovery |
| Describes | Data types via IDL | OMG IDL spec |
| Semantically understands | NO | TopicName is free string |
| Verifies | Type compatibility (structural) | Type checking in IDL |
| Understands capability meaning | NO | Topic name has no semantic meaning |
| Understands ODD | NO | |
| Validates safety constraints | NO | |
| Carries provenance | NO | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO — matching is name + type | |
| Supports heterogeneous vendor semantics | NO | |
| Runtime capability composition | NO | |

**Verdict:** DDS provides topic-based pub-sub with QoS. Two topics named "pedestrian_detection" and "FrontPerception" can be semantically identical but DDS will never discover this. **Not a gap-killer.**

**Important DDS caveat:** DDS-XTYPES (OMG DDS-XTypes 1.3) allows type evolution, but still no semantic meaning.

---

## Standard 5: ROS 2 (Robot Operating System 2)

**Organization:** Open Robotics / ROS2 Technical Steering Committee  
**Scope:** Robot middleware for research and industrial robotics

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Node-topic-service model built on DDS | ROS 2 design docs |
| Discovers | Topic/service by exact name + type | DDS discovery via rmw |
| Describes | Message types via .msg/.srv/.action files | ROS2 IDL |
| Semantically understands | NO | Names are freeform strings |
| Verifies | Type match only | Interface type checking |
| Understands capability meaning | NO | |
| Understands ODD | NO | |
| Validates safety constraints | NO | |
| Carries provenance | NO | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO | |
| Supports heterogeneous vendor semantics | NO — requires same message types | |
| Runtime capability composition | LIMITED | ROS2 composition |

**Verdict:** ROS 2 inherits DDS limitations for semantic discovery. Research community is actively working on semantic extensions (e.g., ROS2-Ontology proposals on GitHub) but nothing is standardized. **Not a gap-killer.** ROS2 proposals actually confirm the gap.

---

## Standard 6: OPC UA (Unified Architecture)

**Organization:** OPC Foundation  
**Scope:** Industrial automation information modeling and communication

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Information model, services, security, pub-sub | OPC UA Part 1–14 |
| Discovers | Service endpoints via Discovery Server | OPC UA Part 4 |
| Describes | Semantic information model (node types, references) | OPC UA Information Model |
| Semantically understands | PARTIAL — within OPC UA node space | Companion spec capability |
| Verifies | Service interface compatibility | Client-server matching |
| Understands capability meaning | PARTIAL — companion specs define domain semantics | OPC 40010 Robotics |
| Understands ODD | NO | No automotive ODD concept |
| Validates safety constraints | NO | Safety not in OPC UA core |
| Carries provenance | NO | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | PARTIAL — session negotiation | |
| Supports heterogeneous vendor semantics | PARTIAL — via companion specs | |
| Runtime capability composition | PARTIAL — method calls and objects | |

**Verdict:** OPC UA is the closest existing standard to AURA's semantic layer concept. Companion specs provide domain semantics. **However:** OPC UA companion specs for automotive/autonomous systems do not exist at scale. No ODD, no ASIL, no change impact. Latency model (client-server polling) is inappropriate for real-time capability negotiation. **Partial gap-killer — addresses semantic modeling but not automotive-specific requirements.**

---

## Standard 7: W3C Web of Things (WoT)

**Organization:** W3C  
**Scope:** IoT device description and interaction

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Thing Description (TD) JSON-LD format | W3C WoT Architecture 2020 |
| Discovers | Links, directories | WoT Discovery spec |
| Describes | Properties, actions, events with semantic types | Thing Description |
| Semantically understands | PARTIAL — JSON-LD semantic annotations | schema.org, custom contexts |
| Verifies | Schema validation only | |
| Understands capability meaning | PARTIAL — via schema.org or custom vocabularies | |
| Understands ODD | NO | |
| Validates safety constraints | NO | |
| Carries provenance | PARTIAL — TD metadata | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO | |
| Supports heterogeneous vendor semantics | PARTIAL — via shared vocabularies | |
| Runtime capability composition | NO | |

**Verdict:** W3C WoT's Thing Description is architecturally similar to AURA's capability manifest. **However:** No automotive safety model, no ODD, no change impact, designed for IoT not real-time safety-critical systems. **Medium gap-killer for P_semantic only.**

---

## Standard 8: ISO 23150 (Road Vehicles — Data Communication)

**Organization:** ISO TC204  
**Scope:** Interface between automated driving system and sensors

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Logical interface between sensor and ADS | ISO 23150:2023 |
| Discovers | NO — static interface definition | |
| Describes | Object list format, track attributes | ISO 23150 data model |
| Semantically understands | PARTIAL — standardized object taxonomy | |
| Verifies | NO | |
| Understands capability meaning | PARTIAL — sensor performance metadata | |
| Understands ODD | PARTIAL — operational conditions | |
| Validates safety constraints | NO | |
| Carries provenance | NO | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO | |
| Supports heterogeneous vendor semantics | YES — inter-sensor standard | |
| Runtime capability composition | NO | |

**Verdict:** ISO 23150 standardizes the sensor-ADS interface. It provides cross-vendor interoperability for sensor output format. But it is a static interface standard, not a dynamic capability negotiation protocol. **Not a gap-killer for runtime semantic negotiation.**

---

## Standard 9: COVESA VSS (Vehicle Signal Specification)

**Organization:** COVESA  
**Scope:** Standardized vehicle data signal naming

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Signal naming tree (e.g., Vehicle.ADAS.LaneDeparture) | VSS v3.0 |
| Discovers | NO | |
| Describes | Signal name, data type, unit | VSS schema |
| Semantically understands | PARTIAL — standardized names | |
| Verifies | NO | |
| Understands capability meaning | NO — signals ≠ capabilities | |
| Understands ODD | NO | |
| Validates safety constraints | NO | |
| Carries provenance | NO | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO | |
| Supports heterogeneous vendor semantics | YES — naming standard | |
| Runtime capability composition | NO | |

**Verdict:** VSS standardizes signal naming. Knowing "Vehicle.ADAS.LaneDeparture.IsActive" exists tells you a lane departure warning is active; it tells you nothing about its detection accuracy, ODD, safety class, or whether you can safely compose it with another system. **Not a gap-killer.**

---

## Standard 10: V2X Standards (C-V2X, DSRC, IEEE 1609)

**Organization:** ETSI, SAE, 3GPP, IEEE  
**Scope:** Vehicle-to-everything communication

| Question | Answer | Evidence |
|---------|--------|---------|
| Standardizes | Radio, MAC, BSM/CAM/DENM message formats | ETSI EN 302 637, SAE J2945 |
| Discovers | Basic Safety Message broadcast | BSM/CAM |
| Describes | Vehicle state (position, speed, heading) | BSM/CAM fields |
| Semantically understands | NO — fixed message fields | |
| Verifies | PKI authentication (IEEE 1609.2) | |
| Understands capability meaning | NO — no capability field in BSM/CAM | |
| Understands ODD | NO | |
| Validates safety constraints | NO | |
| Carries provenance | PARTIAL — certificate chain | |
| Reasons over dependencies | NO | |
| Reasons about change impact | NO | |
| Negotiates compatibility | NO | |
| Supports heterogeneous vendor semantics | NO — fixed message format | |
| Runtime capability composition | NO | |

**Verdict:** V2X standards are broadcast communication protocols with fixed message formats. They communicate vehicle state, not capability semantics. A V2X message does not tell you "I can provide pedestrian detection to 0.3m accuracy, ASIL-B, valid until 2025-12-31." **Not a gap-killer.**

---

## Summary Standards Comparison Matrix

| Standard | Semantic Discovery | Capability Desc | ODD | Safety Contracts | Provenance | Change Impact | Cross-Vendor | RT Negotiation |
|---------|:----------------:|:---------------:|:---:|:---------------:|:----------:|:-------------:|:------------:|:--------------:|
| AUTOSAR Classic | ❌ | ❌ | ❌ | ❌ static | ❌ | ❌ | ❌ | ❌ |
| AUTOSAR Adaptive | ❌ | ❌ | ❌ | ❌ static | ❌ | ❌ | ❌ | ❌ |
| SOME/IP | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| DDS | ❌ | 🟡 types | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ROS 2 | ❌ | 🟡 types | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OPC UA | 🟡 partial | ✅ info model | ❌ | ❌ | ❌ | ❌ | 🟡 via specs | 🟡 |
| W3C WoT | 🟡 JSON-LD | ✅ TD | ❌ | ❌ | 🟡 | ❌ | 🟡 | ❌ |
| ISO 23150 | ❌ | 🟡 sensor | 🟡 | ❌ | ❌ | ❌ | ✅ | ❌ |
| COVESA VSS | 🟡 names | 🟡 signals | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| V2X (C-V2X) | ❌ | ❌ | ❌ | ❌ | 🟡 PKI | ❌ | ✅ | ❌ |
| **AURA (proposed)** | **✅** | **✅** | **✅** | **✅** | **✅** | **✅** | **✅** | **✅** |

Legend: ✅ = Solved | 🟡 = Partial | ❌ = Not Solved

---

## Final Standards Verdict

**No existing standard combines all seven dimensions.**  
**The most similar standard (OPC UA) lacks ODD, safety, change-impact.**  
**The gap is genuine at the intersection of:**  
1. Automotive safety classes (ASIL/ISO 26262)  
2. ODD-aware capability reasoning  
3. Cross-vendor semantic capability matching  
4. Runtime provenance and change-impact tracking  

*Proceed to [04_prior_art_matrix.csv] for structured prior-art classification.*
