# Fashion Campaign Predictor v6.0 - Dress for Good AI Studio

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, base64

st.set_page_config(page_title="Fashion Campaign Predictor", page_icon="D", layout="wide", initial_sidebar_state="expanded")

APP_PASSWORD = "Turati3752"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;900&display=swap');html,body,[class*='css']{background:#fff;color:#111;font-family:Montserrat,sans-serif;}.stApp{background:#fff;}#MainMenu,footer,header{visibility:hidden;}.stButton>button{background:transparent!important;color:#111!important;border:1px solid #111!important;border-radius:0!important;font-family:Montserrat,sans-serif!important;font-size:.65rem!important;font-weight:700!important;letter-spacing:.18em!important;text-transform:uppercase!important;padding:.85rem 2rem!important;transition:all .2s!important;}.stButton>button:hover{background:#C8D400!important;border-color:#C8D400!important;color:#111!important;}</style>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        st.markdown("<div style='text-align:center;padding:5rem 0 2rem'><img src='https://raw.githubusercontent.com/Learning1-eng/fashion-campaign-predictor/main/dress_for_good_logo%20copy.png' style='width:100px;height:100px;border-radius:50%;margin:0 auto;display:block;'><br><span style='font-size:.55rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#999'>Private Access</span></div>", unsafe_allow_html=True)
        pwd = st.text_input("Access code", type="password", placeholder="Enter access code", label_visibility="collapsed")
        if st.button("Enter", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code.")
    st.stop()

st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;900&display=swap');html,body,[class*='css']{font-family:Montserrat,sans-serif!important;background:#fff;color:#111;}.stApp{background:#fff!important;}.main .block-container{background:#fff!important;}.main p,.main span,.main div,.main label{color:#111!important;font-family:Montserrat,sans-serif!important;}section[data-testid='stSidebar']{background:#111!important;}section[data-testid='stSidebar']>div{background:#111!important;}section[data-testid='stSidebar'] label{font-size:.55rem!important;letter-spacing:.12em!important;text-transform:uppercase!important;color:#888!important;font-weight:600!important;}section[data-testid='stSidebar'] input{color:#111!important;background:#fff!important;border:1px solid #ccc!important;border-radius:4px!important;}section[data-testid='stSidebar'] .stNumberInput input{color:#111!important;background:#fff!important;}section[data-testid='stSidebar'] .stNumberInput button{background:#C8D400!important;color:#111!important;border:none!important;font-weight:700!important;}section[data-testid='stSidebar'] [data-baseweb='select'] [data-baseweb='select-container']{background:#fff!important;border:1px solid #111!important;border-radius:4px!important;}section[data-testid='stSidebar'] [data-baseweb='select'] *{color:#111!important;background:#fff!important;}section[data-testid='stSidebar'] [data-baseweb='select'] svg{fill:#111!important;}[data-baseweb='popover'] *{background:#fff!important;color:#111!important;}[data-baseweb='option']{background:#fff!important;color:#111!important;}[data-baseweb='option']:hover{background:#f5f5f5!important;}[data-baseweb='tag']{background:#fff!important;border:1px solid #111!important;border-radius:20px!important;padding:2px 6px 2px 10px!important;margin:2px!important;display:inline-flex!important;align-items:center!important;gap:5px!important;}[data-baseweb='tag'] span{color:#111!important;font-size:.72rem!important;font-weight:500!important;white-space:nowrap!important;}[data-baseweb='tag'] button{background:transparent!important;border:none!important;padding:0!important;margin-left:2px!important;}[data-baseweb='tag'] button svg{fill:#111!important;width:11px!important;height:11px!important;}[data-baseweb='multi-select']{background:#fff!important;border:1px solid #555!important;border-radius:4px!important;}[data-testid='stFileUploader']{padding:0!important;}[data-testid='stFileUploader'] section{padding:.4rem .6rem!important;min-height:unset!important;}[data-testid='stFileUploader'] section > div{gap:.3rem!important;}[data-testid='stFileUploader'] button{font-size:.6rem!important;padding:.3rem .8rem!important;height:auto!important;font-family:Montserrat,sans-serif!important;color:#111!important;background:#fff!important;border:1px solid #555!important;border-radius:4px!important;}[data-testid='stFileUploader'] button svg{width:12px!important;height:12px!important;}[data-testid='stFileUploaderDropzoneInstructions']{display:none!important;}[data-testid='stFileUploader'] small{display:none!important;}[data-testid='stFileUploader'] span[class*='uploadInstructions']{display:none!important;}[data-testid='stSlider'] [role='slider']{background:#C8D400!important;border:2px solid #C8D400!important;width:20px!important;height:20px!important;}.stTabs [data-baseweb='tab-list']{border-bottom:2px solid #111!important;background:transparent!important;gap:0!important;}.stTabs [data-baseweb='tab']{font-family:Montserrat,sans-serif!important;font-size:.6rem!important;font-weight:600!important;letter-spacing:.12em!important;text-transform:uppercase!important;color:#999!important;background:transparent!important;border:none!important;padding:.8rem 1.2rem!important;border-radius:0!important;}.stTabs [data-baseweb='tab']:hover{color:#111!important;}.stTabs [aria-selected='true']{color:#111!important;border-bottom:2px solid #111!important;}.stButton>button{background:transparent!important;color:#fff!important;border:1px solid #fff!important;border-radius:0!important;font-family:Montserrat,sans-serif!important;font-size:.6rem!important;font-weight:700!important;letter-spacing:.18em!important;text-transform:uppercase!important;padding:.9rem 1.5rem!important;width:100%!important;transition:all .2s!important;}.stButton>button:hover{background:#C8D400!important;border-color:#C8D400!important;color:#111!important;}.module-btn>button{background:#111!important;color:#fff!important;border:none!important;border-radius:0!important;font-size:.6rem!important;font-weight:700!important;letter-spacing:.15em!important;padding:.75rem 1.5rem!important;width:auto!important;}.module-btn>button:hover{background:#C8D400!important;color:#111!important;}.metric-card{background:#fff;border:1px solid #E8E8E4;border-top:3px solid #111;padding:1.2rem .8rem;text-align:center;}.metric-value{font-family:Montserrat,sans-serif;font-size:1.8rem;font-weight:700;color:#111;line-height:1;margin-bottom:.3rem;}.metric-label{font-size:.5rem;letter-spacing:.12em;text-transform:uppercase;color:#999;font-weight:600;}.metric-note{font-size:.42rem;color:#bbb;margin-top:.3rem;}.section-label{font-size:.5rem;letter-spacing:.12em;text-transform:uppercase;color:#999;font-weight:600;margin-bottom:.8rem;margin-top:1.5rem;border-bottom:1px solid #E8E8E4;padding-bottom:.4rem;}.insight-card{background:#fff;border:1px solid #E8E8E4;padding:1.2rem;margin-bottom:.8rem;}.insight-card h4{font-family:Montserrat,sans-serif;font-size:.75rem;font-weight:700;color:#111;margin:0 0 .4rem 0;text-transform:uppercase;letter-spacing:.08em;}.insight-card p{font-size:.8rem;color:#444;line-height:1.6;margin:0;}.insight-card .score{font-size:1.6rem;font-weight:900;color:#111;}.insight-card .score-label{font-size:.5rem;color:#999;text-transform:uppercase;letter-spacing:.1em;}.stDataFrame *{color:#111!important;font-family:Montserrat,sans-serif!important;font-size:.75rem!important;}.stDataFrame th{background:#F5F5F3!important;color:#111!important;font-weight:600!important;}.stDownloadButton>button{background:transparent!important;color:#111!important;border:1px solid #111!important;border-radius:0!important;font-size:.55rem!important;letter-spacing:.1em!important;text-transform:uppercase!important;font-weight:600!important;}.stDownloadButton>button:hover{background:#111!important;color:#fff!important;}#MainMenu,footer,header{visibility:hidden;}</style>", unsafe_allow_html=True)

CAMPAIGN_PARAMS = {
    "social_influencer": {"label":"Social Influencer","base_intent_alpha":3.5,"base_intent_beta":4.0,"engagement_multiplier":1.4,"city_bias":{'Milano': 1.05, 'Dubai': 1.2, 'Paris': 1.1, 'Tokyo': 1.15, 'New York': 1.12, 'London': 1.08, 'Riyadh': 1.25, 'Singapore': 1.18, 'Los Angeles': 1.1, 'Shanghai': 1.2},"revenue_per_purchase":(800, 3500)},
    "digital_ar": {"label":"Digital / AR Experience","base_intent_alpha":2.8,"base_intent_beta":4.5,"engagement_multiplier":1.6,"city_bias":{'Milano': 1.1, 'Dubai': 1.3, 'Paris': 1.15, 'Tokyo': 1.35, 'New York': 1.25, 'London': 1.15, 'Riyadh': 1.1, 'Singapore': 1.3, 'Los Angeles': 1.2, 'Shanghai': 1.28},"revenue_per_purchase":(600, 2800)},
    "product_launch": {"label":"Product Launch","base_intent_alpha":4.5,"base_intent_beta":3.0,"engagement_multiplier":1.2,"city_bias":{'Milano': 1.15, 'Dubai': 1.1, 'Paris': 1.2, 'Tokyo': 1.18, 'New York': 1.22, 'London': 1.16, 'Riyadh': 1.08, 'Singapore': 1.12, 'Los Angeles': 1.14, 'Shanghai': 1.1},"revenue_per_purchase":(1200, 6000)},
    "pricing_hike": {"label":"Pricing Hike","base_intent_alpha":2.0,"base_intent_beta":5.0,"engagement_multiplier":0.85,"city_bias":{'Milano': 0.9, 'Dubai': 1.0, 'Paris': 0.95, 'Tokyo': 0.88, 'New York': 0.92, 'London': 0.94, 'Riyadh': 1.05, 'Singapore': 0.96, 'Los Angeles': 0.89, 'Shanghai': 0.85},"revenue_per_purchase":(1500, 8000)},
    "private_client_event": {"label":"Private Client Event","base_intent_alpha":5.0,"base_intent_beta":2.5,"engagement_multiplier":1.1,"city_bias":{'Milano': 1.2, 'Dubai': 1.35, 'Paris': 1.25, 'Tokyo': 1.15, 'New York': 1.3, 'London': 1.22, 'Riyadh': 1.4, 'Singapore': 1.18, 'Los Angeles': 1.15, 'Shanghai': 1.12},"revenue_per_purchase":(2000, 12000)},
}
ALL_CITIES = ["Milano","Paris","London","New York","Los Angeles","Dubai","Riyadh","Tokyo","Shanghai","Singapore"]
VIC_PERSONAS = [
    ("Ultra-HNWI Collector",0.12,1.6,1.4),("Brand Ambassador",0.08,1.0,1.8),
    ("Aspirational Buyer",0.20,0.7,1.1),("Trend Setter Influencer",0.15,0.9,1.5),
    ("Private Client",0.10,1.5,1.2),("Digital Native",0.15,0.6,1.3),
    ("Heritage Loyalist",0.10,1.2,0.9),("Gulf HNWI",0.05,1.8,1.1),("Asia Pacific VIC",0.05,1.4,1.2),
]

def run_simulation(campaign_type, n_vics, cities, budget, seed=42):
    rng = np.random.default_rng(seed)
    cp = CAMPAIGN_PARAMS[campaign_type]
    n_sim = max(n_vics, 1000)
    city_weights = np.ones(len(cities)) / len(cities)
    assigned_cities = rng.choice(cities, size=n_sim, p=city_weights)
    persona_names = [p[0] for p in VIC_PERSONAS]
    persona_shares = np.array([p[1] for p in VIC_PERSONAS]); persona_shares /= persona_shares.sum()
    p_intent = np.array([p[2] for p in VIC_PERSONAS])
    p_eng = np.array([p[3] for p in VIC_PERSONAS])
    assigned_personas = rng.choice(len(VIC_PERSONAS), size=n_sim, p=persona_shares)
    budget_factor = min(1.0 + (budget / 2000000) * 0.3, 1.35)
    agents = []
    for i in range(n_sim):
        city = assigned_cities[i]; cf = cp["city_bias"].get(city,1.0); pi = assigned_personas[i]
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
    total = len(df); buyers = int(df["Purchased"].sum())
    buy_rate = buyers/total*100; total_revenue = df["Revenue (EUR)"].sum()
    roi = (total_revenue-budget)/budget*100 if budget>0 else 0
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
    font = dict(family="Montserrat, sans-serif", color="#111111")
    layout_base = dict(paper_bgcolor="#fff", plot_bgcolor="#fff", font=font,
        margin=dict(l=10,r=10,t=35,b=10), hoverlabel=dict(bgcolor="#111",font_color="#fff",font_family="Montserrat"))
    fig = make_subplots(rows=1, cols=3, column_widths=[0.28,0.44,0.28],
        subplot_titles=["Buy rate by city","Purchase intent distribution","Revenue by city (kEUR)"])
    clrs = ["#111111" if i==0 else "#CCCCCC" for i in range(len(city_summary))]
    fig.add_trace(go.Bar(x=city_summary["City"], y=city_summary["Buy Rate (%)"], marker_color=clrs, hovertemplate="%{x}: %{y:.1f}%<extra></extra>", showlegend=False), row=1, col=1)
    fig.add_trace(go.Histogram(x=df.loc[~df["Purchased"],"Purchase Intent"], name="No Purchase", marker_color="#E8E8E4", opacity=0.9, nbinsx=25), row=1, col=2)
    fig.add_trace(go.Histogram(x=df.loc[df["Purchased"],"Purchase Intent"], name="Purchased", marker_color="#111111", opacity=0.85, nbinsx=25), row=1, col=2)
    top = city_summary.sort_values("Revenue (EUR)")
    clrs3 = ["#C8D400" if i==len(top)-1 else "#CCCCCC" for i in range(len(top))]
    fig.add_trace(go.Bar(y=top["City"], x=top["Revenue (EUR)"]/1000, orientation="h", marker_color=clrs3, hovertemplate="%{y}: EUR%{x:,.0f}k<extra></extra>", showlegend=False), row=1, col=3)
    fig.update_layout(**layout_base, height=250, legend=dict(bgcolor="#fff",bordercolor="#E8E8E4",font=dict(family="Montserrat",size=9)))
    fig.update_xaxes(showgrid=True,gridcolor="#E8E8E4",linecolor="#E8E8E4",tickfont=dict(size=8,color="#111"))
    fig.update_yaxes(showgrid=True,gridcolor="#E8E8E4",linecolor="#E8E8E4",tickfont=dict(size=8,color="#111"))
    for ann in fig.layout.annotations: ann.font.size=9; ann.font.family="Montserrat, sans-serif"; ann.font.color="#111111"
    return fig

LOGO_URL = "https://raw.githubusercontent.com/Learning1-eng/fashion-campaign-predictor/main/dress_for_good_logo%20copy.png"

with st.sidebar:
    try:
        import requests
        from PIL import Image as PILImage
        import io as _io
        r = requests.get(LOGO_URL, timeout=3)
        img = PILImage.open(_io.BytesIO(r.content))
        st.image(img, width=90)
    except:
        st.markdown('<div style="text-align:center;font-size:1.2rem;font-weight:900;color:#C8D400;padding:.8rem 0;">DFG</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:#333;margin:.3rem 0 .8rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.5rem;letter-spacing:.1em;text-transform:uppercase;color:#666;margin-bottom:.3rem;">Client brand logo</div>', unsafe_allow_html=True)
    uploaded_logo = st.file_uploader("logo", type=["png","jpg","jpeg"], label_visibility="collapsed")
    if uploaded_logo:
        logo_data = base64.b64encode(uploaded_logo.read()).decode()
        st.markdown(f'<div style="text-align:center;padding:.3rem 0 .6rem;"><img src="data:image/png;base64,{logo_data}" style="max-width:120px;max-height:50px;object-fit:contain;"></div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:#333;margin:.5rem 0 .8rem;">', unsafe_allow_html=True)
    campaign_type = st.selectbox("Campaign Type",options=list(CAMPAIGN_PARAMS.keys()),format_func=lambda x:CAMPAIGN_PARAMS[x]["label"])
    n_vics = st.slider("VIC Pool Size",min_value=500,max_value=50000,value=5000,step=500)
    cities = st.multiselect("Target Cities",options=ALL_CITIES,default=ALL_CITIES[:5])
    if not cities: cities = ALL_CITIES[:3]
    budget = st.number_input("Campaign Budget (EUR)",min_value=50000,max_value=20000000,value=500000,step=50000)
    st.markdown('<hr style="border-color:#333;margin:1rem 0;">', unsafe_allow_html=True)
    run = st.button("Run simulation")
    st.markdown('<div style="margin-top:1.5rem;text-align:center;font-size:.65rem;font-weight:600;color:#555;letter-spacing:.1em;text-transform:uppercase;">Dress for Good</div>', unsafe_allow_html=True)

st.markdown("<div style='border-bottom:1px solid #E0E0E0;padding-bottom:1.5rem;margin-bottom:2rem;'>" +
    "<div style='font-family:Montserrat,sans-serif;font-size:.65rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#111;margin-bottom:.8rem;'>Dress for Good — AI Luxury Studio</div>" +
    "<div style='font-family:Montserrat,sans-serif;font-size:2.8rem;font-weight:900;color:#111;line-height:1.05;letter-spacing:-.02em;'>Fashion campaign predictor</div>" +
    "<div style='font-family:Montserrat,sans-serif;font-size:.85rem;font-weight:400;color:#111;margin-top:.6rem;'>Multi-agent simulation — Luxury marketing intelligence</div>" +
    "</div>", unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
    "Campaign Simulator",
    "Creative Testing",
    "Product Launch",
    "Price Optimisation",
    "Market Segmentation",
    "Churn Prediction",
    "Brand Perception",
])

