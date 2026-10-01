# 18 — MINIMUM RESEARCH PROTOTYPE & EXPERIMENTAL VALIDATION PLAN

**Document Reference:** `research/autonomous_interoperability/18_EXPERIMENT_PLAN.md`  
**Focus:** Concrete Minimal Demonstrator Specification, Baseline Comparisons, and Adversarial Attack Suite  
**Author:** Lead Experimentalist & Verification Specialist  

---

## 1. The Minimal Demonstrator Philosophy
We do not propose building an impossibly complex, full-scale vehicular ad-hoc network for our next research phase. A student or engineering research team cannot deploy 50 physical autonomous cars on public highways.

Instead, we specify the **smallest possible experiment capable of definitively proving or disproving the core hypothesis**.

---

## 2. The Three-Agent Heterogeneous Emulation Testbed

The minimal demonstrator comprises three distinct software agents running in isolated processes on a local testbench (or across three networked Linux/RTOS edge nodes):

```
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│ AGENT 1: AUTONOMOUS VEHICLE     │         │ AGENT 2: SIDEWALK DELIVERY POD  │
│ • Stack: AUTOSAR Adaptive SOA   │         │ • Stack: ROS 2 (Humble / Iron)  │
│ • Domain: Highway / Urban Major │         │ • Domain: Sidewalk / Crosswalk  │
│ • Mass: 2,100 kg | Speed: 15 m/s│         │ • Mass: 45 kg | Speed: 1.5 m/s  │
│ • Safety: ISO 26262 ASIL-D      │         │ • Safety: ISO 13849 PL-d        │
└────────────────┬────────────────┘         └────────────────┬────────────────┘
                 │                                           │
                 │              AURA PROTOCOL                │
                 └───────────────────┬───────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │ AGENT 3: SMART INTERSECTION RSU │
                    │ • Stack: Linux Edge C++ Daemon  │
                    │ • Domain: Municipal V2I Hub     │
                    │ • Function: Dynamic Scheduler   │
                    │ • Protocol: C-V2X / SOME/IP-SD  │
                    └─────────────────────────────────┘
```

