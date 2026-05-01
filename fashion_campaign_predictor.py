# Fashion Campaign Predictor v3.0 - Dress for Good AI Studio

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

st.set_page_config(page_title="Fashion Campaign Predictor", page_icon="D", layout="wide", initial_sidebar_state="expanded")

APP_PASSWORD = "Turati3752"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');html,body,[class*='css']{background:#fff;color:#111;font-family:Montserrat,sans-serif;}.stApp{background:#fff;}#MainMenu,footer,header{visibility:hidden;}.stButton>button{background:transparent!important;color:#111!important;border:2px solid #111!important;border-radius:24px!important;font-family:Montserrat,sans-serif!important;font-size:0.65rem!important;font-weight:600!important;letter-spacing:0.2em!important;text-transform:uppercase!important;padding:0.75rem 2rem!important;transition:all 0.2s!important;}.stButton>button:hover{background:#C8D400!important;border-color:#C8D400!important;color:#111!important;}</style>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        st.markdown("<div style='text-align:center;padding:5rem 0 2rem'><img src='data:image/png;base64,""' style='width:100px;height:100px;border-radius:50%;'><div style='font-family:Montserrat;font-size:0.55rem;font-weight:600;letter-spacing:0.35em;text-transform:uppercase;color:#999;margin-top:1rem'>Private Access</div></div>", unsafe_allow_html=True)
        pwd = st.text_input("", type="password", placeholder="Access code")
        if st.button("Enter", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code.")
    st.stop()

LOGO_B64 = ""  # loaded from sidebar directly

st.markdown("<style>" +
    "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');" +
    "html,body,[class*='css']{font-family:Montserrat,sans-serif!important;background:#fff;color:#111;}" +
    ".stApp{background:#FAFAF8;}" +
    "section[data-testid='stSidebar']{background:#111!important;}" +
    "section[data-testid='stSidebar'] *{color:#fff!important;font-family:Montserrat,sans-serif!important;}" +
    "section[data-testid='stSidebar'] label{font-size:0.55rem!important;letter-spacing:0.25em!important;text-transform:uppercase!important;color:#888!important;font-weight:600!important;}" +
    ".stButton>button{background:transparent!important;color:#111!important;border:2px solid #111!important;border-radius:24px!important;font-family:Montserrat,sans-serif!important;font-size:0.62rem!important;font-weight:600!important;letter-spacing:0.2em!important;text-transform:uppercase!important;padding:0.8rem 2rem!important;width:100%!important;transition:all 0.25s!important;}" +
    ".stButton>button:hover{background:#C8D400!important;border-color:#C8D400!important;color:#111!important;}" +
    ".metric-card{background:#fff;border:1px solid #E8E8E4;border-top:3px solid #111;padding:1.4rem 1rem;text-align:center;}" +
    ".metric-value{font-family:Montserrat,sans-serif;font-size:2rem;font-weight:700;color:#111;line-height:1;margin-bottom:0.4rem;}" +
    ".metric-label{font-size:0.52rem;letter-spacing:0.28em;text-transform:uppercase;color:#999;font-weight:600;}" +
    ".section-label{font-size:0.52rem;letter-spacing:0.35em;text-transform:uppercase;color:#999;font-weight:600;margin-bottom:0.8rem;margin-top:1.5rem;border-bottom:1px solid #E8E8E4;padding-bottom:0.5rem;}" +
    ".stDownloadButton>button{background:transparent!important;color:#111!important;border:1px solid #111!important;border-radius:24px!important;font-size:0.55rem!important;letter-spacing:0.2em!important;text-transform:uppercase!important;font-weight:600!important;}" +
    ".stDownloadButton>button:hover{background:#111!important;color:#fff!important;}" +
    ".stDataFrame,.stDataFrame *{color:#111!important;font-family:Montserrat,sans-serif!important;font-size:0.75rem!important;}" +
    "#MainMenu,footer,header{visibility:hidden;}" +
    "</style>", unsafe_allow_html=True)

CAMPAIGN_PARAMS = {
    "social_influencer": {"label":"Social Influencer","base_intent_alpha":3.5,"base_intent_beta":4.0,"engagement_multiplier":1.4,"city_bias":{"Milano":1.05,"Dubai":1.20,"Paris":1.10,"Tokyo":1.15,"New York":1.12,"London":1.08,"Riyadh":1.25,"Singapore":1.18,"Los Angeles":1.10,"Shanghai":1.20},"revenue_per_purchase":(8000,35000)},
    "digital_ar": {"label":"Digital / AR Experience","base_intent_alpha":2.8,"base_intent_beta":4.5,"engagement_multiplier":1.6,"city_bias":{"Milano":1.10,"Dubai":1.30,"Paris":1.15,"Tokyo":1.35,"New York":1.25,"London":1.15,"Riyadh":1.10,"Singapore":1.30,"Los Angeles":1.20,"Shanghai":1.28},"revenue_per_purchase":(6000,28000)},
    "product_launch": {"label":"Product Launch","base_intent_alpha":4.5,"base_intent_beta":3.0,"engagement_multiplier":1.2,"city_bias":{"Milano":1.15,"Dubai":1.10,"Paris":1.20,"Tokyo":1.18,"New York":1.22,"London":1.16,"Riyadh":1.08,"Singapore":1.12,"Los Angeles":1.14,"Shanghai":1.10},"revenue_per_purchase":(12000,60000)},
    "pricing_hike": {"label":"Pricing Hike","base_intent_alpha":2.0,"base_intent_beta":5.0,"engagement_multiplier":0.85,"city_bias":{"Milano":0.90,"Dubai":1.00,"Paris":0.95,"Tokyo":0.88,"New York":0.92,"London":0.94,"Riyadh":1.05,"Singapore":0.96,"Los Angeles":0.89,"Shanghai":0.85},"revenue_per_purchase":(15000,80000)},
    "private_client_event": {"label":"Private Client Event","base_intent_alpha":5.0,"base_intent_beta":2.5,"engagement_multiplier":1.1,"city_bias":{"Milano":1.20,"Dubai":1.35,"Paris":1.25,"Tokyo":1.15,"New York":1.30,"London":1.22,"Riyadh":1.40,"Singapore":1.18,"Los Angeles":1.15,"Shanghai":1.12},"revenue_per_purchase":(20000,120000)},
}

ALL_CITIES = ["Milano","Paris","London","New York","Los Angeles","Dubai","Riyadh","Tokyo","Shanghai","Singapore"]

VIC_PERSONAS = [
    ("Ultra-HNWI Collector",0.12,1.6,1.4),
    ("Brand Ambassador",0.08,1.0,1.8),
    ("Aspirational Buyer",0.20,0.7,1.1),
    ("Trend Setter Influencer",0.15,0.9,1.5),
    ("Private Client",0.10,1.5,1.2),
    ("Digital Native",0.15,0.6,1.3),
    ("Heritage Loyalist",0.10,1.2,0.9),
    ("Gulf HNWI",0.05,1.8,1.1),
    ("Asia Pacific VIC",0.05,1.4,1.2),
]

def run_simulation(campaign_type, n_vics, cities, budget, seed=42):
    rng = np.random.default_rng(seed)
    cp = CAMPAIGN_PARAMS[campaign_type]
    n_sim = max(n_vics, 1000)
    city_weights = np.ones(len(cities)) / len(cities)
    assigned_cities = rng.choice(cities, size=n_sim, p=city_weights)
    persona_names = [p[0] for p in VIC_PERSONAS]
    persona_shares = np.array([p[1] for p in VIC_PERSONAS])
    persona_shares /= persona_shares.sum()
    p_intent = np.array([p[2] for p in VIC_PERSONAS])
    p_eng = np.array([p[3] for p in VIC_PERSONAS])
    assigned_personas = rng.choice(len(VIC_PERSONAS), size=n_sim, p=persona_shares)
    budget_factor = min(1.0 + (budget / 2000000) * 0.3, 1.35)
    agents = []
    for i in range(n_sim):
        city = assigned_cities[i]
        cf = cp["city_bias"].get(city, 1.0)
        pi = assigned_personas[i]
        alpha = cp["base_intent_alpha"] * p_intent[pi] * cf * budget_factor
        beta = cp["base_intent_beta"] / (p_intent[pi] * cf)
        intent = float(np.clip(rng.beta(alpha, beta), 0, 1))
        engagement = float(np.clip(rng.beta(3.0*p_eng[pi], 3.5) * cp["engagement_multiplier"] * budget_factor * cf, 0, 1))
        purchased = bool(rng.random() < intent)
        rev_lo, rev_hi = cp["revenue_per_purchase"]
        revenue = float(rng.uniform(rev_lo, rev_hi)) if purchased else 0.0
        influence = float(np.clip(rng.beta(2.0, 5.0) * 100000, 500, 100000))
        agents.append({"VIC ID": f"VIC-{i+1:05d}", "Persona": persona_names[pi], "City": city,
            "Purchase Intent": round(intent*100,1), "Engagement": round(engagement*100,1),
            "Purchased": purchased, "Revenue (EUR)": round(revenue,0), "Influence Score": round(influence,0)})
    df = pd.DataFrame(agents)
    if n_vics < n_sim:
        df = df.sample(n=n_vics, random_state=seed).reset_index(drop=True)
        df["VIC ID"] = [f"VIC-{i+1:05d}" for i in range(len(df))]
    return df

def compute_summary(df, budget):
    total = len(df)
    buyers = int(df["Purchased"].sum())
    buy_rate = buyers / total * 100
    total_revenue = df["Revenue (EUR)"].sum()
    roi = (total_revenue - budget) / budget * 100 if budget > 0 else 0
    city_s = df.groupby("City").agg(VICs=("VIC ID","count"),Buyers=("Purchased","sum"),Avg_Intent=("Purchase Intent","mean"),Revenue=("Revenue (EUR)","sum")).reset_index()
    city_s["Buy Rate (%)"] = (city_s["Buyers"]/city_s["VICs"]*100).round(1)
    city_s["Revenue (EUR)"] = city_s["Revenue"].round(0)
    city_s["Avg Intent (%)"] = city_s["Avg_Intent"].round(1)
    city_s = city_s[["City","VICs","Buyers","Buy Rate (%)","Avg Intent (%)","Revenue (EUR)"]].sort_values("Revenue (EUR)",ascending=False)
    pers_s = df.groupby("Persona").agg(Count=("VIC ID","count"),Buyers=("Purchased","sum"),Avg_Intent=("Purchase Intent","mean"),Revenue=("Revenue (EUR)","sum")).reset_index()
    pers_s["Buy Rate (%)"] = (pers_s["Buyers"]/pers_s["Count"]*100).round(1)
    pers_s["Revenue (EUR)"] = pers_s["Revenue"].round(0)
    pers_s["Avg Intent (%)"] = pers_s["Avg_Intent"].round(1)
    pers_s = pers_s[["Persona","Count","Buy Rate (%)","Avg Intent (%)","Revenue (EUR)"]].sort_values("Revenue (EUR)",ascending=False)
    return {"total":total,"buyers":buyers,"buy_rate":round(buy_rate,1),"total_revenue":round(total_revenue,0),"roi":round(roi,1),"total_reach":int(df["Influence Score"].sum()),"city_summary":city_s,"persona_summary":pers_s}

def make_charts(df, city_summary):
    colors = ["#111111","#C8D400","#444444","#888888","#CCCCCC","#E8E8E4","#333333","#666666","#AAAAAA","#999999"]
    font = dict(family="Montserrat, sans-serif", color="#111111")
    layout_base = dict(paper_bgcolor="#FAFAF8", plot_bgcolor="#FAFAF8", font=font,
        margin=dict(l=20,r=20,t=40,b=20), hoverlabel=dict(bgcolor="#111",font_color="#fff",font_family="Montserrat"))

    fig = make_subplots(rows=1, cols=3,
        subplot_titles=["Buy rate by city", "Purchase intent distribution", "Revenue by city (kEUR)"])

    fig.add_trace(go.Bar(
        x=city_summary["City"], y=city_summary["Buy Rate (%)"],
        marker_color=["#111111" if i==0 else "#CCCCCC" for i in range(len(city_summary))],
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
        showlegend=False), row=1, col=1)

    purchased = df.loc[df["Purchased"], "Purchase Intent"]
    not_purchased = df.loc[~df["Purchased"], "Purchase Intent"]
    fig.add_trace(go.Histogram(x=not_purchased, name="No Purchase", marker_color="#E8E8E4",
        opacity=0.9, nbinsx=25, hovertemplate="Intent: %{x:.0f}%<extra>No Purchase</extra>"), row=1, col=2)
    fig.add_trace(go.Histogram(x=purchased, name="Purchased", marker_color="#111111",
        opacity=0.85, nbinsx=25, hovertemplate="Intent: %{x:.0f}%<extra>Purchased</extra>"), row=1, col=2)

    top = city_summary.sort_values("Revenue (EUR)")
    fig.add_trace(go.Bar(
        y=top["City"], x=top["Revenue (EUR)"]/1000,
        orientation="h",
        marker_color=["#C8D400" if i==len(top)-1 else "#CCCCCC" for i in range(len(top))],
        hovertemplate="%{y}: EUR%{x:,.0f}k<extra></extra>",
        showlegend=False), row=1, col=3)

    fig.update_layout(**layout_base, height=380,
        legend=dict(bgcolor="#FAFAF8", bordercolor="#E8E8E4", font=dict(family="Montserrat")))
    fig.update_xaxes(showgrid=True, gridcolor="#E8E8E4", linecolor="#E8E8E4", tickfont=dict(size=9))
    fig.update_yaxes(showgrid=True, gridcolor="#E8E8E4", linecolor="#E8E8E4", tickfont=dict(size=9))
    for ann in fig.layout.annotations:
        ann.font.size = 10
        ann.font.family = "Montserrat, sans-serif"
        ann.font.color = "#111111"
    return fig

with st.sidebar:
    st.markdown('<div style="text-align:center;padding:1.5rem 0 0.8rem 0;"><img src="https://raw.githubusercontent.com/Learning1-eng/fashion-campaign-predictor/main/dress_for_good_logo copy.png" style="width:80px;height:80px;border-radius:50%;object-fit:cover;"></div><hr style="border-color:#333;margin:0.5rem 0 1.2rem 0;">', unsafe_allow_html=True)
    campaign_type = st.selectbox("Campaign Type",options=list(CAMPAIGN_PARAMS.keys()),format_func=lambda x:CAMPAIGN_PARAMS[x]["label"])
    n_vics = st.slider("Vic Pool Size",min_value=500,max_value=50000,value=5000,step=500)
    cities = st.multiselect("Target Cities",options=ALL_CITIES,default=ALL_CITIES[:5])
    if not cities: cities = ALL_CITIES[:3]
    budget = st.number_input("Campaign Budget (EUR)",min_value=50000,max_value=20000000,value=500000,step=50000)
    st.markdown("<hr style='border-color:#333;margin:1rem 0;'>",unsafe_allow_html=True)
    run = st.button("Run simulation")
    st.markdown("<div style='margin-top:2rem;text-align:center;'><div style='font-family:Montserrat;font-size:0.7rem;font-weight:600;color:#fff;'>Dress for Good</div><div style='font-family:Montserrat;font-size:0.52rem;color:#666;margin-top:0.3rem;'>Milan, Italy — 2026</div></div>", unsafe_allow_html=True)

st.markdown("<div style='border-bottom:2px solid #111;padding-bottom:1rem;margin-bottom:2rem;'>" +
    "<div style='font-family:Montserrat;font-size:0.52rem;font-weight:600;letter-spacing:0.4em;text-transform:uppercase;color:#999;margin-bottom:0.5rem;'>Dress for Good — AI Luxury Studio</div>" +
    "<div style='font-family:Montserrat;font-size:2.4rem;font-weight:700;color:#111;line-height:1.1;'>Fashion campaign predictor</div>" +
    "<div style='font-family:Montserrat;font-size:0.58rem;font-weight:400;letter-spacing:0.15em;color:#999;margin-top:0.5rem;'>Multi-agent simulation — Luxury marketing intelligence</div>" +
    "</div>", unsafe_allow_html=True)

if not run:
    st.markdown("<div style='text-align:center;padding:6rem 2rem;'><div style='font-family:Montserrat;font-size:0.9rem;font-weight:300;color:#CCC;letter-spacing:0.05em;'>Configure parameters and run the simulation</div></div>", unsafe_allow_html=True)
else:
    with st.spinner("Running simulation..."):
        df = run_simulation(campaign_type, n_vics, cities, budget)
        summary = compute_summary(df, budget)
    campaign_label = CAMPAIGN_PARAMS[campaign_type]["label"]
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [(f'{summary["buy_rate"]}%',"Buy rate"),(f'{summary["buyers"]:,}',"Buyers"),(f'EUR {summary["total_revenue"]/1000000:.1f}M',"Revenue"),(f'{summary["roi"]:+.0f}%',"ROI"),(f'{summary["total_reach"]//1000:,}K',"Total reach")]
    for col,(val,label) in zip([c1,c2,c3,c4,c5],kpis):
        with col:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Simulation analysis</div>",unsafe_allow_html=True)
    fig = make_charts(df, summary["city_summary"])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<br>",unsafe_allow_html=True)
    cl,cr = st.columns(2)
    fmt = {"Buy Rate (%)":"{:.1f}","Revenue (EUR)":"EUR{:,.0f}","Avg Intent (%)":"{:.1f}"}
    with cl:
        st.markdown("<div class='section-label'>Performance by city</div>",unsafe_allow_html=True)
        st.dataframe(summary["city_summary"].style.format(fmt),use_container_width=True,hide_index=True)
    with cr:
        st.markdown("<div class='section-label'>Vic persona intelligence</div>",unsafe_allow_html=True)
        st.dataframe(summary["persona_summary"].style.format(fmt),use_container_width=True,hide_index=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Vic agent data</div>",unsafe_allow_html=True)
    disp = df.copy()
    disp["Purchase Intent"] = disp["Purchase Intent"].map("{:.1f}%".format)
    disp["Engagement"] = disp["Engagement"].map("{:.1f}%".format)
    disp["Revenue (EUR)"] = disp["Revenue (EUR)"].map("EUR{:,.0f}".format)
    disp["Influence Score"] = disp["Influence Score"].map("{:,.0f}".format)
    disp["Purchased"] = disp["Purchased"].map({True:"Yes",False:"No"})
    st.dataframe(disp,use_container_width=True,height=320,hide_index=True)
    st.markdown("<br>",unsafe_allow_html=True)
    csv = io.StringIO()
    df.to_csv(csv,index=False)
    st.download_button("Export VIC dataset (CSV)",data=csv.getvalue(),file_name=f"campaign_{campaign_type}_{n_vics}vics.csv",mime="text/csv")
    st.markdown("<hr style='border-color:#E8E8E4;margin:1.5rem 0;'>",unsafe_allow_html=True)
    roi_read = "strong positive" if summary["roi"]>50 else "moderate" if summary["roi"]>0 else "negative"
    top_city = summary["city_summary"].iloc[0]["City"]
    top_persona = summary["persona_summary"].iloc[0]["Persona"]
    readout = (f"Simulation of {summary['total']:,} synthetic VIC agents across {', '.join(cities)} "
               f"projects a {roi_read} ROI of {summary['roi']:+.0f}% on a EUR{budget:,.0f} investment. "
               f"Conversion: {summary['buy_rate']}%. Top market: {top_city}. "
               f"Dominant persona: {top_persona}. Projected revenue: EUR{summary['total_revenue']:,.0f}.")
    st.markdown(f"<div style='font-family:Montserrat;font-size:0.88rem;font-weight:300;color:#111;line-height:1.9;padding:1rem 0 1rem 1.2rem;border-left:3px solid #C8D400;'>{readout}</div>",unsafe_allow_html=True)