with tab1:
    if not run:
        st.markdown("<div style='text-align:center;padding:4rem 2rem;'><span style='font-family:Montserrat,sans-serif;font-size:1.1rem;font-weight:500;color:#111;'>Configure parameters in the sidebar and run the simulation</span></div>", unsafe_allow_html=True)
    else:
        with st.spinner("Running simulation..."):
            df = run_simulation(campaign_type, n_vics, cities, budget)
            summary = compute_summary(df, budget)
        campaign_label = CAMPAIGN_PARAMS[campaign_type]["label"]
        c1,c2,c3,c4,c5 = st.columns(5)
        kpis = [
            (f'{summary["buy_rate"]}%',"Buy rate","Beta-dist. intent model"),
            (f'{summary["buyers"]:,}',"Buyers","VICs with intent > threshold"),
            (f'EUR {summary["total_revenue"]/1000000:.1f}M',"Revenue","Avg ticket x buyers"),
            (f'{summary["roi"]:+.0f}%',"ROI","(Revenue - Budget) / Budget"),
            (f'{summary["total_reach"]//1000000:.1f}M',"Total reach","Sum influence scores"),
        ]
        for col,(val,label,note) in zip([c1,c2,c3,c4,c5],kpis):
            with col:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}*</div><div class='metric-label'>{label}</div><div class='metric-note'>{note}</div></div>",unsafe_allow_html=True)
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
            st.markdown("<div class='section-label'>VIC persona intelligence</div>",unsafe_allow_html=True)
            st.dataframe(summary["persona_summary"].style.format(fmt),use_container_width=True,hide_index=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("<div class='section-label'>VIC agent data</div>",unsafe_allow_html=True)
        disp = df.copy()
        disp["Purchase Intent"] = disp["Purchase Intent"].map("{:.1f}%".format)
        disp["Engagement"] = disp["Engagement"].map("{:.1f}%".format)
        disp["Revenue (EUR)"] = disp["Revenue (EUR)"].map("EUR{:,.0f}".format)
        disp["Influence Score"] = disp["Influence Score"].map("{:,.0f}".format)
        disp["Purchased"] = disp["Purchased"].map({True:"Yes",False:"No"})
        st.dataframe(disp,use_container_width=True,height=300,hide_index=True)
        st.markdown("<br>",unsafe_allow_html=True)
        csv = io.StringIO(); df.to_csv(csv,index=False)
        exc_buf = io.BytesIO()
        with pd.ExcelWriter(exc_buf, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="VIC Data")
            summary["city_summary"].to_excel(writer, index=False, sheet_name="City Summary")
            summary["persona_summary"].to_excel(writer, index=False, sheet_name="Persona Summary")
        exc_buf.seek(0)
        col_csv,col_xl = st.columns(2)
        with col_csv:
            st.download_button("Export CSV",data=csv.getvalue(),file_name=f"campaign_{campaign_type}_{n_vics}vics.csv",mime="text/csv")
        with col_xl:
            st.download_button("Export Excel",data=exc_buf.read(),file_name=f"campaign_{campaign_type}_{n_vics}vics.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.markdown("<hr style='border-color:#E8E8E4;margin:1.5rem 0;'>",unsafe_allow_html=True)
        roi_read = "strong positive" if summary["roi"]>50 else "moderate" if summary["roi"]>0 else "negative"
        top_city = summary["city_summary"].iloc[0]["City"]
        top_persona = summary["persona_summary"].iloc[0]["Persona"]
        readout = (f"Simulation of {summary['total']:,} synthetic VIC agents across {', '.join(cities)} "
                   f"projects a {roi_read} ROI of {summary['roi']:+.0f}% on a EUR{budget:,.0f} investment. "
                   f"Conversion: {summary['buy_rate']}%. Top market: {top_city}. Dominant persona: {top_persona}. "
                   f"Projected revenue: EUR{summary['total_revenue']:,.0f}.")
        st.markdown(f"<div style='font-family:Montserrat;font-size:.88rem;font-weight:300;color:#111;line-height:1.9;padding:1rem 0 1rem 1.2rem;border-left:3px solid #C8D400;'>{readout}</div>",unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='section-label'>Creative Testing</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Test creative concepts against synthetic VIC panels before campaign launch. Compare visual, copy, and format variants.</p>",unsafe_allow_html=True)
    rng2 = np.random.default_rng(99)
    concepts = st.text_area("Enter creative concepts (one per line)", "Heritage storytelling\nProduct close-up\nLifestyle aspiration\nCelebrity endorsement", height=100)
    panel_size = st.slider("VIC panel size", 200, 5000, 1000, 100, key="ct_panel")
    if st.button("Test Concepts", key="ct_run"):
        concept_list = [c.strip() for c in concepts.split("\n") if c.strip()]
        results = []
        for concept in concept_list:
            np.random.seed(hash(concept) % 10000)
            recall = round(np.random.beta(3,4)*100, 1)
            purchase_lift = round(np.random.beta(2,5)*60, 1)
            engagement = round(np.random.beta(4,3)*100, 1)
            brand_fit = round(np.random.beta(5,2)*100, 1)
            results.append({"Concept": concept, "Recall (%)": recall, "Purchase Lift (%)": purchase_lift, "Engagement (%)": engagement, "Brand Fit (%)": brand_fit})
        res_df = pd.DataFrame(results).sort_values("Purchase Lift (%)", ascending=False)
        winner = res_df.iloc[0]["Concept"]
        c1,c2,c3,c4 = st.columns(4)
        for col, metric in zip([c1,c2,c3,c4], ["Recall (%)","Purchase Lift (%)","Engagement (%)","Brand Fit (%)"]):
            with col:
                best = res_df.iloc[0][metric]
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{best:.0f}%</div><div class='metric-label'>{metric.replace(" (%)","")}</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        fig_ct = go.Figure()
        for metric, color in [("Recall (%)","#111"),("Engagement (%)","#C8D400"),("Purchase Lift (%)","#888"),("Brand Fit (%)","#ccc")]:
            fig_ct.add_trace(go.Bar(name=metric.replace(" (%)",""), x=res_df["Concept"], y=res_df[metric], marker_color=color))
        fig_ct.update_layout(barmode="group", paper_bgcolor="#fff", plot_bgcolor="#fff", height=300,
            font=dict(family="Montserrat",color="#111"), legend=dict(font=dict(size=9)),
            margin=dict(l=10,r=10,t=20,b=10))
        fig_ct.update_xaxes(tickfont=dict(size=9,color="#111"), gridcolor="#E8E8E4")
        fig_ct.update_yaxes(tickfont=dict(size=9,color="#111"), gridcolor="#E8E8E4")
        st.plotly_chart(fig_ct, use_container_width=True)
        st.markdown(f"<div style='padding:1rem;border-left:3px solid #C8D400;font-size:.88rem;color:#111;'><strong>Winner:</strong> {winner} leads on purchase lift with the highest conversion potential across the VIC panel.</div>",unsafe_allow_html=True)
        st.dataframe(res_df.style.format({"Recall (%)":"{:.1f}","Purchase Lift (%)":"{:.1f}","Engagement (%)":"{:.1f}","Brand Fit (%)":"{:.1f}"}),use_container_width=True,hide_index=True)

with tab3:
    st.markdown("<div class='section-label'>Product Launch Simulator</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Forecast adoption curves, revenue potential, and VIC response to new product introductions across markets.</p>",unsafe_allow_html=True)
    pl_col1, pl_col2 = st.columns(2)
    with pl_col1:
        product_name = st.text_input("Product name", "New Collection SS26")
        price_point = st.number_input("Price point (EUR)", 500, 50000, 2500, 500)
        launch_cities = st.multiselect("Launch markets", ALL_CITIES, ALL_CITIES[:3], key="pl_cities")
    with pl_col2:
        exclusivity = st.select_slider("Exclusivity level", ["Mass","Premium","Luxury","Ultra-Luxury"], "Luxury")
        launch_window = st.slider("Launch window (weeks)", 1, 12, 4, key="pl_weeks")
        marketing_budget = st.number_input("Marketing budget (EUR)", 50000, 5000000, 200000, 50000, key="pl_budget")
    if st.button("Simulate Launch", key="pl_run"):
        excl_map = {"Mass":0.6,"Premium":0.8,"Luxury":1.0,"Ultra-Luxury":1.2}
        excl_factor = excl_map[exclusivity]
        rng_pl = np.random.default_rng(42)
        weeks = list(range(1, launch_window+1))
        adoption = [round(min(100, 2*w*excl_factor*(marketing_budget/200000)**0.3 + rng_pl.normal(0,2)), 1) for w in weeks]
        revenue_proj = [round(a/100 * len(launch_cities or ["Milano"]) * 500 * price_point * excl_factor, 0) for a in adoption]
        total_rev = sum(revenue_proj)
        roi_pl = (total_rev - marketing_budget) / marketing_budget * 100
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{adoption[-1]:.0f}%</div><div class='metric-label'>Peak adoption</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {total_rev/1000000:.1f}M</div><div class='metric-label'>Projected revenue</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>{roi_pl:+.0f}%</div><div class='metric-label'>ROI</div></div>",unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(launch_cities or ["Milano"])}</div><div class='metric-label'>Markets</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        fig_pl = go.Figure()
        fig_pl.add_trace(go.Scatter(x=weeks, y=adoption, mode="lines+markers", name="Adoption %",
            line=dict(color="#111",width=2), marker=dict(color="#C8D400",size=8)))
        fig_pl.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=250,
            font=dict(family="Montserrat",color="#111"),margin=dict(l=10,r=10,t=20,b=10),
            xaxis_title="Week",yaxis_title="Adoption (%)")
        fig_pl.update_xaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        fig_pl.update_yaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        st.plotly_chart(fig_pl, use_container_width=True)
        st.markdown(f"<div style='padding:1rem;border-left:3px solid #C8D400;font-size:.88rem;color:#111;'>Launch projection for <strong>{product_name}</strong> at EUR{price_point:,} across {len(launch_cities or ["Milano"])} markets. {exclusivity} positioning drives peak adoption of {adoption[-1]:.0f}% by week {launch_window}.</div>",unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='section-label'>Price Optimisation</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Model price elasticity across VIC segments and identify the optimal price point that maximises revenue without eroding brand equity.</p>",unsafe_allow_html=True)
    po_col1, po_col2 = st.columns(2)
    with po_col1:
        current_price = st.number_input("Current price (EUR)", 500, 100000, 3000, 500, key="po_price")
        price_range = st.slider("Price range to test", 0.5, 2.0, (0.7, 1.5), 0.1, key="po_range")
    with po_col2:
        segment = st.selectbox("VIC segment", ["All segments","Ultra-HNWI Collector","Private Client","Aspirational Buyer"], key="po_seg")
        po_cities = st.multiselect("Markets", ALL_CITIES, ALL_CITIES[:3], key="po_cities")
    if st.button("Run Price Model", key="po_run"):
        prices = np.linspace(current_price*price_range[0], current_price*price_range[1], 20)
        elasticity = -1.8 if "Aspirational" in segment else -0.9 if "HNWI" in segment else -1.3
        base_demand = 1000
        demand = [max(0, base_demand * (p/current_price)**elasticity + np.random.normal(0,20)) for p in prices]
        revenue = [p*d for p,d in zip(prices,demand)]
        opt_idx = int(np.argmax(revenue))
        opt_price = prices[opt_idx]
        opt_rev = revenue[opt_idx]
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {opt_price:,.0f}</div><div class='metric-label'>Optimal price</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value'>{(opt_price/current_price-1)*100:+.0f}%</div><div class='metric-label'>vs current</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {opt_rev/1000:.0f}K</div><div class='metric-label'>Max revenue</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        fig_po = go.Figure()
        fig_po.add_trace(go.Scatter(x=list(prices), y=revenue, mode="lines", name="Revenue", line=dict(color="#111",width=2)))
        fig_po.add_vline(x=opt_price, line_dash="dash", line_color="#C8D400", annotation_text=f"Optimal EUR{opt_price:,.0f}", annotation_font_color="#111")
        fig_po.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=250,font=dict(family="Montserrat",color="#111"),margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Price (EUR)",yaxis_title="Revenue (EUR)")
        fig_po.update_xaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        fig_po.update_yaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        st.plotly_chart(fig_po, use_container_width=True)

with tab5:
    st.markdown("<div class='section-label'>Market Segmentation</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Analyse VIC population distribution across personas, cities, and behavioural clusters to identify high-value micro-segments.</p>",unsafe_allow_html=True)
    seg_cities = st.multiselect("Markets to analyse", ALL_CITIES, ALL_CITIES, key="seg_cities")
    if st.button("Run Segmentation", key="seg_run"):
        rng_seg = np.random.default_rng(77)
        seg_data = []
        for city in (seg_cities or ALL_CITIES):
            for persona_name, share, intent_m, eng_m in VIC_PERSONAS:
                size = int(rng_seg.normal(1000*share, 50))
                ltv = round(rng_seg.uniform(5000,80000) * intent_m, 0)
                churn_risk = round(rng_seg.beta(2,5)*100, 1)
                seg_data.append({"City":city,"Segment":persona_name,"Size":size,"Avg LTV (EUR)":ltv,"Churn Risk (%)":churn_risk})
        seg_df = pd.DataFrame(seg_data)
        top_segs = seg_df.groupby("Segment").agg({"Size":"sum","Avg LTV (EUR)":"mean","Churn Risk (%)":"mean"}).reset_index().sort_values("Avg LTV (EUR)",ascending=False)
        fig_seg = go.Figure(go.Treemap(
            labels=top_segs["Segment"],
            parents=["" for _ in top_segs["Segment"]],
            values=top_segs["Size"],
            customdata=top_segs["Avg LTV (EUR)"].apply(lambda x: f"EUR{x:,.0f}"),
            texttemplate="<b>%{label}</b><br>%{customdata}",
            marker=dict(colors=top_segs["Avg LTV (EUR)"], colorscale=[[0,"#E8E8E4"],[0.5,"#888"],[1,"#111"]])
        ))
        fig_seg.update_layout(paper_bgcolor="#fff",height=350,margin=dict(l=0,r=0,t=10,b=0),font=dict(family="Montserrat",color="#111"))
        st.plotly_chart(fig_seg, use_container_width=True)
        fmt_seg = {"Avg LTV (EUR)":"EUR{:,.0f}","Churn Risk (%)":"{:.1f}"} 
        st.dataframe(top_segs.style.format(fmt_seg),use_container_width=True,hide_index=True)

with tab6:
    st.markdown("<div class='section-label'>Churn Prediction</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Identify VICs at risk of disengagement based on purchase recency, engagement decay, and competitive exposure signals.</p>",unsafe_allow_html=True)
    ch_col1, ch_col2 = st.columns(2)
    with ch_col1:
        ch_cities = st.multiselect("Markets", ALL_CITIES, ALL_CITIES[:4], key="ch_cities")
        ch_threshold = st.slider("Churn risk threshold (%)", 30, 80, 50, 5, key="ch_threshold")
    with ch_col2:
        recency_weight = st.slider("Recency weight", 0.1, 1.0, 0.5, 0.1, key="ch_recency")
        engagement_weight = st.slider("Engagement weight", 0.1, 1.0, 0.5, 0.1, key="ch_eng")
    if st.button("Predict Churn", key="ch_run"):
        rng_ch = np.random.default_rng(55)
        ch_data = []
        for i in range(500):
            city = rng_ch.choice(ch_cities or ALL_CITIES[:4])
            persona = VIC_PERSONAS[rng_ch.integers(0, len(VIC_PERSONAS))][0]
            recency = rng_ch.integers(1, 365)
            eng_score = round(rng_ch.beta(3,4)*100, 1)
            churn_prob = min(100, recency_weight*(recency/365*100) + engagement_weight*(100-eng_score) + rng_ch.normal(0,5))
            ltv = round(rng_ch.uniform(2000, 50000), 0)
            ch_data.append({"City":city,"Persona":persona,"Days since purchase":recency,"Engagement (%)":eng_score,"Churn risk (%)":round(churn_prob,1),"LTV (EUR)":ltv})
        ch_df = pd.DataFrame(ch_data)
        at_risk = ch_df[ch_df["Churn risk (%)"] >= ch_threshold]
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(at_risk)}</div><div class='metric-label'>At-risk VICs</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(at_risk)/5:.0f}%</div><div class='metric-label'>Churn rate</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {at_risk['LTV (EUR)'].sum()/1000:.0f}K</div><div class='metric-label'>Revenue at risk</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        fig_ch = go.Figure(go.Scatter(
            x=ch_df["Days since purchase"], y=ch_df["Churn risk (%)"],
            mode="markers", marker=dict(
                color=ch_df["Churn risk (%)"], colorscale=[[0,"#E8E8E4"],[0.5,"#888"],[1,"#111"]],
                size=6, showscale=False),
            text=ch_df["Persona"], hovertemplate="%{text}<br>Days: %{x}<br>Risk: %{y:.1f}%<extra></extra>"))
        fig_ch.add_hline(y=ch_threshold, line_dash="dash", line_color="#C8D400")
        fig_ch.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=280,font=dict(family="Montserrat",color="#111"),margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Days since last purchase",yaxis_title="Churn risk (%)")
        fig_ch.update_xaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        fig_ch.update_yaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        st.plotly_chart(fig_ch, use_container_width=True)
        st.markdown("<div class='section-label'>At-risk VICs</div>",unsafe_allow_html=True)
        fmt_ch = {"Engagement (%)":"{:.1f}","Churn risk (%)":"{:.1f}","LTV (EUR)":"EUR{:,.0f}"}
        st.dataframe(at_risk.sort_values("Churn risk (%)",ascending=False).head(50).style.format(fmt_ch),use_container_width=True,hide_index=True)

with tab7:
    st.markdown("<div class='section-label'>Brand Perception Tracking</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Track brand equity dimensions across VIC segments and markets. Benchmark desirability, exclusivity, heritage, and innovation scores.</p>",unsafe_allow_html=True)
    bp_col1, bp_col2 = st.columns(2)
    with bp_col1:
        bp_brand = st.text_input("Brand name", "Your Brand")
        bp_cities = st.multiselect("Markets", ALL_CITIES, ALL_CITIES[:5], key="bp_cities")
    with bp_col2:
        bp_segment = st.multiselect("VIC segments", [p[0] for p in VIC_PERSONAS], [p[0] for p in VIC_PERSONAS[:4]], key="bp_seg")
    if st.button("Run Brand Perception", key="bp_run"):
        dimensions = ["Desirability","Exclusivity","Heritage","Innovation","Sustainability","Digital Presence"]
        rng_bp = np.random.default_rng(33)
        scores = {d: round(rng_bp.beta(4,2)*100, 1) for d in dimensions}
        city_scores = {city: {d: round(rng_bp.beta(3.5,2)*100,1) for d in dimensions} for city in (bp_cities or ALL_CITIES[:5])}
        c1,c2,c3 = st.columns(3)
        overall = round(np.mean(list(scores.values())),1)
        strongest = max(scores, key=scores.get)
        weakest = min(scores, key=scores.get)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{overall}</div><div class='metric-label'>Brand equity score</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value' style='font-size:1.2rem;'>{strongest}</div><div class='metric-label'>Strongest dimension</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value' style='font-size:1.2rem;'>{weakest}</div><div class='metric-label'>Opportunity area</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatterpolar(
            r=list(scores.values()), theta=dimensions, fill="toself",
            line_color="#111", fillcolor="rgba(200,212,0,0.15)", name=bp_brand))
        fig_bp.update_layout(
            polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=8,color="#111"),gridcolor="#E8E8E4"),
                       angularaxis=dict(tickfont=dict(size=9,color="#111"),gridcolor="#E8E8E4")),
            paper_bgcolor="#fff", height=350, showlegend=True,
            font=dict(family="Montserrat",color="#111"), margin=dict(l=40,r=40,t=20,b=20))
        st.plotly_chart(fig_bp, use_container_width=True)
        city_df = pd.DataFrame(city_scores).T.reset_index().rename(columns={"index":"City"})
        st.markdown("<div class='section-label'>Brand perception by market</div>",unsafe_allow_html=True)
        fmt_bp = {d:"{:.1f}" for d in dimensions}
        st.dataframe(city_df.style.format(fmt_bp),use_container_width=True,hide_index=True)