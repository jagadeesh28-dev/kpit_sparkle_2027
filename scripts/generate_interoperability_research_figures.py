"""
AURA-Impact: Autonomous Interoperability Research Study Figure Generator.
Generates publication-quality diagrams and charts for the deep research study.
Outputs to research/autonomous_interoperability/figures/ in both PNG (300 DPI) and vector SVG.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
import numpy as np

OUTPUT_DIR = os.path.join("research", "autonomous_interoperability", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Executive Color Palette (Engineering Slate, Navy, Teal, Indigo, Alert Red, Success Green)
COLOR_NAVY = "#0F172A"       # Slate 900
COLOR_SLATE = "#475569"      # Slate 600
COLOR_LIGHT_BG = "#F8FAFC"   # Slate 50
COLOR_BORDER = "#CBD5E1"     # Slate 300
COLOR_PRIMARY = "#0284C7"    # Sky 600
COLOR_AURA = "#0D9488"       # Teal 600
COLOR_GRAPH = "#2563EB"      # Blue 600
COLOR_EMBED = "#7C3AED"      # Purple 600
COLOR_SUCCESS = "#16A34A"    # Green 600
COLOR_ALERT = "#DC2626"      # Red 600
COLOR_AMBER = "#D97706"      # Amber 600
COLOR_CARD = "#FFFFFF"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['text.color'] = COLOR_NAVY
plt.rcParams['axes.labelcolor'] = COLOR_NAVY
plt.rcParams['xtick.color'] = COLOR_NAVY
plt.rcParams['ytick.color'] = COLOR_NAVY

def save_fig(fig, name):
    png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    svg_path = os.path.join(OUTPUT_DIR, f"{name}.svg")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.savefig(svg_path)
    plt.close()
    print(f"Generated: {name}")


# ==============================================================================
# FIGURE 1: Modern Autonomous System Software Engineering Stack
# ==============================================================================
def generate_fig1_autonomous_stack():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 12)
    ax.axis('off')

    layers = [
        ("LAYER 7: FLEET & CLOUD MLOPS", "Shadow mode data logging, active learning, digital twin simulation, OTA lifecycle (ISO 24089)", "#F1F5F9", COLOR_SLATE),
        ("LAYER 6: INDEPENDENT SAFETY MONITOR (MRM)", "Deterministic ASIL-D safety shield, RSS boundary checkers, minimum risk maneuver fallback", "#FEF2F2", COLOR_ALERT),
        ("LAYER 5: BEHAVIORAL PLANNING & CONTROL", "Behavioral state machine, cost-function trajectory optimization, lateral/longitudinal MPC", "#EFF6FF", COLOR_GRAPH),
        ("LAYER 4: WORLD MODEL & SCENE PREDICTION", "Multi-modal occupancy grids, agent trajectory forecasting, vectorized HD map fusion", "#FAF5FF", COLOR_EMBED),
        ("LAYER 3: PERCEPTION & STATE ESTIMATION", "Object detection/tracking, semantic segmentation, visual/LiDAR SLAM, RTK-GNSS/IMU sync", "#F0FDFA", COLOR_AURA),
        ("LAYER 2: SENSOR ABSTRACTION & MIDDLEWARE", "ISO 23150 sensor interfaces, SOME/IP, DDS, ROS 2, time synchronization (IEEE 802.1AS)", "#F0F9FF", COLOR_PRIMARY),
        ("LAYER 1: COMPUTE & OPERATING SYSTEM", "Heterogeneous SoCs (CPU+GPU+NPU+Safety Island), RTOS (QNX, VxWorks), POSIX Linux", "#F8FAFC", COLOR_NAVY),
        ("LAYER 0: PHYSICAL SENSORS & ACTUATORS", "Surround cameras, imaging radars, LiDARs, ultrasonics, steer-by-wire, brake-by-wire", "#E2E8F0", COLOR_SLATE)
    ]

    y_start = 10.5
    h = 0.95
    spacing = 1.25

    for i, (title, desc, bg_col, border_col) in enumerate(layers):
        y = y_start - i * spacing
        box = FancyBboxPatch((0.6, y - h), 9.8, h, boxstyle="round,pad=0.04", fc=bg_col, ec=border_col, lw=1.6)
        ax.add_patch(box)
        ax.text(0.9, y - 0.32, title, fontsize=10.5, fontweight='bold', color=border_col)
        ax.text(0.9, y - 0.68, desc, fontsize=8.8, color=COLOR_NAVY)

    ax.text(5.5, 11.4, "FIGURE 1: Canonical Autonomous System Software Architecture", ha='center', fontsize=14, fontweight='bold', color=COLOR_NAVY)
    save_fig(fig, "fig01_autonomous_system_stack")


# ==============================================================================
# FIGURE 2: Waymo Architecture Overview
# ==============================================================================
def generate_fig2_waymo():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Header Card
    top = FancyBboxPatch((0.5, 8.4), 9.0, 1.2, boxstyle="round,pad=0.04", fc="#EFF6FF", ec=COLOR_GRAPH, lw=1.6)
    ax.add_patch(top)
    ax.text(5.0, 9.2, "WAYMO DRIVER (5th & 6th Gen): Vertically Integrated Robotaxi Stack", ha='center', fontsize=12, fontweight='bold', color=COLOR_GRAPH)
    ax.text(5.0, 8.7, "Commercial Fleet Operator Model • Fully Proprietary Vertical Integration • Closed Ecosystem", ha='center', fontsize=9, color=COLOR_SLATE)

    # 3 Columns
    col_w = 2.8
    # Col 1: Hardware & Sensors
    c1 = FancyBboxPatch((0.5, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc=COLOR_LIGHT_BG, ec=COLOR_BORDER, lw=1.4)
    ax.add_patch(c1)
    ax.text(1.9, 7.5, "SENSING & COMPUTE", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    c1_text = (
        "• Custom proprietary LiDARs\n"
        "  (Perimeter & long-range)\n"
        "• 360-degree cameras\n"
        "• High-res imaging radar\n"
        "• External audio receivers\n\n"
        "• Custom Onboard Compute:\n"
        "  - High-performance CPUs\n"
        "  - Custom Google TPU / AI\n"
        "  - Redundant safety compute"
    )
    ax.text(0.7, 4.6, c1_text, fontsize=8.5, color=COLOR_NAVY)

    # Col 2: Software Stack
    c2 = FancyBboxPatch((3.6, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc=COLOR_LIGHT_BG, ec=COLOR_BORDER, lw=1.4)
    ax.add_patch(c2)
    ax.text(5.0, 7.5, "SOFTWARE & AI", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    c2_text = (
        "• Hardened custom Linux OS\n"
        "• Modular deep neural nets:\n"
        "  - Perception & tracking\n"
        "  - Behavior prediction\n"
        "• Rule-based & optimization\n"
        "  planning engine\n"
        "• High-definition (HD) maps\n\n"
        "• Proprietary low-latency\n"
        "  IPC/RPC messaging"
    )
    ax.text(3.8, 4.6, c2_text, fontsize=8.5, color=COLOR_NAVY)

    # Col 3: Safety & Interoperability
    c3 = FancyBboxPatch((6.7, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc="#FEF2F2", ec=COLOR_ALERT, lw=1.6)
    ax.add_patch(c3)
    ax.text(8.1, 7.5, "SAFETY & INTEGRATION", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_ALERT)
    c3_text = (
        "• Independent Safety\n"
        "  Supervisor & fallback\n"
        "• Simulation City validation\n"
        "  (Billions of virtual miles)\n"
        "• ANSI/UL 4600 safety case\n\n"
        "• Interoperability Stance:\n"
        "  STRICTLY CLOSED.\n"
        "  Zero public semantic API;\n"
        "  Interacts purely via\n"
        "  physical road behavior."
    )
    ax.text(6.9, 4.6, c3_text, fontsize=8.5, color=COLOR_NAVY)

    # Bottom Callout
    bot = FancyBboxPatch((0.5, 0.4), 9.0, 1.2, boxstyle="round,pad=0.04", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(bot)
    ax.text(5.0, 1.15, "ARCHITECTURAL ASSESSMENT: Highest safety rigor, but represents a complete walled garden.",
            ha='center', fontsize=10, fontweight='bold', color="#FFFFFF")
    ax.text(5.0, 0.70, "Proves Level 4 commercial feasibility without requiring external multi-vendor semantic protocols.",
            ha='center', fontsize=8.5, color=COLOR_BORDER)

    save_fig(fig, "fig02_waymo_architecture")


# ==============================================================================
# FIGURE 3: Tesla Architecture Overview
# ==============================================================================
def generate_fig3_tesla():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Header Card
    top = FancyBboxPatch((0.5, 8.4), 9.0, 1.2, boxstyle="round,pad=0.04", fc="#FEF2F2", ec=COLOR_ALERT, lw=1.6)
    ax.add_patch(top)
    ax.text(5.0, 9.2, "TESLA FULL SELF-DRIVING (FSD V12+): Vision-Only End-to-End Neural Stack", ha='center', fontsize=12, fontweight='bold', color=COLOR_ALERT)
    ax.text(5.0, 8.7, "Consumer OEM Model • Anti-Standard Philosophy • Direct Photon-to-Control Neural Networks", ha='center', fontsize=9, color=COLOR_SLATE)

    col_w = 2.8
    # Col 1: Hardware & Sensors
    c1 = FancyBboxPatch((0.5, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc=COLOR_LIGHT_BG, ec=COLOR_BORDER, lw=1.4)
    ax.add_patch(c1)
    ax.text(1.9, 7.5, "SENSING & SILICON", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    c1_text = (
        "• Pure Vision Philosophy:\n"
        "  - 8 optical surround cameras\n"
        "  - Zero LiDAR\n"
        "  - Zero Radar (removed)\n"
        "  - Zero Ultrasonics (removed)\n\n"
        "• Custom FSD Computer:\n"
        "  - HW3 (144 TOPS)\n"
        "  - HW4 (300+ TOPS)\n"
        "  - Dual redundant NPU chips"
    )
    ax.text(0.7, 4.6, c1_text, fontsize=8.5, color=COLOR_NAVY)

    # Col 2: Software & AI Model
    c2 = FancyBboxPatch((3.6, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc=COLOR_LIGHT_BG, ec=COLOR_BORDER, lw=1.4)
    ax.add_patch(c2)
    ax.text(5.0, 7.5, "END-TO-END AI", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    c2_text = (
        "• End-to-End Transformer:\n"
        "  Photons in → Trajectory out\n"
        "• Replaced 300k+ lines of C++\n"
        "  heuristic planning code\n"
        "• Trained on millions of hours\n"
        "  of human driving video\n\n"
        "• Dojo & H100 GPU clusters\n"
        "• Zero HD maps (relies on\n"
        "  online spatial memory)"
    )
    ax.text(3.8, 4.6, c2_text, fontsize=8.5, color=COLOR_NAVY)

    # Col 3: Fleet Loop & Integration Stance
    c3 = FancyBboxPatch((6.7, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc="#FEF2F2", ec=COLOR_ALERT, lw=1.6)
    ax.add_patch(c3)
    ax.text(8.1, 7.5, "INTEGRATION STANCE", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_ALERT)
    c3_text = (
        "• Massive Fleet Data Loop:\n"
        "  - Millions of customer cars\n"
        "  - Shadow mode edge triggers\n"
        "  - Rapid OTA iterations\n\n"
        "• Interoperability Stance:\n"
        "  ACTIVELY ANTI-STANDARD.\n"
        "  Rejects V2X, AUTOSAR,\n"
        "  and external interfaces.\n"
        "  Believes intelligence alone\n"
        "  must navigate roads."
    )
    ax.text(6.9, 4.6, c3_text, fontsize=8.5, color=COLOR_NAVY)

    # Bottom Callout
    bot = FancyBboxPatch((0.5, 0.4), 9.0, 1.2, boxstyle="round,pad=0.04", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(bot)
    ax.text(5.0, 1.15, "ARCHITECTURAL ASSESSMENT: Brilliant consumer data engine, but fundamentally hostile to interoperability.",
            ha='center', fontsize=10, fontweight='bold', color="#FFFFFF")
    ax.text(5.0, 0.70, "Demonstrates that single-agent vision can scale, but offers zero framework for cooperative multi-agent autonomy.",
            ha='center', fontsize=8.5, color=COLOR_BORDER)

    save_fig(fig, "fig03_tesla_architecture")


# ==============================================================================
# FIGURE 4: NVIDIA DRIVE Platform Architecture
# ==============================================================================
def generate_fig4_nvidia():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Header Card
    top = FancyBboxPatch((0.5, 8.4), 9.0, 1.2, boxstyle="round,pad=0.04", fc="#F0FDF4", ec=COLOR_SUCCESS, lw=1.6)
    ax.add_patch(top)
    ax.text(5.0, 9.2, "NVIDIA DRIVE / HYPERION: Open Automotive Platform & Compute Ecosystem", ha='center', fontsize=12, fontweight='bold', color=COLOR_SUCCESS)
    ax.text(5.0, 8.7, "Tier-2/Tier-1 Platform Provider • Modular SoC, OS & SDKs • Powers Global OEMs (Mercedes, Volvo, JLR)", ha='center', fontsize=9, color=COLOR_SLATE)

    col_w = 2.8
    # Col 1: Silicon & Hardware
    c1 = FancyBboxPatch((0.5, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc=COLOR_LIGHT_BG, ec=COLOR_BORDER, lw=1.4)
    ax.add_patch(c1)
    ax.text(1.9, 7.5, "DRIVE HARDWARE", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    c1_text = (
        "• Scalable System-on-Chip:\n"
        "  - DRIVE Orin (254 TOPS)\n"
        "  - DRIVE Thor (1000+ TOPS)\n"
        "• Heterogeneous Compute:\n"
        "  - ARM Cortex-A CPUs\n"
        "  - Blackwell/Ampere GPUs\n"
        "  - Deep Learning Accel (DLA)\n"
        "  - Programmable Vision (PVA)\n"
        "  - ASIL-D Lockstep Cortex-R"
    )
    ax.text(0.7, 4.6, c1_text, fontsize=8.5, color=COLOR_NAVY)

    # Col 2: Software & Middleware
    c2 = FancyBboxPatch((3.6, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc=COLOR_LIGHT_BG, ec=COLOR_BORDER, lw=1.4)
    ax.add_patch(c2)
    ax.text(5.0, 7.5, "DRIVE OS & MIDDLEWARE", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    c2_text = (
        "• DRIVE OS:\n"
        "  - QNX OS for Safety\n"
        "  - Real-time Linux\n"
        "  - CUDA & TensorRT\n"
        "• DriveWorks SDK:\n"
        "  - Sensor abstraction\n"
        "  - Multi-camera pipeline\n"
        "  - High-bandwidth IPC\n"
        "• Supports AUTOSAR Adaptive\n"
        "  and DDS middleware"
    )
    ax.text(3.8, 4.6, c2_text, fontsize=8.5, color=COLOR_NAVY)

    # Col 3: Ecosystem & Interoperability
    c3 = FancyBboxPatch((6.7, 2.0), col_w, 6.0, boxstyle="round,pad=0.04", fc="#F0F9FF", ec=COLOR_PRIMARY, lw=1.6)
    ax.add_patch(c3)
    ax.text(8.1, 7.5, "ECOSYSTEM & STANDARDS", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_PRIMARY)
    c3_text = (
        "• Platform Ecosystem Model:\n"
        "  - OEMs build proprietary\n"
        "    apps on top of DRIVE\n"
        "  - Omniverse / DRIVE Sim\n"
        "    for physical HIL testing\n\n"
        "• Interoperability Stance:\n"
        "  MODULAR & EXTENSIBLE.\n"
        "  Enables intra-vehicle\n"
        "  standards; however, cross-\n"
        "  OEM semantic layer remains\n"
        "  unstandardized."
    )
    ax.text(6.9, 4.6, c3_text, fontsize=8.5, color=COLOR_NAVY)

    # Bottom Callout
    bot = FancyBboxPatch((0.5, 0.4), 9.0, 1.2, boxstyle="round,pad=0.04", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(bot)
    ax.text(5.0, 1.15, "ARCHITECTURAL ASSESSMENT: The dominant open hardware/OS platform for modern SDVs.",
            ha='center', fontsize=10, fontweight='bold', color="#FFFFFF")
    ax.text(5.0, 0.70, "Solves intra-vehicle compute and middleware, creating the ideal runtime host for higher-level semantic protocols.",
            ha='center', fontsize=8.5, color=COLOR_BORDER)

    save_fig(fig, "fig04_nvidia_drive_architecture")


# ==============================================================================
# FIGURE 5: Existing Interoperability Landscape & The Unsolved Gap
# ==============================================================================
def generate_fig5_interoperability_landscape():
    fig, ax = plt.subplots(figsize=(11, 7.0), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 11)
    ax.axis('off')
    ax.set_ylim(0, 11)

    # Left: Well-Solved Communication & Middleware Layers
    box_left = FancyBboxPatch((0.6, 1.0), 4.7, 8.8, boxstyle="round,pad=0.05", fc="#F8FAFC", ec=COLOR_SUCCESS, lw=2.0)
    ax.add_patch(box_left)
    ax.text(2.95, 9.4, "COMMUNICATION & SYNTAX\n(INDUSTRY-SOLVED)", ha='center', fontsize=11, fontweight='bold', color=COLOR_SUCCESS)

    solved_items = [
        ("Physical & Link Layer", "CAN, CAN-FD, Automotive Ethernet (100Base-T1, 1000Base-T1), C-V2X PC5"),
        ("Transport & Network Layer", "TCP/IP, UDP, AVB/TSN (IEEE 802.1AS time sync)"),
        ("Middleware & Serialization", "OMG DDS, SOME/IP, ROS 2, gRPC, Protobuf"),
        ("Service Discovery", "SOME/IP-SD, DDS SPDP/SEDP (Local broadcast)"),
        ("Sensor Abstraction", "ISO 23150, ASAM OSI (Radar/Camera object lists)")
    ]
    y_l = 8.4
    for title, desc in solved_items:
        b = FancyBboxPatch((0.8, y_l - 1.1), 4.3, 1.1, boxstyle="round,pad=0.03", fc="#FFFFFF", ec=COLOR_BORDER, lw=1.2)
        ax.add_patch(b)
        ax.text(1.0, y_l - 0.35, f"✓ {title}", fontsize=9.5, fontweight='bold', color=COLOR_NAVY)
        ax.text(1.0, y_l - 0.75, desc, fontsize=8, color=COLOR_SLATE)
        y_l -= 1.4

    # Right: Unsolved Semantic & Safety Gap
    box_right = FancyBboxPatch((5.7, 1.0), 4.7, 8.8, boxstyle="round,pad=0.05", fc="#FEF2F2", ec=COLOR_ALERT, lw=2.0)
    ax.add_patch(box_right)
    ax.text(8.05, 9.4, "SEMANTIC & SAFETY DEPENDENCIES\n(THE CRITICAL UNRESOLVED GAP)", ha='center', fontsize=11, fontweight='bold', color=COLOR_ALERT)

    unsolved_items = [
        ("Dynamic Capability Negotiation", "Expressing ODD bounds, degraded sensor modes, deceleration limits across multi-vendor fleets"),
        ("Architectural Context Gates", "Rejection of out-of-subsystem semantic decoys (preventing cross-domain hallucinations)"),
        ("Safety Contract Invariants", "Enforcing non-bypassable ISO 26262 ASIL contracts: C_safe ⊆ C_contract across external agents"),
        ("Cross-System Traceability", "Tracing software dependencies when external infrastructure or partner vehicles update capabilities"),
        ("Automated Change Propagation", "Predicting ripple effects of external API/capability changes on local vehicle regression suites")
    ]
    y_r = 8.4
    for title, desc in unsolved_items:
        b = FancyBboxPatch((5.9, y_r - 1.1), 4.3, 1.1, boxstyle="round,pad=0.03", fc="#FFFFFF", ec=COLOR_ALERT, lw=1.2)
        ax.add_patch(b)
        ax.text(6.1, y_r - 0.35, f"✗ {title}", fontsize=9.5, fontweight='bold', color=COLOR_ALERT)
        ax.text(6.1, y_r - 0.75, desc, fontsize=8, color=COLOR_NAVY)
        y_r -= 1.4

    # Banner across bottom
    banner = FancyBboxPatch((0.6, 0.1), 9.8, 0.7, boxstyle="round,pad=0.03", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(banner)
    ax.text(5.5, 0.45, "AURA DOES NOT REPLACE TRANSPORT: It operates strictly as a higher-level Semantic & Safety Contract Layer.",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color="#FFFFFF")

    ax.set_title("FIGURE 5: The Autonomous Systems Interoperability Landscape", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig05_interoperability_landscape")


# ==============================================================================
# FIGURE 6: Communication vs Semantic Interoperability
# ==============================================================================
def generate_fig6_comm_vs_semantics():
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Left: Communication Interoperability
    c_left = FancyBboxPatch((0.5, 1.2), 4.2, 7.8, boxstyle="round,pad=0.06", fc="#F8FAFC", ec=COLOR_GRAPH, lw=1.8)
    ax.add_patch(c_left)
    ax.text(2.6, 8.5, "COMMUNICATION / SYNTAX\n(DDS, SOME/IP, ROS 2)", ha='center', fontsize=11, fontweight='bold', color=COLOR_GRAPH)

    comm_text = (
        "• What it answers:\n"
        '  "How do I send bytes across the wire?"\n\n'
        "• Focus:\n"
        "  - Serialization / deserialization\n"
        "  - Network routing & pub/sub topics\n"
        "  - Transport latency & packet loss\n\n"
        "• Example Payload:\n"
        "  struct Twist {\n"
        "    float64 linear_x = 5.2;\n"
        "    float64 angular_z = 0.1;\n"
        "  };\n\n"
        "• Blindness:\n"
        "  The receiver knows the numbers,\n"
        "  but has ZERO understanding of\n"
        "  whether the vehicle can stop safely\n"
        "  or what its braking limits are."
    )
    ax.text(0.8, 5.0, comm_text, fontsize=8.8, color=COLOR_NAVY)

    # Right: Semantic & Safety Interoperability
    c_right = FancyBboxPatch((5.3, 1.2), 4.2, 7.8, boxstyle="round,pad=0.06", fc="#F0FDFA", ec=COLOR_AURA, lw=1.8)
    ax.add_patch(c_right)
    ax.text(7.4, 8.5, "SEMANTIC & SAFETY\n(AURA INTEROPERABILITY LAYER)", ha='center', fontsize=11, fontweight='bold', color=COLOR_AURA)

    sem_text = (
        "• What it answers:\n"
        '  "What does this capability mean,\n'
        '   and is it safe to cooperate?"\n\n'
        "• Focus:\n"
        "  - Operational Design Domain (ODD)\n"
        "  - Deceleration & clearance limits\n"
        "  - Sensing degradation state\n"
        "  - ISO 26262 ASIL safety invariants\n\n"
        "• Example Contract:\n"
        "  AURA_Manifest {\n"
        "    Agent: Delivery_Pod_42;\n"
        "    Max_Decel: 3.5 m/s² (Rain);\n"
        "    Safety_Level: ASIL-B;\n"
        "    Clearance_Req: 1.8m corridor;\n"
        "  };\n\n"
        "• Intelligence:\n"
        "  Verifies mutual safety contracts\n"
        "  before initiating physical action."
    )
    ax.text(5.6, 5.0, sem_text, fontsize=8.8, color=COLOR_NAVY)

    # Bottom Callout
    bot = FancyBboxPatch((0.5, 0.2), 9.0, 0.7, boxstyle="round,pad=0.03", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(bot)
    ax.text(5.0, 0.55, "FUNDAMENTAL DISTINCTION: Communication transfers data; Semantics validates shared truth and safety.",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color="#FFFFFF")

    ax.set_title("FIGURE 6: Communication vs Semantic Interoperability", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig06_communication_vs_semantics")


# ==============================================================================
# FIGURE 7: Current AURA-Impact Architecture
# ==============================================================================
def generate_fig7_current_aura():
    fig, ax = plt.subplots(figsize=(10, 6.0), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Central Ingestion Card
    ingest = FancyBboxPatch((0.8, 8.2), 8.4, 1.2, boxstyle="round,pad=0.04", fc="#F8FAFC", ec=COLOR_BORDER, lw=1.5)
    ax.add_patch(ingest)
    ax.text(5.0, 9.0, "STAGE 0: TYPED ENGINEERING INGESTION & GRAPH BUILD", ha='center', fontsize=11, fontweight='bold', color=COLOR_NAVY)
    ax.text(5.0, 8.5, "Requirements (reqs.json)  |  AUTOSAR (*.arxml)  |  C Source Code  |  Verification Tests", ha='center', fontsize=9, color=COLOR_SLATE)

    # Stage 1: Graph Traversal
    s1 = FancyBboxPatch((0.8, 5.8), 3.9, 1.8, boxstyle="round,pad=0.04", fc="#EFF6FF", ec=COLOR_GRAPH, lw=1.6)
    ax.add_patch(s1)
    ax.text(2.75, 7.2, "STAGE 1: GRAPH FIRST", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_GRAPH)
    ax.text(2.75, 6.5, "• Bounded BFS (k ≤ 3 hops)\n• Explicit Traceability Links\n• Output: S_struct", ha='center', fontsize=8.8, color=COLOR_NAVY)

    # Stage 2: Contextual Semantic Recovery
    s2 = FancyBboxPatch((5.3, 5.8), 3.9, 1.8, boxstyle="round,pad=0.04", fc="#FAF5FF", ec=COLOR_EMBED, lw=1.6)
    ax.add_patch(s2)
    ax.text(7.25, 7.2, "STAGE 2: SEMANTIC FALLBACK", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_EMBED)
    ax.text(7.25, 6.5, "• DomainHashEmbedder-384\n• Context Filter (ECU/Subsystem)\n• Output: S_semantic", ha='center', fontsize=8.8, color=COLOR_NAVY)

    # Stage 3: Strict Set Union & Routing
    union_box = FancyBboxPatch((0.8, 3.8), 8.4, 1.4, boxstyle="round,pad=0.04", fc="#F0FDFA", ec=COLOR_AURA, lw=1.8)
    ax.add_patch(union_box)
    ax.text(5.0, 4.75, "CANONICAL SET UNION: S_final = S_struct ∪ S_semantic", ha='center', fontsize=11, fontweight='bold', color=COLOR_AURA)
    ax.text(5.0, 4.20, "Guarantees deterministic structural evidence is never suppressed by semantic scoring (Strict Set Union)", ha='center', fontsize=8.8, color=COLOR_NAVY)

    # Stage 4: Safety Gate & Test Selection
    safe_box = FancyBboxPatch((0.8, 1.8), 8.4, 1.5, boxstyle="round,pad=0.04", fc="#F0FDF4", ec=COLOR_SUCCESS, lw=1.8)
    ax.add_patch(safe_box)
    ax.text(5.0, 2.85, "STAGE 4: TEST SELECTION & NON-BYPASSABLE SAFETY GATE", ha='center', fontsize=11, fontweight='bold', color=COLOR_SUCCESS)
    ax.text(5.0, 2.25, "• Enforces Invariant: T_safe ⊆ T_selected (100% ASIL-C/D Mandatory Retention)\n• Slashes regression test execution overhead by 82.29% on canonical benchmark", ha='center', fontsize=8.8, color="#14532D")

    # Bottom Metric Badge
    bot = FancyBboxPatch((0.8, 0.4), 8.4, 0.9, boxstyle="round,pad=0.03", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(bot)
    ax.text(5.0, 0.85, "VALIDATED BASELINE: 63.11% Recall | 54.92% Precision | 82.29% Test Reduction | 0.79 ms Latency",
            ha='center', fontsize=9.5, fontweight='bold', color="#FFFFFF")

    # Arrows
    ax.annotate('', xy=(2.75, 7.6), xytext=(2.75, 8.2), arrowprops=dict(arrowstyle="->", color=COLOR_SLATE, lw=1.4))
    ax.annotate('', xy=(7.25, 7.6), xytext=(7.25, 8.2), arrowprops=dict(arrowstyle="->", color=COLOR_SLATE, lw=1.4))
    ax.annotate('', xy=(5.0, 5.2), xytext=(2.75, 5.8), arrowprops=dict(arrowstyle="->", color=COLOR_SLATE, lw=1.4))
    ax.annotate('', xy=(5.0, 5.2), xytext=(7.25, 5.8), arrowprops=dict(arrowstyle="->", color=COLOR_SLATE, lw=1.4))
    ax.annotate('', xy=(5.0, 3.3), xytext=(5.0, 3.8), arrowprops=dict(arrowstyle="->", color=COLOR_SLATE, lw=1.4))

    ax.set_title("FIGURE 7: Current Validated AURA-Impact Internal Architecture", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig07_current_aura_architecture")


# ==============================================================================
# FIGURE 8: AURA Evolution to Inter-System Protocol
# ==============================================================================
def generate_fig8_aura_evolution():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Left: Internal System A
    sys_a = FancyBboxPatch((0.5, 2.0), 3.0, 6.8, boxstyle="round,pad=0.05", fc="#EFF6FF", ec=COLOR_GRAPH, lw=1.8)
    ax.add_patch(sys_a)
    ax.text(2.0, 8.3, "SYSTEM A\n(Autonomous Vehicle)", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_GRAPH)
    ax.text(2.0, 5.2,
            "• Internal AUTOSAR Stack\n"
            "• Radar/Camera Fusion\n"
            "• Path Planner MPC\n"
            "• ISO 26262 ASIL-D Core\n\n"
            "────── AURA Core ──────\n"
            "• Dependency Graph\n"
            "• Context Gate\n"
            "• Safety Invariant Gate",
            ha='center', fontsize=8.5, color=COLOR_NAVY)

    # Right: Internal System B
    sys_b = FancyBboxPatch((7.5, 2.0), 3.0, 6.8, boxstyle="round,pad=0.05", fc="#FAF5FF", ec=COLOR_EMBED, lw=1.8)
    ax.add_patch(sys_b)
    ax.text(9.0, 8.3, "SYSTEM B\n(Delivery Robot)", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_EMBED)
    ax.text(9.0, 5.2,
            "• Internal ROS 2 Stack\n"
            "• Low-cost LiDAR/Vision\n"
            "• Sidewalk Nav Engine\n"
            "• ISO 13849 PL-d Core\n\n"
            "────── AURA Core ──────\n"
            "• Dependency Graph\n"
            "• Context Gate\n"
            "• Safety Invariant Gate",
            ha='center', fontsize=8.5, color=COLOR_NAVY)

    # Center: The Proposed AURA Interoperability Protocol Layer
    proto = FancyBboxPatch((4.0, 2.6), 3.0, 5.6, boxstyle="round,pad=0.05", fc="#F0FDFA", ec=COLOR_AURA, lw=2.0)
    ax.add_patch(proto)
    ax.text(5.5, 7.8, "AURA SEMANTIC\nINTEROPERABILITY\nLAYER", ha='center', fontsize=11, fontweight='bold', color=COLOR_AURA)

    proto_steps = (
        "1. DISCOVER\n"
        "   Broadcast Identity\n\n"
        "2. DESCRIBE\n"
        "   AURA Manifest (ODD,\n"
        "   Decel limits, Latency)\n\n"
        "3. MATCH\n"
        "   Context Gate Screening\n\n"
        "4. VERIFY\n"
        "   C_safe ⊆ C_contract\n\n"
        "5. COORDINATE\n"
        "   Execute Shared Plan"
    )
    ax.text(5.5, 4.8, proto_steps, ha='center', fontsize=8.2, color=COLOR_NAVY)

    # Bidirectional negotiation arrows
    ax.annotate('', xy=(4.0, 6.0), xytext=(3.5, 6.0), arrowprops=dict(arrowstyle="<->", color=COLOR_AURA, lw=2.0))
    ax.annotate('', xy=(7.5, 6.0), xytext=(7.0, 6.0), arrowprops=dict(arrowstyle="<->", color=COLOR_AURA, lw=2.0))

    # Transport substrate at bottom
    trans = FancyBboxPatch((0.5, 0.4), 10.0, 1.0, boxstyle="round,pad=0.03", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(trans)
    ax.text(5.5, 0.9, "UNDERLYING TRANSPORT SUBSTRATE (Unmodified Existing Standards)", ha='center', fontsize=9.5, fontweight='bold', color="#FFFFFF")
    ax.text(5.5, 0.6, "Automotive Ethernet (TSN)  |  C-V2X (PC5)  |  OMG DDS  |  SOME/IP  |  5G NR V2X", ha='center', fontsize=8.5, color=COLOR_BORDER)

    ax.set_title("FIGURE 8: Conceptual Evolution: Internal Intelligence → Cross-System Interoperability Layer", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig08_aura_evolution_interoperability")


# ==============================================================================
# FIGURE 9: UPI Analogy Mapping & Failure Points
# ==============================================================================
def generate_fig9_upi_analogy():
    fig, ax = plt.subplots(figsize=(10, 6.0), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Left: Where UPI Analogy Works
    b_works = FancyBboxPatch((0.5, 1.2), 4.2, 7.8, boxstyle="round,pad=0.06", fc="#F0FDF4", ec=COLOR_SUCCESS, lw=1.8)
    ax.add_patch(b_works)
    ax.text(2.6, 8.5, "WHERE THE ANALOGY WORKS\n(DECOUPLING & ROUTING)", ha='center', fontsize=11, fontweight='bold', color=COLOR_SUCCESS)

    w_text = (
        "• Common Routing Protocol:\n"
        "  Decouples heterogeneous endpoints\n"
        "  without requiring custom N×N APIs.\n\n"
        "• Universal Identity Addressing:\n"
        "  Virtual Address (VPA) in UPI\n"
        "  → System Manifest URI in AURA.\n\n"
        "• Standard Transaction Envelope:\n"
        "  Payment payload in UPI\n"
        "  → Capability Contract in AURA.\n\n"
        "• Trust & Attestation:\n"
        "  Cryptographic signing of claims\n"
        "  guarantees provenance."
    )
    ax.text(0.8, 5.0, w_text, fontsize=8.8, color=COLOR_NAVY)

    # Right: Where UPI Analogy Fails
    b_fails = FancyBboxPatch((5.3, 1.2), 4.2, 7.8, boxstyle="round,pad=0.06", fc="#FEF2F2", ec=COLOR_ALERT, lw=1.8)
    ax.add_patch(b_fails)
    ax.text(7.4, 8.5, "WHERE THE ANALOGY BREAKS\n(PHYSICS & SAFETY)", ha='center', fontsize=11, fontweight='bold', color=COLOR_ALERT)

    f_text = (
        "• Real-Time Latency Limits:\n"
        "  UPI settles in 1,000–3,000 ms.\n"
        "  Autonomous systems require < 10 ms\n"
        "  deadlines for kinetic collision bounds.\n\n"
        "• Continuous Physics vs Discrete Cash:\n"
        "  UPI transactions are discrete.\n"
        "  Vehicles have continuous kinematics,\n"
        "  inertia, and dynamic road friction.\n\n"
        "• Zero Reversibility / No Rollbacks:\n"
        "  Failed UPI transactions refund cash.\n"
        "  A kinetic collision cannot be undone.\n\n"
        "• No Central Clearinghouse:\n"
        "  UPI relies on central NPCI servers.\n"
        "  Vehicles must negotiate offline/P2P."
    )
    ax.text(5.6, 5.0, f_text, fontsize=8.8, color=COLOR_NAVY)

    # Bottom Verdict
    bot = FancyBboxPatch((0.5, 0.2), 9.0, 0.7, boxstyle="round,pad=0.03", fc=COLOR_NAVY, ec=COLOR_NAVY)
    ax.add_patch(bot)
    ax.text(5.0, 0.55, "RESEARCH VERDICT: Analogy is effective for explaining architectural decoupling, but fails as an engineering blueprint.",
            ha='center', va='center', fontsize=9, fontweight='bold', color="#FFFFFF")

    ax.set_title("FIGURE 9: Critical Stress-Testing of the 'UPI for Autonomous Systems' Analogy", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig09_upi_analogy_analysis")


# ==============================================================================
# FIGURE 10: Three-Agent Protocol Interaction
# ==============================================================================
def generate_fig10_three_agent():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Agent 1: Autonomous Vehicle (AV)
    a1 = FancyBboxPatch((0.6, 6.2), 2.6, 2.6, boxstyle="round,pad=0.04", fc="#EFF6FF", ec=COLOR_GRAPH, lw=1.6)
    ax.add_patch(a1)
    ax.text(1.9, 8.4, "AGENT 1: AV", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_GRAPH)
    ax.text(1.9, 7.3, "• High-speed robotaxi\n• ASIL-D AEB & MPC\n• Decel: 8.0 m/s² max\n• Request: Right-of-way", ha='center', fontsize=8.2, color=COLOR_NAVY)

    # Agent 2: Sidewalk Delivery Pod
    a2 = FancyBboxPatch((6.8, 6.2), 2.6, 2.6, boxstyle="round,pad=0.04", fc="#FAF5FF", ec=COLOR_EMBED, lw=1.6)
    ax.add_patch(a2)
    ax.text(8.1, 8.4, "AGENT 2: POD", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_EMBED)
    ax.text(8.1, 7.3, "• Sidewalk delivery robot\n• Speed: 1.5 m/s max\n• Low braking inertia\n• Intent: Cross crosswalk", ha='center', fontsize=8.2, color=COLOR_NAVY)

    # Agent 3: Smart Intersection RSU
    a3 = FancyBboxPatch((3.7, 1.2), 2.6, 2.6, boxstyle="round,pad=0.04", fc="#F0FDF4", ec=COLOR_SUCCESS, lw=1.6)
    ax.add_patch(a3)
    ax.text(5.0, 3.4, "AGENT 3: SMART RSU", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_SUCCESS)
    ax.text(5.0, 2.3, "• Roadside Infrastructure\n• V2X beaconing (RSU)\n• Traffic phase scheduler\n• Blind-spot camera feed", ha='center', fontsize=8.2, color=COLOR_NAVY)

    # Central Contract Box
    c_box = FancyBboxPatch((3.4, 4.6), 3.2, 2.6, boxstyle="round,pad=0.04", fc="#F0FDFA", ec=COLOR_AURA, lw=1.8)
    ax.add_patch(c_box)
    ax.text(5.0, 6.8, "AURA CAPABILITY CONTRACT", ha='center', fontsize=9.5, fontweight='bold', color=COLOR_AURA)
    c_text = (
        "1. Identity & ODD Exchange\n"
        "2. Context Gate: Decoy Check\n"
        "3. Safety Invariant Evaluated:\n"
        "   T_safe ⊆ T_selected\n"
        "   (Pod clears in 4.2s;\n"
        "    AV yields at 25m distance)\n"
        "4. Contract Signed & Verified"
    )
    ax.text(5.0, 5.5, c_text, ha='center', fontsize=7.8, color=COLOR_NAVY)

    # Interaction lines
    ax.annotate('', xy=(3.4, 6.0), xytext=(3.2, 7.0), arrowprops=dict(arrowstyle="<->", color=COLOR_AURA, lw=1.5))
    ax.annotate('', xy=(6.6, 6.0), xytext=(6.8, 7.0), arrowprops=dict(arrowstyle="<->", color=COLOR_AURA, lw=1.5))
    ax.annotate('', xy=(5.0, 4.6), xytext=(5.0, 3.8), arrowprops=dict(arrowstyle="<->", color=COLOR_AURA, lw=1.5))

    ax.set_title("FIGURE 10: Three-Agent Cooperative Capability Negotiation Scenario", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig10_three_agent_interaction")


# ==============================================================================
# FIGURE 11: Current vs Proposed Workflow
# ==============================================================================
def generate_fig11_workflow_comparison():
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Top: Current Workflow
    c_curr = FancyBboxPatch((0.5, 5.3), 9.0, 3.8, boxstyle="round,pad=0.05", fc="#FEF2F2", ec=COLOR_ALERT, lw=1.6)
    ax.add_patch(c_curr)
    ax.text(0.8, 8.6, "CURRENT WORKFLOW: Fragmented, Manual N×N Bilateral Integration", fontsize=11, fontweight='bold', color=COLOR_ALERT)
    curr_steps = (
        "1. Vendor A and Vendor B sign custom bilateral legal and technical contracts.\n"
        "2. Engineers manually map CAN DBC files or custom ROS 2 messages (Weeks of effort).\n"
        "3. Hardcoded interface assumptions fail silently when Vendor B pushes an OTA software update.\n"
        "4. Testing requires exhaustive, brute-force HIL simulation of all permutations.\n"
        "[PROBLEM] 40-50% engineering budget consumed by integration bottlenecks; high risk of safety escapes."
    )
    ax.text(0.8, 6.8, curr_steps, fontsize=8.5, color=COLOR_NAVY)

    # Bottom: Proposed AURA Workflow
    c_prop = FancyBboxPatch((0.5, 0.6), 9.0, 4.2, boxstyle="round,pad=0.05", fc="#F0FDFA", ec=COLOR_AURA, lw=1.8)
    ax.add_patch(c_prop)
    ax.text(0.8, 4.3, "PROPOSED AURA WORKFLOW: Automated Machine-Readable Semantic Contracts", fontsize=11, fontweight='bold', color=COLOR_AURA)
    prop_steps = (
        "1. Heterogeneous systems broadcast machine-readable AURA Capability Manifests.\n"
        "2. Context-Constrained Semantic Retriever maps unfamiliar capabilities to canonical domain ontologies.\n"
        "3. Architectural Context Gate strictly rejects cross-subsystem decoys and invalid hardware boundaries.\n"
        "4. Non-Bypassable Safety Gate formally verifies that mutual constraints satisfy ISO 26262 ASIL invariants.\n"
        "5. When an agent updates firmware, AURA's Change Impact Engine immediately identifies affected interfaces.\n"
        "[RESULT] Automated interoperability in milliseconds; zero manual DBC re-mapping; provable safety bounds."
    )
    ax.text(0.8, 2.3, prop_steps, fontsize=8.5, color=COLOR_NAVY)

    ax.set_title("FIGURE 11: Current Manual Integration vs Proposed AURA Interoperability Workflow", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig11_current_vs_proposed_workflow")


# ==============================================================================
# FIGURE 12: Problem → Solution → Impact Chain
# ==============================================================================
def generate_fig12_problem_solution_impact():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    col_w = 2.8

    # Col 1: Problem
    c1 = FancyBboxPatch((0.5, 1.2), col_w, 7.8, boxstyle="round,pad=0.05", fc="#FEF2F2", ec=COLOR_ALERT, lw=1.6)
    ax.add_patch(c1)
    ax.text(1.9, 8.5, "THE PROBLEM", ha='center', fontsize=11, fontweight='bold', color=COLOR_ALERT)
    t1 = (
        "• Traceability Decay:\n"
        "  Internal links break during\n"
        "  continuous integration.\n\n"
        "• Graph Blindness:\n"
        "  ALM tools miss unlinked\n"
        "  cross-artifact bugs.\n\n"
        "• Semantic Hallucinations:\n"
        "  Unconstrained AI flags\n"
        "  wrong-subsystem decoys.\n\n"
        "• Multi-Agent Silos:\n"
        "  Heterogeneous systems\n"
        "  cannot negotiate safety."
    )
    ax.text(0.7, 5.0, t1, fontsize=8.5, color=COLOR_NAVY)

    # Col 2: AURA Solution
    c2 = FancyBboxPatch((3.6, 1.2), col_w, 7.8, boxstyle="round,pad=0.05", fc="#F0FDFA", ec=COLOR_AURA, lw=1.8)
    ax.add_patch(c2)
    ax.text(5.0, 8.5, "AURA SOLUTION", ha='center', fontsize=11, fontweight='bold', color=COLOR_AURA)
    t2 = (
        "• Two-Stage Architecture:\n"
        "  Bounded graph first +\n"
        "  contextual semantic fallback.\n\n"
        "• DomainHashEmbedder:\n"
        "  Fast, deterministic vectorizer\n"
        "  (no cloud LLM dependency).\n\n"
        "• Architectural Context Gate:\n"
        "  Strict ECU/subsystem isolation.\n\n"
        "• Non-Bypassable Safety Gate:\n"
        "  Enforces T_safe ⊆ T_selected."
    )
    ax.text(3.8, 5.0, t2, fontsize=8.5, color=COLOR_NAVY)

    # Col 3: Measurable Impact
    c3 = FancyBboxPatch((6.7, 1.2), col_w, 7.8, boxstyle="round,pad=0.05", fc="#F0FDF4", ec=COLOR_SUCCESS, lw=1.8)
    ax.add_patch(c3)
    ax.text(8.1, 8.5, "MEASURABLE IMPACT", ha='center', fontsize=11, fontweight='bold', color=COLOR_SUCCESS)
    t3 = (
        "• Validated Benchmark:\n"
        "  - 63.11% Artifact Recall\n"
        "  - 0.5503 F1 (Highest)\n"
        "  - 82.29% Test Reduction\n"
        "  - 100% Safety Invariant\n"
        "  - 0.79 ms Execution Latency\n\n"
        "• Future Protocol Impact:\n"
        "  - Slashes integration time\n"
        "  - Prevents semantic escapes\n"
        "  - Enables cross-agent safety"
    )
    ax.text(6.9, 5.0, t3, fontsize=8.5, color=COLOR_NAVY)

    # Connector arrows
    ax.annotate('', xy=(3.6, 5.2), xytext=(3.3, 5.2), arrowprops=dict(arrowstyle="->", color=COLOR_AURA, lw=2.0))
    ax.annotate('', xy=(6.7, 5.2), xytext=(6.4, 5.2), arrowprops=dict(arrowstyle="->", color=COLOR_SUCCESS, lw=2.0))

    ax.set_title("FIGURE 12: Problem → Solution → Measurable Engineering Impact Chain", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig12_problem_solution_impact")


# ==============================================================================
# FIGURE 13: Future Research Roadmap
# ==============================================================================
def generate_fig13_research_roadmap():
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    phases = [
        ("PHASE 1: INTERNAL SYSTEM VALIDATION (COMPLETE)",
         "• Architecture B canonical freeze (Graph + DomainHashEmbedder-384 + Strict Union)\n"
         "• Validated benchmark: 63.11% recall, 82.29% test reduction, 100% safety invariant (150/150)\n"
         "• Working interactive demonstrator and 252 passing automated tests",
         COLOR_SUCCESS, "#F0FDF4"),
        ("PHASE 2: OPEN SCHEMA & THREE-AGENT EMULATION (NEXT)",
         "• Formulate formal AURA Capability Manifest schema (JSON-LD / ASN.1)\n"
         "• Build 3-agent software emulation (AV, Delivery Pod, Smart Intersection)\n"
         "• Test capability negotiation, semantic decoy rejection, and safety bounds under simulated packet loss",
         COLOR_AURA, "#F0FDFA"),
        ("PHASE 3: HARDWARE-IN-THE-LOOP (HIL) PILOT (FUTURE RESEARCH)",
         "• Deploy AURA Interoperability Layer over real Automotive Ethernet (TSN) and DDS testbench\n"
         "• Integrate with Vector CANoe and dSPACE HIL simulator for real-time latency verification (<5ms)\n"
         "• Evaluate cross-system change propagation during dynamic over-the-air firmware updates",
         COLOR_PRIMARY, "#EFF6FF"),
        ("PHASE 4: INDUSTRY STANDARDIZATION & OEM EVALUATION (LONG-TERM)",
         "• Propose AURA Semantic Contract extension to AUTOSAR Adaptive and ASAM working groups\n"
         "• Conduct multi-vendor field trial with automotive OEM and Tier-1 partners\n"
         "• Complete ISO 26262 Tool Confidence Level (TCL2/3) qualification",
         COLOR_NAVY, "#F8FAFC")
    ]

    y_pos = 8.5
    h = 1.7
    spacing = 2.1

    for i, (title, desc, border_col, bg_col) in enumerate(phases):
        b = FancyBboxPatch((0.6, y_pos - h), 8.8, h, boxstyle="round,pad=0.04", fc=bg_col, ec=border_col, lw=1.6)
        ax.add_patch(b)
        ax.text(0.9, y_pos - 0.35, title, fontsize=10.5, fontweight='bold', color=border_col)
        ax.text(0.9, y_pos - 1.0, desc, fontsize=8.5, color=COLOR_NAVY)

        if i < len(phases) - 1:
            ax.annotate('', xy=(5.0, y_pos - h - 0.32), xytext=(5.0, y_pos - h - 0.05),
                        arrowprops=dict(arrowstyle="->", color=COLOR_SLATE, lw=1.4))
        y_pos -= spacing

    ax.set_title("FIGURE 13: AURA-Impact Strategic Technology & Research Roadmap", fontsize=14, fontweight='bold', pad=12)
    save_fig(fig, "fig13_future_research_roadmap")


# ==============================================================================
# CHARTS: Interoperability Matrix & Canonical AURA Performance
# ==============================================================================
def generate_chart_a_matrix():
    fig, ax = plt.subplots(figsize=(10, 5.0), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.axis('off')

    headers = ["Technology", "Transport", "Discovery", "Semantics", "Capability ODD", "Safety Invariant"]
    data = [
        ["CAN / CAN-FD", "High (Bitwise)", "None (Static)", "Zero (Raw)", "Zero", "None (CRC)"],
        ["SOME/IP", "High (Ethernet)", "SOME/IP-SD", "Zero (IDL)", "Zero", "External Only"],
        ["OMG DDS", "Very High (RTPS)", "SPDP / SEDP", "Low (Typed)", "Zero", "QoS Only (No Safety)"],
        ["ROS 2", "High (DDS-based)", "DDS Discovery", "Low (msg/srv)", "Low", "None (Zero ISO 26262)"],
        ["C-V2X (J2735)", "Medium (Wireless)", "Periodic BSM", "Medium (Kinematics)", "Low (Static Type)", "Advisory Only"],
        ["AURA Protocol", "Overlay (Runs on DDS)", "Federated", "Very High (Ontology)", "Very High (ODD/Decel)", "Strict (C_safe ⊆ C_contract)"]
    ]

    table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1.1, 1.8)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(COLOR_BORDER)
        if r == 0:
            cell.set_facecolor(COLOR_NAVY)
            cell.set_text_props(color="#FFFFFF", fontweight='bold')
        elif r == 6:  # AURA row
            cell.set_facecolor("#CCFBF1")
            cell.set_text_props(fontweight='bold', color=COLOR_NAVY)
        else:
            cell.set_facecolor("#F8FAFC" if r % 2 == 1 else "#FFFFFF")

    ax.set_title("CHART A: Interoperability Capability Matrix Across Middleware and Standards", fontsize=13, fontweight='bold', pad=14)
    save_fig(fig, "chart_a_interoperability_capability_matrix")


def generate_chart_b_benchmark():
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.set_facecolor(COLOR_CARD)

    methods = ["Keyword", "Embedding", "Graph-Only", "AURA-Impact"]
    f1_vals = [0.1485, 0.3114, 0.4557, 0.5503]
    colors = [COLOR_SLATE, COLOR_EMBED, COLOR_GRAPH, COLOR_AURA]

    bars = ax.bar(methods, f1_vals, color=colors, width=0.52, edgecolor=COLOR_NAVY, linewidth=1.1, zorder=3)
    for b, v in zip(bars, f1_vals):
        ax.text(b.get_x() + b.get_width()/2., v + 0.015, f"{v:.4f}", ha='center', va='bottom', fontsize=10.5, fontweight='bold')

    ax.set_ylim(0, 0.68)
    ax.set_ylabel("Artifact F1 Score", fontsize=11, fontweight='bold')
    ax.set_title("CHART B: AURA-Impact Canonical Research Benchmark F1", fontsize=13, fontweight='bold', pad=14)
    ax.text(0.5, 1.02, "Validated on 150 automated mutation batches (Seed 42)", transform=ax.transAxes, ha='center', fontsize=9, color=COLOR_SLATE)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color=COLOR_BORDER, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, "chart_b_canonical_benchmark_metrics")


def generate_chart_c_evaluation():
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=300)
    fig.patch.set_facecolor(COLOR_CARD)
    ax.axis('off')

    headers = ["Evaluation Metric", "Status", "Target / Measured Value", "Methodological Basis"]
    data = [
        ["Artifact Recall / F1", "MEASURED", "63.11% Recall / 0.5503 F1", "150 mutation batches on canonical benchmark"],
        ["Test Suite Reduction", "MEASURED", "82.29% reduction (90.07% test recall)", "Evaluated against full regression suite"],
        ["Safety Invariant Enforcement", "MEASURED", "100.0% retention (150/150 mutations)", "Non-bypassable safety gate assertion"],
        ["Execution Latency", "MEASURED", "0.79 ms mean in-memory benchmark", "Measured on single-thread CPU"],
        ["3-Agent Semantic Discovery Accuracy", "PROJECTED", "≥ 95% discovery under context constraints", "Projected from internal Context Gate performance"],
        ["Cross-Agent Safety Escape Rate", "PROJECTED", "0.0% safety contract violations", "Projected from C_safe ⊆ C_contract gate enforcement"],
        ["Multi-Vendor OEM Integration Time", "HYPOTHETICAL", "60-70% reduction in manual interface mapping", "Hypothetical economic projection based on industry data"]
    ]

    table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(8.8)
    table.scale(1.1, 1.7)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(COLOR_BORDER)
        if r == 0:
            cell.set_facecolor(COLOR_NAVY)
            cell.set_text_props(color="#FFFFFF", fontweight='bold')
        else:
            status = data[r - 1][1]
            if status == "MEASURED":
                cell.set_facecolor("#ECFDF5" if c == 1 else "#FFFFFF")
            elif status == "PROJECTED":
                cell.set_facecolor("#EFF6FF" if c == 1 else "#FFFFFF")
            else:
                cell.set_facecolor("#FFFBEB" if c == 1 else "#FFFFFF")

    ax.set_title("CHART C: Quantitative Evaluation Framework (Distinguishing Measured vs Projected)", fontsize=13, fontweight='bold', pad=14)
    save_fig(fig, "chart_c_hypothetical_evaluation_framework")


def main():
    print("Generating all research figures and charts...")
    generate_fig1_autonomous_stack()
    generate_fig2_waymo()
    generate_fig3_tesla()
    generate_fig4_nvidia()
    generate_fig5_interoperability_landscape()
    generate_fig6_comm_vs_semantics()
    generate_fig7_current_aura()
    generate_fig8_aura_evolution()
    generate_fig9_upi_analogy()
    generate_fig10_three_agent()
    generate_fig11_workflow_comparison()
    generate_fig12_problem_solution_impact()
    generate_fig13_research_roadmap()
    generate_chart_a_matrix()
    generate_chart_b_benchmark()
    generate_chart_c_evaluation()
    print("All research figures generated successfully!")

if __name__ == "__main__":
    main()
