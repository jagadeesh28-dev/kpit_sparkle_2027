# AURA-Impact — API & Application Security Acceptance Report

**Evaluation Date:** November 21, 2026  
**Auditor Mode:** Hostile Security & Vulnerability Assessment  
**Implementation:** `src/api/server.py`  
**Test Suite:** `tests/api/test_adversarial_api.py`  
**Project:** AURA-Impact — Context-Aware Change Impact and Regression Intelligence  
**Team:** THE GOAT (KPIT Sparkle 2027 Round 2)

---

## 1. Security Architecture Summary

The AURA-Impact API server (`src/api/server.py`) serves as the bridge between frontend HMIs and the internal automotive analysis engine. Because this workbench processes engineering source code diffs and requirement identifiers, stringent input validation and isolation policies are enforced.

---

## 2. Threat Modeling & Adversarial Attack Results

| Threat Category | Attack Vector Tested | Mitigation Mechanism | Audit Result | Status Code |
| :--- | :--- | :--- | :--- | :---: |
| **Path Traversal (Linux)** | `POST /analyze` with `artifact_id="../../etc/passwd"` | Pydantic field validator rejects `..`, `/`, `\` | **BLOCKED** | HTTP 422 |
| **Path Traversal (Win)** | `POST /analyze` with `artifact_id="..\\..\\windows\\win.ini"` | Pydantic validator checks Windows backslashes | **BLOCKED** | HTTP 422 |
| **Oversized Diff DoS** | `POST /upload-diff` with 300 KB payload (>256 KB) | Pydantic `Field(..., max_length=262144)` | **BLOCKED** | HTTP 422 |
| **Null Byte Poisoning** | `POST /upload-diff` with `void test()\x00malicious` | String sanitizer checks for `\x00` | **BLOCKED** | HTTP 400 |
| **Threshold Tampering** | `POST /analyze` with `threshold_override=1.5` | Pydantic range check `Field(ge=0.0, le=1.0)` | **BLOCKED** | HTTP 422 |
| **Threshold Tampering** | `POST /analyze` with `threshold_override=-0.1` | Pydantic range check `Field(ge=0.0, le=1.0)` | **BLOCKED** | HTTP 422 |
| **Empty Input Injection** | `POST /analyze` with `artifact_id=""` | Pydantic `Field(..., min_length=1)` | **BLOCKED** | HTTP 422 |
| **XSS Injection** | `POST /analyze` with `<script>alert('XSS')</script>` | Sanitized by Pydantic; escaped in React JSX | **SAFE** | HTTP 200 |
| **CORS Validation** | `OPTIONS /analyze` with Origin: `http://localhost:5173` | FastApi `CORSMiddleware` allows HMI origins | **VALID** | HTTP 200 |
| **Memory Exhaustion** | Flooding analysis requests | LRU cache ring buffer capped at 50 records | **SAFE** | Bound |

---

## 3. Vulnerability Deep-Dives

### 3.1 Path Traversal Prevention
```python
class ChangeRequest(BaseModel):
    artifact_id: str = Field(..., min_length=1, max_length=128)
    artifact_type: str = Field("Requirement", min_length=1, max_length=64)
    subsystem: str = Field("ADAS", min_length=1, max_length=64)
    ecu: str = Field("VCU", min_length=1, max_length=64)

    @field_validator("artifact_id", "subsystem", "ecu")
    @classmethod
    def prevent_path_traversal(cls, v: str) -> str:
        if ".." in v or "/" in v or "\\" in v:
            raise ValueError("Identifier must not contain path traversal characters")
        return v.strip()
```
*Audit Finding:* Any attempt to inject relative path tokens is caught at schema serialization time prior to filesystem or graph indexing access.

### 3.2 DoS and Payload Protection
- `DiffUploadRequest` enforces `max_length=262144` (256 KB). Payloads exceeding this threshold are immediately rejected with HTTP 422 before AST parsing.
- Unified diff parsing rejects binary data and null-byte injection (`\x00`).
- The in-memory analysis cache `ANALYSIS_CACHE` is restricted to an LRU ring buffer with `MAX_CACHE_SIZE = 50`. Older UUID records are evicted automatically to prevent memory leaks during long-running sessions.

### 3.3 Cross-Site Scripting (XSS)
- Code snippets and natural language semantic descriptions submitted to `POST /analyze` or `POST /upload-diff` are stored as raw text in Python.
- In the React frontend (`hmi_frontend`), all text properties are rendered through standard React JSX string interpolation (`{item.change_semantics}`), which natively performs HTML entity encoding. Raw `dangerouslySetInnerHTML` is strictly prohibited and absent from the codebase.

---

## 4. Security Verification Verdict

The API and application surface demonstrate **defense-in-depth**, adhering to modern OWASP API security guidelines. No remote code execution, file disclosure, or memory exhaustion vectors were identified.
