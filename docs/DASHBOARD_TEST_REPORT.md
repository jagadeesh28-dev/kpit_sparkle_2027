# AURA-Impact: Comprehensive Dashboard Test & Validation Report

**Test Execution Date:** November 21, 2026  
**Auditor:** Principal QA Automation & Software Validation Engineer  
**Status:** **100% PASS (277 Python Tests + 4 Frontend Tests + Live E2E Integration Verified)**  

---

## 1. Test Suite Summary

| Layer | Framework | Total Tests | Passed | Failed | Skipped | Execution Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Python Unit & Subsystem Tests** | pytest 9.1.1 | 248 | 248 | 0 | 0 | 20.08s |
| **Backend API End-to-End Tests** | pytest + TestClient | 13 | 13 | 0 | 0 | 1.85s |
| **Adversarial Security & Attack Tests** | pytest + TestClient | 8 | 8 | 0 | 0 | 1.44s |
| **Frontend Unit & Contract Tests** | Vitest 5.1.1 | 4 | 4 | 0 | 0 | 1.33s |
| **Live Process Integration Suite** | PowerShell E2E | 5 | 5 | 0 | 0 | 3.50s |
| **TOTAL** | | **278** | **278** | **0** | **0** | **~28s** |

---

## 2. Detailed Test Coverage Breakdown

### 2.1 Backend API Tests (`tests/api/test_server_api.py`)
- `test_health_endpoint`: Verified telemetry reporting, version string, loaded node count (>0), edge count (>0), and dataset status.
- `test_scenarios_endpoint`: Verified all 4 automotive scenario presets are returned with distinct payloads.
- `test_analyze_structural_scenario`: Verified Scenario 1 (Braking Threshold) structural impact propagation.
- `test_analyze_semantic_and_rejected_candidates`: Verified candidate separation: accepted vs rejected with explicit reasons.
- `test_analyze_safety_retention_invariant`: Verified non-bypassable mandatory ASIL-D test retention.
- `test_analyze_path_traversal_rejection`: Verified rejection of path traversal tokens (`../`).
- `test_analyze_empty_payload_rejection`: Verified 422 Unprocessable Entity on empty required fields.
- `test_benchmarks_endpoint`: Verified reading of `master_benchmark_summary.csv` and publication figures manifest.
- `test_upload_diff_valid_c_patch`: Verified unified Git diff parsing and C function extraction.
- `test_upload_diff_malformed_rejection`: Verified 400 Bad Request on unparseable input.
- `test_upload_diff_null_byte_rejection`: Verified 400 Bad Request on null byte injection.
- `test_get_analysis_by_id`: Verified retrieval from in-memory LRU audit cache.
- `test_get_analysis_by_id_not_found`: Verified 404 on missing analysis ID.

### 2.2 Adversarial Security Tests (`tests/api/test_adversarial_api.py`)
- `test_attack_xss_in_semantics`: Script injection (`<script>alert()</script>`) is safely treated as string literal without execution.
- `test_attack_path_traversal_linux`: Linux traversal (`../../etc/shadow`) rejected with 422.
- `test_attack_path_traversal_windows`: Windows traversal (`..\..\Windows\System32`) rejected with 422.
- `test_attack_invalid_threshold_over_bounds`: Threshold > 1.0 rejected with 422.
- `test_attack_invalid_threshold_negative`: Threshold < 0.0 rejected with 422.
- `test_attack_oversized_diff_payload`: Payloads > 256 KB rejected with 413/422.
- `test_attack_null_byte_in_diff`: Null bytes (`\x00`) rejected with 400.
- `test_resilience_rapid_repeated_queries`: 5 consecutive rapid requests executed without race condition.

### 2.3 Frontend Tests (`hmi_frontend/src/__tests__/api_and_components.test.ts`)
- `validates scenario preset schema structure`: Confirms TypeScript types align with backend Pydantic models.
- `validates semantic candidate status and rejection reason`: Confirms `status: 'ACCEPT' | 'REJECT' | 'REVIEW_REQUIRED'`.
- `validates selected test structure and safety classification`: Confirms `ASIL-D` and `MANDATORY_SAFETY_GATE` mapping.
- `normalizes various ASIL string formats`: Confirms `ASIL_D` -> `ASIL-D`.

### 2.4 Live Process E2E Output (Real Backend Server on Port 8000)
```
1. HEALTH: healthy | nodes: 217
2. SCENARIOS: 4 presets loaded
3. BENCHMARKS: 3 summary rows | 8 figures
4. SCENARIO 1 ANALYZE: status=success | impacts=4 | tests=1 | reduction=99.0% | latency=0.091ms
5. SCENARIO 3 DECOY ATTACK: rejected_count=6 | first_reason=Similarity score (0.230) below threshold (0.450)
```
