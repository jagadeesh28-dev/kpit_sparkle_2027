# 16 — Experimental Protocol
## AURA Synthetic Heterogeneous Ecosystem: Detailed Test Design
**Classification:** Experimental Protocol Specification  
**Date:** 2026-10-01

---

## 1. Three-System Experimental Ecosystem

### System A — AUTOSAR-Analog (Supplier A)

```yaml
system_id: "sys-a-autosar"
architecture: AUTOSAR_Adaptive_analog
middleware: SOME/IP over Ethernet (simulated)
language: C++
safety_standard: ISO_26262

capabilities_advertised:
  - name: "ForwardObjectDetection"
    internal_name: "FwdObjDet_AUTOSAR"
    semantic_type: null  # No ontology declared
    outputs:
      format: "Object list"
      units: "centimeters"  # NOTE: cm not m
      coordinate_frame: "vehicle-local-front-left-up"
    accuracy: 25  # cm
    latency_typical_ms: 55
    latency_worst_case_ms: 100
    odd:
      speed_max_kph: 60
      weather: ["CLEAR", "LIGHT_RAIN"]
      domain: "URBAN"
    safety:
      classification: "ASIL_B"
      standard: "ISO_26262"
    provenance:
      sw_version: "1.4.2"
      valid_until: "2025-06-30"
```

---

### System B — ROS2 Analog (Supplier B)

```yaml
system_id: "sys-b-ros2"
architecture: ROS2_based
middleware: DDS (CycloneDDS)
language: Python/C++
safety_standard: None declared

capabilities_advertised:
  - name: "FrontObstaclePerception"
    internal_name: "/perception/front/obstacles"
    semantic_type: null  # No ontology declared
    outputs:
      format: "Detection3DArray"
      units: "meters"
      coordinate_frame: "ENU"
    accuracy: 0.30  # m
    latency_typical_ms: 65
    latency_worst_case_ms: 120
    odd:
      speed_max_ms: 16.7  # 60 km/h in m/s
      weather: ["CLEAR", "LIGHT_RAIN", "FOG"]
      domain: "URBAN"
      time_of_day: ["DAY", "DUSK"]
    safety:
      classification: "QM"  # Not safety-qualified
      standard: "NONE"
    provenance:
      sw_version: "0.9.7"
      valid_until: "2025-12-31"
```

---

### System C — Generic Vendor (Supplier C)

```yaml
system_id: "sys-c-generic"
architecture: custom_vendor
middleware: REST/WebSocket + JSON
language: Java
safety_standard: IEC_61508

capabilities_advertised:
  - name: "RoadObjectTracking"
    internal_name: "tracking-service/v2/objects"
    semantic_type: "http://automotive-caps.vendor-c.com/tracking/road-objects"
    outputs:
      format: "JSON object list"
      units: "millimeters"  # NOTE: mm
      coordinate_frame: "WGS84"  # GPS
    accuracy: 0.30  # m (but actual accuracy in mm: 300 mm)
    latency_typical_ms: 80
    latency_worst_case_ms: 200  # REST overhead
    odd:
      speed_max_mph: 37  # 60 km/h in mph — different unit
      weather: ["CLEAR", "RAIN"]
      domain: ["URBAN", "SUBURBAN"]
    safety:
      classification: "SIL_2"  # IEC 61508, not ISO 26262
      standard: "IEC_61508"
    provenance:
      sw_version: "2.1.0"
      valid_until: "2025-09-30"
```

---

## 2. The Core Experiment: Three Scenarios

### Scenario 1 — Valet Parking Capability Handover

**Context:** AV Consumer (ASIL-B, urban, pedestrian detection, 0.3m required accuracy, 100ms budget)

**Request:**
```json
{
  "required_semantic_type": "PedestrianDetection",
  "odd": {"domain": "URBAN", "speed_ms": 3.0, "weather": "CLEAR", "time": "DAY"},
  "quality": {"accuracy_m": 0.30, "latency_budget_ms": 100},
  "safety": {"required_asil": "ASIL_B", "standard": "ISO_26262"}
}
```

**Expected AURA Results:**

| Provider | Semantic | ODD | Units/Frame | Safety | Provenance | Decision | Reason |
|---------|---------|-----|------------|--------|-----------|---------|--------|
| System A (ForwardObjectDetection) | MATCH | PASS | CONVERT (cm→m, frame) | PASS (ASIL-B) | VALID | **ACCEPT** | All gates pass after unit conversion |
| System B (FrontObstaclePerception) | MATCH | PASS | PASS (already m, ENU) | **FAIL** (QM < ASIL-B) | VALID | **REJECT** | Safety gate: QM < ASIL-B required |
| System C (RoadObjectTracking) | MATCH (similar) | PASS | CONVERT (mm→m, WGS84) | REVIEW (SIL-2 ↔ ASIL-B cross-standard) | VALID | **REVIEW_REQUIRED** | Cross-standard safety mapping needs human approval |

