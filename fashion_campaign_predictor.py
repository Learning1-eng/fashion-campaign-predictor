# Fashion Campaign Predictor v2.1 - Dress for Good AI Studio

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests
from PIL import Image

st.set_page_config(page_title="Fashion Campaign Predictor", page_icon="D", layout="wide", initial_sidebar_state="expanded")

APP_PASSWORD = "Turati3752"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');html,body,[class*='css']{background:#fff;color:#111;font-family:Lato,sans-serif;}.stApp{background:#fff;}#MainMenu,footer,header{visibility:hidden;}</style>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        st.markdown("<div style='text-align:center;padding:5rem 0 2rem'><div style='font-size:0.6rem;font-weight:700;letter-spacing:0.4em;text-transform:uppercase;color:#999;margin-bottom:1rem'>AI Luxury Studio</div><div style='font-size:2rem;font-weight:900;color:#111;text-transform:uppercase'>DRESS FOR GOOD</div><div style='width:40px;height:2px;background:#111;margin:1rem auto'></div><div style='font-size:0.58rem;font-weight:700;letter-spacing:0.3em;text-transform:uppercase;color:#999'>Private Access</div></div>", unsafe_allow_html=True)
        pwd = st.text_input("", type="password", placeholder="Access code")
        if st.button("ENTER", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code.")
    st.stop()

CSS = ("""<style>"""
    """@import url("https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap");"""
    """html,body,[class*="css"]{font-family:Lato,sans-serif!important;background-color:#FAFAF8;color:#111;}"""
    """.stApp{background:#FAFAF8;}"""
    """section[data-testid="stSidebar"]{background:#111111!important;border-right:none;}"""
    """section[data-testid="stSidebar"] *{color:#FFF!important;font-family:Lato,sans-serif!important;}"""
    """section[data-testid="stSidebar"] label{font-size:0.58rem!important;letter-spacing:0.32em!important;text-transform:uppercase!important;color:#888!important;font-weight:700!important;}"""
    """.stButton>button{background:#111!important;color:#fff!important;border:none!important;border-radius:0!important;font-family:Lato,sans-serif!important;font-size:0.65rem!important;font-weight:700!important;letter-spacing:0.35em!important;text-transform:uppercase!important;padding:0.9rem 2rem!important;width:100%!important;transition:all 0.2s!important;}"""
    """.stButton>button:hover{background:#C8D400!important;color:#111!important;}"""
    """.metric-card{background:#fff;border:1px solid #E8E8E4;border-top:3px solid #111;padding:1.4rem 1.2rem;text-align:center;}"""
    """.metric-value{font-family:Lato,sans-serif;font-size:2.1rem;font-weight:900;color:#111;line-height:1;margin-bottom:0.4rem;letter-spacing:-0.02em;}"""
    """.metric-label{font-size:0.56rem;letter-spacing:0.32em;text-transform:uppercase;color:#999;font-weight:700;}"""
    """.section-label{font-size:0.56rem;letter-spacing:0.4em;text-transform:uppercase;color:#999;font-weight:700;margin-bottom:0.8rem;margin-top:1.5rem;border-bottom:1px solid #E8E8E4;padding-bottom:0.5rem;}"""
    """.stDownloadButton>button{background:transparent!important;color:#111!important;border:1px solid #111!important;border-radius:0!important;font-size:0.58rem!important;letter-spacing:0.25em!important;text-transform:uppercase!important;font-weight:700!important;}"""
    """.stDownloadButton>button:hover{background:#111!important;color:#fff!important;}"""
    """.stDataFrame,.stDataFrame *{color:#111!important;font-family:Lato,sans-serif!important;font-size:0.78rem!important;}"""
    """#MainMenu,footer,header{visibility:hidden;}"""
    """</style>""")
st.markdown(CSS, unsafe_allow_html=True)

CAMPAIGN_PARAMS = {
    "social_influencer": {"label":"Social Influencer","base_intent_alpha":3.5,"base_intent_beta":4.0,"engagement_multiplier":1.4,"vip_sensitivity":0.8,"city_bias":{"Milano":1.05,"Dubai":1.20,"Paris":1.10,"Tokyo":1.15,"New York":1.12,"London":1.08,"Riyadh":1.25,"Singapore":1.18,"Los Angeles":1.10,"Shanghai":1.20},"revenue_per_purchase":(8000,35000)},
    "digital_ar": {"label":"Digital / AR Experience","base_intent_alpha":2.8,"base_intent_beta":4.5,"engagement_multiplier":1.6,"vip_sensitivity":0.6,"city_bias":{"Milano":1.10,"Dubai":1.30,"Paris":1.15,"Tokyo":1.35,"New York":1.25,"London":1.15,"Riyadh":1.10,"Singapore":1.30,"Los Angeles":1.20,"Shanghai":1.28},"revenue_per_purchase":(6000,28000)},
    "product_launch": {"label":"Product Launch","base_intent_alpha":4.5,"base_intent_beta":3.0,"engagement_multiplier":1.2,"vip_sensitivity":1.1,"city_bias":{"Milano":1.15,"Dubai":1.10,"Paris":1.20,"Tokyo":1.18,"New York":1.22,"London":1.16,"Riyadh":1.08,"Singapore":1.12,"Los Angeles":1.14,"Shanghai":1.10},"revenue_per_purchase":(12000,60000)},
    "pricing_hike": {"label":"Pricing Hike","base_intent_alpha":2.0,"base_intent_beta":5.0,"engagement_multiplier":0.85,"vip_sensitivity":1.3,"city_bias":{"Milano":0.90,"Dubai":1.00,"Paris":0.95,"Tokyo":0.88,"New York":0.92,"London":0.94,"Riyadh":1.05,"Singapore":0.96,"Los Angeles":0.89,"Shanghai":0.85},"revenue_per_purchase":(15000,80000)},
    "private_client_event": {"label":"Private Client Event","base_intent_alpha":5.0,"base_intent_beta":2.5,"engagement_multiplier":1.1,"vip_sensitivity":1.5,"city_bias":{"Milano":1.20,"Dubai":1.35,"Paris":1.25,"Tokyo":1.15,"New York":1.30,"London":1.22,"Riyadh":1.40,"Singapore":1.18,"Los Angeles":1.15,"Shanghai":1.12},"revenue_per_purchase":(20000,120000)},
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

def make_chart(df, city_summary, campaign_label):
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    fig.patch.set_facecolor("#FAFAF8")
    black,lime,lgray,mgray,bg = "#111111","#C8D400","#E8E8E4","#999999","#FAFAF8"
    for ax in axes:
        ax.set_facecolor(bg); ax.tick_params(colors=mgray,labelsize=7)
        for sp in ax.spines.values(): sp.set_color(lgray)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax1 = axes[0]
    clrs = [black if i==0 else "#CCCCCC" for i in range(len(city_summary))]
    bars = ax1.bar(city_summary["City"], city_summary["Buy Rate (%)"], color=clrs, width=0.55, zorder=2)
    ax1.yaxis.grid(True,color=lgray,linewidth=0.5,zorder=1); ax1.set_axisbelow(True)
    ax1.set_title("BUY RATE BY CITY",color=black,fontsize=7,fontweight="bold",pad=14,loc="left")
    ax1.set_ylabel("%",color=mgray,fontsize=7)
    plt.setp(ax1.get_xticklabels(),rotation=35,ha="right",fontsize=6)
    for bar in bars:
        ax1.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.3,f"{bar.get_height():.1f}%",ha="center",va="bottom",color=black,fontsize=6,fontweight="bold")
    ax2 = axes[1]
    bins = np.linspace(0,100,28)
    ax2.hist(df.loc[~df["Purchased"],"Purchase Intent"],bins=bins,color=lgray,alpha=0.9,label="No Purchase",zorder=2)
    ax2.hist(df.loc[df["Purchased"],"Purchase Intent"],bins=bins,color=black,alpha=0.85,label="Purchased",zorder=3)
    ax2.yaxis.grid(True,color=lgray,linewidth=0.5,zorder=1); ax2.set_axisbelow(True)
    ax2.set_title("PURCHASE INTENT DISTRIBUTION",color=black,fontsize=7,fontweight="bold",pad=14,loc="left")
    ax2.set_xlabel("Intent (%)",color=mgray,fontsize=7); ax2.set_ylabel("VICs",color=mgray,fontsize=7)
    ax2.legend(fontsize=6,facecolor=bg,edgecolor=lgray,labelcolor=black)
    ax3 = axes[2]
    top = city_summary.head(8)
    clrs3 = [lime if i==0 else "#CCCCCC" for i in range(len(top))]
    ax3.barh(top["City"],top["Revenue (EUR)"]/1000,color=clrs3,height=0.5,zorder=2)
    ax3.xaxis.grid(True,color=lgray,linewidth=0.5,zorder=1); ax3.set_axisbelow(True)
    ax3.set_title("REVENUE BY CITY (kEUR)",color=black,fontsize=7,fontweight="bold",pad=14,loc="left")
    ax3.set_xlabel("Revenue (kEUR)",color=mgray,fontsize=7)
    ax3.invert_yaxis(); ax3.tick_params(axis="y",labelsize=6)
    plt.tight_layout(pad=2.0)
    return fig

with st.sidebar:
    try:
        logo_url = "https://raw.githubusercontent.com/Learning1-eng/fashion-campaign-predictor/main/dress_for_good_logo.png"
        logo = Image.open(requests.get(logo_url, stream=True).raw)
        st.image(logo, width=90)
    except:
        st.markdown("<div style='font-size:1.2rem;font-weight:900;color:#C8D400;text-align:center;'>DFG</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#333;margin:0.5rem 0 1.2rem 0;'>", unsafe_allow_html=True)
    campaign_type = st.selectbox("Campaign Type",options=list(CAMPAIGN_PARAMS.keys()),format_func=lambda x:CAMPAIGN_PARAMS[x]["label"])
    n_vics = st.slider("VIC Pool Size",min_value=500,max_value=50000,value=5000,step=500)
    cities = st.multiselect("Target Cities",options=ALL_CITIES,default=ALL_CITIES[:5])
    if not cities: cities = ALL_CITIES[:3]
    budget = st.number_input("Campaign Budget (EUR)",min_value=50000,max_value=20000000,value=500000,step=50000)
    st.markdown("<hr style='border-color:#333;margin:1rem 0;'>", unsafe_allow_html=True)
    run = st.button("RUN SIMULATION")
    st.markdown("<div style='margin-top:2rem;text-align:center;'><div style='font-size:0.72rem;font-weight:700;color:#fff;text-transform:uppercase;'>Dress for Good</div><div style='font-size:0.55rem;color:#666;margin-top:0.3rem;'>Milan, Italy - 2026</div></div>", unsafe_allow_html=True)

st.markdown("<div style='border-bottom:2px solid #111;padding-bottom:1.2rem;margin-bottom:2rem;'><div style='font-size:0.58rem;font-weight:700;letter-spacing:0.45em;text-transform:uppercase;color:#999;margin-bottom:0.5rem;'>Dress for Good - AI Luxury Studio</div><div style='font-size:2.6rem;font-weight:900;color:#111;line-height:1;text-transform:uppercase;'>Fashion Campaign Predictor</div><div style='font-size:0.62rem;font-weight:400;letter-spacing:0.22em;color:#999;margin-top:0.5rem;text-transform:uppercase;'>Multi-Agent Simulation - Luxury Marketing Intelligence</div></div>", unsafe_allow_html=True)

if not run:
    st.markdown("<div style='text-align:center;padding:6rem 2rem;'><div style='font-size:1rem;font-weight:300;color:#CCC;letter-spacing:0.08em;text-transform:uppercase;'>Configure parameters and run the simulation</div></div>", unsafe_allow_html=True)
else:
    with st.spinner("Running simulation..."):
        df = run_simulation(campaign_type, n_vics, cities, budget)
        summary = compute_summary(df, budget)
    campaign_label = CAMPAIGN_PARAMS[campaign_type]["label"]
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [(f'{summary["buy_rate"]}%',"Buy Rate"),(f'{summary["buyers"]:,}',"Buyers"),(f'EUR {summary["total_revenue"]/1000000:.1f}M',"Revenue"),(f'{summary["roi"]:+.0f}%',"ROI"),(f'{summary["total_reach"]//1000:,}K',"Reach")]
    for col,(val,label) in zip([c1,c2,c3,c4,c5],kpis):
        with col:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Simulation Analysis</div>",unsafe_allow_html=True)
    fig = make_chart(df,summary["city_summary"],campaign_label)
    st.pyplot(fig,use_container_width=True); plt.close(fig)
    st.markdown("<br>",unsafe_allow_html=True)
    cl,cr = st.columns(2)
    fmt = {"Buy Rate (%)":"{:.1f}","Revenue (EUR)":"EUR{:,.0f}","Avg Intent (%)":"{:.1f}"}
    with cl:
        st.markdown("<div class='section-label'>Performance by City</div>",unsafe_allow_html=True)
        st.dataframe(summary["city_summary"].style.format(fmt),use_container_width=True,hide_index=True)
    with cr:
        st.markdown("<div class='section-label'>VIC Persona Intelligence</div>",unsafe_allow_html=True)
        st.dataframe(summary["persona_summary"].style.format(fmt),use_container_width=True,hide_index=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<div class='section-label'>VIC Agent Data</div>",unsafe_allow_html=True)
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
    st.download_button("Export VIC Dataset (CSV)",data=csv.getvalue(),file_name=f"campaign_{campaign_type}_{n_vics}vics.csv",mime="text/csv")
    st.markdown("<hr style='border-color:#E8E8E4;margin:1.5rem 0;'>",unsafe_allow_html=True)
    roi_read = "strong positive" if summary["roi"]>50 else "moderate" if summary["roi"]>0 else "negative"
    top_city = summary["city_summary"].iloc[0]["City"]
    top_persona = summary["persona_summary"].iloc[0]["Persona"]
    readout = (f"Simulation of {summary['total']:,} synthetic VIC agents across {', '.join(cities)} "
               f"projects a {roi_read} ROI of {summary['roi']:+.0f}% on a EUR{budget:,.0f} investment. "
               f"Conversion: {summary['buy_rate']}%. Top market: {top_city}. "
               f"Dominant persona: {top_persona}. Projected revenue: EUR{summary['total_revenue']:,.0f}.")
    st.markdown(f"<div style='font-size:0.92rem;font-weight:300;color:#111;line-height:1.9;padding:1rem 0 1rem 1.2rem;border-left:3px solid #C8D400;'>{readout}</div>",unsafe_allow_html=True)
