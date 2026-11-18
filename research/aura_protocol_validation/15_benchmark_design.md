# 15 — Benchmark Design
## Formal Benchmark for AURA Semantic Interoperability Hypothesis
**Classification:** Experimental Design  
**Date:** 2026-10-01

---

## 1. Benchmark Objectives

The benchmark must:
1. **Prove or disprove** that AURA semantic matching can correctly classify capability compatibility
2. **Measure** accuracy, safety (UAR=0), and latency
3. **Compare** against baselines with statistical rigor
4. **Be reproducible** by independent researchers without access to AURA internals

---

## 2. Benchmark Dataset Classes

Each class is a distinct compatibility scenario with a ground truth label.

---

### CLASS A — Exact Semantic Match

**Description:** Request and provider use identical semantic type, identical units, identical coordinate frame, compatible ODD, compatible safety class.  
**Ground Truth:** ACCEPT  
**AURA Challenge:** Should be trivial. Validates basic pipeline correctness.  
**Example:**
- Request: "PedestrianDetection, ASIL-B, urban, 0.3m accuracy, ENU, meters, CLEAR|RAIN, 60 instances"
- Provider: "PedestrianDetection, ASIL-B, urban, 0.25m accuracy, ENU, meters, CLEAR|RAIN|FOG"
- Ground Truth: ACCEPT

---

### CLASS B — Synonym/Vocabulary Mismatch

**Description:** Request and provider refer to same capability with different names from different vendor vocabularies. All other attributes compatible.  
**Ground Truth:** ACCEPT  
**AURA Challenge:** Semantic matching must bridge vocabulary gap without human intervention.  
**Examples:**
- "ForwardObjectDetection" ↔ "FrontObstaclePerception" ↔ "RoadObjectTracking" → ACCEPT (same concept)
- "EmergencyBraking" ↔ "AutomaticEmergencyStop" ↔ "CollisionMitigation" → ACCEPT
- "LaneDepartureWarning" ↔ "LaneKeepingAssist" → REJECT (different capabilities — warning vs. control)

---

### CLASS C — Unit Mismatch (Resolvable)

**Description:** Identical capability, compatible ODD and safety, but different units. Conversion exists and introduces acceptable error.  
**Ground Truth:** ACCEPT (after unit conversion)  
**AURA Challenge:** Unit normalization layer must resolve and verify accuracy is preserved.  
**Example:**
- Request: "SpeedMeasurement, accuracy ≤ 0.1 m/s"
- Provider: "SpeedMeasurement, accuracy 0.08 m/s in km/h"
- Ground Truth: ACCEPT (km/h to m/s is lossless)

**Class C-Negative:** Unit conversion exists but introduces error exceeding accuracy bound → REJECT

---

### CLASS D — Coordinate Frame Mismatch (Resolvable)

**Description:** Identical capability, different coordinate frame. Transform exists with acceptable accuracy cost.  
**Ground Truth:** ACCEPT (after frame transform)  
**Example:**
- Request: "ObjectPosition, ENU frame, accuracy ≤ 0.5m"
- Provider: "ObjectPosition, WGS84, accuracy 0.3m at source"
- Transform ENU→WGS84 at typical location introduces error ≤ 0.02m
- Ground Truth: ACCEPT

**Class D-Negative:** Coordinate frame transform introduces error exceeding accuracy bound → REJECT

---

### CLASS E — Different Ontology

**Description:** Provider and requester are using capabilities from ontologically distinct domains that happen to sound similar.  
**Ground Truth:** REJECT  
**AURA Challenge:** Semantic matching must identify ontological incompatibility, not just name similarity.  
**Example:**
- Request: "ObjectDetection" (autonomy domain: 3D physical object in road scene)
- Provider: "ObjectDetection" (database domain: record retrieval from object store)
- Ground Truth: REJECT (homonymous terms from different domains)

---

### CLASS F — Different Middleware (Transport Binding)