**Ground Truth:** A=ACCEPT, B=REJECT, C=REVIEW_REQUIRED  
**UAR Requirement:** System B must NEVER be accepted.

---

### Scenario 2 — Change-Impact Contract Invalidation

**Setup:**
1. Consumer has established binding with System A (ForwardObjectDetection)
2. System A's development team releases a software patch v1.4.3 that:
   - Changes the default coordinate frame from "vehicle-local-front-left-up" to "vehicle-local-front-right-down" (sign flip in Y and Z)
   - Updates latency from 100ms WCET to 85ms WCET (improvement)

**AURA Change-Impact Response:**

```
Step 1: System A publishes new build to CI/CD
Step 2: AURA change-impact engine detects dependency_graph_hash change
Step 3: AURA identifies affected consumers: [Consumer-X with binding sys-a-autosar-binding-001]
Step 4: AURA computes impact severity:
  - coordinate_frame changed: HIGH impact (sign flip invalidates output interpretation)
  - latency improved: LOW impact (no contract violation)
Step 5: AURA sends CapabilityInvalidationNotice to Consumer-X:
  {
    "binding_id": "sys-a-autosar-binding-001",
    "reason": "PROVIDER_SOFTWARE_CHANGE",
    "severity": "HIGH",
    "changed_fields": ["interface_binding.coordinate_frame"],
    "consumer_action_required": "RENEGOTIATE_OR_FAIL_SAFE",
    "new_capability_version": "1.4.3"
  }
Step 6: Consumer-X must:
  OPTION A: Re-negotiate with System A v1.4.3 (new coordinate frame)
  OPTION B: Activate fail-safe behavior
  NOT ALLOWED: Continue operating on stale v1.4.2 contract
```

**Measurement:** Time from System A software change commit to Consumer-X invalidation notice.  
**Target:** < 500ms (automated detection), < 5s (end-to-end invalidation flow)

---

### Scenario 3 — Adversarial Class K Attack

**Attack:** Attacker crafts a capability contract for System D (malicious) that:
- Uses semantic name "PedestrianDetection" (same as valid providers)
- Claims ASIL-D safety class (higher than needed)
- Claims 0.1m accuracy (better than needed)
- Has a valid-looking certificate (but signed by unrecognized CA)
- Has forged `software_hash` claiming to be System A's hash
- Actual capability: returns random bounding boxes

**AURA Response:**
```
Stage 5 (Provenance Check):
  sig_valid(contract-malicious) → FALSE (unrecognized CA in signature chain)
  → REJECT immediately, REASON: INVALID_CERTIFICATE_CHAIN
  → Log security event with attacker's certificate details
  → No further processing
```

**Ground Truth:** REJECT with reason INVALID_CERTIFICATE_CHAIN  
**UAR Constraint:** This MUST be REJECTED. If AURA accepts this, the experiment fails.

---

## 3. Measurement Protocol

### 3.1 Accuracy Measurement

```python
def evaluate_aura(benchmark_dataset):
    results = []
    for instance in benchmark_dataset:
        prediction = aura.evaluate(instance.request, instance.contracts)
        results.append({
            "ground_truth": instance.ground_truth,
            "prediction": prediction.decision,
            "confidence": prediction.confidence,
            "reason": prediction.reason,
            "latency_ms": prediction.latency_ms
        })
    
    # Critical: Compute UAR before anything else
    unsafe_attempts = [r for r in results if r["ground_truth"] in [CLASS_I_SAFETY, CLASS_K_MALICIOUS]]
    unsafe_acceptances = [r for r in unsafe_attempts if r["prediction"] == "ACCEPT"]
    uar = len(unsafe_acceptances) / len(unsafe_attempts)
    
    if uar > 0:
        raise CriticalSafetyFailure(f"UAR = {uar}. HYPOTHESIS FALSIFIED.")
    
    return compute_metrics(results)
```

### 3.2 Latency Measurement

- Measure wall-clock time from CapabilityDiscoverRequest to final ACCEPT/REJECT decision
- 100 repetitions per test case
- Report: P50, P95, P99
- Separate reporting for:
  - Safety gate latency (stages 3-4 only)
  - Full pipeline latency (all stages)
  - Warm cache vs. cold cache

### 3.3 Reproducibility

- All benchmark data published as JSON files (no model-specific format)
- All ground truth labels published separately from test data
- AURA and all baselines evaluated on identical data
- Random seed fixed for any stochastic components
- Results table includes standard deviation and 95% CI

---

## 4. Experiment Control Conditions

### What Is Controlled
- Benchmark dataset: fixed, versioned
- Ground truth: established before experiments
- Baselines: identical input format to AURA
- Evaluation metrics: fixed, computed from same script for all methods

### What Is Not Controlled (Acknowledged)
- Embedding model quality — depends on training data
- Ontology completeness — partial ontology reduces effectiveness for Class B
- Network conditions — provenance check latency varies with OCSP response time

---

*Proceed to [17_prototype_architecture.md] for MVP prototype design.*
