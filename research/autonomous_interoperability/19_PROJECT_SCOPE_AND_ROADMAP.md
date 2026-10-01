# 19 — PROJECT SCOPE & RESEARCH ROADMAP: RIGID STRATEGIC BOUNDARIES

**Document Reference:** `research/autonomous_interoperability/19_PROJECT_SCOPE_AND_ROADMAP.md`  
**Focus:** Strict Boundary Lines Demarcating Current Implementation, Next Prototype, Academic Research, and Future Vision  
**Author:** Lead Systems Architect & Technology Strategist  

---

## 1. The Strategic Imperative: Boundary Discipline
A frequent critique of ambitious engineering projects is the blurring of lines between what is currently working, what is being prototyped, and what is merely future speculation. To protect the scientific integrity of the AURA project, we establish **four non-negotiable scope categories**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 1: WHAT WE HAVE BUILT (CURRENT - VALIDATED BASELINE)             │
│ • Canonical AURA-Impact internal change impact & regression engine     │
│ • Validated benchmark: 63.11% recall, 82.29% reduction, 100% safety   │
│ • Working interactive Streamlit demonstrator (dashboard/app.py)        │
│ • 252 automated unit and integration tests passing (100%)              │
│ • STRICT SCOPE: Single-system software CI/CD environment               │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ [MONTHS 1 - 6]
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 2: WHAT WE CAN BUILD NEXT (NEXT - MINIMAL RESEARCH PROTOTYPE)    │
│ • Machine-readable AURA Capability Manifest schema (JSON-LD / ASN.1)   │
│ • Three-agent software emulation (AV + Delivery Pod + Smart RSU)       │
│ • Single-shot capability negotiation and Context Gate decoy rejection  │
│ • Automated 10-attack fault injection testbench                        │
│ • STRICT SCOPE: Local process / LAN emulation testbed                  │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ [MONTHS 6 - 18]
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 3: WHAT IS RESEARCH (APPLIED ACADEMIC RESEARCH)                  │
│ • Hardware-in-the-Loop (HIL) integration on Automotive Ethernet (TSN)  │
│ • Real-time latency benchmarking on NVIDIA DRIVE Orin & QNX RTOS       │
│ • Mathematical formalization of cross-system SOTIF / ASIL contracts    │
│ • Multi-vendor dynamic ontology drift alignment                        │
│ • STRICT SCOPE: Laboratory testbed with academic & Tier-1 partners     │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ [YEARS 2 - 5+]
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 4: WHAT IS FUTURE VISION (LONG-TERM INDUSTRY ADOPTION)           │
│ • International standardization via AUTOSAR Adaptive and ASAM         │
│ • Production multi-OEM commercial mobility fleet deployment            │
│ • Municipal smart city infrastructure integration                      │
│ • STRICT SCOPE: Global industrial deployment                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Explicit Negative Scope: What is STRICTLY OUT OF SCOPE

To prevent scope creep and eliminate judge confusion, we declare:
1. **NOT A NEW PHYSICAL PROTOCOL:** We do not design new radio hardware, RF transceivers, or wireless physical standards. AURA relies on existing C-V2X (PC5), 5G NR, and Automotive Ethernet.
2. **NOT A MIDDLEWARE REPLACEMENT:** We do not rewrite DDS, SOME/IP, or ROS 2. AURA uses them as underlying serialization and transport rails.
3. **NOT A FULL AUTONOMOUS DRIVING STACK:** AURA is not an autonomous driving AI model. We do not build end-to-end vision transformers, object detection neural nets, or vehicle drive-by-wire motor controllers. AURA is the **semantic and safety coordination layer above the autonomy stack**.
4. **NOT A BLOCKCHAIN / DLT SYSTEM:** We do not implement distributed ledgers, crypto tokens, consensus algorithms, or smart contracts. Trust is established via standard PKI asymmetric cryptography (Ed25519) and Hardware Security Modules (HSMs).
5. **NOT AN UNCONSTRAINED CLOUD LLM:** AURA does not call external OpenAI, Google, or Anthropic APIs during runtime execution. All semantic vector hashing (`DomainHashEmbedder-384`) runs deterministically on edge CPUs in sub-millisecond time.

---

## 3. Four-Phase Strategic Technology Roadmap

| Phase | Milestone Name | Timeframe | Core Technical Deliverables | Primary Success Criteria |
|:---:|:---|:---:|:---|:---|
| **Phase 1** | **Internal System Intelligence (CURRENT)** | **Completed** | • Frozen Architecture B (Graph + Embedder + Strict Union).<br>• Canonical benchmark report & metric integrity audit.<br>• Working demonstrator & 252 automated tests. | **Artifact Recall: 63.11%**<br>**Test Reduction: 82.29%**<br>**Safety Invariant: 100.0%** |
| **Phase 2** | **Three-Agent Emulation Prototype (NEXT)** | **Months 1–6** | • AURA Capability Manifest schema definition.<br>• Python/C++ 3-agent local network testbed.<br>• Single-shot negotiation engine & Context Gate.<br>• 10-attack automated adversarial validation suite. | **Negotiation Latency < 5 ms**<br>**Decoy FPR = 0.0%**<br>**Safety Escapes = 0.0%** |
| **Phase 3** | **Real-Time HIL Hardware Testbed (RESEARCH)** | **Months 6–18** | • Porting AURA layer to QNX RTOS on NVIDIA Orin.<br>• Integration over real Automotive Ethernet (TSN) & C-V2X.<br>• HIL testbench integration with Vector CANoe / dSPACE.<br>• Cross-system OTA change impact propagation validation. | **End-to-End Latency < 10 ms**<br>**ISO 26262 TCL2 Evidence**<br>**Change Detection ≥ 95%** |
| **Phase 4** | **Standardization & Industrial Pilot (FUTURE)** | **Years 2–5+** | • Standard submission to AUTOSAR Adaptive & ASAM.<br>• Commercial multi-OEM pilot with Tier-1 partners (KPIT).<br>• Municipal smart intersection trial deployments. | **Commercial Adoption**<br>**Multi-Vendor Interoperability** |
