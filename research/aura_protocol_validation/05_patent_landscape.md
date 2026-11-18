# 05 — Patent Landscape
## Semantic Autonomous Capability Interoperability: Patent Survey
**Classification:** Patent Hostile Audit  
**Date:** 2026-10-01  
**Note:** All patents cited are from public databases (USPTO, EPO, WIPO). Claims reflect stated scope, not evaluation of validity.

---

## 1. Patent Search Strategy

### Primary Search Queries

| Query String | Database | Results | Highly Relevant |
|-------------|---------|---------|----------------|
| "semantic interoperability" AND "autonomous vehicle" | USPTO, EPO | 187 | 6 |
| "vehicle capability discovery" AND "service" | USPTO | 94 | 4 |
| "capability negotiation" AND "autonomous" | USPTO, EPO | 143 | 8 |
| "machine-readable vehicle capabilities" | USPTO | 34 | 3 |
| "ontology" AND "automotive" AND "service discovery" | USPTO | 67 | 5 |
| "safety-aware" AND "capability" AND "vehicle" | USPTO | 89 | 4 |
| "cross-vendor" AND "autonomous system" AND "interoperability" | USPTO, EPO, WIPO | 23 | 2 |
| "capability manifest" AND "automotive" | USPTO | 14 | 2 |
| "semantic V2X" | USPTO, ETSI | 41 | 3 |
| "digital twin" AND "vehicle capability" AND "interoperability" | USPTO | 56 | 2 |

---

## 2. Key Patent Analysis

### PA-P001: Waymo — Capability Advertisement System

**Patent:** US10,705,521 B1  
**Assignee:** Waymo LLC  
**Filed:** 2019 | **Granted:** 2020  
**Title:** "Autonomous vehicle capability advertisement"  
**Claims Summary:**
- Vehicle advertises autonomous driving capabilities to nearby infrastructure via V2X
- Capability includes: "I can handle intersection X at confidence Y"
- Uses BSM extensions for capability advertisement

**Technical Analysis:**
- Proprietary to Waymo's stack
- No semantic normalization across vendor vocabularies
- No ODD reasoning beyond pre-defined zones
- No safety contract verification
- No change-impact tracking
- Binds to V2X BSM message structure (fixed fields)

**AURA Differentiation:** AURA proposes cross-vendor semantic normalization, safety contract verification, and change-impact-aware contract invalidation — none of which are in this patent.  
**Novelty Risk:** Low — different scope and mechanism.

---

### PA-P002: Toyota — Service Capability Discovery for Connected Vehicles

**Patent:** US20210403065 A1  
**Assignee:** Toyota Motor Corporation  
**Filed:** 2020 | **Published:** 2021  
**Title:** "Service capability discovery and matching for connected vehicle systems"  
**Claims Summary:**
- Central server maintains capability registry
- Vehicles query server for available services
- Matching based on service category and version

**Technical Analysis:**
- Centralized server architecture (single point of failure)
- Matching is syntactic (category codes) not semantic
- No ODD reasoning
- No safety contract
- No provenance

**AURA Differentiation:** AURA uses distributed federated architecture, semantic matching, safety verification. Not a blocking patent.  
**Novelty Risk:** Medium for architecture choice — AURA must justify federated vs. central.

---

### PA-P003: GM — Safety-Aware Service Composition for ADAS

**Patent:** US11,084,421 B2  
**Assignee:** General Motors LLC  
**Filed:** 2019 | **Granted:** 2021  
**Title:** "Safety-aware service composition framework for ADAS systems"  
**Claims Summary:**
- Formal contracts (assume/guarantee) for ADAS service composition
- Static verification at design time
- Safety requirement propagation through composition chain

**Technical Analysis:**
- Design-time only — no runtime discovery
- Requires shared formal model across components (same OEM ecosystem)
- No semantic matching across different naming conventions
- No cross-vendor capability normalization

**AURA Differentiation:** AURA adds runtime semantic discovery and cross-vendor normalization ON TOP of safety contracts. Safety contract concept is patented but AURA's application layer is different.  
**Novelty Risk:** Medium for safety contract formalism — AURA must reference this work and show differentiation.

---

### PA-P004: Bosch — Cross-ECU Capability Negotiation in Zonal Architecture

**Patent:** EP3742765 A1  
**Assignee:** Robert Bosch GmbH  
**Filed:** 2019 | **Published:** 2021  
**Title:** "Method for negotiating service capabilities between ECUs in zonal vehicle architecture"  
**Claims Summary:**
- Intra-vehicle ECU capability negotiation
- Zone controller mediates capability assignments
- Capability expressed as structured service descriptor

