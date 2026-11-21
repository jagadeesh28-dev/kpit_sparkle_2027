# AURA-Impact: Dashboard Known Limitations & Boundary Conditions

**Document Version:** 1.0.0  
**Target:** KPIT Sparkle 2027 Scientific Rigor & Disclosure  

---

## 1. Scientific & Evaluation Boundaries

1. **Synthetic Link Deletion vs. Organic Hidden Dependencies:**
   - On the Dronology dataset, missing links are evaluated via controlled random link deletion experiments (10%, 20%, 30%).
   - These measure the mathematical recall of intentionally withheld edges; they are synthetic experiments, not organically discovered undocumented dependencies in production vehicles.

2. **Co-Change Mining as a Proxy for Relatedness:**
   - Alexandria evaluation mines historical Git commits to assess whether semantic similarity correlates with co-changing files.
   - Co-change reflects historical developer commit habits, which is a statistical proxy for semantic relatedness, not a verified C++ function call graph.

3. **Safety Gate Invariant vs. Safety Certification:**
   - The Safety Gate enforces a deterministic software invariant ($T_{\text{safe}} \subseteq T_{\text{selected}}$) within an engineering research prototype.
   - It guarantees that mapped ASIL-C/D tests are never pruned by optimization algorithms.
   - It does **not** constitute a formal ISO 26262 Part 8 / Part 6 safety certification or production ASIL sign-off.

---

## 2. Engineering & Tooling Boundaries

1. **Graph Layout Scaling Limits:**
   - The browser-side `elkjs` layout engine performs smoothly on subgraphs up to ~150 nodes.
   - For repository graphs exceeding 500 nodes, the UI automatically applies 1-hop BFS subgraph extraction centered on the change seed to maintain 60 FPS rendering.

2. **Source Code Diff Parsing:**
   - `/upload-diff` currently extracts C/C++ function definitions and requirement/SWC tokens using regex pattern matching.
   - Complex C++ templates, macros, and multi-file unified patches containing non-standard formatting may fail to map to an existing graph node and will return HTTP 400.

3. **Single Active Analysis Session:**
   - The FastAPI backend maintains an in-memory ring buffer (50 records) for fast lookup. It does not currently persist long-term historical analysis runs to an external SQL database.
