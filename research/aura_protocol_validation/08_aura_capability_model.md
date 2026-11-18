# 08 — AURA Capability Model
## Formal Capability Contract Design: Minimum Necessary Fields
**Classification:** Formal Model Design  
**Date:** 2026-10-01

---

## 1. Design Methodology

The candidate model presented in the research brief was:

```json
CapabilityContract = {
  capability_id, provider_id, semantic_type, inputs, outputs,
  preconditions, postconditions, operating_domain, ODD, 
  spatial_reference, temporal_constraints, units, accuracy, confidence,
  latency, availability, resource_requirements, safety_constraints,
  ASIL_or_safety_class, provenance, version, validity_interval,
  dependencies, interface_binding, trust_metadata
}
```

**Hostile Design Process:**
1. Start with empty model
2. Add only fields that are necessary (not merely desirable)
3. Justify each field with a failure mode if omitted
4. Classify: mandatory vs optional vs derived vs runtime vs static
5. Determine: signed vs mutable

---

## 2. Field-by-Field Justification

### 2.1 SEMANTIC IDENTITY (Mandatory)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `capability_id` | UUID v4 | YES | Cannot reference or revoke contracts |
| `semantic_type` | URI (ontology term) | YES | P_semantic gap — cannot match across vendors |
| `semantic_synonyms[]` | Array of URI | OPTIONAL | Helps matching but not critical |
| `natural_language_description` | String | OPTIONAL | Human readability only |

**Justification for `semantic_type` as URI:**
Using a URI (e.g., `https://automotive-capabilities.org/perception/pedestrian-detection`) rather than a free string forces normalization against a shared vocabulary. Without this, matching reduces to keyword matching with high false-positive and false-negative rates.

---

### 2.2 INTERFACE IDENTITY (Mandatory)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `provider_id` | URI (system identifier) | YES | Cannot verify source |
| `interface_binding.type` | Enum (SOME_IP, DDS, ROS2, OPC_UA, HTTP) | YES | Cannot establish physical connection |
| `interface_binding.endpoint` | String | YES | Cannot reach service |
| `interface_binding.message_type` | String | YES | Cannot deserialize messages |
| `inputs[]` | Typed parameter list | CONDITIONAL | If service requires inputs |
| `outputs[]` | Typed parameter list | YES | Must verify output format compatibility |

---

### 2.3 OPERATIONAL CONTEXT (Mandatory for Safety)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `odd.domain_type` | Enum (URBAN, HIGHWAY, RURAL, PARKING, INTERSECTION) | YES | Capability may be used outside valid domain |
| `odd.speed_range_ms` | {min: float, max: float} | YES | Speed-dependent capabilities silently misused |
| `odd.weather_conditions[]` | Enum list (CLEAR, RAIN, FOG, SNOW) | YES | Fog-only failure modes invisible |
| `odd.time_of_day[]` | Enum list (DAY, NIGHT, DUSK) | YES | Night-mode capability misapplied |
| `odd.road_types[]` | List | OPTIONAL | More specific ODD refinement |
| `spatial_reference.frame` | String (WGS84, ENU, UTM, vehicle-local) | YES | Coordinate frame mismatch = collision risk |
| `spatial_reference.datum` | String | OPTIONAL | Usually implied by frame |
| `units.spatial` | String (m, cm, mm) | YES | Unit mismatch = catastrophic |
| `units.temporal` | String (ms, s) | YES | |
| `units.angular` | String (rad, deg) | CONDITIONAL | If angular output |

**Critical Evidence For `odd` Mandatory Status:**
From ISO 21448 (SOTIF): "Performance limitations of a system may result in hazardous behavior when the system operates outside its designed operational domain." Without machine-readable ODD in the capability contract, cross-system composition can silently violate this requirement.

---

### 2.4 QUALITY ATTRIBUTES (Mandatory)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `accuracy.spatial_m` | float | YES for perception | System assumes accuracy that doesn't hold |
| `accuracy.temporal_ms` | float | YES | Latency-sensitive fusion fails |
| `latency.typical_ms` | float | YES | Real-time constraints violated |
| `latency.worst_case_ms` | float | YES | WCET analysis fails |
| `availability.target_pct` | float 0-100 | OPTIONAL | Graceful degradation planning |
| `confidence.typical` | float 0-1 | OPTIONAL | Helps downstream fusion |
| `confidence.minimum_acceptable` | float | OPTIONAL | Rejection threshold for consumers |

---

### 2.5 SAFETY CONSTRAINTS (Mandatory)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `safety.classification` | Enum (ASIL_A, ASIL_B, ASIL_C, ASIL_D, QM, SIL_1..4) | YES | Cannot verify safety requirement satisfaction |
| `safety.integrity_level_standard` | Enum (ISO_26262, IEC_61508, ISO_21448) | YES | ASIL and SIL are not directly comparable |
| `safety.failure_mode` | String | OPTIONAL | Documents expected failure behavior |
| `safety.fail_safe_behavior` | Enum (STOP, DEGRADED, MRM) | YES | Consumer must know how provider fails |
| `safety.assumes[]` | List of precondition contracts | OPTIONAL | Compositional safety requires explicit assumptions |
| `safety.guarantees[]` | List of postcondition contracts | OPTIONAL | Composable with Adler et al. approach |

