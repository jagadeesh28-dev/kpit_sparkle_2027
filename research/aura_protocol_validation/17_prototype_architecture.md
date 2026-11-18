# 17 — Prototype Architecture
## AURA Semantic Gateway: MVP Design and Component Specification
**Classification:** Prototype Engineering Specification  
**Date:** 2026-10-01

---

## 1. MVP Scope Decision

**What IS in the MVP:**
- Capability contract parsing and validation
- Semantic matching pipeline (Stages 1-4)
- Deterministic safety gate (Stage 4 — hard gate)
- Provenance verification (Stage 5) — simplified (no HSM, no OCSP, use test PKI)
- Change-impact engine (Stage 6) — integrated with AURA-Impact graph engine
- Audit log
- Three-system synthetic testbed (Systems A, B, C from experiment protocol)
- CLI interface for demonstration

**What IS NOT in the MVP:**
- Real PKI infrastructure (HSM, production CA)
- Standardized automotive capability ontology (use prototype vocabulary)
- Real V2X or SOME/IP transport integration (simulated)
- Production-grade security (research prototype)
- ASIL-B software certification

---

## 2. Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      AURA SEMANTIC GATEWAY MVP                           │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                    AURA Gateway Core                                  ││
│  │                                                                       ││
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ││
│  │  │ 1. Capability    │  │ 2. Semantic       │  │ 3. Context       │  ││
│  │  │    Manifest      │→ │    Normalizer     │→ │    Engine        │  ││
│  │  │    Parser        │  │                   │  │                   │  ││
│  │  └──────────────────┘  └──────────────────┘  └────────┬─────────┘  ││
│  │                                                          │            ││
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌────────▼─────────┐  ││
│  │  │ 6. Change-Impact │  │ 5. Provenance    │  │ 4. Safety Gate   │  ││
│  │  │    Engine        │← │    Verifier       │← │    (HARD GATE)  │  ││
│  │  └────────┬─────────┘  └──────────────────┘  └──────────────────┘  ││
│  │           │                                                            ││
│  │  ┌────────▼─────────┐  ┌──────────────────┐  ┌──────────────────┐  ││
│  │  │ 7. Compatibility │  │ 8. Negotiation   │  │ 9. Middleware    │  ││
│  │  │    Engine        │→ │    Manager        │→ │    Adapter       │  ││
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  ││
│  │                                                                       ││
│  │  ┌─────────────────────────────────────────────────────────────────┐││
│  │  │                      10. Audit Log                               │││
│  │  └─────────────────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────────────┐│
│  │  Capability │  │  Automotive │  │  AURA-Impact Graph Engine        ││
│  │  Manifest   │  │  Capability │  │  (existing — reused for          ││
│  │  Registry   │  │  Ontology   │  │   change-impact detection)       ││
│  └─────────────┘  └─────────────┘  └──────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Specifications

### Component 1: Capability Manifest Parser

**Input:** Raw JSON/YAML capability contract  
**Output:** Parsed, validated CapabilityContract Python object  
**Behavior:**
- Validate schema (JSON Schema validation)
- Check mandatory fields are present
- Parse units, coordinate frames, ASIL classes into typed enumerations
- Verify internal consistency (e.g., valid_from < valid_until)
- Fail fast on malformed contracts with descriptive errors

**Implementation:** Python dataclass with Pydantic validation

```python
from pydantic import BaseModel, validator
from typing import List, Optional
from enum import Enum

class ASILClass(str, Enum):
    QM = "QM"; A = "ASIL_A"; B = "ASIL_B"; C = "ASIL_C"; D = "ASIL_D"

class ODD(BaseModel):
    domain_types: List[str]
    speed_range_ms: dict  # {min: float, max: float}
    weather_conditions: List[str]
    time_of_day: List[str]

class Safety(BaseModel):
    classification: ASILClass
    integrity_level_standard: str
    fail_safe_behavior: str

class CapabilityContract(BaseModel):
    capability_id: str
    semantic_type: str  # URI or name for prototype
    provider_id: str
    interface_binding: dict
    outputs: List[dict]
    quality: dict
    odd: ODD
    safety: Safety
    trust: dict
    provenance: dict
    change_impact: Optional[dict] = None
```

---

### Component 2: Semantic Normalizer

**Input:** Raw CapabilityContract  
**Output:** Normalized CapabilityContract (canonical units, canonical frame)

