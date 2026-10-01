# 10 — THE FUTURE AURA INTEROPERABILITY LAYER: SCHEMA, LIFECYCLE & CORE ALGORITHMS

**Document Reference:** `research/autonomous_interoperability/10_FUTURE_AURA_PROTOCOL.md`  
**Focus:** Conceptual Architecture of the Semantic Interoperability Layer, Machine-Readable Manifests, and Capability Mapping  
**Author:** Lead Software Architect & Protocol Designer  

---

## 1. Architectural Injunction: We Do Not Design a Transport Protocol
A critical failure mode of academic proposals is attempting to reinvent the transport layer. We formally declare:
> **The AURA Interoperability Layer does NOT replace or reinvent CAN, Automotive Ethernet, DDS, SOME/IP, ROS 2, or C-V2X.**

Existing protocols excel at transporting bytes across physical wires and radio spectrum. AURA operates **strictly above them**, acting as a lightweight, machine-readable **Semantic Capability & Safety Contract Layer**.

---

## 2. The Machine-Readable AURA Capability Manifest Schema

To enable heterogeneous autonomous systems to understand each other without human intervention, each agent exports an **AURA Capability Manifest** (serialized as lightweight JSON-LD or ASN.1 binary):

```json
{
  "$schema": "https://aura-impact.org/schemas/v1/manifest.json",
  "system_identity": {
    "agent_id": "urn:aura:agent:autonomous_delivery_pod:v42_dal",
    "vendor": "Nuro / Cartken Partner",
    "model": "Courier-Pod-4",
    "software_version": "3.4.1+build.892",
    "cryptographic_attestation": "ed25519:3bf9a8e2..."
  },
  "operational_design_domain": {
    "weather_envelope": ["CLEAR", "LIGHT_RAIN"],
    "max_operating_speed_mps": 6.94,
    "road_classifications": ["SIDEWALK", "CROSSWALK", "PARKING_LOT", "URBAN_SECONDARY"],
    "ambient_temperature_range_c": [-10, 45]
  },
  "kinetic_capabilities": {
    "nominal_deceleration_mps2": 2.5,
    "emergency_deceleration_mps2": 4.5,
    "stopping_distance_envelope_m": {
      "at_5mps_dry": 3.8,
      "at_5mps_wet": 5.2
    },
    "turning_radius_m": 0.8
  },
  "sensor_and_perception_envelope": {
    "primary_modalities": ["STEREO_VISION", "SOLID_STATE_LIDAR"],
    "effective_detection_range_m": 35.0,
    "perception_latency_ms": 42.5,
    "current_degraded_modes": []
  },
  "interfaces_and_services": [
    {
      "service_id": "srv:intent:crosswalk_yield_request",
      "transport_binding": "DDS://domain_42/topic_crosswalk",
      "protocol_syntax": "SOMEIP_v2",
      "direction": "BIDIRECTIONAL"
    }
  ],
  "safety_contracts": {
    "iso_classification": "ISO_13849_PL_d / ISO_26262_ASIL_B",
    "minimum_risk_maneuver": "IMMEDIATE_CONTROLLED_STOP_IN_PLACE",
    "fail_safe_timeout_ms": 150,
    "mandatory_invariants": [
      "SAFE_CLEARANCE_CORRIDOR_MIN_1_5M",
      "COLLISION_AVOIDANCE_OVERRIDE_ACTIVE"
    ]
  },
  "provenance_and_dependencies": {
    "upstream_firmware_hash": "sha256:7a92c3...",
    "compatible_aura_protocol_version": "1.2.0"
  }
}
```

---

## 3. Protocol Operational Lifecycle: From Discovery to Action

We evaluate the full theoretical lifecycle and distinguish **strictly necessary phases** from **over-engineered academic bloat**:

```
[ PHASE 1: DISCOVER ] ──► [ PHASE 2: DESCRIBE ] ──► [ PHASE 3: MATCH ]
                                                          │
                                                          ▼
[ PHASE 6: EXECUTE ]  ◄── [ PHASE 5: VERIFY ]   ◄── [ PHASE 4: NEGOTIATE ]
       │
       ▼
[ PHASE 7: MONITOR ]  ──► [ PHASE 8: UPDATE ]
```

### Critical Elimination: Which Phases Are Actually Necessary?
* **STRICTLY NECESSARY (Must be supported):**
  1. **DISCOVER:** Detect surrounding autonomous agents via existing local discovery (DDS SPDP, SOME/IP-SD, C-V2X beacons).
  2. **DESCRIBE:** Exchange the lightweight AURA Capability Manifest.
  3. **MATCH:** Screen capabilities using the Architectural Context Gate to reject semantic decoys.
  4. **VERIFY:** Formally prove that the proposed cooperation satisfies internal safety invariants ($C_{safe} \subseteq C_{contract}$).
  5. **EXECUTE:** Execute coordinated kinetic trajectory with hard local watchdog override.
