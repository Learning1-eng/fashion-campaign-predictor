"""
Fashion Campaign Predictor — Dress for Good AI Studio
Multi-agent simulation for luxury fashion marketing campaigns.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Fashion Campaign Predictor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PASSWORD GATE
# ─────────────────────────────────────────────
APP_PASSWORD = "Turati3752"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400&family=Montserrat:wght@300;400;500&display=swap');
    html, body, [class*="css"] { background-color: #0A0A0A; color: #E8E0D4; font-family: 'Montserrat', sans-serif; }
    .stApp { background: #0A0A0A; }
    #MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 4rem 0 2rem 0;'>
            <div style='font-family: "Cormorant Garamond", serif; font-size: 2.2rem;
                        font-weight: 300; color: #D4B896; letter-spacing: 0.15em;'>◈ Dress for Good</div>
            <div style='font-size: 0.6rem; letter-spacing: 0.35em; text-transform: uppercase;
                        color: #5A5048; margin-top: 0.4rem;'>AI Luxury Studio — Private Access</div>
        </div>
        """, unsafe_allow_html=True)

        pwd = st.text_input("Access Code", type="password", placeholder="Enter password")
        if st.button("Enter"):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code.")
    st.stop()

# ─────────────────────────────────────────────
# CUSTOM CSS — Luxury Editorial Dark
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background-color: #0A0A0A;
    color: #E8E0D4;
}

.stApp {
    background: linear-gradient(160deg, #0A0A0A 0%, #111109 50%, #0D0A0A 100%);
}

/* Header */
.main-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 300;
    letter-spacing: 0.12em;
    color: #D4B896;
    margin-bottom: 0;
    line-height: 1.1;
}
.main-subtitle {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.35em;
    color: #7A6E64;
    text-transform: uppercase;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}
.divider {
    border: none;
    border-top: 1px solid #2A2520;
    margin: 1.5rem 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0D0B09 !important;
    border-right: 1px solid #2A2520;
}
section[data-testid="stSidebar"] * {
    color: #B8AFA6 !important;
    font-family: 'Montserrat', sans-serif !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.65rem !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    color: #7A6E64 !important;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #161410 0%, #1A1714 100%);
    border: 1px solid #2A2520;
    border-radius: 2px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #D4B896, #8B6E52);
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem;
    font-weight: 300;
    color: #D4B896;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #5A5048;
    font-weight: 500;
}

/* Agent status */
.agent-tag {
    display: inline-block;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7A6E64;
    border: 1px solid #2A2520;
    padding: 0.2rem 0.6rem;
    margin: 0.15rem;
    border-radius: 1px;
}

/* Section labels */
.section-label {
    font-size: 0.6rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: #7A6E64;
    font-weight: 500;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #D4B896, #B8956E) !important;
    color: #0A0A0A !important;
    border: none !important;
    border-radius: 1px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2.5rem !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #E8CCA8, #D4A87C) !important;
    transform: translateY(-1px) !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid #2A2520;
}

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    color: #D4B896 !important;
    border: 1px solid #2A2520 !important;
    border-radius: 1px !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover {
    border-color: #D4B896 !important;
    background: #161410 !important;
}

