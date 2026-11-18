"""
Publication-Quality Visualization Generator (evaluation/reports/plotter.py)
Generates high-resolution figures from actual experimental outputs into results/plots/:
1. fig01_precision_recall_f1.png
2. fig02_hidden_dependency_recovery_by_rate.png
3. fig03_false_positive_rate_comparison.png
4. fig04_regression_test_selection_and_reduction.png
5. fig05_safety_test_retention_invariant.png
6. fig06_execution_latency_comparison.png
7. fig07_architecture_ablation_study.png
8. fig08_dataset_cross_comparison.png
"""
import os
import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# Modern Clean Dark/Light Scientific Palette
COLORS = {
    "Keyword": "#64748b",         # Slate Grey
    "Embedding_Only": "#38bdf8",   # Sky Blue
    "Graph_Only": "#f59e0b",       # Amber Orange
    "AURA_Impact": "#10b981",      # Emerald Green
    "Safety": "#ef4444"            # Crimson Red
}


class PublicationPlotter:
    """Generates publication-ready figures grounded strictly in measured experiment CSVs."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.dpi": 300,
            "savefig.bbox": "tight"
        })

    def plot_all(
        self,
        df_dronology: pd.DataFrame,
        df_defects4j: pd.DataFrame,
        df_autoware: pd.DataFrame,
        df_alexandria: pd.DataFrame
    ):
        print(f"Generating publication plots in {self.output_dir}...")
        self.plot_precision_recall_f1(df_dronology, df_autoware)
        self.plot_hidden_recovery_by_rate(df_dronology)
        self.plot_false_positive_rates(df_dronology, df_autoware)
        self.plot_rts_and_reduction(df_defects4j)
        self.plot_safety_retention(df_dronology, df_autoware)
        self.plot_latency(df_dronology, df_defects4j, df_autoware)
        self.plot_ablation(df_dronology)
        self.plot_dataset_comparison(df_dronology, df_defects4j, df_autoware)
        print("[OK] All 8 publication figures generated successfully.")

    def plot_precision_recall_f1(self, df_dron: pd.DataFrame, df_auto: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(7, 4.2))
        combined = pd.concat([df_dron, df_auto], ignore_index=True)
        agg = combined.groupby("method")[["precision", "recall", "f1"]].mean().reindex(
            ["Keyword", "Embedding_Only", "Graph_Only", "AURA_Impact"]
        )

        x = np.arange(len(agg))
        width = 0.25

        ax.bar(x - width, agg["precision"], width, label="Precision", color="#38bdf8", edgecolor="#0284c7")
        ax.bar(x, agg["recall"], width, label="Recall", color="#10b981", edgecolor="#059669")
        ax.bar(x + width, agg["f1"], width, label="F1-Score", color="#8b5cf6", edgecolor="#6d28d9")

        ax.set_ylabel("Metric Score (0.0 - 1.0)")
        ax.set_title("Dependency Recovery Performance Across Baselines (Public Datasets)")
        ax.set_xticks(x)
        ax.set_xticklabels(["Keyword\n(TF-IDF)", "Embedding\n(384-d)", "Graph\n(BFS)", "AURA-Impact\n(Hybrid)"])
        ax.set_ylim(0, 1.1)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.legend(frameon=True)

        for i in x:
            f1_val = agg["f1"].iloc[i]
            ax.text(i + width, f1_val + 0.02, f"{f1_val:.2f}", ha="center", fontsize=8, fontweight="bold")

        fig.savefig(self.output_dir / "fig01_precision_recall_f1.png")
        plt.close(fig)

    def plot_hidden_recovery_by_rate(self, df_dron: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6.5, 4))
        rates = [0.10, 0.20, 0.30]
        methods = ["Keyword", "Embedding_Only", "Graph_Only", "AURA_Impact"]
        styles = {"Keyword": ("--", "o"), "Embedding_Only": ("-.", "s"), "Graph_Only": (":", "x"), "AURA_Impact": ("-", "D")}

        for m in methods:
            m_sub = df_dron[df_dron["method"] == m]
            rec_means = [m_sub[m_sub["deletion_rate"] == r]["recall"].mean() for r in rates]
            ls, marker = styles[m]
            ax.plot([f"{int(r*100)}%" for r in rates], rec_means, label=m.replace("_", " "), color=COLORS.get(m, "#000"), linestyle=ls, marker=marker, linewidth=2, markersize=6)

        ax.set_xlabel("Controlled Trace-Link Deletion Rate")
        ax.set_ylabel("Hidden Dependency Recovery Recall")
        ax.set_title("Traceability Recovery Under Controlled Synthetic Link Deletion (Dronology)")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend(frameon=True)

        fig.savefig(self.output_dir / "fig02_hidden_dependency_recovery_by_rate.png")
        plt.close(fig)

    def plot_false_positive_rates(self, df_dron: pd.DataFrame, df_auto: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6, 3.8))
        combined = pd.concat([df_dron, df_auto], ignore_index=True)
        fpr_agg = combined.groupby("method")["fpr"].mean().reindex(["Keyword", "Embedding_Only", "Graph_Only", "AURA_Impact"])

        bars = ax.bar(["Keyword", "Embedding-Only\n(Raw)", "Graph-Only\n(BFS)", "AURA-Impact\n(Filtered)"], fpr_agg.values, color=["#64748b", "#ef4444", "#f59e0b", "#10b981"], width=0.55)
        ax.set_ylabel("False Positive Rate (FPR)")
        ax.set_title("Distractor & Decoy False Positive Rate Suppression")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.005, f"{yval*100:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

        fig.savefig(self.output_dir / "fig03_false_positive_rate_comparison.png")
        plt.close(fig)

    def plot_rts_and_reduction(self, df_defects: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(7, 4))
        agg = df_defects.groupby("method")[["test_recall", "test_reduction"]].mean().reindex(["Keyword", "Embedding_Only", "Graph_Only", "AURA_Impact"])

        x = np.arange(len(agg))
        width = 0.35

        ax.bar(x - width/2, agg["test_recall"], width, label="Triggering Test Recall", color="#38bdf8")
        ax.bar(x + width/2, agg["test_reduction"], width, label="Test Suite Reduction", color="#10b981")

        ax.set_ylabel("Ratio (0.0 - 1.0)")
        ax.set_title("Real Defect Test Selection: Recall vs Suite Reduction (Defects4J)")
        ax.set_xticks(x)
        ax.set_xticklabels(["Keyword", "Embedding", "Graph", "AURA-Impact"])
        ax.set_ylim(0, 1.15)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.legend(frameon=True)

        fig.savefig(self.output_dir / "fig04_regression_test_selection_and_reduction.png")
        plt.close(fig)

    def plot_safety_retention(self, df_dron: pd.DataFrame, df_auto: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6, 3.8))
        d_safe = df_dron.groupby("method")["safety_retention_pct"].mean().reindex(["Keyword", "Embedding_Only", "Graph_Only", "AURA_Impact"])

        bars = ax.bar(["Keyword", "Embedding", "Graph", "AURA-Impact\n(Safety Gate)"], d_safe.values, color=["#94a3b8", "#94a3b8", "#f59e0b", "#10b981"], width=0.55)
        ax.axhline(100.0, color="#ef4444", linestyle="--", label="Mandatory Invariant (100%)")
        ax.set_ylabel("Safety-Critical Test Retention (%)")
        ax.set_title("Mandatory Safety Test Retention Under ISO 26262 Invariant")
        ax.set_ylim(0, 115)
        ax.legend(loc="lower right")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 2, f"{yval:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

        fig.savefig(self.output_dir / "fig05_safety_test_retention_invariant.png")
        plt.close(fig)

    def plot_latency(self, df_dron: pd.DataFrame, df_def: pd.DataFrame, df_auto: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6.5, 3.8))
        comb = pd.concat([df_dron, df_def, df_auto], ignore_index=True)
        lat = comb.groupby("method")["latency_ms"].mean().reindex(["Keyword", "Embedding_Only", "Graph_Only", "AURA_Impact"])

        bars = ax.bar(["Keyword\n(TF-IDF)", "Embedding\n(384-d)", "Graph\n(BFS)", "AURA-Impact\n(Hybrid)"], lat.values, color=["#64748b", "#38bdf8", "#f59e0b", "#10b981"], width=0.55)
        ax.set_ylabel("Mean Execution Latency (ms)")
        ax.set_title("End-to-End Analysis Latency Across Evaluation Baselines")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.02, f"{yval:.2f} ms", ha="center", va="bottom", fontsize=9, fontweight="bold")

        fig.savefig(self.output_dir / "fig06_execution_latency_comparison.png")
        plt.close(fig)

    def plot_ablation(self, df_dron: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6.5, 3.8))
        # Architectural progression
        configs = ["Graph-Only", "Embedding-Only (Raw)", "AURA-Impact (Full Hybrid)"]
        f1_vals = [
            df_dron[df_dron["method"] == "Graph_Only"]["f1"].mean(),
            df_dron[df_dron["method"] == "Embedding_Only"]["f1"].mean(),
            df_dron[df_dron["method"] == "AURA_Impact"]["f1"].mean()
        ]

        bars = ax.bar(configs, f1_vals, color=["#f59e0b", "#38bdf8", "#10b981"], width=0.5)
        ax.set_ylabel("F1 Score")
        ax.set_title("Architectural Component Contribution Ablation (Dronology)")
        ax.set_ylim(0, 1.0)
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.02, f"{yval:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

        fig.savefig(self.output_dir / "fig07_architecture_ablation_study.png")
        plt.close(fig)

    def plot_dataset_comparison(self, df_dron: pd.DataFrame, df_def: pd.DataFrame, df_auto: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(7, 4))
        datasets = ["Dronology (CPS)", "Defects4J (Bugs)", "Autoware (Automotive)"]
        aura_recalls = [
            df_dron[df_dron["method"] == "AURA_Impact"]["recall"].mean(),
            df_def[df_def["method"] == "AURA_Impact"]["test_recall"].mean(),
            df_auto[df_auto["method"] == "AURA_Impact"]["recall"].mean()
        ]

        bars = ax.bar(datasets, aura_recalls, color=["#0284c7", "#059669", "#7c3aed"], width=0.45)
        ax.set_ylabel("Recall Score")
        ax.set_title("AURA-Impact Generalization Across Heterogeneous Public Datasets")
        ax.set_ylim(0, 1.15)
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.02, f"{yval*100:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

        fig.savefig(self.output_dir / "fig08_dataset_cross_comparison.png")
        plt.close(fig)
