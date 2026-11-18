# 09 — Semantic Matching Architecture
## Approach Evaluation and Engine Design
**Classification:** Technical Architecture Decision  
**Date:** 2026-10-01

---

## 1. Evaluation Framework for Matching Approaches

### 1.1 Evaluation Dimensions

| Dimension | Why It Matters |
|-----------|---------------|
| Accuracy | Core function — wrong match = system failure |
| Explainability | Safety-critical systems MUST explain decisions |
| Latency | Must fit within capability session establishment budget (~seconds) |
| Determinism | Safety systems cannot have non-deterministic outcomes |
| Hallucination Risk | LLM/embedding systems can confidently produce wrong matches |
| Adversarial Robustness | Malicious capability must not pass |
| Vendor Portability | Must work without internet access, cloud APIs |
| OOD Behavior | Novel capability names must fail SAFELY (reject, not accept) |

### 1.2 Safety-Critical Failure Mode Classification

```
Type I Error (False Acceptance — CRITICAL):
  AURA incorrectly accepts an incompatible capability as compatible.
  Impact: Potentially catastrophic — system operates on wrong capability assumptions.
  
Type II Error (False Rejection — ACCEPTABLE):
  AURA incorrectly rejects a compatible capability as incompatible.
  Impact: Requires human review. System degrades gracefully.
  
Ruling:
  A matching system MUST be calibrated to minimize Type I errors.
  Type II errors are the acceptable cost of safety.
```

---

## 2. Approach Analysis

### Approach A: Exact String Matching (Baseline)

**Method:** Match `capability_type` and interface fields by exact string equality.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 15% | "pedestrian_detection" ≠ "pedestrianDetect" ≠ "PedestrianPerception" |
| Explainability | 100% | Boolean — trivially explainable |
| Latency | <1ms | O(1) per comparison |
| Determinism | 100% | |
| Hallucination Risk | 0% | |
| Adversarial Robustness | Medium | Exact match is hard to spoof but easy to block |
| OOD Behavior | SAFE — rejects unknown | |

**Verdict:** Unacceptably low accuracy. Valid as a fast-path tier-0 check only. Not a primary matching approach.

---

### Approach B: Keyword / TF-IDF Matching

**Method:** Tokenize capability names, compute term frequency–inverse document frequency similarity.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 45% | "ForwardObjectDetection" and "FrontObstaclePerception" share tokens |
| Explainability | High | Token overlap is inspectable |
| Latency | <5ms | |
| Determinism | 100% | |
| Hallucination Risk | Low | |
| Adversarial Robustness | LOW — adversary can craft high-TF-IDF names that fool keyword system | |
| OOD Behavior | PARTIAL | |

**Verdict:** Better than exact match but too many false positives and false negatives. Cannot handle coordinate frame or unit mismatches. Baseline comparison only.

---

### Approach C: Dense Vector Embeddings (Standalone)

**Method:** Encode capability descriptions into dense vectors (SBERT, BGE-M3, etc.); use cosine similarity.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 70–80% | Strong on semantic synonyms |
| Explainability | LOW | Vector similarity not inspectable |
| Latency | 10–50ms per comparison | Depends on model size |
| Determinism | MEDIUM — floating-point, model-version dependent | |
| Hallucination Risk | HIGH | "braking_deceleration" and "steering_angle" may embed similarly in certain vector spaces |
| Adversarial Robustness | LOW | Vector spaces can be fooled by adversarial perturbations |
| OOD Behavior | DANGEROUS — OOD inputs get arbitrary similarity scores | |

**CRITICAL FAILURE MODE:** A unit-mismatch capability (m/s² vs g) may have high semantic embedding similarity but be physically incompatible. Embeddings alone cannot detect unit or coordinate-frame mismatches.

**Verdict:** Embeddings are useful for semantic synonym resolution but CANNOT be the primary safety decision mechanism. Must be combined with symbolic checking.

---

### Approach D: Symbolic Constraints (Rule-Based)