**Description:** Same semantic capability but incompatible transport bindings. AURA must determine if middleware bridge is available.  
**Ground Truth:** ACCEPT if middleware adapter exists, REJECT if not  
**Example:**
- Request: "LiDAR_PointCloud via ROS2 topic /points"
- Provider: "LiDAR_PointCloud via DDS topic lidar.points"
- If ROS2↔DDS bridge deployed: ACCEPT with bridge annotation
- If no bridge: REVIEW_REQUIRED (not REJECT — bridge may be creatable)

---

### CLASS G — Different Software Architecture

**Description:** Request and provider implement the same functional capability but with different internal architectures (modular vs monolithic). AURA should care about the external interface, not internal architecture.  
**Ground Truth:** ACCEPT if external interface is compatible  
**Example:**
- Request: "TrafficSignRecognition, 50ms latency"
- Provider A: CNN-based, 45ms latency, same output format
- Provider B: Rule-based, 42ms latency, same output format
- Ground Truth: Both ACCEPT (architecture is irrelevant to AURA)

---

### CLASS H — Context (ODD) Mismatch

**Description:** Semantically identical capability but provider's ODD does not cover requester's current operating environment.  
**Ground Truth:** REJECT  
**Example:**
- Request: "PedestrianDetection, current_env=FOG_HEAVY, speed=40kph"
- Provider: ODD = {CLEAR, LIGHT_RAIN, max_speed=60kph}
- Ground Truth: REJECT (FOG_HEAVY not in provider ODD)

**Class H-Marginal:** Provider ODD covers 80% of requester context → REVIEW_REQUIRED

---

### CLASS I — Safety Mismatch

**Description:** Semantically compatible capability but provider's safety class is insufficient for requester's requirement.  
**Ground Truth:** REJECT (HARD gate — no exceptions)  
**Example:**
- Request: "AutomaticEmergencyBraking, required ASIL-D"
- Provider: "AutomaticEmergencyBraking, declared ASIL-B"
- Ground Truth: REJECT (ASIL-B < ASIL-D, regardless of other attributes)

---

### CLASS J — Stale Capability

**Description:** Capability contract is temporally expired or the provider's software has changed since contract was published.  
**Ground Truth:** REJECT (expired) or REVIEW_REQUIRED (software changed)  
**Example:**
- Provider: Capability published 2024-01-01, valid_until=2024-06-30
- Current date: 2024-07-15
- Ground Truth: REJECT (expired)

---

### CLASS K — Malicious Capability

**Description:** Adversarially crafted capability contract designed to fool AURA into accepting an incompatible provider.  
**Sub-classes:**
- K1: Signature invalid → REJECT
- K2: Certificate revoked → REJECT
- K3: Declared ASIL-D but unit mismatch in output → REJECT (I gate)
- K4: Semantic embedding crafted to maximize cosine similarity to target while being ontologically incompatible → REJECT (S gate — ontology check)
- K5: Replay of valid but expired contract → REJECT (P gate)

**Ground Truth:** All Class K → REJECT  
**UAR Constraint:** UAR for Class K = 0 is a hard requirement.

---

### CLASS L — Ambiguous Capability

**Description:** Capability name is genuinely ambiguous between multiple possible semantic meanings. AURA should route to human review, not make an autonomous decision.  
**Ground Truth:** REVIEW_REQUIRED  
**Example:**
- Request: "Tracking" (could mean: object tracking in scene, GPS tracking, fleet tracking)
- Provider: "Tracking, module: SensorFusion"
- Ground Truth: REVIEW_REQUIRED (ambiguity)

---

### CLASS M — Out-of-Distribution (OOD) Capability

**Description:** Provider advertises a capability type that does not appear in the automotive capability ontology and has not been seen in training data.  
**Ground Truth:** REVIEW_REQUIRED (not REJECT — the capability may be valid but unrecognized)  
**Example:**
- Provider: "QuantumRadar_3D" (novel technology not in ontology)
- Ground Truth: REVIEW_REQUIRED (AURA cannot verify compatibility with unknown type)

---

### CLASS N — Conflicting Providers

