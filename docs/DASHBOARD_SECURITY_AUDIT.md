# AURA-Impact: Dashboard Security & Integrity Audit

**Audit Date:** November 21, 2026  
**Auditor:** QA Automation & Security Engineering Team  
**Scope:** FastAPI REST Backend, Vite/React Frontend, Standalone HTML HMI, Upload Handlers  
**Status:** **PASSED — NO CRITICAL OR HIGH VULNERABILITIES IDENTIFIED**  

---

## 1. Threat Modeling & Vulnerability Assessment

| Threat Vector | Attack Scenario | Mitigation in Place | Validation Test | Severity |
| :--- | :--- | :--- | :--- | :---: |
| **Arbitrary Code Execution** | Attacker uploads malicious C++ code or shell script via `/upload-diff`. | • Submitted diffs are **parsed with regex/AST patterns only**.<br>• Code is **never compiled, executed, or passed to subprocess/shell**.<br>• No temporary executable files are created. | `test_upload_diff_valid_c_patch` | **NONE** |
| **Path Traversal (CWE-22)** | Attacker submits `../../etc/shadow` or `C:\Windows` in artifact ID or subsystem fields. | • `@field_validator` in `ChangeRequest` enforces strict rejection of `/`, `\`, and `..` tokens.<br>• File lookup occurs exclusively against in-memory NetworkX graph nodes. | `test_attack_path_traversal_linux`, `test_attack_path_traversal_windows` | **MITIGATED** |
| **Cross-Site Scripting (XSS)** | Attacker injects HTML/JS into `change_semantics` (e.g. `<script>alert(1)</script>`). | • React virtual DOM automatically escapes all text nodes.<br>• No instances of `dangerouslySetInnerHTML` exist in the frontend.<br>• Content is treated as raw string literal. | `test_attack_xss_in_semantics` | **MITIGATED** |
| **Denial of Service (DoS)** | Attacker floods `/upload-diff` with multi-gigabyte files. | • Maximum payload limit is strictly enforced at 262,144 bytes (256 KB).<br>• Pydantic schema rejects oversized payloads with HTTP 413 / 422. | `test_attack_oversized_diff_payload` | **MITIGATED** |
| **Null Byte Poisoning** | Attacker inserts `\x00` in diff text to bypass file extension checks. | • Explicit check for `\x00` rejects the payload with HTTP 400 Bad Request. | `test_attack_null_byte_in_diff` | **MITIGATED** |
| **Safety Gate Invariant Bypass** | Attacker submits 0.0 threshold or empty test list to strip safety tests. | • `SafetyGate.enforce()` unconditionally re-injects all ASIL-C/D tests mapped to impacted nodes.<br>• If a safety test is missing, raises `SafetyInvariantViolationError` (HTTP 422). | `test_analyze_safety_retention_invariant` | **MITIGATED** |

---

## 2. Dependency Audit

- **Frontend:** `npm audit` shows 0 critical vulnerabilities in production bundles.
- **Python Backend:** Uses standard, battle-tested packages: `fastapi >= 0.128`, `pydantic >= 2.12`, `uvicorn >= 0.40`, `networkx >= 3.6`.