**Method:** Define formal rules: if `safety.classification == ASIL_D` and requester needs `ASIL_B`, check ISO 26262 decomposition rules.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 95%+ for defined constraint domains | |
| Explainability | 100% — rules are inspectable | |
| Latency | <1ms | Rule table lookup |
| Determinism | 100% | |
| Hallucination Risk | 0% | |
| Adversarial Robustness | HIGH for defined constraints | |
| OOD Behavior | SAFE — undefined rules → reject | |

**Limitation:** Cannot handle semantic synonym matching. Requires pre-defined rule sets for every constraint type. Does not generalize to novel capability types.

**Verdict:** Mandatory for safety, units, coordinate frame, and ODD checking. Cannot substitute for semantic matching.

---

### Approach E: Ontology Reasoning (OWL-DL)

**Method:** Express capabilities in OWL ontology; use description logic reasoners (HermiT, Pellet, FaCT++) for subsumption checking.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 85–95% for well-populated ontology | |
| Explainability | HIGH — reasoning trace available | |
| Latency | 50–500ms for complex ontologies | Benchmark: HermiT reasoner |
| Determinism | 100% — description logic is decidable | |
| Hallucination Risk | 0% | |
| Adversarial Robustness | HIGH for ontology attacks, LOW for ontology gap attacks | |
| OOD Behavior | SAFE — unknown terms rejected as unclassified | |

**Limitation:** Ontology must be maintained and kept current. OWL reasoning latency can be prohibitive for large ontologies. Requires shared automotive capability ontology (which does not yet exist as standard).

**Verdict:** Excellent for structured domain where shared ontology exists. The **automotive capability ontology must be developed** — this is itself a research contribution. Viable for Phase 2 implementation.

---

### Approach F: Knowledge Graph Matching

**Method:** Build knowledge graph of automotive capabilities; use graph traversal and GNN-based similarity for matching.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 80–90% with sufficient training data | |
| Explainability | MEDIUM — graph paths are inspectable | |
| Latency | 20–100ms | |
| Determinism | LOW — learned weights | |
| Hallucination Risk | MEDIUM | |
| OOD Behavior | UNSAFE if graph boundary is not enforced | |

**Verdict:** Useful for multi-hop reasoning (e.g., "emergency braking" subsumes "automatic braking" which subsumes "deceleration control"). Requires training data. Not appropriate as a safety decision mechanism without symbolic gates.

---

### Approach G: LLM-Based Semantic Translation

**Method:** Use a Large Language Model (e.g., GPT-4, Gemini) to determine if two capabilities are semantically equivalent.

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | Appears high — ~85-90% in controlled tests | |
| Explainability | LOW — reasoning is opaque | |
| Latency | 500ms–3000ms (API call) | |
| Determinism | NO — stochastic | |
| Hallucination Risk | CRITICAL — LLMs confidently hallucinate equivalences | |
| Adversarial Robustness | LOW — prompt injection is trivial | |
| OOD Behavior | DANGEROUS — LLMs do not know when to say "I don't know" reliably | |
| Vendor Portability | NONE — requires cloud API or large local model | |

**CRITICAL FINDING:** LLM-based matching MUST NOT be used as a safety decision mechanism in autonomous systems. ISO 26262 requires verifiable, deterministic behavior for ASIL-B and above. Stochastic LLMs are fundamentally incompatible with this requirement.

**Verdict:** LLMs may be used as a pre-processing step for ontology population (generating initial semantic mappings that humans validate). They MUST NOT make final capability binding decisions.

---

### Approach H: Hybrid Symbolic + Semantic (AURA Proposed)

**Method:** Pipeline combining dense embeddings (for semantic synonym resolution) with deterministic symbolic checking (for safety, units, ODD).

