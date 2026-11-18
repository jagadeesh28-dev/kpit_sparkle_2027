"""
Evaluation Metrics & Statistical Validation Module (evaluation/metrics/evaluator.py)
Implements formal metrics defined in Master Mission Section 8:
A. Dependency Recovery (Precision, Recall, F1, FPR)
B. Regression Test Selection (Test Recall, Test Precision, Test Suite Reduction)
C. Safety Validation (Safety Retention Invariant: T_safe <= T_selected)
D. Performance Telemetry (Latency ms, Memory MB)
E. Statistical Significance Testing (Paired Wilcoxon Signed-Rank Test)
"""
import time
import numpy as np
from typing import Dict, Any, List, Set, Optional, Tuple
from scipy import stats


class MetricsEvaluator:
    """Computes dependency recovery, regression test selection, and safety metrics."""

    @staticmethod
    def compute_dependency_metrics(
        predicted: Set[str] | List[str],
        ground_truth: Set[str] | List[str],
        total_universe_size: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Computes Precision, Recall, F1, and False Positive Rate (FPR).
        """
        pred_set = set(predicted)
        gt_set = set(ground_truth)

        tp = len(pred_set & gt_set)
        fp = len(pred_set - gt_set)
        fn = len(gt_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        fpr = 0.0
        if total_universe_size is not None and total_universe_size > len(gt_set):
            tn = max(0, total_universe_size - len(gt_set) - fp)
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        return {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "fpr": round(fpr, 4)
        }

    @staticmethod
    def compute_rts_metrics(
        selected_tests: Set[str] | List[str],
        triggering_tests: Set[str] | List[str],
        total_test_pool_size: int
    ) -> Dict[str, float]:
        """
        Computes Test Selection Recall, Test Selection Precision, and Test Suite Reduction.
        """
        sel_set = set(selected_tests)
        trig_set = set(triggering_tests)

        relevant_selected = len(sel_set & trig_set)
        total_relevant = len(trig_set)
        total_selected = len(sel_set)

        test_recall = (relevant_selected / total_relevant) if total_relevant > 0 else 1.0
        test_precision = (relevant_selected / total_selected) if total_selected > 0 else 0.0

        total_pool = max(1, total_test_pool_size)
        test_reduction = 1.0 - (total_selected / total_pool)

        return {
            "relevant_selected": relevant_selected,
            "total_relevant": total_relevant,
            "total_selected": total_selected,
            "test_recall": round(test_recall, 4),
            "test_precision": round(test_precision, 4),
            "test_reduction": round(max(0.0, test_reduction), 4)
        }

    @staticmethod
    def compute_safety_retention(
        selected_tests: Set[str] | List[str],
        safety_critical_tests: Set[str] | List[str]
    ) -> Dict[str, Any]:
        """
        Validates the Mandatory Safety Invariant:
        T_safe SUBSET_OF T_selected (Safety Retention = 100.0%)
        """
        sel_set = set(selected_tests)
        safe_set = set(safety_critical_tests)

        if not safe_set:
            return {"safety_retention_pct": 100.0, "omitted_safety_tests": [], "invariant_satisfied": True}

        retained = sel_set & safe_set
        omitted = safe_set - sel_set
        retention_pct = (len(retained) / len(safe_set)) * 100.0

        return {
            "safety_retention_pct": round(retention_pct, 2),
            "omitted_safety_tests": list(omitted),
            "invariant_satisfied": (len(omitted) == 0)
        }

    @staticmethod
    def compute_statistical_significance(
        series_a: List[float],
        series_b: List[float]
    ) -> Dict[str, Any]:
        """
        Runs a paired Wilcoxon signed-rank test comparing two baselines.
        """
        if len(series_a) != len(series_b) or len(series_a) < 5:
            return {"statistic": None, "p_value": None, "significant": False}

        diffs = [a - b for a, b in zip(series_a, series_b)]
        if all(d == 0 for d in diffs):
            return {"statistic": 0.0, "p_value": 1.0, "significant": False}

        try:
            res = stats.wilcoxon(series_a, series_b)
            return {
                "statistic": float(res.statistic),
                "p_value": float(res.pvalue),
                "significant": bool(res.pvalue < 0.05)
            }
        except Exception:
            return {"statistic": None, "p_value": None, "significant": False}