/* Progress / spinner */
.stProgress .st-bo { background-color: #D4B896 !important; }

/* Hide Streamlit default chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIMULATION ENGINE
# ─────────────────────────────────────────────

CAMPAIGN_PARAMS = {
    "social_influencer": {
        "label": "Social Influencer",
        "base_intent_alpha": 3.5,
        "base_intent_beta": 4.0,
        "engagement_multiplier": 1.4,
        "vip_sensitivity": 0.8,
        "city_bias": {"Milano": 1.05, "Dubai": 1.20, "Paris": 1.10},
        "revenue_per_purchase": (8_000, 35_000),
    },
    "digital_ar": {
        "label": "Digital / AR Experience",
        "base_intent_alpha": 2.8,
        "base_intent_beta": 4.5,
        "engagement_multiplier": 1.6,
        "vip_sensitivity": 0.6,
        "city_bias": {"Milano": 1.10, "Dubai": 1.30, "Paris": 1.15},
        "revenue_per_purchase": (6_000, 28_000),
    },
    "product_launch": {
        "label": "Product Launch",
        "base_intent_alpha": 4.5,
        "base_intent_beta": 3.0,
        "engagement_multiplier": 1.2,
        "vip_sensitivity": 1.1,
        "city_bias": {"Milano": 1.15, "Dubai": 1.10, "Paris": 1.20},
        "revenue_per_purchase": (12_000, 60_000),
    },
    "pricing_hike": {
        "label": "Pricing Hike",
        "base_intent_alpha": 2.0,
        "base_intent_beta": 5.0,
        "engagement_multiplier": 0.85,
        "vip_sensitivity": 1.3,
        "city_bias": {"Milano": 0.90, "Dubai": 1.00, "Paris": 0.95},
        "revenue_per_purchase": (15_000, 80_000),
    },
}

VIP_PERSONAS = [
    ("Ultra-HNWI Collector",    0.12, 1.6,  1.4),
    ("Brand Ambassador",        0.08, 1.0,  1.8),
    ("Aspirational Buyer",      0.25, 0.7,  1.1),
    ("Trend Setter Influencer", 0.15, 0.9,  1.5),
    ("Private Client",          0.10, 1.5,  1.2),
    ("Digital Native",          0.18, 0.6,  1.3),
    ("Heritage Loyalist",       0.12, 1.2,  0.9),
)


def run_simulation(
    campaign_type: str,
    n_vips: int,
    cities: list,
    budget: float,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    cp = CAMPAIGN_PARAMS[campaign_type]

    n_sim = max(n_vips, 1000)  # always simulate at least 1000
    agents = []

    # City distribution
    city_weights = np.array([1.0 / len(cities)] * len(cities))
    city_weights /= city_weights.sum()
    assigned_cities = rng.choice(cities, size=n_sim, p=city_weights)

    # Persona distribution
    persona_names  = [p[0] for p in VIP_PERSONAS]
    persona_shares = np.array([p[1] for p in VIP_PERSONAS])
    persona_shares /= persona_shares.sum()
    persona_intent_mult = np.array([p[2] for p in VIP_PERSONAS])
    persona_eng_mult    = np.array([p[3] for p in VIP_PERSONAS])

    assigned_personas = rng.choice(
        len(VIP_PERSONAS), size=n_sim, p=persona_shares
    )

    # Budget efficiency factor
    budget_factor = min(1.0 + (budget / 2_000_000) * 0.3, 1.35)

    for i in range(n_sim):
        city = assigned_cities[i]
        city_factor = cp["city_bias"].get(city, 1.0)
        persona_idx = assigned_personas[i]
        p_intent_m  = persona_intent_mult[persona_idx]
        p_eng_m     = persona_eng_mult[persona_idx]

        # Purchase intent via Beta distribution
        alpha = cp["base_intent_alpha"] * p_intent_m * city_factor * budget_factor
        beta  = cp["base_intent_beta"]  / (p_intent_m * city_factor)
        intent = float(rng.beta(alpha, beta))
        intent = np.clip(intent, 0.0, 1.0)

        # Engagement score
        eng_base = rng.beta(3.0 * p_eng_m, 3.5)
        engagement = float(np.clip(
            eng_base * cp["engagement_multiplier"] * budget_factor * city_factor,
            0.0, 1.0
        ))

        # Purchase decision (Bernoulli draw)
        purchased = bool(rng.random() < intent)

        # Revenue if purchased
        rev_lo, rev_hi = cp["revenue_per_purchase"]
        revenue = float(rng.uniform(rev_lo, rev_hi)) if purchased else 0.0

        # Influence score (reach)
        influence = float(np.clip(rng.beta(2.0, 5.0) * 100_000, 500, 100_000))

        agents.append({
            "Agent ID":        f"VIP-{i+1:05d}",
            "Persona":         persona_names[persona_idx],
            "City":            city,
            "Purchase Intent": round(intent * 100, 1),
            "Engagement":      round(engagement * 100, 1),
            "Purchased":       purchased,
            "Revenue (€)":     round(revenue, 0),
            "Influence Score": round(influence, 0),
        })

    df = pd.DataFrame(agents)

    # Scale to requested n_vips if larger than 1000
    if n_vips < n_sim:
        df = df.sample(n=n_vips, random_state=seed).reset_index(drop=True)
        df["Agent ID"] = [f"VIP-{i+1:05d}" for i in range(len(df))]

    return df


def compute_summary(df: pd.DataFrame, campaign_type: str, budget: float):
    cp = CAMPAIGN_PARAMS[campaign_type]
    total = len(df)
    buyers = df["Purchased"].sum()
    buy_rate = buyers / total * 100
    total_revenue = df["Revenue (€)"].sum()
    avg_intent = df["Purchase Intent"].mean()
    avg_eng = df["Engagement"].mean()
    roi = (total_revenue - budget) / budget * 100 if budget > 0 else 0
    total_reach = df["Influence Score"].sum()

    city_summary = (
        df.groupby("City")
        .agg(
            VIPs=("Agent ID", "count"),
            Buyers=("Purchased", "sum"),
            Avg_Intent=("Purchase Intent", "mean"),
            Revenue=("Revenue (€)", "sum"),
        )
        .reset_index()
    )
    city_summary["Buy Rate (%)"] = (city_summary["Buyers"] / city_summary["VIPs"] * 100).round(1)
    city_summary["Revenue (€)"] = city_summary["Revenue"].round(0)
    city_summary["Avg Intent (%)"] = city_summary["Avg_Intent"].round(1)
    city_summary = city_summary[["City", "VIPs", "Buyers", "Buy Rate (%)", "Avg Intent (%)", "Revenue (€)"]]

    persona_summary = (
        df.groupby("Persona")
        .agg(
            Count=("Agent ID", "count"),
            Buyers=("Purchased", "sum"),
            Avg_Intent=("Purchase Intent", "mean"),
            Revenue=("Revenue (€)", "sum"),
        )
        .reset_index()
    )
    persona_summary["Buy Rate (%)"] = (persona_summary["Buyers"] / persona_summary["Count"] * 100).round(1)
    persona_summary["Revenue (€)"] = persona_summary["Revenue"].round(0)
    persona_summary = persona_summary.rename(columns={"Avg_Intent": "Avg Intent (%)"})
    persona_summary["Avg Intent (%)"] = persona_summary["Avg Intent (%)"].round(1)
    persona_summary = persona_summary.sort_values("Revenue (€)", ascending=False)

    return {
        "total": total,
        "buyers": int(buyers),
        "buy_rate": round(buy_rate, 1),
        "total_revenue": round(total_revenue, 0),
        "avg_intent": round(avg_intent, 1),
        "avg_eng": round(avg_eng, 1),
        "roi": round(roi, 1),
        "total_reach": int(total_reach),
        "city_summary": city_summary,
        "persona_summary": persona_summary,
    }


def make_chart(df: pd.DataFrame, city_summary: pd.DataFrame, campaign_label: str):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor("#0D0B09")

    gold   = "#D4B896"
    bronze = "#8B6E52"
    dark   = "#0D0B09"
    grid_c = "#1E1C18"
    text_c = "#7A6E64"
    cream  = "#E8E0D4"

    for ax in axes:
        ax.set_facecolor(dark)
        ax.tick_params(colors=text_c, labelsize=7)
        for spine in ax.spines.values():
            spine.set_color("#2A2520")

    # Chart 1 — Buy Rate by City
    ax1 = axes[0]
    bars = ax1.bar(
        city_summary["City"],
        city_summary["Buy Rate (%)"],
        color=[gold, bronze, "#6E5040"][:len(city_summary)],
        width=0.5,
        zorder=2,
    )
    ax1.yaxis.grid(True, color=grid_c, linewidth=0.5, zorder=1)
    ax1.set_axisbelow(True)
    ax1.set_title("Buy Rate by City", color=cream, fontsize=8, fontweight="normal",
                  letter_spacing=5, pad=12)
    ax1.set_ylabel("%", color=text_c, fontsize=7)
    ax1.set_xlabel("", color=text_c)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f"{bar.get_height():.1f}%",
                 ha="center", va="bottom", color=cream, fontsize=7)

    # Chart 2 — Intent Distribution (histogram)
    ax2 = axes[1]
    purchased_intent    = df.loc[df["Purchased"],     "Purchase Intent"]
    not_purchased_intent = df.loc[~df["Purchased"],   "Purchase Intent"]
    bins = np.linspace(0, 100, 30)
    ax2.hist(not_purchased_intent, bins=bins, color=bronze,   alpha=0.6, label="No Purchase", zorder=2)
    ax2.hist(purchased_intent,     bins=bins, color=gold,     alpha=0.8, label="Purchased",   zorder=3)
    ax2.yaxis.grid(True, color=grid_c, linewidth=0.5, zorder=1)
    ax2.set_axisbelow(True)
    ax2.set_title("Intent Distribution", color=cream, fontsize=8, fontweight="normal", pad=12)
    ax2.set_xlabel("Purchase Intent (%)", color=text_c, fontsize=7)
    ax2.set_ylabel("Agents", color=text_c, fontsize=7)
    legend = ax2.legend(fontsize=6, facecolor="#161410", edgecolor="#2A2520", labelcolor=cream)

    # Chart 3 — Revenue by City
    ax3 = axes[2]
    rev_bars = ax3.barh(
        city_summary["City"],
        city_summary["Revenue (€)"] / 1000,
        color=[gold, bronze, "#6E5040"][:len(city_summary)],
        height=0.4,
        zorder=2,
    )
    ax3.xaxis.grid(True, color=grid_c, linewidth=0.5, zorder=1)
    ax3.set_axisbelow(True)
    ax3.set_title("Revenue by City (k€)", color=cream, fontsize=8, fontweight="normal", pad=12)
    ax3.set_xlabel("Revenue (k€)", color=text_c, fontsize=7)
    for bar in rev_bars:
        w = bar.get_width()
        ax3.text(w + max(w * 0.01, 1), bar.get_y() + bar.get_height() / 2,
                 f"{w:,.0f}k",
                 va="center", ha="left", color=cream, fontsize=7)

    fig.suptitle(
        f"Campaign Simulation — {campaign_label}",
        color=cream, fontsize=9, fontweight="normal", y=1.02,
        fontfamily="serif", style="italic"
    )
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# SIDEBAR — INPUT PANEL
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding: 1.2rem 0 0.5rem 0;'>
        <div style='font-family: "Cormorant Garamond", serif; font-size: 1.4rem; font-weight: 300;
                    letter-spacing: 0.1em; color: #D4B896;'>
            ◈ Dress for Good
        </div>
        <div style='font-size: 0.58rem; letter-spacing: 0.3em; text-transform: uppercase;
                    color: #5A5048; margin-top: 0.2rem;'>
            AI Luxury Studio — Simulation Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #2A2520; margin: 1rem 0;'>", unsafe_allow_html=True)

    campaign_type = st.selectbox(
        "Campaign Type",
        options=list(CAMPAIGN_PARAMS.keys()),
        format_func=lambda x: CAMPAIGN_PARAMS[x]["label"],
    )

    n_vips = st.slider("VIP Pool Size", min_value=100, max_value=10_000, value=2_000, step=100)

    all_cities = ["Milano", "Dubai", "Paris"]
    cities = st.multiselect(
        "Target Cities",
        options=all_cities,
        default=all_cities,
    )
    if not cities:
        cities = all_cities

    budget = st.number_input(
        "Campaign Budget (€)",
        min_value=50_000,
        max_value=10_000_000,
        value=500_000,
        step=50_000,
    )

    seed = st.number_input("Simulation Seed", min_value=1, max_value=9999, value=42)

    st.markdown("<hr style='border-color: #2A2520; margin: 1rem 0;'>", unsafe_allow_html=True)

    run = st.button("▸ Run Simulation")

    st.markdown("""
    <div style='margin-top: 2rem;'>
        <div style='font-size: 0.58rem; letter-spacing: 0.2em; text-transform: uppercase;
                    color: #3A3530; line-height: 2;'>
            Agents: Beta-distribution intent<br>
            Personas: 7 luxury archetypes<br>
            Engine: NumPy probabilistic sim<br>
            Version: 1.0 — Milan 2025
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN PANEL
# ─────────────────────────────────────────────

st.markdown("""
<div class='main-title'>Fashion Campaign Predictor</div>
<div class='main-subtitle'>Multi-Agent Simulation for Luxury Marketing Intelligence</div>
<hr class='divider'>
""", unsafe_allow_html=True)

if not run:
    # Landing state
    st.markdown("""
    <div style='text-align: center; padding: 5rem 2rem;'>
        <div style='font-family: "Cormorant Garamond", serif; font-size: 1.8rem;
                    font-weight: 300; color: #3A3530; letter-spacing: 0.08em; font-style: italic;'>
            Configure your campaign parameters<br>and run the simulation.
        </div>
        <div style='margin-top: 1.5rem; font-size: 0.6rem; letter-spacing: 0.3em;
                    text-transform: uppercase; color: #2A2520;'>
            Powered by synthetic VIP agent modeling — Dress for Good AI Studio
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Run simulation
    with st.spinner("Simulating synthetic VIP agents..."):
        df = run_simulation(campaign_type, n_vips, cities, budget, seed=int(seed))
        summary = compute_summary(df, campaign_type, budget)

    campaign_label = CAMPAIGN_PARAMS[campaign_type]["label"]

    # ── Agent tags
    st.markdown(f"""
    <div style='margin-bottom: 1.5rem;'>
        <span class='agent-tag'>◈ {summary["total"]:,} agents</span>
        <span class='agent-tag'>◈ {len(cities)} cities</span>
        <span class='agent-tag'>◈ {campaign_label}</span>
        <span class='agent-tag'>◈ 7 personas active</span>
        <span class='agent-tag'>◈ Beta-distribution intent</span>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{summary["buy_rate"]}%</div>
            <div class='metric-label'>Buy Rate</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{summary["buyers"]:,}</div>
            <div class='metric-label'>Buyers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        rev_m = summary["total_revenue"] / 1_000_000
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>€{rev_m:.1f}M</div>
            <div class='metric-label'>Projected Revenue</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{summary["roi"]:+.0f}%</div>
            <div class='metric-label'>ROI</div>
        </div>""", unsafe_allow_html=True)
    with col5:
        reach_k = summary["total_reach"] // 1000
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{reach_k:,}K</div>
            <div class='metric-label'>Total Reach</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts
    st.markdown("<div class='section-label'>Simulation Analysis</div>", unsafe_allow_html=True)
    fig = make_chart(df, summary["city_summary"], campaign_label)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # ── City + Persona breakdown
    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("<div class='section-label'>Performance by City</div>", unsafe_allow_html=True)
        st.dataframe(
            summary["city_summary"].style.format({
                "Buy Rate (%)": "{:.1f}",
                "Avg Intent (%)": "{:.1f}",
                "Revenue (€)": "€{:,.0f}",
            }).set_properties(**{
                "background-color": "#0D0B09",
                "color": "#B8AFA6",
                "border-color": "#2A2520",
            }),
            use_container_width=True,
            hide_index=True,
        )

    with c_right:
        st.markdown("<div class='section-label'>Persona Intelligence</div>", unsafe_allow_html=True)
        st.dataframe(
            summary["persona_summary"][["Persona", "Count", "Buy Rate (%)", "Revenue (€)"]].style.format({
                "Buy Rate (%)": "{:.1f}",
                "Revenue (€)": "€{:,.0f}",
            }).set_properties(**{
                "background-color": "#0D0B09",
                "color": "#B8AFA6",
                "border-color": "#2A2520",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # ── Full Agent Table (paginated via Streamlit)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Agent-Level Data</div>", unsafe_allow_html=True)

    display_df = df.copy()
    display_df["Purchase Intent"] = display_df["Purchase Intent"].map("{:.1f}%".format)
    display_df["Engagement"]      = display_df["Engagement"].map("{:.1f}%".format)
    display_df["Revenue (€)"]     = display_df["Revenue (€)"].map("€{:,.0f}".format)
    display_df["Influence Score"] = display_df["Influence Score"].map("{:,.0f}".format)
    display_df["Purchased"]       = display_df["Purchased"].map({True: "✓", False: "—"})

    st.dataframe(display_df, use_container_width=True, height=340, hide_index=True)

    # ── CSV Export
    st.markdown("<br>", unsafe_allow_html=True)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="↓ Export Full Dataset (CSV)",
        data=csv_data,
        file_name=f"fashion_campaign_{campaign_type}_{n_vips}vips.csv",
        mime="text/csv",
    )

    # ── Strategic read-out
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    roi_read = "strong positive" if summary["roi"] > 50 else "moderate" if summary["roi"] > 0 else "negative"
    top_city = summary["city_summary"].loc[summary["city_summary"]["Buy Rate (%)"].idxmax(), "City"]
    top_persona = summary["persona_summary"].iloc[0]["Persona"]

    st.markdown(f"""
    <div style='font-family: "Cormorant Garamond", serif; font-size: 1.05rem; font-weight: 300;
                color: #7A6E64; line-height: 1.9; font-style: italic; padding: 1rem 0;'>
        Simulation of {summary["total"]:,} synthetic VIP agents across {", ".join(cities)} 
        projects a <strong style='color: #D4B896;'>{roi_read} ROI of {summary["roi"]:+.0f}%</strong> 
        on a €{budget:,.0f} investment. Conversion rate holds at 
        <strong style='color: #D4B896;'>{summary["buy_rate"]}%</strong>, with 
        <strong style='color: #D4B896;'>{top_city}</strong> as highest-performing market 
        and <strong style='color: #D4B896;'>{top_persona}</strong> as dominant revenue persona. 
        Projected gross revenue: <strong style='color: #D4B896;'>€{summary["total_revenue"]:,.0f}</strong>.
    </div>
    """, unsafe_allow_html=True)
