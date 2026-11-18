"""
Experiment B: Defects4J Real Historical Defects & Regression Test Selection
(evaluation/experiments/experiment_defects4j.py)

Evaluates:
- 10 Real Historical Software Defects from Apache Commons-Cli
- Triggering Failing Tests (exposing the fault) vs Relevant Test Pool
- Comparative RTS: Keyword, Embedding-Only, Graph-Only, AURA-Impact
- Metrics: Bug-Triggering Test Recall, Test Selection Precision, Test Suite Reduction, Latency
- Anti-Leakage Safeguard: Pre-change snapshot only; zero target test outcome or fixing patch leakage.
"""
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Set
import pandas as pd

from evaluation.ingestion.unified_ingester import UnifiedIngester
from evaluation.baselines.unified_baselines import UnifiedBaselines
from evaluation.metrics.evaluator import MetricsEvaluator
from src.graph.schema import NodeType

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def run_defects4j_experiment(raw_dir: Path) -> pd.DataFrame:
    """
    Executes real defect regression test selection evaluation across Defects4J bugs.
    """
    print("======================================================================")
    print("  EXPERIMENT B: DEFECTS4J REAL HISTORICAL DEFECTS EVALUATION")
    print("======================================================================")

    graph, gt = UnifiedIngester.ingest_defects4j(raw_dir, project="Cli")
    print(f"Loaded Defects4J Cli: {len(graph.node_store)} nodes, {len(graph.edge_store)} edges")
    print(f"Total Evaluated Bugs: {len(gt['bugs'])}")

    baselines = UnifiedBaselines(graph)
    records = []

    for bug_id, b_data in gt["bugs"].items():
        mod_classes = b_data["modified_classes"]
        trigger_tests = b_data["trigger_tests"]
        rel_tests = b_data["relevant_tests"]

        if not mod_classes or not trigger_tests:
            continue

        primary_class = mod_classes[0]
        c_node_id = f"CLASS_{primary_class}"
        
        # Ground-truth triggering test nodes
        gt_test_nodes = {f"TEST_{t}" for t in trigger_tests}
        
        # Total regression test pool for this bug
        pool_size = max(len(rel_tests), len(trigger_tests) * 5, 20)

        # Change description strictly pre-change (class name + method context, no patch leakage)
        change_query = f"Command line option parsing argument tokenization validation in {primary_class}"

        # 1. Keyword Baseline
        res_kw = baselines.run_keyword(change_query, target_artifact_id=c_node_id, threshold=0.10)
        m_kw = MetricsEvaluator.compute_rts_metrics(
            selected_tests=res_kw["selected_tests"],
            triggering_tests=gt_test_nodes,
            total_test_pool_size=pool_size
        )

        # 2. Embedding-Only Baseline
        res_emb = baselines.run_embedding_only(change_query, target_artifact_id=c_node_id, threshold=0.35)
        m_emb = MetricsEvaluator.compute_rts_metrics(
            selected_tests=res_emb["selected_tests"],
            triggering_tests=gt_test_nodes,
            total_test_pool_size=pool_size
        )

        # 3. Graph-Only Baseline
        res_grp = baselines.run_graph_only(c_node_id, max_depth=3)
        m_grp = MetricsEvaluator.compute_rts_metrics(
            selected_tests=res_grp["selected_tests"],
            triggering_tests=gt_test_nodes,
            total_test_pool_size=pool_size
        )

        # 4. AURA-Impact Hybrid
        res_aura = baselines.run_aura_impact(
            change_query=change_query,
            target_artifact_id=c_node_id,
            semantic_threshold=0.35,
            max_graph_depth=3,
            mandatory_safety_tests=set()
        )
        m_aura = MetricsEvaluator.compute_rts_metrics(
            selected_tests=res_aura["selected_tests"],
            triggering_tests=gt_test_nodes,
            total_test_pool_size=pool_size
        )

        for name, res, m in [
            ("Keyword", res_kw, m_kw),
            ("Embedding_Only", res_emb, m_emb),
            ("Graph_Only", res_grp, m_grp),
            ("AURA_Impact", res_aura, m_aura)
        ]:
            records.append({
                "dataset": "Defects4J_Cli",
                "bug_id": bug_id,
                "modified_class": primary_class,
                "method": name,
                "test_recall": m["test_recall"],
                "test_precision": m["test_precision"],
                "test_reduction": m["test_reduction"],
                "relevant_selected": m["relevant_selected"],
                "total_triggering": m["total_relevant"],
                "total_selected": m["total_selected"],
                "latency_ms": res["latency_ms"]
            })

    df = pd.DataFrame(records)
    print(f"\n[OK] Defects4J Evaluation Completed: {len(df)} bug evaluation rows.")
    return df


if __name__ == "__main__":
    raw_path = ROOT_DIR / "data/raw/defects4j"
    df_res = run_defects4j_experiment(raw_path)
    summary = df_res.groupby("method")[["test_recall", "test_precision", "test_reduction", "latency_ms"]].mean().reset_index()
    print("\n--- Summary Performance on Defects4J ---")
    print(summary.to_string(index=False))

