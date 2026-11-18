# AURA-Impact — Gate 11: Final Benchmark Report
**Version:** GATE-14-v2.0.0  
**Timestamp:** 2026-11-18T18:45:17.451890+00:00  
**PRNG Seed:** 42  
**Dataset Fingerprint (SHA-256[:16]):** `3bc8c11efb2398a0`  
**Mutations:** 150 (Calibration=30, Validation=30, Test=90)  
**Projects:** ADAS, POWERTRAIN, BATTERY_EV  

---

## 1. Headline Results

| Metric | Graph-Only Baseline | Embedding+Context | **AURA Hybrid Routed** | Δ vs Graph |
|:---|---:|---:|---:|---:|
| Artifact Recall | 0.5770 | 0.4320 | **0.5773** | ++0.0004 |
| Artifact Precision | 0.7276 | 0.4091 | **0.6981** | +-0.0295 |
| Artifact F1-Score | 0.4944 | 0.2648 | **0.5815** | ++0.0871 |
| Test Suite Reduction | — | — | **89.12%** | — |
| Test Recall | — | — | **0.8368** | — |
| **Safety Test Recall** | **100.00%** | **100.00%** | **100.00%** | Invariant |

---

## 2. Safety Gate Invariant (T_safe ⊆ T_selected)

- **Status:** ✅ PASS
- Safety-critical mutations with 100% recall: **150 / 150**
- Safety pass rate: **100.00%**
- Any violation would have raised `SafetyInvariantViolationError` and aborted execution.

---

## 3. Semantic Retrieval Performance

| k | Recall@k |
|:---|---:|
| 1 | 3.33% |
| 3 | 6.67% |
| 5 | 13.33% |
| 10 | 20.00% |
| MRR | 0.0665 |

---

## 4. Context Ablation

| Variant | Mean F1 |
|:---|---:|
| Embedding_Only (Raw) | 0.0100 |
| Embedding + Soft Context | 0.0170 |
| Embedding + Hard Filter + Soft Rank | 0.0170 |

---

## 5. Statistical Significance (Paired Wilcoxon Signed-Rank, Bonferroni α=0.0125)

| Test | W-statistic | p-value | Significant? |
|:---|---:|---:|:---:|
| Recall (Hybrid vs Graph) | 5513.0 | 7.4800e-01 | ❌ No |
| Precision (Hybrid vs Graph) | 981.0 | 8.5269e-01 | ❌ No |

---

## 6. Scalability

| Nodes | Graph Build (ms) | Query (ms) | Peak Mem (MB) |
|---:|---:|---:|---:|
| 100 | 2.41 | 0.596 | 0.15 |
| 500 | 7.47 | 0.288 | 0.76 |
| 1,000 | 15.64 | 0.354 | 1.52 |
| 5,000 | 99.76 | 0.412 | 7.53 |
| 10,000 | 170.44 | 0.355 | 15.07 |
| 25,000 | 476.32 | 0.368 | 39.38 |

---

## 7. Method Summary Table

| Method | Recall μ | Recall σ | Precision μ | Precision σ | F1 μ | F1 σ | Latency (ms) |
|:---|---:|---:|---:|---:|---:|---:|---:|
| Embedding_Context | 0.4320 | 0.4550 | 0.4091 | 0.3865 | 0.2648 | 0.3356 | 0.776 |
| Embedding_Only | 0.4245 | 0.4589 | 0.6678 | 0.4277 | 0.3113 | 0.3848 | 0.184 |
| Graph_Only | 0.5770 | 0.3644 | 0.7276 | 0.3469 | 0.4944 | 0.3554 | 0.035 |
| Hybrid_AURA_Fixed | 0.5797 | 0.3613 | 0.4424 | 0.3394 | 0.3975 | 0.3072 | 0.829 |
| Hybrid_AURA_Routed | 0.5773 | 0.3638 | 0.6981 | 0.3454 | 0.5815 | 0.3478 | 0.338 |
| Keyword | 0.4290 | 0.4553 | 0.1949 | 0.1706 | 0.1502 | 0.1665 | 0.419 |

---

## 8. Reproducibility Checklist

- [x] PRNG seed frozen to `42` (dataset + splits + runner)
- [x] Dataset fingerprint recorded: `3bc8c11efb2398a0`
- [x] Calibration split strictly isolated (no leakage into test)
- [x] Safety gate enforced on all 150 mutations × 7 methods
- [x] All CSVs saved to `benchmark/final/outputs/`
- [x] Gate artifact: `artifacts/gates/stage_14_gate.json`

---

## 9. Gate 11 Verdict

```
BENCHMARK VALIDITY:        PASS
SAFETY INVARIANT:          PASS (150/150)
GROUND-TRUTH INTEGRITY:    PASS (Bounded k=5)
DATA LEAKAGE:              PASS (0 leaks, calibration isolated)
STATISTICAL SIGNIFICANCE:  Recall sig=False, Precision sig=False
ARCHITECTURE VERDICT:      B — Graph + Context-Constrained Semantic Fallback
GATE STATUS:               PASS ✅
```

*Run duration: 1.7 s*