### The 7-Step Executable Lifecycle
1. **DISCOVER:** Agent 1 and Agent 2 enter the 100-meter communication cell of Agent 3, detected via DDS / SOME/IP multicast.
2. **UNDERSTAND:** Each agent broadcasts its machine-readable AURA Capability Manifest.
3. **MATCH:** AURA's `DomainHashEmbedder-384` and Context Gate screen capabilities, normalizing different vendor terminologies into canonical SI units.
4. **VERIFY:** The Safety Contract Gate checks the invariant: $C_{safe} \subseteq C_{contract}$ (ensuring Agent 1's stopping distance is preserved while Agent 2 safely clears the crosswalk).
5. **REQUEST:** Agent 3 proposes a single-shot, conflict-free spatio-temporal clearance corridor.
6. **EXECUTE:** Both agents execute their trajectories; internal trajectory watchdogs monitor physical compliance.
7. **REPORT & UPDATE:** When Agent 3 simulates an Over-the-Air (OTA) interface change, AURA's Change Impact Engine evaluates downstream compatibility on Agent 1 and Agent 2.

---

## 3. Baseline Comparison Framework

To establish empirical rigor, the proposed AURA layer is benchmarked against three industry baseline paradigms under identical physical scenarios:

| Evaluation Dimension | Baseline 1: No Interoperability Layer (Pure Vision / Sensor Tracking) | Baseline 2: Manual Bilateral Mapping (Hardcoded Custom Bridge) | Baseline 3: Conventional Syntactic Middleware (Raw DDS / SOME/IP IDLs) | Proposed: AURA Semantic Interoperability Layer |
|:---|:---|:---|:---|:---|
| **Mechanism** | Agents do not communicate; rely strictly on cameras/LiDAR tracking. | Custom C++ ROS-to-AUTOSAR translation bridge written by engineers. | Standard DDS topics publishing raw `geometry_msgs/Twist` structs. | AURA Capability Manifests + Context Gate + Safety Contract Gate. |
| **Integration Overhead** | Zero communication setup; high perception compute overhead. | High manual effort: 80–120 engineering hours to write translation tables. | Moderate manual effort: 30–50 hours defining shared IDL interfaces. | **< 2 hours** (Automated manifest ingestion and context matching). |
| **Decoy Rejection** | Fails on visual edge cases (e.g., reflections, occlusions). | Fixed static rules; fails when vendor updates vocabulary. | **Fails completely:** Accepts any validly typed struct regardless of domain. | **100% rejection** of cross-domain semantic decoys via Context Gate. |
| **Safety Invariant Enforcement** | None (Relies on passive emergency braking). | Implicit in custom code; brittle to timing changes. | None (DDS QoS guarantees delivery, not physical safety). | **Strictly enforced:** $C_{safe} \subseteq C_{contract}$ (0.0% safety escapes). |
| **Adaptability to OTA Updates** | Robust to external code; blind to external intent. | **Breaks silently:** External update invalidates hardcoded translation tables. | **Breaks at compile/runtime:** IDL hash mismatch halts communication. | **Automated Change Propagation:** Predicts affected runnables and alerts fallback. |

---

## 4. The 10 Adversarial Attack Scenarios (Fault Injection Suite)

To ensure the research prototype is hostilely stress-tested, the testbed must execute 10 automated fault injection attacks:

| Attack ID | Adversarial Vector | Injected Flaw / Attack Payload | Success Criteria (AURA Must Pass) |
|:---|:---|:---|:---|
| **ATK-01** | **Misleading Capability** | Low-cost rover falsely advertises 10.0 m/s² braking deceleration. | Safety Gate verifies against local physical radar tracking; rejects false claim. |
| **ATK-02** | **Cross-Domain Decoy** | Autonomous lawnmower advertises obstacle avoidance in vehicle path. | Context Gate flags `SUBSYSTEM_MISMATCH` (`OFFROAD_GARDEN` vs `HIGHWAY`); rejected. |
| **ATK-03** | **Incompatible Units** | British system advertises speed in `miles_per_hour`; receiver expects `m/s`. | Manifest unit parser detects mismatch; normalizes to SI `m/s` or rejects. |
| **ATK-04** | **Stale Manifest Cache** | Attacker replays a valid signed manifest with expired timestamp ($TTL > 5\text{s}$). | Manifest validator flags `STALE_MANIFEST_DETECTED`; discards packet. |
| **ATK-05** | **Cryptographic Tampering** | Manifest payload modified in transit without valid Ed25519 signature. | HSM security gate detects signature failure; drops packet immediately. |
| **ATK-06** | **RF Packet Loss / Jamming** | Synthetic 40% to 80% packet drop injected over wireless socket. | Failsafe timeout triggers at 100 ms; system transitions cleanly to internal MRM. |
| **ATK-07** | **Semantic Ambiguity** | Candidate capability has borderline cosine similarity (0.41, below 0.50 threshold). | System flags `REVIEW_REQUIRED`; treats external agent as an uncoordinated obstacle. |
| **ATK-08** | **Safety Invariant Breach** | Infrastructure requests intersection entry with stopping margin $d_{margin} < 0$. | Safety Gate flags `SAFETY_INVARIANT_VIOLATION`; blocks contract execution. |
| **ATK-09** | **Coordinate Frame Shift** | External camera shifts coordinate origin from road surface to optical center. | Change Impact Engine detects origin mismatch; isolates infrastructure feed. |
| **ATK-10** | **Multi-Agent Deadlock** | Two agents arrive at four-way stop with identical priority requests. | Deterministic tie-breaker rules (lower Agent ID yields) resolve standoff in < 5 ms. |

---

## 5. Quantitative Experimental Metrics to Record
During the execution of the experimental testbed, the test runner will automatically log:
1. **Capability Discovery Latency ($t_{disc}$):** Target $< 2.0\text{ ms}$.
2. **Context Gate Screening Latency ($t_{gate}$):** Target $< 0.5\text{ ms}$.
3. **Safety Verification Latency ($t_{safe}$):** Target $< 0.2\text{ ms}$.
4. **Decoy False Positive Rate ($FPR_{decoy}$):** Target $\mathbf{0.0\%}$.
5. **Safety Invariant Escape Rate ($SER$):** Target $\mathbf{0.0\%}$.
6. **Change Impact Propagation Accuracy:** Target $\mathbf{\ge 95\%}$ of affected interfaces identified.