**Unit Normalization:**
```python
UNIT_CONVERTERS = {
    ("cm", "m"): lambda x: x / 100,
    ("mm", "m"): lambda x: x / 1000,
    ("km/h", "m/s"): lambda x: x / 3.6,
    ("mph", "m/s"): lambda x: x * 0.44704,
    ("deg", "rad"): lambda x: x * pi / 180,
    # ... comprehensive unit registry
}

def normalize_units(contract: CapabilityContract) -> CapabilityContract:
    for output in contract.outputs:
        canonical_unit = "m"  # or "m/s", "rad" etc by parameter type
        if output.units != canonical_unit:
            converter = UNIT_CONVERTERS.get((output.units, canonical_unit))
            if converter is None:
                raise UnitConversionError(f"No converter: {output.units} → {canonical_unit}")
            output.accuracy = converter(output.accuracy)
            output.units = canonical_unit
    return contract
```

**Coordinate Frame Normalization:**
- Canonical frame: ENU (East-North-Up)
- Transforms: WGS84→ENU (via local tangent plane), vehicle-local→ENU (requires vehicle pose)
- If vehicle pose unavailable: flag as REVIEW_REQUIRED, not REJECT

---

### Component 3: Context Engine (ODD Checker)

**Input:** Normalized contract + current consumer context  
**Output:** ODD_PASS or ODD_FAIL with reason

```python
def check_odd_compatibility(contract: CapabilityContract, 
                             consumer_context: ConsumerContext) -> ODDResult:
    
    checks = {
        "domain": consumer_context.domain in contract.odd.domain_types,
        "speed": (contract.odd.speed_range_ms["min"] <= 
                  consumer_context.speed_ms <= 
                  contract.odd.speed_range_ms["max"]),
        "weather": consumer_context.weather in contract.odd.weather_conditions,
        "time_of_day": consumer_context.time_of_day in contract.odd.time_of_day,
    }
    
    failed = {k: v for k, v in checks.items() if not v}
    
    if not failed:
        return ODDResult(status=ODDStatus.PASS)
    else:
        return ODDResult(status=ODDStatus.FAIL, reasons=failed)
```

---

### Component 4: Safety Gate (Hard Gate)

**This component is the most critical. No bypass path.**

```python
ASIL_LEVELS = {"QM": 0, "ASIL_A": 1, "ASIL_B": 2, "ASIL_C": 3, "ASIL_D": 4}

def safety_gate(contract: CapabilityContract, 
                required_safety: SafetyRequirement) -> SafetyResult:
    
    # Standard must match or be in approved cross-standard mapping
    if contract.safety.integrity_level_standard != required_safety.standard:
        if not is_approved_cross_standard(contract.safety.integrity_level_standard,
                                          required_safety.standard):
            return SafetyResult(
                status=SafetyStatus.REJECT,
                reason=f"Cross-standard mapping {contract.safety.integrity_level_standard} "
                       f"↔ {required_safety.standard} not approved"
            )
    
    # ASIL level must be sufficient
    if ASIL_LEVELS[contract.safety.classification] < ASIL_LEVELS[required_safety.required_asil]:
        return SafetyResult(
            status=SafetyStatus.REJECT,
            reason=f"Insufficient ASIL: {contract.safety.classification} < {required_safety.required_asil}"
        )
    
    # Fail-safe behavior must be acceptable
    if contract.safety.fail_safe_behavior not in required_safety.acceptable_fail_modes:
        return SafetyResult(
            status=SafetyStatus.REJECT,
            reason=f"Fail-safe behavior {contract.safety.fail_safe_behavior} not acceptable"
        )
    
    return SafetyResult(status=SafetyStatus.PASS)
    
# NO EXCEPTION HANDLING THAT SWALLOWS ERRORS
# ANY EXCEPTION IN SAFETY GATE → REJECT
```

---

### Component 5: Provenance Verifier

**Input:** Contract, current timestamp  
**Output:** TRUST_PASS or TRUST_FAIL

For prototype:
- Certificate verification: use test PKI (self-signed CA)
- Signature: Ed25519 signatures on contract JSON
- Revocation: in-memory revocation list (not OCSP for prototype)
- Freshness: timestamp comparison

---

### Component 6: Change-Impact Engine (AURA-Impact Integration)

**This is the direct connection to the existing AURA-Impact engine.**