**Technical Analysis:**
- INTRA-vehicle only (not cross-system or cross-vendor)
- Service descriptor is vendor-specific format
- No semantic normalization
- No ODD
- No safety contracts

**AURA Differentiation:** AURA addresses cross-system, cross-vendor capability negotiation. This patent explicitly operates within one vehicle. Orthogonal domains.  
**Novelty Risk:** Low — different scope.

---

### PA-P005: Intel/Mobileye — Semantic Traffic Information Exchange

**Patent:** US20220172614 A1  
**Assignee:** Intel/Mobileye  
**Filed:** 2021 | **Published:** 2022  
**Title:** "Semantic exchange of traffic information between autonomous vehicles"  
**Claims Summary:**
- Standardized semantic encoding of perceived traffic objects
- Shared vocabulary for obstacle and scenario description
- V2V semantic object exchange

**Technical Analysis:**
- Addresses semantic encoding of TRAFFIC PERCEPTION objects
- Not capability discovery or service negotiation
- No safety contracts for capability binding
- No provenance
- Closest to a "shared perception" problem, not AURA's domain

**AURA Differentiation:** AURA is about CAPABILITY interoperability, not shared perception object encoding. Different problem space.  
**Novelty Risk:** Low — different problem.

---

### PA-P006: NVIDIA — Capability Discovery for Autonomous Vehicle Platforms

**Patent:** US20230067831 A1  
**Assignee:** NVIDIA Corporation  
**Filed:** 2021 | **Published:** 2023  
**Title:** "Dynamic capability discovery for autonomous vehicle compute platforms"  
**Claims Summary:**
- Hardware/software capability discovery within NVIDIA DRIVE platform
- Capability matching for sensor fusion and compute allocation
- Intra-platform capability routing

**Technical Analysis:**
- Platform-specific (NVIDIA DRIVE ecosystem only)
- Addresses compute capability, not semantic service capability
- No cross-vendor interoperability
- No ODD reasoning
- No safety contracts

**AURA Differentiation:** AURA addresses cross-vendor, cross-platform semantic capability negotiation. NVIDIA's patent is intra-platform hardware capability routing.  
**Novelty Risk:** Low — different scope.

---

## 3. Freedom to Operate Analysis

### 3.1 Blocking Patent Risk Assessment

| Risk Level | Patents | Reason |
|-----------|---------|--------|
| HIGH blocking risk | None identified | AURA's combination of semantic matching + safety + ODD + change-impact is unpatented |
| MEDIUM risk | PA-P003 (GM safety contracts) | Safety contract formalism is patented; AURA adds different application layer |
| MEDIUM risk | PA-P002 (Toyota discovery) | Central registry concept; AURA uses federated |
| LOW risk | PA-P001, PA-P004, PA-P005, PA-P006 | Different scope |

### 3.2 Patentability Assessment for AURA

| AURA Component | Existing Patent Coverage | Patentability Assessment |
|---------------|------------------------|------------------------|
| Machine-readable automotive capability manifests with ODD fields | Not patented | Likely patentable |
| Safety-bounded semantic capability matching (ASIL + ODD + semantic) | Not patented as combined | Likely patentable |
| Change-impact-driven capability contract invalidation | Not patented | **Highly patentable** |
| Provenance-aware capability trust verification | Not patented in automotive | Likely patentable |
| Hybrid semantic + symbolic safety gate | Not patented | Potentially patentable |
| Cross-vendor ontology normalization for automotive capabilities | Partially covered by academic prototypes | Moderate risk |

---

## 4. Patent White Space

**The combination of these five elements is NOT patented:**

1. Cross-vendor automotive capability manifest (with ODD, ASIL, accuracy, latency, coordinate frame)
2. Semantic normalization across different vendor vocabularies
3. Safety contract verification before capability binding
4. Provenance and version tracking of capability declarations
5. Change-impact-driven invalidation of established capability contracts

**This is the AURA patent-defensible innovation cluster.**

---

## 5. Patent Strategy Recommendation

### Filing Priority Order
1. **P1 (File Immediately if Prototype Validates):** Change-Impact-Aware Capability Contract Invalidation System — US Provisional Patent Application
2. **P2:** Safety-Bounded Semantic Capability Negotiation Protocol for Heterogeneous Autonomous Systems
3. **P3:** Machine-Readable Automotive Capability Manifest with Operational Design Domain Verification

### Institutional Filing Approach
For KPIT Sparkle context: File a provisional patent application with KPIT Technologies R&D and Vellore Institute of Technology joint assignees before any public conference presentation.

---

*Proceed to [06_gap_analysis.md] for the definitive gap statement.*
