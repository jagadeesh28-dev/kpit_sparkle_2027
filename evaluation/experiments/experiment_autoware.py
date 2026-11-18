"""
Experiment C: Autoware.Universe Production Automotive Architecture Validation
(evaluation/experiments/experiment_autoware.py)

Evaluates:
- Real-World ROS 2 / C++ Autonomous Driving Architecture (AEB & Vehicle Cmd Gate)
- Representative Automotive Change Scenarios (Braking Threshold, Actuation Command, Interface Update, Doc Decoy)
- Comparative Evaluation: Keyword, Embedding-Only, Graph-Only, AURA-Impact
- Metrics: Precision, Recall, F1, Decoy Rejection, Safety Gate Preservation, Latency
"""
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

from evaluation.ingestion.unified_ingester import UnifiedIngester
from evaluation.baselines.unified_baselines import UnifiedBaselines
from evaluation.metrics.evaluator import MetricsEvaluator

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def run_autoware_experiment(raw_dir: Path) -> pd.DataFrame:
    """
    Executes automotive architecture change impact validation on Autoware.Universe.
    """
    print("======================================================================")
    print("  EXPERIMENT C: AUTOWARE.UNIVERSE AUTOMOTIVE ARCHITECTURE VALIDATION")
    print("======================================================================")

    graph, gt = UnifiedIngester.ingest_autoware(raw_dir)
    print(f"Loaded Autoware.Universe: {len(graph.node_store)} nodes, {len(graph.edge_store)} edges")

    baselines = UnifiedBaselines(graph)

    # Define realistic automotive change scenarios
    scenarios = [
        {
            "id": "AUTOWARE_SCN_01",
            "name": "AEB Deceleration Parameter Calibration",
            "target_artifact": "NODE_autoware_aeb",
            "query": "Autonomous emergency braking collision detection deceleration clamp threshold calibration",
            "ground_truth": {"NODE_autoware_aeb", "PACKAGE_autoware_autonomous_emergency_braking", "PACKAGE_autoware_vehicle_cmd_gate"},
            "is_safety_critical": True
        },
        {
            "id": "AUTOWARE_SCN_02",
            "name": "Vehicle Command Gate Emergency Stop Interface",
            "target_artifact": "PACKAGE_autoware_vehicle_cmd_gate",
            "query": "Emergency stop command gate override actuation signal transmission",
            "ground_truth": {"PACKAGE_autoware_vehicle_cmd_gate", "PACKAGE_autoware_autonomous_emergency_braking"},
            "is_safety_critical": True
        },
        {
            "id": "AUTOWARE_SCN_03",
            "name": "Motion Velocity Dependency Update",
            "target_artifact": "PACKAGE_autoware_motion_velocity_planner",
            "query": "Motion velocity trajectory planning speed profile calculation",
            "ground_truth": {"PACKAGE_autoware_motion_velocity_planner", "PACKAGE_autoware_autonomous_emergency_braking"},
            "is_safety_critical": False
        },
        {
            "id": "AUTOWARE_SCN_04",
            "name": "Markdown Documentation Clean-up (Decoy)",
            "target_artifact": "NODE_autoware_aeb",
            "query": "Update developer README and markdown formatting guidelines for package contributors",
            "ground_truth": set(),
            "is_safety_critical": False
        }
    ]

    records = []
    for scn in scenarios:
        tgt = scn["target_artifact"]
        query = scn["query"]
        gt_set = scn["ground_truth"]

        # 1. Keyword Baseline
        res_kw = baselines.run_keyword(query, target_artifact_id=tgt, threshold=0.15)
        m_kw = MetricsEvaluator.compute_dependency_metrics(res_kw["impacted_artifacts"], gt_set, len(graph.node_store))

        # 2. Embedding-Only Baseline
        res_emb = baselines.run_embedding_only(query, target_artifact_id=tgt, threshold=0.45)
        m_emb = MetricsEvaluator.compute_dependency_metrics(res_emb["impacted_artifacts"], gt_set, len(graph.node_store))

        # 3. Graph-Only Baseline
        res_grp = baselines.run_graph_only(tgt, max_depth=3)
        m_grp = MetricsEvaluator.compute_dependency_metrics(res_grp["impacted_artifacts"], gt_set, len(graph.node_store))

        # 4. AURA-Impact Hybrid
        res_aura = baselines.run_aura_impact(
            change_query=query,
            target_artifact_id=tgt,
            semantic_threshold=0.45,
            max_graph_depth=3,
            mandatory_safety_tests={"TEST_autoware_aeb_test"} if scn["is_safety_critical"] else set()
        )
        m_aura = MetricsEvaluator.compute_dependency_metrics(res_aura["impacted_artifacts"], gt_set, len(graph.node_store))

        for name, res, m in [
            ("Keyword", res_kw, m_kw),
            ("Embedding_Only", res_emb, m_emb),
            ("Graph_Only", res_grp, m_grp),
            ("AURA_Impact", res_aura, m_aura)
        ]:
            records.append({
                "dataset": "Autoware.Universe",
                "scenario_id": scn["id"],
                "scenario_name": scn["name"],
                "method": name,
                "precision": m["precision"],
                "recall": m["recall"],
                "f1": m["f1"],
                "fpr": m["fpr"],
                "safety_retained": "TEST_autoware_aeb_test" in res["selected_tests"] if scn["is_safety_critical"] else True,
                "latency_ms": res["latency_ms"]
            })

    df = pd.DataFrame(records)
    print(f"\n[OK] Autoware Evaluation Completed: {len(df)} evaluation rows.")
    return df


if __name__ == "__main__":
    raw_path = ROOT_DIR / "data/raw/autoware"
    df_res = run_autoware_experiment(raw_path)
    summary = df_res.groupby("method")[["precision", "recall", "f1", "fpr", "latency_ms"]].mean().reset_index()
    print("\n--- Summary Performance on Autoware.Universe ---")
    print(summary.to_string(index=False))