**Description:** Multiple providers offer the same semantic capability with incompatible attributes (different accuracy, latency, ODD).  
**Ground Truth:** Consumer must choose; AURA provides ranked list with explanations  
**Example:**
- Provider A: PedestrianDetection, 0.2m, 50ms, ASIL-C
- Provider B: PedestrianDetection, 0.4m, 30ms, ASIL-B
- Consumer needs: 0.3m accuracy, 60ms budget, ASIL-B minimum
- Ground Truth: Provider A ACCEPT (0.2m < 0.3m, 50ms < 60ms, ASIL-C ≥ ASIL-B), Provider B REJECT (0.4m > 0.3m)

---

## 3. Benchmark Dataset Size

| Class | Instances | Train Split | Test Split |
|-------|-----------|------------|-----------|
| A (Exact) | 200 | 70% | 30% |
| B (Synonym) | 200 | 70% | 30% |
| C (Unit) | 150 | 70% | 30% |
| D (Frame) | 100 | 70% | 30% |
| E (Wrong Ontology) | 150 | 70% | 30% |
| F (Middleware) | 100 | 70% | 30% |
| G (Architecture) | 100 | 70% | 30% |
| H (ODD) | 200 | 70% | 30% |
| I (Safety) | 200 | 70% | 30% |
| J (Stale) | 150 | 70% | 30% |
| K (Malicious) | 200 | 70% | 30% |
| L (Ambiguous) | 100 | 70% | 30% |
| M (OOD) | 100 | 70% | 30% |
| N (Conflicting) | 100 | 70% | 30% |
| **TOTAL** | **1,850** | **1,295** | **555** |

---

## 4. Baselines for Comparison

| Baseline | Method | Purpose |
|---------|--------|---------|
| B0 | Exact string match | Lower bound |
| B1 | Keyword/TF-IDF similarity | Keyword baseline |
| B2 | Raw sentence embeddings (SentenceTransformer) | Embedding baseline |
| B3 | Contextual embeddings (BGE-M3, current AURA) | Extended AURA baseline |
| B4 | OWL ontology reasoning only | Symbolic baseline |
| B5 | LLM semantic matching (GPT-4) | LLM baseline |
| B6 | AURA Hybrid (proposed, full pipeline) | Full AURA |

---

## 5. Evaluation Metrics

### Per-Class Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Precision | TP / (TP + FP) | > 90% |
| Recall | TP / (TP + FN) | > 85% |
| F1 | 2 × P × R / (P + R) | > 87% |
| UAR | FP_unsafe / total_unsafe | **= 0** |
| SAR | TP / total_compatible | > 85% |
| FRR | FN / total_compatible | < 15% |
| Review Rate | REVIEW / total_requests | < 10% |

### Latency Metrics

| Metric | Target |
|--------|--------|
| P50 latency (session establishment) | < 100ms |
| P99 latency | < 500ms |
| Safety gate latency | < 5ms |
| Cold start (cold ontology cache) | < 2s |

### Safety Metrics (Primary)

```
UAR = 0 is a BINARY requirement, not a target.
If UAR > 0 in ANY test run: hypothesis is NOT confirmed.
```

---

## 6. Ground Truth Methodology

Ground truth is established by:
1. Expert panel of 3 automotive software engineers independently classify each instance
2. Consensus required — disagreements flagged for adjudication
3. Majority rule (2/3) for ambiguous cases
4. Adversarial instances (Class K) validated by security engineer
5. All ground truth decisions are documented with reasoning (not just label)

**Ground truth must be established before AURA results are generated.** No post-hoc adjustment of ground truth.

---

## 7. What Would Falsify The Hypothesis

```
HYPOTHESIS FALSIFIED IF:
  (a) UAR > 0 for any Class K (malicious) instance
  (b) UAR > 0 for any Class I (safety mismatch) instance
  (c) Recall (Class B synonym) < 60% (semantic matching fails on basic synonyms)
  (d) F1 < 70% across all classes combined
  (e) P99 latency > 5s (too slow for session establishment)
  (f) AURA fails to outperform B2 (raw embeddings) on Classes H, I (requires deterministic checking advantage)
```

---

*Proceed to [16_experimental_protocol.md] for execution methodology.*