```
INPUT: Capability Request + Capability Contract

STAGE 1: Semantic Embedding Match (Fast Filter)
  ├── If cosine_similarity < threshold_low → REJECT immediately
  ├── If cosine_similarity > threshold_high → Advance to Stage 2
  └── If cosine_similarity in [low, high] → REVIEW_REQUIRED

STAGE 2: Ontology Subsumption Check
  ├── Load automotive capability ontology
  ├── Check if semantic_type_request ⊑ semantic_type_contract (subsumption)
  └── If fails → REJECT

STAGE 3: Symbolic Constraint Verification (Deterministic)
  ├── Units check: require same unit for all measurement parameters
  ├── Coordinate frame check: require same or compatible frame
  ├── ODD check: requester's context ⊆ provider's ODD
  ├── Quality check: provider.accuracy ≤ requester.required_accuracy
  ├── Latency check: provider.latency_worst_case ≤ requester.latency_budget
  └── If any fails → REJECT

STAGE 4: Safety Contract Gate (Hard Gate)
  ├── Provider safety class ≥ required safety class (per ISO 26262 decomposition rules)
  ├── Fail-safe behavior compatible with consumer's required fail mode
  └── If fails → REJECT (no exceptions)

STAGE 5: Provenance and Trust Verification
  ├── Verify cryptographic signature on contract
  ├── Check revocation status
  ├── Check validity window (valid_from ≤ now ≤ valid_until)
  └── If fails → REJECT

STAGE 6: Change Impact Check
  ├── Query AURA change impact engine for provider's last commit
  ├── Verify dependency_graph_hash unchanged
  └── If changed since contract publication → REVIEW_REQUIRED

OUTPUT:
  ACCEPT (all stages pass)
  REJECT (any deterministic stage fails)
  REVIEW_REQUIRED (embedding uncertainty OR change detected)
```

| Criterion | Score | Evidence |
|-----------|-------|---------|
| Accuracy | 85–90% expected | Combines semantic + deterministic strengths |
| Explainability | HIGH — each stage produces trace | |
| Latency | 50–200ms total (cold), 5–20ms (warm cache) | |
| Determinism | DETERMINISTIC for safety gates; probabilistic for semantic stage | |
| Hallucination Risk | LOW — deterministic gates override semantic stage | |
| Adversarial Robustness | HIGH — safety gate is not bypassable | |
| OOD Behavior | SAFE — novel inputs fail semantic stage (review) or safety gate (reject) | |

**Verdict: This is the recommended AURA matching architecture.**

---

## 3. Extension of Current AURA-Impact Engine

Current AURA-Impact uses:
- Dense contextual embeddings for semantic recovery (BGE-M3 or similar)
- Typed dependency graphs for structural matching
- Safety gate for test retention

**Extension path:**
1. The embedding component → Stage 1 of AURA Semantic Matching
2. The typed graph engine → used for dependency tracking (Change Impact Engine)
3. The safety gate → directly becomes Stage 4 (Safety Contract Gate)

The existing AURA-Impact engine provides approximately **60% of the required components.** The new components to build are:
- Automotive capability ontology (Stages 1–2)
- Symbolic constraint checking layer (Stage 3)
- Provenance verification (Stage 5)
- Change-impact webhook integration (Stage 6)

---

## 4. Automotive Capability Ontology: Design Requirements

The ontology does not exist as a standard. Its creation is a research contribution.

**Minimum vocabulary required:**
```
AutomotiveCapability (root)
├── PerceptionCapability
│   ├── ObjectDetection
│   │   ├── PedestrianDetection
│   │   ├── VehicleDetection
│   │   └── ObstacleDetection
│   ├── LaneDetection
│   └── SemanticSegmentation
├── LocalizationCapability
│   ├── GlobalLocalization (GPS/GNSS)
│   └── LocalLocalization (HD map / odometry)
├── PlanningCapability
│   ├── RoutePlanning
│   └── TrajectoryPlanning
├── ActuationCapability
│   ├── LongitudinalControl
│   └── LateralControl
└── CommunicationCapability
    ├── V2VCommunication
    └── V2ICommunication
```

**Standard to build on:** Extend COVESA VSS with OWL semantics. Use OPC UA for Robotics companion spec patterns for structure.

---

*Proceed to [10_negotiation_protocol.md] for protocol state machine design.*
