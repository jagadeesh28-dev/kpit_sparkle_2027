# AURA-Impact Complete Reproducibility Runbook
**KPIT Sparkle Round 2 — Step-by-Step Verification Guide**  
**Document Reference:** AURA-REPRO-2027  
**Auditor:** THE GOAT (AURA-Impact Research Engineering)  

---

## 1. System Requirements & Environment

- **Python Runtime:** Python 3.10, 3.11, 3.12, 3.13, or 3.14 (Verified on Python 3.14.0 Windows x64)
- **Version Control:** Git 2.40+ (MinGit 2.56.1 verified)
- **Memory:** Minimum 4 GB RAM (Total footprint during benchmarks is $<120$ MB)
- **Dependencies:** Standard scientific libraries defined in `requirements.txt`:
  - `networkx>=3.0`, `numpy>=1.24`, `pandas>=2.0`, `scipy>=1.10`, `scikit-learn>=1.2`, `streamlit>=1.24`, `matplotlib>=3.7`, `pytest>=7.3`

---

## 2. Fast Reproduction Sequence (5 Steps)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download & Ingest Public Datasets
Downloads raw public datasets (Dronology, Defects4J, Autoware.Universe, Alexandria), verifies SHA-256 checksums, and compiles `data/manifests/dataset_manifest.json`:
```bash
python scripts/download_datasets.py
```
*Expected Output:*
- Downloads 57 files into `data/raw/`
- Manifest written to `data/manifests/dataset_manifest.json`

### Step 3: Run Complete Automated Test Suite (256 Tests)
Executes the full unit, integration, safety invariant, and adversarial regression suite:
```bash
python -m pytest tests/ -v
```
*Expected Output:*
```
============================ 256 passed in ~10.8s ============================
```

### Step 4: Execute Master Public Dataset Benchmark Pipeline
Executes Experiment A (Dronology link deletion), Experiment B (Defects4J RTS), Experiment C (Autoware automotive architecture), and Experiment D (Alexandria co-changes):
```bash
python evaluation/experiments/run_all_experiments.py
```
*Expected Output:*
- Executes in ~1.3 seconds
- Generates 5 standardized tables in `results/tables/`
- Generates 8 publication-quality plots in `results/plots/`
- Generates machine-readable evidence in `results/evidence/evaluation_master_evidence.json`

### Step 5: Launch the Interactive Engineering Demonstrator
Launches the Streamlit demonstrator supporting live scenario inspections, visual graph traversal, and public dataset evidence exploration:
```bash
streamlit run dashboard/app.py
```
*Access in browser at:* `http://localhost:8501`

---

## 3. Individual Experiment Verification Commands

If an auditor or mentor wants to run individual experiments:

### Run Dronology Link Deletion Alone (Experiment A):
```bash
python evaluation/experiments/experiment_dronology.py
```

### Run Defects4J Real Defects RTS Alone (Experiment B):
```bash
python evaluation/experiments/experiment_defects4j.py
```

### Run Autoware.Universe Automotive Impact Alone (Experiment C):
```bash
python evaluation/experiments/experiment_autoware.py
```

### Run Alexandria Co-Change Evolution Alone (Experiment D):
```bash
python evaluation/experiments/experiment_alexandria.py
```

### Run Canonical Synthetic 150-Mutation Benchmark (Gate 11):
```bash
python benchmark/final/runner.py
```

---

## 4. Key Output Artifact Locations

| Artifact Type | File Location | Description |
| :--- | :--- | :--- |
| **Cross-Dataset Summary** | `results/tables/master_benchmark_summary.csv` | High-level summary of all 4 datasets |
| **Dronology Metrics** | `results/tables/dronology_link_deletion.csv` | Deletion rates (10%, 20%, 30%) by method |
| **Defects4J Metrics** | `results/tables/defects4j_rts.csv` | Real defect test recall and suite reduction |
| **Autoware Metrics** | `results/tables/autoware_architecture.csv` | ROS 2 AEB impact metrics |
| **Alexandria Metrics** | `results/tables/alexandria_co_change.csv` | Historical co-change recovery results |
| **Publication Figures** | `results/plots/*.png` (8 Figures) | High-DPI publication charts |
| **Master Evidence JSON** | `results/evidence/evaluation_master_evidence.json` | Complete cryptographic JSON trace |
| **Dataset Manifest** | `data/manifests/dataset_manifest.json` | Download provenance & SHA-256 hashes |

