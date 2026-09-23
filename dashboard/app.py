"""
AURA-Impact Production Prototype Dashboard (Locked Architecture B)
Interactive Streamlit UI for Change Impact Analysis, Visual Graph Traversal, Semantic Recovery, and Safety-Gated Regression Selection.
"""
import streamlit as st
import json
from pathlib import Path
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from src.api.pipeline import AuraImpactPipeline
from src.ingestion.git_diff import ChangedArtifact

st.set_page_config(
    page_title="AURA-Impact | Production Prototype",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.05rem; color: #94a3b8; margin-bottom: 1.5rem; }
    .metric-box { background-color: #1e293b; padding: 1rem; border-radius: 8px; border-left: 4px solid #38bdf8; }
    .tag-struct { color: #34d399; font-weight: bold; }
    .tag-sem { color: #38bdf8; font-weight: bold; }
    .tag-safety { color: #f87171; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_pipeline():
    p = AuraImpactPipeline()
    p.ingest_repository(Path("examples/demo_repo"))
    return p


pipeline = load_pipeline()

# Sidebar Navigation
st.sidebar.title("🛡️ AURA-Impact")
st.sidebar.caption("Locked Architecture B Prototype")
page = st.sidebar.radio(
    "Navigation",
    ["1. Change Analysis", "2. Visual Impact Graph", "3. Semantic Candidates", "4. Test Selection", "5. Evidence Report"]
)

# Demo Scenarios
st.sidebar.subheader("Load Demo Change")
demo_choice = st.sidebar.selectbox(
    "Select Scenario",
    [
        "Explicit Structural (REQ_AEB_001)",
        "Hidden Semantic Recovery (REQ_AEB_014)",
        "Semantic Decoy Rejection (REQ_BODY_005)",
        "Ambiguous Requirement (REQ_AMB_099)"
    ]
)

demo_file_map = {
    "Explicit Structural (REQ_AEB_001)": "examples/demo_repo/change_structural.json",
    "Hidden Semantic Recovery (REQ_AEB_014)": "examples/demo_repo/change_hidden_semantic.json",
    "Semantic Decoy Rejection (REQ_BODY_005)": "examples/demo_repo/change_decoy.json",
    "Ambiguous Requirement (REQ_AMB_099)": "examples/demo_repo/change_ambiguous.json"
}

with open(demo_file_map[demo_choice], "r", encoding="utf-8") as f:
    change_data = json.load(f)

change_obj = ChangedArtifact(
    artifact_id=change_data.get("artifact_id", "REQ_001"),
    artifact_type=change_data.get("artifact_type", "Requirement"),
    subsystem=change_data.get("subsystem", "ADAS"),
    ecu=change_data.get("ecu", "ECU_1"),
    change_type=change_data.get("change_type", "MODIFY"),
    after_content=change_data.get("after_content", ""),
    change_semantics=change_data.get("change_semantics", "")
)

# Run Analysis
impact_res, test_res, report = pipeline.analyze_change(change_obj)

# =============================================================================
# PAGE 1: CHANGE ANALYSIS
# =============================================================================
if page == "1. Change Analysis":
    st.markdown('<div class="main-header">Change Impact Analysis</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Evaluating change in <code>{change_obj.artifact_id}</code> ({change_obj.subsystem})</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Impacts", report.total_impacts_count)
    with col2:
        st.metric("Structural (Stage 1)", report.structural_impacts_count)
    with col3:
        st.metric("Semantic (Stage 2)", report.semantic_recoveries_count)
    with col4:
        st.metric("Tests Selected", f"{report.tests_selected_count} / {report.total_test_suite_size}", f"-{report.test_reduction_pct}%")

    st.subheader("Change Details")
    st.json(change_data)

    st.subheader("Impacted Engineering Artifacts")
    if report.impact_items:
        df_impacts = pd.DataFrame(report.impact_items)
        st.dataframe(df_impacts, use_container_width=True)
    else:
        st.info("No downstream impacts detected (Change isolated or rejected).")

# =============================================================================
# PAGE 2: VISUAL IMPACT GRAPH
# =============================================================================
elif page == "2. Visual Impact Graph":
    st.markdown('<div class="main-header">Multi-Layer Engineering Impact Graph</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Visualizing traceability paths: Requirement → SWC → Runnable → Function → Test</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    G = nx.DiGraph()

    root = change_obj.artifact_id
    G.add_node(root, label="[CHANGE]\n" + root, color="#38bdf8")

    for imp in impact_res.structural_impacts:
        G.add_node(imp.artifact_id, label=f"[STRUCT]\n{imp.artifact_id}", color="#34d399")
        G.add_edge(root, imp.artifact_id, label="EXPLICIT")

    for imp in impact_res.semantic_impacts:
        G.add_node(imp.artifact_id, label=f"[SEMANTIC]\n{imp.artifact_id}", color="#818cf8")
        G.add_edge(root, imp.artifact_id, label=f"SEMANTIC\n({imp.confidence:.2f})")

    for rev in impact_res.review_required_items:
        G.add_node(rev.artifact_id, label=f"[REVIEW]\n{rev.artifact_id}", color="#fbbf24")
        G.add_edge(root, rev.artifact_id, label="AMBIGUOUS")

    for t in test_res.selected_tests:
        G.add_node(t.test_id, label=f"[TEST]\n{t.test_id}", color="#f87171")
        G.add_edge(t.mapped_from_artifact, t.test_id, label="VERIFIES")

    pos = nx.spring_layout(G, seed=42)
    colors = [G.nodes[n].get("color", "#94a3b8") for n in G.nodes]

    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2800, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n].get("label", n) for n in G.nodes}, font_size=8, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color="#64748b", ax=ax)
    ax.axis("off")
    st.pyplot(fig)

# =============================================================================
# PAGE 3: SEMANTIC CANDIDATES
# =============================================================================
elif page == "3. Semantic Candidates":
    st.markdown('<div class="main-header">Semantic Retrieval & Context Filtering</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Stage 2 BGE-M3 candidate generation with hard engineering context constraints</div>', unsafe_allow_html=True)

    if impact_res.all_semantic_candidates:
        cand_rows = []
        for c in impact_res.all_semantic_candidates:
            cand_rows.append({
                "Artifact ID": c.artifact_id,
                "Type": c.artifact_type,
                "Subsystem": c.subsystem,
                "Similarity": round(c.similarity_score, 3),
                "Context Score": round(c.context_score, 2),
                "Status": c.status,
                "Rejection / Action Reason": c.rejection_reason or "Validated Context"
            })
        st.dataframe(pd.DataFrame(cand_rows), use_container_width=True)
    else:
        st.info("Stage 1 Graph Traversal was fully complete. Semantic fallback not required.")

# =============================================================================
# PAGE 4: TEST SELECTION
# =============================================================================
elif page == "4. Test Selection":
    st.markdown('<div class="main-header">Safety-Gated Regression Selection</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enforcing mandatory ASIL-C/D retention and optimizing regression execution</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Test Suite", test_res.all_tests_count)
    with col2:
        st.metric("Selected Tests", len(test_res.selected_tests))
    with col3:
        st.metric("Suite Reduction", f"{test_res.test_reduction_pct}%")

    st.subheader("Selected Test Suite")
    st.dataframe(pd.DataFrame(report.test_items), use_container_width=True)

# =============================================================================
# PAGE 5: EVIDENCE REPORT
# =============================================================================
elif page == "5. Evidence Report":
    st.markdown('<div class="main-header">Auditable Evidence Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Full provenance and decision justifications for ISO 26262 compliance</div>', unsafe_allow_html=True)

    st.json(json.loads(json.dumps(report, default=lambda o: o.__dict__)))
