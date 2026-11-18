"""
Standardized Four Baselines Implementation (evaluation/baselines/unified_baselines.py)
Implements:
1. Baseline 1: Keyword Matching (TF-IDF with sublinear term frequency scaling)
2. Baseline 2: Embedding-Only (AURA-DomainHashEmbedder-384 dense cosine retrieval)
3. Baseline 3: Graph-Only (Deterministic bounded BFS graph traversal, k <= 3)
4. Baseline 4: AURA-Impact (Two-stage hybrid: Graph + Semantic Fallback + Context Filter + Safety Gate)
"""
import time
from typing import Dict, Any, List, Set, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from src.graph.builder import EngineeringGraph
from src.graph.schema import GraphNode, RelationType, SafetyLevel, NodeType
from src.semantic.embedder import SemanticEmbedder
from src.semantic.index import FAISSSemanticIndex, IndexedArtifact
from src.semantic.context_filter import ContextFilter
from src.testing.safety_gate import SafetyGate


class UnifiedBaselines:
    """Standard execution harness for all four comparison baselines."""

    def __init__(self, graph: EngineeringGraph, embedder: Optional[SemanticEmbedder] = None):
        self.graph = graph
        self.embedder = embedder or SemanticEmbedder()
        self.context_filter = ContextFilter(enforce_subsystem=True, enforce_artifact_type=True)
        self.safety_gate = SafetyGate()

        # Build corpus for Keyword Baseline
        self.node_ids = list(graph.node_store.keys())
        self.corpus = []
        for nid in self.node_ids:
            node = graph.get_node(nid)
            desc = node.metadata.get("description", "")
            text = f"{node.name} {desc} {node.subsystem} {node.type.value if hasattr(node.type, 'value') else node.type}"
            self.corpus.append(text)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, token_pattern=r"(?u)\b\w+\b")
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        else:
            self.tfidf_matrix = None

        # Build FAISS Dense Semantic Index
        self.semantic_index = FAISSSemanticIndex(dimension=384, embedder=self.embedder)
        nodes_list = [graph.get_node(nid) for nid in self.node_ids]
        self.semantic_index.build_index(nodes_list)

        # Precompute Test Mappings
        self.artifact_to_tests: Dict[str, Set[str]] = {}
        self.all_tests: Set[str] = set()
        self.safety_critical_tests: Set[str] = set()

        for nid, node in graph.node_store.items():
            if node.type in [NodeType.TEST, NodeType.TEST_CASE]:
                self.all_tests.add(nid)
                if node.safety_level in [SafetyLevel.ASIL_C, SafetyLevel.ASIL_D, SafetyLevel.SAFETY_CRITICAL]:
                    self.safety_critical_tests.add(nid)
            
            # Map downstream tests
            if self.graph.graph.has_node(nid):
                for succ_id in self.graph.graph.successors(nid):
                    succ = graph.get_node(succ_id)
                    if succ and succ.type in [NodeType.TEST, NodeType.TEST_CASE]:
                        self.artifact_to_tests.setdefault(nid, set()).add(succ_id)
                
                # Map upstream tests (if test -> TESTS -> artifact)
                for pred_id in self.graph.graph.predecessors(nid):
                    pred = graph.get_node(pred_id)
                    if pred and pred.type in [NodeType.TEST, NodeType.TEST_CASE]:
                        self.artifact_to_tests.setdefault(nid, set()).add(pred_id)

    def _map_artifacts_to_tests(self, artifact_ids: List[str]) -> Set[str]:
        tests = set()
        for aid in artifact_ids:
            if aid in self.all_tests:
                tests.add(aid)
            tests.update(self.artifact_to_tests.get(aid, set()))
        return tests

    # ──────────────────────────────────────────────────────────────────────────
    # BASELINE 1: KEYWORD MATCHING
    # ──────────────────────────────────────────────────────────────────────────
    def run_keyword(self, change_query: str, target_artifact_id: str = "", threshold: float = 0.20) -> Dict[str, Any]:
        start_t = time.perf_counter()
        impacted = []

        if self.tfidf_matrix is not None and change_query.strip():
            q_vec = self.vectorizer.transform([change_query])
            scores = (self.tfidf_matrix * q_vec.T).toarray().flatten()
            for idx, score in enumerate(scores):
                if score >= threshold:
                    impacted.append(self.node_ids[idx])

        if target_artifact_id and target_artifact_id not in impacted:
            impacted.append(target_artifact_id)

        selected_tests = self._map_artifacts_to_tests(impacted)
        latency = (time.perf_counter() - start_t) * 1000.0

        return {
            "method": "Keyword (TF-IDF)",
            "impacted_artifacts": impacted,
            "selected_tests": list(selected_tests),
            "latency_ms": round(latency, 3)
        }

    # ──────────────────────────────────────────────────────────────────────────
    # BASELINE 2: EMBEDDING ONLY
    # ──────────────────────────────────────────────────────────────────────────
    def run_embedding_only(self, change_query: str, target_artifact_id: str = "", threshold: float = 0.45) -> Dict[str, Any]:
        start_t = time.perf_counter()
        q_vec = self.embedder.embed_text(change_query)
        candidates = self.semantic_index.search(q_vec, top_k=20)

        impacted = [art.artifact_id for art, score in candidates if score >= threshold]
        if target_artifact_id and target_artifact_id not in impacted:
            impacted.append(target_artifact_id)

        selected_tests = self._map_artifacts_to_tests(impacted)
        latency = (time.perf_counter() - start_t) * 1000.0

        return {
            "method": "Embedding-Only (384-d)",
            "impacted_artifacts": impacted,
            "selected_tests": list(selected_tests),
            "latency_ms": round(latency, 3)
        }

    # ──────────────────────────────────────────────────────────────────────────
    # BASELINE 3: GRAPH ONLY (DETERMINISTIC BFS)
    # ──────────────────────────────────────────────────────────────────────────
    def run_graph_only(self, target_artifact_id: str, max_depth: int = 3) -> Dict[str, Any]:
        start_t = time.perf_counter()
        visited = set()
        queue = [(target_artifact_id, 0)] if target_artifact_id in self.graph.node_store else []

        while queue:
            curr, depth = queue.pop(0)
            if curr in visited or depth > max_depth:
                continue
            visited.add(curr)

            # Follow downstream and upstream architectural relationships
            neighbors = []
            if self.graph.graph.has_node(curr):
                neighbors = list(self.graph.graph.successors(curr)) + list(self.graph.graph.predecessors(curr))
            for nxt in neighbors:
                if nxt not in visited:
                    queue.append((nxt, depth + 1))

        impacted = list(visited)
        selected_tests = self._map_artifacts_to_tests(impacted)
        latency = (time.perf_counter() - start_t) * 1000.0

        return {
            "method": "Graph-Only (BFS)",
            "impacted_artifacts": impacted,
            "selected_tests": list(selected_tests),
            "latency_ms": round(latency, 3)
        }

    # ──────────────────────────────────────────────────────────────────────────
    # BASELINE 4: AURA-IMPACT (PROVE -> RECOVER -> FILTER -> PROTECT)
    # ──────────────────────────────────────────────────────────────────────────
    def run_aura_impact(
        self,
        change_query: str,
        target_artifact_id: str,
        semantic_threshold: float = 0.45,
        max_graph_depth: int = 3,
        mandatory_safety_tests: Optional[Set[str]] = None
    ) -> Dict[str, Any]:
        start_t = time.perf_counter()

        # 1. STAGE 1: PROVE (Deterministic Graph Traversal)
        struct_res = self.run_graph_only(target_artifact_id, max_depth=max_graph_depth)
        struct_impacts = set(struct_res["impacted_artifacts"])

        # 2. STAGE 2: RECOVER (Context-Aware Semantic Retrieval on Missing Links)
        q_vec = self.embedder.embed_text(change_query)
        target_node = self.graph.get_node(target_artifact_id)
        target_subsystem = target_node.subsystem if target_node else ""

        raw_candidates = self.semantic_index.search(
            q_vec,
            top_k=20,
            subsystem_filter=target_subsystem if target_subsystem else None
        )

        # 3. STAGE 3: FILTER (Automotive Context & Subsystem Isolation Gate)
        semantic_impacts = set()
        filtered_out = []
        for art, score in raw_candidates:
            if score < semantic_threshold:
                continue
            # Evaluate hard context filter
            passed = self.context_filter.passes_hard_filter(
                source_subsystem=target_subsystem,
                candidate_subsystem=art.subsystem,
                candidate_type=art.artifact_type,
                raw_cosine=score
            )
            if passed:
                semantic_impacts.add(art.artifact_id)
            else:
                filtered_out.append(art.artifact_id)

        # 4. FUSION (Strict Set Union: S_final = S_struct ∪ S_semantic)
        final_impacts = struct_impacts | semantic_impacts

        # 5. REGRESSION TEST SELECTION
        candidate_tests = self._map_artifacts_to_tests(list(final_impacts))

        # 6. STAGE 4: PROTECT (Non-Bypassable Safety Gate Invariant Enforcement)
        # Unconditionally retain all mandatory safety-critical tests
        mand_set = set(mandatory_safety_tests) if mandatory_safety_tests else set()
        mand_set.update(self.safety_critical_tests)
        
        final_tests = self.safety_gate.apply_safety_gate(
            candidate_tests=candidate_tests,
            mandatory_safety_tests=mand_set
        )

        latency = (time.perf_counter() - start_t) * 1000.0

        return {
            "method": "AURA-Impact",
            "impacted_artifacts": list(final_impacts),
            "structural_count": len(struct_impacts),
            "semantic_recovered_count": len(semantic_impacts),
            "filtered_out_count": len(filtered_out),
            "selected_tests": list(final_tests),
            "safety_tests_retained": list(mand_set),
            "latency_ms": round(latency, 3),
            "rationale": f"PROVE ({len(struct_impacts)}) -> RECOVER ({len(semantic_impacts)}) -> FILTER ({len(filtered_out)} rejected) -> PROTECT ({len(mand_set)} safety)"
        }