**Critical Insight:** `safety.integrity_level_standard` is MANDATORY because ASIL-B (ISO 26262 automotive) and SIL-2 (IEC 61508 general) are NOT the same thing. Cross-standard translation requires explicit knowledge of which standard applies.

---

### 2.6 SECURITY AND TRUST (Mandatory)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `trust.provider_certificate` | X.509 cert or URI | YES | Cannot verify identity |
| `trust.signature` | Cryptographic signature over contract | YES | Contract can be tampered |
| `trust.revocation_endpoint` | URI | YES | Cannot check revocation |
| `trust.authorization_scope` | Enum (PUBLIC, FLEET, BILATERAL, PRIVATE) | YES | Access control |

---

### 2.7 PROVENANCE AND LIFECYCLE (Mandatory)

| Field | Type | Mandatory? | Failure if omitted |
|-------|------|------------|-------------------|
| `provenance.software_version` | SemVer string | YES | Cannot correlate with change impact |
| `provenance.software_hash` | SHA-256 | YES | Cannot verify binaries match declared version |
| `provenance.valid_from` | ISO 8601 datetime | YES | Stale contract detection |
| `provenance.valid_until` | ISO 8601 datetime | YES | Stale contract detection |
| `provenance.last_validated` | ISO 8601 datetime | YES | Freshness check |
| `provenance.validation_evidence_uri` | URI | OPTIONAL | Links to test reports |
| `version` | SemVer | YES | Change detection |
| `dependencies[]` | List of capability_ids | OPTIONAL | For compositional contracts |

---

### 2.8 CHANGE IMPACT EXTENSION (AURA-Specific — Novel)

This section has NO equivalent in any existing standard. It is the core AURA differentiator.

| Field | Type | Mandatory? | Justification |
|-------|------|------------|--------------|
| `change_impact.dependency_graph_hash` | SHA-256 | YES (for AURA) | Detects when provider dependency graph changes |
| `change_impact.invalidation_webhook` | URI | YES (for AURA) | Consumer receives change notifications |
| `change_impact.last_provider_commit` | Git SHA or build hash | YES (for AURA) | Ties contract to specific software state |
| `change_impact.affected_artifact_ids[]` | List | OPTIONAL | Which internal artifacts affect this capability |
| `change_impact.invalidation_condition` | Enum (ANY_CHANGE, SAFETY_CHANGE, SEMANTIC_CHANGE) | YES (for AURA) | Granularity of invalidation trigger |

---

## 3. Minimum Viable Capability Contract

After the hostile analysis, the **minimum viable capability contract** requires:

```json
{
  "capability_id": "uuid-v4",
  "semantic_type": "https://aura-automotive.org/capability/pedestrian-detection",
  "provider_id": "https://supplier-b.example.com/systems/perception-node-v2",

  "interface_binding": {
    "type": "ROS2",
    "topic": "/perception/pedestrians",
    "message_type": "vision_msgs/Detection3DArray"
  },

  "outputs": [{
    "name": "pedestrian_positions",
    "type": "Detection3DArray",
    "spatial_reference": {"frame": "ENU", "datum": "WGS84"},
    "units": {"spatial": "m", "temporal": "ms"}
  }],

  "quality": {
    "accuracy_spatial_m": 0.25,
    "latency_typical_ms": 65,
    "latency_worst_case_ms": 100
  },

  "odd": {
    "domain_type": ["URBAN"],
    "speed_range_ms": {"min": 0, "max": 14},
    "weather": ["CLEAR", "LIGHT_RAIN"],
    "time_of_day": ["DAY", "DUSK"]
  },

  "safety": {
    "classification": "ASIL_B",
    "standard": "ISO_26262",
    "fail_safe_behavior": "DEGRADED_OUTPUT_WITH_CONFIDENCE_FLAG"
  },

  "trust": {
    "provider_cert": "https://pki.aura.example.com/certs/supplier-b-2024",
    "signature": "ed25519:base64...",
    "revocation_uri": "https://pki.aura.example.com/revoke/supplier-b-2024"
  },

  "provenance": {
    "software_version": "2.3.1",
    "software_hash": "sha256:abc123...",
    "valid_from": "2024-01-01T00:00:00Z",
    "valid_until": "2024-12-31T23:59:59Z"
  },

  "change_impact": {
    "dependency_graph_hash": "sha256:def456...",
    "invalidation_webhook": "https://consumer-a.example.com/webhooks/capability-invalidated",
    "last_provider_commit": "git:a7f3b2c",
    "invalidation_condition": "SAFETY_CHANGE"
  }
}
```

---

## 4. Field Classification Summary

| Field Group | Count | Classification |
|------------|-------|---------------|
| Semantic Identity | 2 mandatory, 2 optional | Static, signed at publication |
| Interface Identity | 5 mandatory | Static, signed |
| Operational Context | 9 mandatory, 3 optional | Static, signed |
| Quality Attributes | 4 mandatory, 2 optional | Static, signed |
| Safety Constraints | 5 mandatory, 2 optional | Static, signed |
| Security/Trust | 4 mandatory | Static, externally signed |
| Provenance/Lifecycle | 5 mandatory, 1 optional | Partially runtime (valid_until) |
| Change Impact (AURA) | 5 mandatory | Runtime-updated |

**Total: ~35 meaningful fields. 30 mandatory. 8 optional. Considerably fewer than the proposed 40+.**

---

*Proceed to [09_semantic_matching_architecture.md] for matching engine design.*
