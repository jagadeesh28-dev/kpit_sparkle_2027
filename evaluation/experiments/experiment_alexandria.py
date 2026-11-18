"""
Experiment D: Alexandria Historical Co-Change Mining & Proxy Relationship Validation
(evaluation/experiments/experiment_alexandria.py)

Evaluates:
- Historical Git commit co-change pairs extracted across autonomous and systems software
- Prediction of co-modifications lacking explicit static call graph links
- Evaluates Semantic Recovery against Historical Evolution as a supplementary proxy metric
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np

from evaluation.ingestion.unified_ingester import UnifiedIngester
from src.semantic.embedder import SemanticEmbedder

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def run_alexandria_experiment(raw_dir: Path) -> pd.DataFrame:
    """
    Evaluates semantic recovery on historical co-change pairs.
    """
    print("======================================================================")
    print("  EXPERIMENT D: ALEXANDRIA HISTORICAL CO-CHANGE EVOLUTION")
    print("======================================================================")

    pairs = UnifiedIngester.ingest_alexandria(raw_dir)
    print(f"Loaded Alexandria: {len(pairs)} historical co-change records")

    embedder = SemanticEmbedder()
    records = []

    for p in pairs:
        file_a = p["file_a"]
        file_b = p["file_b"]
        co_count = p["co_change_count"]
        support = p["support"]
        has_static = p["has_direct_static_call"]

        # Compute semantic similarity between file paths/names
        vec_a = embedder.embed_text(file_a)
        vec_b = embedder.embed_text(file_b)
        cosine_sim = float(np.dot(vec_a, vec_b))

        # Prediction thresholds
        sem_predicted = bool(cosine_sim >= 0.40)
        graph_predicted = bool(has_static)
        aura_predicted = bool(has_static or sem_predicted)

        records.append({
            "dataset": "Alexandria_Evolution",
            "file_a": file_a,
            "file_b": file_b,
            "co_change_count": co_count,
            "co_change_support": support,
            "has_direct_static_call": has_static,
            "cosine_similarity": round(cosine_sim, 4),
            "graph_only_recovered": graph_predicted,
            "embedding_only_recovered": sem_predicted,
            "aura_impact_recovered": aura_predicted
        })

    df = pd.DataFrame(records)
    print(f"\n[OK] Alexandria Evaluation Completed: {len(df)} co-change evaluations.")
    return df


if __name__ == "__main__":
    raw_path = ROOT_DIR / "data/raw/alexandria"
    df_res = run_alexandria_experiment(raw_path)
    print("\n--- Alexandria Co-Change Recovery Summary ---")
    print(df_res[["file_a", "file_b", "has_direct_static_call", "cosine_similarity", "aura_impact_recovered"]].to_string(index=False))

