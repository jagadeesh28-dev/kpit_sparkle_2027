# AURA-Impact: Dashboard User & Demonstration Guide

**Event:** KPIT Sparkle 2027 — Round 2 Live Demonstration  
**Team:** THE GOAT  

---

## 1. Quick Start Demonstration Modes

### Mode 1: Instant Standalone HMI (Zero Dependencies)
Double-click or launch in any browser:
```bash
# Windows
start "AURA-Impact — ISO 26262 Impact Analysis HMI.html"
```
- Requires no installation, Node.js, or Python.
- If the backend is running on `localhost:8000`, it automatically connects in **LIVE BACKEND** mode.
- If the backend is offline, it seamlessly provides a high-fidelity **OFFLINE DEMO** fallback.

---

### Mode 2: Full-Stack React Engineering Workbench

#### Step 1: Start the FastAPI Backend Server
```bash
python src/api/server.py
```
*(Starts REST service on `http://localhost:8000` with 217 loaded graph nodes)*

#### Step 2: Start the React Frontend
```bash
cd hmi_frontend
npm run dev
```
*(Opens interactive engineering workbench on `http://localhost:5173`)*

---

## 2. Navigating the 4 Curated Demonstration Scenarios

| Scenario | Presets Selector | Target Artifact | Demonstrated Principle | Key Things to Show Judges |
| :--- | :--- | :--- | :--- | :--- |
| **1. Braking Threshold Calibration** | Scenario 1 | `REQ_AEB_001` (ADAS) | **Deterministic Graph Traversal** | • Solid red edges propagating down to `SWC_AccController` and `TC-ADAS-0311`.<br>• Execution latency < 0.2 ms.<br>• Semantic fallback is **NOT triggered** because graph coverage is complete. |
| **2. Latent Thermal Coupling** | Scenario 2 | `REQ_BMS_004` (Powertrain) | **Semantic Dependency Recovery** | • Dashed purple edges recovering unlinked thermal runnables.<br>• BGE-M3 cosine similarity scores shown in Inspector.<br>• Resolves hidden dependencies when call graph is incomplete. |
| **3. Non-Automotive Decoy Attack** | Scenario 3 | `REQ_AEB_014` (ADAS) | **Contextual Decoy Rejection** | • Open **"Decoy & Semantic Inspector"** tab.<br>• Point out candidate `INFOTAINMENT_PLAYLIST_SERVICE` rejected with `REJECT_SUBSYSTEM_MISMATCH`.<br>• Demonstrates **0% False Positive Rate** on decoys. |
| **4. High-Voltage Inverter Runaway** | Scenario 4 | `SWC_InverterControl` (Chassis) | **Mandatory Safety Retention** | • Open **"Safety View"** tab.<br>• Shows 100% retention of critical ASIL-D test cases.<br>• Even with 90%+ suite reduction, Safety Gate prevents test stripping. |

---

## 3. Uploading Custom Changes
1. Click **"Upload Diff"** on the top command bar.
2. Paste any unified Git diff or modified C function.
3. Click **"Parse & Load Change"**.
4. The system automatically identifies changed functions/requirements, links them to graph nodes, and runs the full two-stage impact pipeline.