```python
class ChangeImpactEngine:
    """
    Wraps the existing AURA-Impact dependency graph engine.
    Monitors providers for software changes and triggers invalidations.
    """
    
    def __init__(self, aura_impact_graph):
        self.graph = aura_impact_graph
        self.bindings = {}  # binding_id → (contract, consumer_webhook)
    
    def register_binding(self, binding_id, contract, consumer_webhook):
        self.bindings[binding_id] = {
            "contract": contract,
            "consumer_webhook": consumer_webhook,
            "baseline_graph_hash": self._get_current_graph_hash(contract.provider_id)
        }
    
    def check_for_changes(self, binding_id):
        """Called periodically by monitoring loop."""
        binding = self.bindings[binding_id]
        current_hash = self._get_current_graph_hash(binding["contract"].provider_id)
        
        if current_hash != binding["baseline_graph_hash"]:
            # Provider software has changed — analyze impact
            impact = self.graph.analyze_change_impact(
                provider=binding["contract"].provider_id,
                capability=binding["contract"].capability_id
            )
            
            if impact.severity >= ImpactSeverity.MEDIUM:
                self._send_invalidation_notice(binding_id, impact)
    
    def _send_invalidation_notice(self, binding_id, impact):
        """Send webhook notification to consumer."""
        notice = CapabilityInvalidationNotice(
            binding_id=binding_id,
            reason="PROVIDER_SOFTWARE_CHANGE",
            impact_severity=impact.severity,
            changed_artifacts=impact.affected_artifacts
        )
        # POST to consumer_webhook
        requests.post(self.bindings[binding_id]["consumer_webhook"], json=notice.dict())
```

---

## 4. Full Protocol Demonstration

**Example invocation:**

```
$ python aura_gateway.py negotiate \
    --request examples/consumer_request.json \
    --providers sys-a,sys-b,sys-c \
    --consumer-context '{"domain":"URBAN","speed_ms":3.0,"weather":"CLEAR","time":"DAY"}'

=== AURA SEMANTIC GATEWAY v1.0 ===

Processing request: PedestrianDetection (ASIL-B, 0.3m accuracy, urban)

Provider sys-a (ForwardObjectDetection):
  [✓] Semantic match: 0.91 (ontology: PedestrianDetection ⊑ ObjectDetection)
  [✓] Context/ODD: URBAN ✓, speed 3.0 ≤ 16.7 ✓, CLEAR ✓, DAY ✓
  [→] Unit conversion: 25cm → 0.25m ✓ (accuracy preserved)
  [→] Frame conversion: vehicle-local → ENU (error <0.01m ✓)
  [✓] Safety: ASIL-B ≥ ASIL-B ✓
  [✓] Provenance: sig valid, cert valid, not expired
  [✓] Change impact: dep_graph_hash unchanged
  DECISION: ACCEPT
  Compatibility score: 0.94

Provider sys-b (FrontObstaclePerception):
  [✓] Semantic match: 0.89 (synonym resolved via ontology)
  [✓] Context/ODD: URBAN ✓, speed ✓, CLEAR ✓, DAY ✓
  [✗] Safety gate: QM < ASIL-B required
  DECISION: REJECT
  Reason: SAFETY_CLASS_INSUFFICIENT (QM < ASIL_B)

Provider sys-c (RoadObjectTracking):
  [✓] Semantic match: 0.82
  [✓] Context/ODD: URBAN ✓
  [→] Unit conversion: 300mm → 0.30m ✓
  [→] Frame: WGS84 → ENU ✓
  [?] Safety: SIL-2 ↔ ASIL-B: cross-standard mapping not pre-approved
  DECISION: REVIEW_REQUIRED
  Reason: CROSS_STANDARD_SAFETY_APPROVAL_NEEDED

=== RECOMMENDATION ===
Bind to: sys-a (ForwardObjectDetection)
Binding ID: binding-uuid-001
Monitor: change-impact webhook registered
```

---

## 5. MVP Deliverable Checklist

| Component | Status | Implementation |
|-----------|--------|---------------|
| Capability manifest schema | ✅ Design complete | Pydantic model |
| Semantic normalizer | ✅ Design complete | Unit + frame converters |
| Context (ODD) engine | ✅ Design complete | Deterministic checks |
| Safety gate | ✅ Design complete | ASIL table lookup |
| Provenance verifier | ✅ Design complete | Test PKI + Ed25519 |
| Change-impact engine | ✅ Design complete | AURA-Impact integration |
| Compatibility scorer | ✅ Design complete | Weighted combination |
| Negotiation manager | ✅ Design complete | 3-round protocol |
| Audit log | ✅ Design complete | Append-only JSON log |
| CLI interface | ✅ Design complete | argparse CLI |
| Three-system testbed | ✅ Design complete | Simulated providers |
| Benchmark runner | ✅ Design complete | Automated evaluation |

---

*Proceed to [18_failure_analysis.md] for hostile failure mode analysis.*