* **OVER-ENGINEERED / DANGEROUS (Eliminated or Simplified):**
  - *Complex Multi-Round Bidding / Negotiation:* Autonomous kinetic vehicles traveling at 80 km/h cannot engage in iterative, multi-round contract auctions. Negotiation must be **single-shot, deterministic, and bounded within 5 milliseconds**. If agreement is not achieved in one shot, the system must immediately default to its local defensive fallback.
  - *Heavy Distributed Consensus:* BFT or Paxos consensus across vehicles creates fatal latency and network partitioning risks. AURA uses **direct peer-to-peer verification**.

---

## 4. How Internal AURA-Impact Algorithms Map to the Future Protocol

The core scientific strength of this proposal is that **we do not invent new algorithms from scratch**. We extend the four mathematically proven components of internal AURA-Impact:

```
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│ INTERNAL AURA-IMPACT (CURRENT)  │         │ AURA PROTOCOL LAYER (FUTURE)    │
├─────────────────────────────────┤         ├─────────────────────────────────┤
│ Artifact Dependency Graph       │ ──────► │ Multi-Agent Capability Graph    │
│ (Req → Component → Code → Test) │         │ (Agent A → Manifest → Agent B)  │
├─────────────────────────────────┤         ├─────────────────────────────────┤
│ DomainHashEmbedder-384          │ ──────► │ Cross-Vendor Ontology Matcher   │
│ (384-dim token vectorizer)      │         │ (Maps vendor terms to ontology) │
├─────────────────────────────────┤         ├─────────────────────────────────┤
│ Architectural Context Gate      │ ──────► │ Semantic Decoy Rejection Gate   │
│ (ECU + Subsystem + Interface)   │         │ (Rejects invalid ODD/Domains)   │
├─────────────────────────────────┤         ├─────────────────────────────────┤
│ Non-Bypassable Safety Gate      │ ──────► │ Dynamic Safety Contract Gate    │
│ Invariant: T_safe ⊆ T_selected  │         │ Invariant: C_safe ⊆ C_contract  │
├─────────────────────────────────┤         ├─────────────────────────────────┤
│ Change Impact Analysis          │ ──────► │ Cross-System Change Propagation │
│ (Diff → Affected Regression)    │         │ (OTA update → Downstream impact)│
└─────────────────────────────────┘         └─────────────────────────────────┘
```

### 1. Architectural Context Filtering: Rejecting Multi-Agent Decoys
In our internal demonstrator, the Context Gate rejected `SWC_BodyLightController` (Body domain) when modifying an ADAS deceleration requirement, despite 0.78 raw cosine similarity. 

In the multi-agent protocol, the Context Gate performs an identical vital function:
* *Example Decoy Attack:* An autonomous lawnmower robot broadcasts an operational state *"Active obstacle avoidance at 2.0 m/s² deceleration."* A high-speed highway autonomous truck picks up the broadcast. Raw text similarity is high.
* *Context Gate Action:* Evaluates ODD domain mismatch: `LAWNMOWER_OFFROAD` vs. `HIGHWAY_CLASS_8_TRUCK`.
* *Verdict:* **REJECTED.** Prevents the truck from treating a low-speed lawnmower as a peer platooning candidate.

### 2. The Non-Bypassable Safety Contract Gate ($C_{safe} \subseteq C_{contract}$)
In internal AURA-Impact, the Safety Gate blocks any optimizer from deselecting an ASIL-C/D test case. 

In the multi-agent protocol, the Safety Gate enforces:
$$\mathbf{C_{safe} \subseteq C_{contract}}$$
Where $C_{safe}$ is the set of non-negotiable physical constraints dictated by the vehicle's internal ISO 26262 safety case (e.g., minimum stopping distance on current road friction, minimum lateral clearance of 1.5 meters, fail-safe emergency stop timeout). 

If an external infrastructure controller requests an aggressive intersection merge that violates $C_{safe}$, **the Safety Gate intercepts and blocks the contract**. The vehicle defaults to its local Minimum Risk Maneuver (MRM), guaranteeing that external communication can never compromise passenger safety.

---

## 5. New Research Required
Extending AURA to multi-agent environments requires three substantial new research efforts:
1. **Dynamic Ontology Alignment:** Handling vocabulary drift across vendors without relying on cloud LLM inference at runtime.
2. **Cryptographic Identity & Attestation:** Lightweight hardware-root-of-trust (HSM) signing of manifests with sub-millisecond verification overhead.
3. **Lossy Wireless Channel Degradation:** Evaluating gate behavior when packet loss or wireless jamming interrupts contract completion.
