# Fashion Campaign Predictor v16.0 - Dress for Good AI Studio
# Gen Z TACLA — 136 profiles (2 macro x 4 sub-types x 17 regions)

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
    import base64 as _b64
    login_css = _b64.b64decode("QGltcG9ydCB1cmwoJ2h0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20vY3NzMj9mYW1pbHk9TW9udHNlcnJhdDp3Z2h0QDMwMDs0MDA7NTAwOzYwMDs3MDA7OTAwJmRpc3BsYXk9c3dhcCcpO2h0bWwsYm9keSxbY2xhc3MqPSdjc3MnXXtiYWNrZ3JvdW5kOiNGQUZBRjg7Y29sb3I6IzExMTtmb250LWZhbWlseTpNb250c2VycmF0LHNhbnMtc2VyaWY7fS5zdEFwcHtiYWNrZ3JvdW5kOiNGQUZBRjg7fS5zdEJ1dHRvbj5idXR0b257YmFja2dyb3VuZDojMTExIWltcG9ydGFudDtjb2xvcjojZmZmIWltcG9ydGFudDtib3JkZXI6bm9uZSFpbXBvcnRhbnQ7Ym9yZGVyLXJhZGl1czowIWltcG9ydGFudDtmb250LWZhbWlseTpNb250c2VycmF0LHNhbnMtc2VyaWYhaW1wb3J0YW50O2ZvbnQtc2l6ZTouNnJlbSFpbXBvcnRhbnQ7Zm9udC13ZWlnaHQ6NzAwIWltcG9ydGFudDtsZXR0ZXItc3BhY2luZzouMmVtIWltcG9ydGFudDt0ZXh0LXRyYW5zZm9ybTp1cHBlcmNhc2UhaW1wb3J0YW50O3BhZGRpbmc6Ljg1cmVtIDJyZW0haW1wb3J0YW50O30uc3RCdXR0b24+YnV0dG9uOmhvdmVye2JhY2tncm91bmQ6I0M4RDQwMCFpbXBvcnRhbnQ7Y29sb3I6IzExMSFpbXBvcnRhbnQ7fSNNYWluTWVudSxmb290ZXIsaGVhZGVye3Zpc2liaWxpdHk6aGlkZGVuO30=").decode()
    st.markdown(f'<style>{login_css}</style>', unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        logo_html = '<img src="https://raw.githubusercontent.com/Learning1-eng/fashion-campaign-predictor/main/dress%20for%20good%20logo%20copy.png" style="width:72px;height:72px;border-radius:50%;object-fit:cover;display:block;margin:0 0 1.5rem 0;">'
        planet = ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="position:absolute;right:-20px;top:0;width:90%;height:100%;opacity:0.06;">'
            '<circle cx="75" cy="50" r="38" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<circle cx="75" cy="50" r="28" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<circle cx="75" cy="50" r="18" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<ellipse cx="75" cy="50" rx="38" ry="11" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<ellipse cx="75" cy="50" rx="38" ry="22" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<ellipse cx="75" cy="50" rx="38" ry="32" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<ellipse cx="75" cy="50" rx="12" ry="38" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<ellipse cx="75" cy="50" rx="24" ry="38" fill="none" stroke="#111" stroke-width="0.3"/>'
            '<ellipse cx="75" cy="50" rx="52" ry="9" fill="none" stroke="#111" stroke-width="0.25"/>'
            '</svg>')
        wrapper = ('<div style="position:relative;padding:3rem 0 2rem;min-height:380px;">'
            + planet +
            '<div style="position:relative;z-index:1;">'
            + logo_html +
            '<div style="font-size:.55rem;font-weight:600;letter-spacing:.3em;text-transform:uppercase;color:#999;margin-bottom:.4rem;">Dress for Good</div>'
            '<div style="font-size:1.8rem;font-weight:900;color:#111;line-height:1.1;margin-bottom:.3rem;">Welcome back</div>'
            '<div style="font-size:.8rem;font-weight:300;color:#555;margin-bottom:2rem;">AI Luxury Studio — Private access</div>'
            '</div></div>')
        st.markdown(wrapper, unsafe_allow_html=True)
        pwd = st.text_input('Access code', type='password', placeholder='Enter access code', label_visibility='collapsed')
        if st.button('Enter', use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error('Invalid access code.')
        st.markdown('<div style="margin-top:1.5rem;font-size:.55rem;color:#ccc;letter-spacing:.05em;">Powered by synthetic VIC agent modeling</div>', unsafe_allow_html=True)
    st.stop()


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
    return {"total":total,"buyers":buyers,"buy_rate":round(buy_rate,1),"total_revenue":round(total_revenue,0),"roi":round(roi,1),"total_reach":int(df["Influence Score"].sum()) if "Influence Score" in df.columns else 0,"city_summary":city_s,"persona_summary":pers_s}

def make_charts(df, city_summary):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    font = dict(family="Montserrat, sans-serif", color="#111111")
    layout_base = dict(paper_bgcolor="#fff", plot_bgcolor="#fff", font=font, margin=dict(l=10,r=10,t=35,b=10))
    fig = make_subplots(rows=1, cols=3, column_widths=[0.28,0.44,0.28],
        subplot_titles=["Buy rate by city","Purchase intent distribution","Revenue by city (kEUR)"])
    clrs = ["#111111" if i==0 else "#CCCCCC" for i in range(len(city_summary))]
    fig.add_trace(go.Bar(x=city_summary["City"], y=city_summary["Buy Rate (%)"], marker_color=clrs, showlegend=False), row=1, col=1)
    fig.add_trace(go.Histogram(x=df.loc[~df["Purchased"],"Purchase Intent"], name="No Purchase", marker_color="#E8E8E4", opacity=0.9, nbinsx=25), row=1, col=2)
    fig.add_trace(go.Histogram(x=df.loc[df["Purchased"],"Purchase Intent"], name="Purchased", marker_color="#111111", opacity=0.85, nbinsx=25), row=1, col=2)
    top = city_summary.sort_values("Revenue (EUR)")
    clrs3 = ["#C8D400" if i==len(top)-1 else "#CCCCCC" for i in range(len(top))]
    fig.add_trace(go.Bar(y=top["City"], x=top["Revenue (EUR)"]/1000, orientation="h", marker_color=clrs3, showlegend=False, hovertemplate="%{y}: EUR %{x:.0f}k<extra></extra>", name="Revenue"), row=1, col=3)
    fig.update_layout(**layout_base, height=250, legend=dict(bgcolor="#fff",bordercolor="#E8E8E4",font=dict(family="Montserrat",size=9)))
    fig.update_xaxes(showgrid=True,gridcolor="#E8E8E4",linecolor="#E8E8E4",tickfont=dict(size=8,color="#111"))
    fig.update_yaxes(showgrid=True,gridcolor="#E8E8E4",linecolor="#E8E8E4",tickfont=dict(size=8,color="#111"))
    for ann in fig.layout.annotations: ann.font.size=9; ann.font.family="Montserrat, sans-serif"; ann.font.color="#111111"
    return fig

LOGO_URL = "https://raw.githubusercontent.com/Learning1-eng/fashion-campaign-predictor/main/dress%20for%20good%20logo%20copy.png"
st.markdown('<style>:root{--primary-color:#111111!important;}input[type=range]{accent-color:#111111!important;-webkit-appearance:none!important;appearance:none!important;background:transparent!important;}input[type=range]:focus{outline:none!important;}input[type=range]::-webkit-slider-runnable-track{background:#111111!important;height:3px!important;border-radius:2px!important;border:none!important;-webkit-appearance:none!important;}input[type=range]::-moz-range-track{background:#111111!important;height:3px!important;border-radius:2px!important;border:none!important;}input[type=range]::-ms-track{background:#111111!important;height:3px!important;border-radius:2px!important;border:none!important;}input[type=range]::-webkit-slider-thumb{-webkit-appearance:none!important;appearance:none!important;background:#C8D400!important;width:18px!important;height:18px!important;border-radius:50%!important;margin-top:-8px!important;cursor:pointer!important;border:none!important;}input[type=range]::-moz-range-thumb{background:#C8D400!important;width:16px!important;height:16px!important;border-radius:50%!important;border:none!important;cursor:pointer!important;}[data-baseweb=tab-highlight]{background-color:#111111!important;}[data-baseweb=tab-border]{background-color:#E8E8E4!important;}</style>', unsafe_allow_html=True)
import base64 as _b64css
css = _b64css.b64decode("QGltcG9ydCB1cmwoJ2h0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20vY3NzMj9mYW1pbHk9TW9udHNlcnJhdDp3Z2h0QDMwMDs0MDA7NTAwOzYwMDs3MDA7OTAwJmRpc3BsYXk9c3dhcCcpOwpodG1sLGJvZHksW2NsYXNzKj0nY3NzJ117Zm9udC1mYW1pbHk6TW9udHNlcnJhdCxzYW5zLXNlcmlmO2JhY2tncm91bmQ6I0ZBRkFGODtjb2xvcjojMTExO30KLnN0QXBwe2JhY2tncm91bmQ6I0ZBRkFGODt9Cjpyb290ey0tcHJpbWFyeS1jb2xvcjojMTExMTExIWltcG9ydGFudDt9CmJ1dHRvbltkYXRhLXRlc3RpZD0ic3ROdW1iZXJJbnB1dC1TdGVwVXAiXSxidXR0b25bZGF0YS10ZXN0aWQ9InN0TnVtYmVySW5wdXQtU3RlcERvd24iXXtiYWNrZ3JvdW5kOiMxMTEhaW1wb3J0YW50O2NvbG9yOiNmZmYhaW1wb3J0YW50O2JvcmRlcjpub25lIWltcG9ydGFudDt9CmJ1dHRvbltkYXRhLXRlc3RpZD0ic3ROdW1iZXJJbnB1dC1TdGVwVXAiXTpob3ZlcixidXR0b25bZGF0YS10ZXN0aWQ9InN0TnVtYmVySW5wdXQtU3RlcERvd24iXTpob3ZlcntiYWNrZ3JvdW5kOiNDOEQ0MDAhaW1wb3J0YW50O2NvbG9yOiMxMTEhaW1wb3J0YW50O30KLnN0VGFicyBbZGF0YS1iYXNld2ViPSd0YWItbGlzdCdde2JhY2tncm91bmQ6I2ZmZjtib3JkZXItYm90dG9tOjFweCBzb2xpZCAjRThFOEU0O2dhcDowO30KLnN0VGFicyBbZGF0YS1iYXNld2ViPSd0YWInXXtmb250LWZhbWlseTpNb250c2VycmF0LHNhbnMtc2VyaWY7Zm9udC1zaXplOi42cmVtO2ZvbnQtd2VpZ2h0OjYwMDtsZXR0ZXItc3BhY2luZzouMTJlbTt0ZXh0LXRyYW5zZm9ybTp1cHBlcmNhc2U7Y29sb3I6Izg4ODtwYWRkaW5nOi43cmVtIDEuMnJlbTtib3JkZXItcmFkaXVzOjA7fQouc3RUYWJzIFthcmlhLXNlbGVjdGVkPSd0cnVlJ117Y29sb3I6IzExMSFpbXBvcnRhbnQ7fQoubWV0cmljLWNhcmR7YmFja2dyb3VuZDojZmZmO2JvcmRlcjoxcHggc29saWQgI0U4RThFNDtwYWRkaW5nOjFyZW0gMS4ycmVtO21hcmdpbi1ib3R0b206LjVyZW07fQoubWV0cmljLXZhbHVle2ZvbnQtc2l6ZToxLjhyZW07Zm9udC13ZWlnaHQ6NzAwO2NvbG9yOiMxMTE7bGluZS1oZWlnaHQ6MTt9Ci5tZXRyaWMtbGFiZWx7Zm9udC1zaXplOi41NXJlbTtmb250LXdlaWdodDo2MDA7bGV0dGVyLXNwYWNpbmc6LjEyZW07dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2NvbG9yOiM4ODg7bWFyZ2luLXRvcDouM3JlbTt9Ci5zZWN0aW9uLWxhYmVse2ZvbnQtc2l6ZTouNTVyZW07Zm9udC13ZWlnaHQ6NzAwO2xldHRlci1zcGFjaW5nOi4xNWVtO3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZTtjb2xvcjojMTExO21hcmdpbjoxLjVyZW0gMCAuNnJlbTtib3JkZXItYm90dG9tOjFweCBzb2xpZCAjRThFOEU0O3BhZGRpbmctYm90dG9tOi40cmVtO30KZGl2W2RhdGEtdGVzdGlkPSdzdFNpZGViYXInXXtiYWNrZ3JvdW5kOiMxMTEhaW1wb3J0YW50O2NvbG9yOiNmZmY7fQpkaXZbZGF0YS10ZXN0aWQ9J3N0U2lkZWJhciddICp7Y29sb3I6I2ZmZiFpbXBvcnRhbnQ7fQpkaXZbZGF0YS10ZXN0aWQ9J3N0U2lkZWJhciddIC5zdFNlbGVjdGJveCBsYWJlbCwKZGl2W2RhdGEtdGVzdGlkPSdzdFNpZGViYXInXSAuc3RNdWx0aVNlbGVjdCBsYWJlbCwKZGl2W2RhdGEtdGVzdGlkPSdzdFNpZGViYXInXSAuc3ROdW1iZXJJbnB1dCBsYWJlbHtjb2xvcjojOTk5IWltcG9ydGFudDtmb250LXNpemU6LjU1cmVtIWltcG9ydGFudDtsZXR0ZXItc3BhY2luZzouMWVtIWltcG9ydGFudDt0ZXh0LXRyYW5zZm9ybTp1cHBlcmNhc2UhaW1wb3J0YW50O30KZGl2W2RhdGEtdGVzdGlkPSdzdFNpZGViYXInXSAuc3RCdXR0b24+YnV0dG9ue2JhY2tncm91bmQ6I0M4RDQwMCFpbXBvcnRhbnQ7Y29sb3I6IzExMSFpbXBvcnRhbnQ7Zm9udC13ZWlnaHQ6NzAwIWltcG9ydGFudDt9CmRpdltkYXRhLXRlc3RpZD0nc3RTaWRlYmFyJ10gW2RhdGEtdGVzdGlkPSJzdE51bWJlcklucHV0Il0gYnV0dG9ue2JhY2tncm91bmQ6IzMzMyFpbXBvcnRhbnQ7Y29sb3I6I2ZmZiFpbXBvcnRhbnQ7Ym9yZGVyOm5vbmUhaW1wb3J0YW50O30KZGl2W2RhdGEtdGVzdGlkPSdzdFNpZGViYXInXSBbZGF0YS10ZXN0aWQ9InN0TnVtYmVySW5wdXQiXSBidXR0b246aG92ZXJ7YmFja2dyb3VuZDojQzhENDAwIWltcG9ydGFudDtjb2xvcjojMTExIWltcG9ydGFudDt9CmRpdltkYXRhLXRlc3RpZD0nc3RTaWRlYmFyJ10gW2RhdGEtdGVzdGlkPSJzdE51bWJlcklucHV0Il0gYnV0dG9uIHN2Z3tmaWxsOiNmZmYhaW1wb3J0YW50O30KZGl2W2RhdGEtdGVzdGlkPSdzdFNpZGViYXInXSBbZGF0YS10ZXN0aWQ9InN0TnVtYmVySW5wdXQiXSBidXR0b246aG92ZXIgc3Zne2ZpbGw6IzExMSFpbXBvcnRhbnQ7fQouc3RCdXR0b24+YnV0dG9ue2JhY2tncm91bmQ6IzExMSFpbXBvcnRhbnQ7Y29sb3I6I2ZmZiFpbXBvcnRhbnQ7Ym9yZGVyOjFweCBzb2xpZCAjMTExIWltcG9ydGFudDtib3JkZXItcmFkaXVzOjAhaW1wb3J0YW50O2ZvbnQtZmFtaWx5Ok1vbnRzZXJyYXQsc2Fucy1zZXJpZiFpbXBvcnRhbnQ7Zm9udC1zaXplOi42cmVtIWltcG9ydGFudDtmb250LXdlaWdodDo3MDAhaW1wb3J0YW50O2xldHRlci1zcGFjaW5nOi4yZW0haW1wb3J0YW50O3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZSFpbXBvcnRhbnQ7cGFkZGluZzouODVyZW0gMnJlbSFpbXBvcnRhbnQ7d2lkdGg6MTAwJSFpbXBvcnRhbnQ7fQouc3RCdXR0b24+YnV0dG9uOmhvdmVye2JhY2tncm91bmQ6I0M4RDQwMCFpbXBvcnRhbnQ7Ym9yZGVyLWNvbG9yOiNDOEQ0MDAhaW1wb3J0YW50O2NvbG9yOiMxMTEhaW1wb3J0YW50O30KYnV0dG9uW2RhdGEtdGVzdGlkPSJiYXNlQnV0dG9uLXNlY29uZGFyeSJde2JhY2tncm91bmQ6IzExMSFpbXBvcnRhbnQ7Y29sb3I6I2ZmZiFpbXBvcnRhbnQ7Ym9yZGVyOjFweCBzb2xpZCAjMTExIWltcG9ydGFudDtib3JkZXItcmFkaXVzOjAhaW1wb3J0YW50O30KYnV0dG9uW2RhdGEtdGVzdGlkPSJiYXNlQnV0dG9uLXNlY29uZGFyeSJdOmhvdmVye2JhY2tncm91bmQ6I0M4RDQwMCFpbXBvcnRhbnQ7Y29sb3I6IzExMSFpbXBvcnRhbnQ7fQpbZGF0YS1iYXNld2ViPSd0YWcnXXtiYWNrZ3JvdW5kOiNmZmYhaW1wb3J0YW50O2JvcmRlcjoxcHggc29saWQgIzExMSFpbXBvcnRhbnQ7Ym9yZGVyLXJhZGl1czoyMHB4IWltcG9ydGFudDtwYWRkaW5nOjNweCA4cHggM3B4IDEycHghaW1wb3J0YW50O21hcmdpbjozcHghaW1wb3J0YW50O2Rpc3BsYXk6aW5saW5lLWZsZXghaW1wb3J0YW50O2FsaWduLWl0ZW1zOmNlbnRlciFpbXBvcnRhbnQ7Z2FwOjhweCFpbXBvcnRhbnQ7fQpbZGF0YS1iYXNld2ViPSd0YWcnXSBzcGFue2NvbG9yOiMxMTEhaW1wb3J0YW50O2ZvbnQtc2l6ZTouNzJyZW0haW1wb3J0YW50O2ZvbnQtd2VpZ2h0OjUwMCFpbXBvcnRhbnQ7d2hpdGUtc3BhY2U6bm93cmFwIWltcG9ydGFudDt9CltkYXRhLWJhc2V3ZWI9J3RhZyddIGJ1dHRvbntiYWNrZ3JvdW5kOnRyYW5zcGFyZW50IWltcG9ydGFudDtib3JkZXI6bm9uZSFpbXBvcnRhbnQ7cGFkZGluZzowIWltcG9ydGFudDt9CltkYXRhLWJhc2V3ZWI9J3RhZyddIGJ1dHRvbiBzdmd7ZmlsbDojMTExIWltcG9ydGFudDt3aWR0aDoxMXB4IWltcG9ydGFudDtoZWlnaHQ6MTFweCFpbXBvcnRhbnQ7fQpbZGF0YS1iYXNld2ViPSdtdWx0aS1zZWxlY3QnXXtiYWNrZ3JvdW5kOiNmZmYhaW1wb3J0YW50O2JvcmRlcjoxcHggc29saWQgIzU1NSFpbXBvcnRhbnQ7Ym9yZGVyLXJhZGl1czo0cHghaW1wb3J0YW50O31bZGF0YS1iYXNld2ViPSdpbnB1dCdde2JvcmRlci1jb2xvcjojMTExIWltcG9ydGFudDtib3JkZXItd2lkdGg6MXB4IWltcG9ydGFudDt9W2RhdGEtYmFzZXdlYj0nYmFzZS1pbnB1dCdde2JvcmRlci1jb2xvcjojMTExIWltcG9ydGFudDtib3JkZXItd2lkdGg6MXB4IWltcG9ydGFudDt9W2RhdGEtYmFzZXdlYj0nc2VsZWN0J10gPiBkaXZ7Ym9yZGVyLWNvbG9yOiMxMTEhaW1wb3J0YW50O2JvcmRlci13aWR0aDoxcHghaW1wb3J0YW50O31kaXZbZGF0YS10ZXN0aWQ9J3N0TnVtYmVySW5wdXQnXSA+IGRpdntib3JkZXI6MXB4IHNvbGlkICMxMTEhaW1wb3J0YW50O31pbnB1dHtib3JkZXI6MXB4IHNvbGlkICMxMTEhaW1wb3J0YW50O31pbnB1dDpmb2N1c3tib3gtc2hhZG93Om5vbmUhaW1wb3J0YW50O291dGxpbmU6bm9uZSFpbXBvcnRhbnQ7Ym9yZGVyLWNvbG9yOiMxMTEhaW1wb3J0YW50O310ZXh0YXJlYXtib3JkZXI6MXB4IHNvbGlkICMxMTEhaW1wb3J0YW50O30KYnV0dG9uW2RhdGEtdGVzdGlkPSJzdE51bWJlcklucHV0LVN0ZXBEb3duIl0sYnV0dG9uW2RhdGEtdGVzdGlkPSJzdE51bWJlcklucHV0LVN0ZXBVcCJde2JhY2tncm91bmQ6IzExMSFpbXBvcnRhbnQ7Y29sb3I6I2ZmZiFpbXBvcnRhbnQ7Ym9yZGVyOm5vbmUhaW1wb3J0YW50O30KYnV0dG9uW2RhdGEtdGVzdGlkPSJzdE51bWJlcklucHV0LVN0ZXBEb3duIl06aG92ZXIsYnV0dG9uW2RhdGEtdGVzdGlkPSJzdE51bWJlcklucHV0LVN0ZXBVcCJdOmhvdmVye2JhY2tncm91bmQ6I0M4RDQwMCFpbXBvcnRhbnQ7Y29sb3I6IzExMSFpbXBvcnRhbnQ7fQpbZGF0YS10ZXN0aWQ9InN0U2xpZGVyIl0gcHtjb2xvcjojMTExIWltcG9ydGFudDtmb250LXdlaWdodDo2MDAhaW1wb3J0YW50O30KW2RhdGEtdGVzdGlkPSJzdFNsaWRlciJdIFtkYXRhLXRlc3RpZD0ic3RNYXJrZG93bkNvbnRhaW5lciJdIHB7Y29sb3I6IzExMSFpbXBvcnRhbnQ7fQpkaXZbZGF0YS10ZXN0aWQ9InN0U2xpZGVyIl0gPiBkaXYgPiBkaXYgPiBkaXZbcm9sZT0icHJlc2VudGF0aW9uIl17Y29sb3I6IzExMSFpbXBvcnRhbnQ7fQpbZGF0YS10ZXN0aWQ9InN0U2xpZGVyIl0gc3Bhbntjb2xvcjojMTExIWltcG9ydGFudDt9Cjpyb290ey0tcHJpbWFyeS1jb2xvcjojMTExMTExIWltcG9ydGFudDstLXNlY29uZGFyeS1iYWNrZ3JvdW5kLWNvbG9yOiNGNUY1RjMhaW1wb3J0YW50O30KYnV0dG9ue2NvbG9yOiMxMTEhaW1wb3J0YW50O30KLnN0QWxlcnR7ZGlzcGxheTpub25lO30KW2RhdGEtYmFzZXdlYj0ibm90aWZpY2F0aW9uIl17YmFja2dyb3VuZDojMTExIWltcG9ydGFudDt9Ci5zdEV4Y2VwdGlvbntib3JkZXItbGVmdDozcHggc29saWQgIzExMSFpbXBvcnRhbnQ7fQpkaXZbZGF0YS10ZXN0aWQ9InN0Tm90aWZpY2F0aW9uIl17YmFja2dyb3VuZDojMTExIWltcG9ydGFudDt9Cipbc3R5bGUqPSJjb2xvcjogcmdiKDI1NSJde2NvbG9yOiMxMTEhaW1wb3J0YW50O30KKltzdHlsZSo9ImJhY2tncm91bmQtY29sb3I6IHJnYigyNTUsIDc1Il17YmFja2dyb3VuZC1jb2xvcjojMTExIWltcG9ydGFudDt9Cipbc3R5bGUqPSJiYWNrZ3JvdW5kOiByZ2IoMjU1LCA3NSJde2JhY2tncm91bmQ6IzExMSFpbXBvcnRhbnQ7fQo=").decode()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


CAMPAIGN_PARAMS = {
    "seasonal_collection":   {"label":"Seasonal Collection","base_intent_alpha":4.5,"base_intent_beta":2.8,"engagement_multiplier":1.3,"city_bias":{"Milano":1.4,"Paris":1.5,"London":1.3,"New York":1.2,"Los Angeles":1.1,"Dubai":1.1,"Riyadh":1.0,"Tokyo":1.2,"Shanghai":1.2,"Singapore":1.0},"revenue_per_purchase":(1500,8000)},
    "heritage_savoir_faire": {"label":"Heritage & Savoir-Faire","base_intent_alpha":3.8,"base_intent_beta":2.8,"engagement_multiplier":1.1,"city_bias":{"Milano":1.4,"Paris":1.5,"London":1.3,"New York":1.1,"Los Angeles":1.0,"Dubai":1.1,"Riyadh":1.0,"Tokyo":1.2,"Shanghai":1.1,"Singapore":1.0},"revenue_per_purchase":(3000,20000)},
    "celebrity_ambassador":  {"label":"Celebrity & Ambassador","base_intent_alpha":3.5,"base_intent_beta":3.0,"engagement_multiplier":1.5,"city_bias":{"Milano":1.1,"Paris":1.2,"London":1.1,"New York":1.4,"Los Angeles":1.5,"Dubai":1.2,"Riyadh":1.1,"Tokyo":1.3,"Shanghai":1.3,"Singapore":1.1},"revenue_per_purchase":(800,5000)},
    "immersive_experience":  {"label":"Immersive Experience","base_intent_alpha":4.0,"base_intent_beta":2.5,"engagement_multiplier":1.6,"city_bias":{"Milano":1.3,"Paris":1.4,"London":1.2,"New York":1.3,"Los Angeles":1.2,"Dubai":1.3,"Riyadh":1.0,"Tokyo":1.3,"Shanghai":1.2,"Singapore":1.2},"revenue_per_purchase":(2000,10000)},
    "digital_social":        {"label":"Digital & Social","base_intent_alpha":2.8,"base_intent_beta":4.0,"engagement_multiplier":1.8,"city_bias":{"Milano":1.1,"Paris":1.1,"London":1.2,"New York":1.4,"Los Angeles":1.5,"Dubai":1.1,"Riyadh":0.9,"Tokyo":1.4,"Shanghai":1.4,"Singapore":1.3},"revenue_per_purchase":(500,3000)},
    "collaboration_capsule": {"label":"Collaboration & Capsule","base_intent_alpha":4.2,"base_intent_beta":2.6,"engagement_multiplier":1.4,"city_bias":{"Milano":1.2,"Paris":1.3,"London":1.3,"New York":1.4,"Los Angeles":1.4,"Dubai":1.1,"Riyadh":0.9,"Tokyo":1.3,"Shanghai":1.2,"Singapore":1.1},"revenue_per_purchase":(1200,7000)},
    "sustainability_re_edit": {"label":"Sustainability & Re-Edition","base_intent_alpha":3.0,"base_intent_beta":3.5,"engagement_multiplier":1.2,"city_bias":{"Milano":1.2,"Paris":1.3,"London":1.4,"New York":1.3,"Los Angeles":1.3,"Dubai":0.9,"Riyadh":0.8,"Tokyo":1.1,"Shanghai":1.0,"Singapore":1.1},"revenue_per_purchase":(1000,6000)},
    "product_launch":        {"label":"Product Launch","base_intent_alpha":4.5,"base_intent_beta":2.5,"engagement_multiplier":1.3,"city_bias":{"Milano":1.3,"Paris":1.4,"London":1.2,"New York":1.3,"Los Angeles":1.2,"Dubai":1.2,"Riyadh":1.0,"Tokyo":1.2,"Shanghai":1.2,"Singapore":1.0},"revenue_per_purchase":(1200,8000)},
    "private_client_event":  {"label":"Private Client Event","base_intent_alpha":5.0,"base_intent_beta":2.0,"engagement_multiplier":1.1,"city_bias":{"Milano":1.2,"Paris":1.4,"London":1.3,"New York":1.3,"Los Angeles":1.1,"Dubai":1.5,"Riyadh":1.4,"Tokyo":1.2,"Shanghai":1.2,"Singapore":1.2},"revenue_per_purchase":(5000,50000)},
    "cultural_activation":   {"label":"Cultural Activation","base_intent_alpha":3.5,"base_intent_beta":3.0,"engagement_multiplier":1.4,"city_bias":{"Milano":1.3,"Paris":1.4,"London":1.3,"New York":1.3,"Los Angeles":1.3,"Dubai":1.1,"Riyadh":0.9,"Tokyo":1.4,"Shanghai":1.3,"Singapore":1.2},"revenue_per_purchase":(1000,6000)},
}

ALL_CITIES = ["Milano","Paris","London","New York","Los Angeles","Dubai","Riyadh","Tokyo","Shanghai","Singapore"]

VIC_PERSONAS = [
    ("Ultra-HNWI Collector",    0.12, 1.6, 1.4),
    ("Brand Ambassador",        0.08, 1.0, 1.8),
    ("Aspirational Buyer",      0.20, 0.7, 1.1),
    ("Trend Setter Influencer", 0.15, 0.9, 1.5),
    ("Private Client",          0.10, 1.5, 1.2),
    ("Digital Native",          0.15, 0.6, 1.3),
    ("Heritage Loyalist",       0.10, 1.2, 0.9),
    ("Gulf HNWI",               0.05, 1.8, 1.1),
    ("Asia Pacific VIC",        0.05, 1.4, 1.2),
]


GEN_Z_PROFILES = {

    # FASHIONISTA > CENTURION
    "Gen Z — Fashionista › Centurion › EU-StTropez":   {"Parent":0.06,"Adult":0.24,"Child":0.70,"rd":"New","conflict":45,"life_script":"I need to be seen at the right place","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Centurion › EU-Mykonos":    {"Parent":0.04,"Adult":0.18,"Child":0.78,"rd":"New","conflict":52,"life_script":"Everyone needs to see where I am","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Centurion › EU-Portofino":  {"Parent":0.08,"Adult":0.27,"Child":0.65,"rd":"New","conflict":38,"life_script":"Beauty is my filter for everything","trigger_top":["Cultural Moment","New Product Launch"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Centurion › EU-Taormina":   {"Parent":0.07,"Adult":0.25,"Child":0.68,"rd":"New","conflict":40,"life_script":"I discovered this before it became obvious","trigger_top":["Cultural Moment","New Product Launch"],"trigger_null":["Heritage Campaign"]},
    "Gen Z — Fashionista › Centurion › EU-StMoritz":   {"Parent":0.12,"Adult":0.33,"Child":0.55,"rd":"Established","conflict":32,"life_script":"I experience luxury others can only imagine","trigger_top":["Exclusivity Signaling","Cultural Moment"],"trigger_null":["Price Hike","Mass Campaign"]},
    "Gen Z — Fashionista › Centurion › EU-Capri":      {"Parent":0.09,"Adult":0.28,"Child":0.63,"rd":"New","conflict":36,"life_script":"Dolce vita is a lifestyle, not a postcard","trigger_top":["Cultural Moment","Exclusivity Signaling"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Centurion › EU-Courchevel": {"Parent":0.14,"Adult":0.34,"Child":0.52,"rd":"Established","conflict":30,"life_script":"Status is lived, not displayed","trigger_top":["Exclusivity Signaling","New Product Launch"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Centurion › EU-ForteMarmi": {"Parent":0.16,"Adult":0.36,"Child":0.48,"rd":"Established","conflict":28,"life_script":"I know the codes before they become obvious","trigger_top":["Exclusivity Signaling","Heritage Campaign"],"trigger_null":["Mass Campaign","Price Hike"]},
    "Gen Z — Fashionista › Centurion › EU-PortoCervo": {"Parent":0.10,"Adult":0.28,"Child":0.62,"rd":"New","conflict":38,"life_script":"The right crowd at the right time","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Centurion › EU-Ibiza":      {"Parent":0.04,"Adult":0.20,"Child":0.76,"rd":"New","conflict":50,"life_script":"I set the trend before it trends","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Centurion › US":            {"Parent":0.05,"Adult":0.22,"Child":0.73,"rd":"New","conflict":52,"life_script":"I set the trend before it trends","trigger_top":["Cultural Moment","Scarcity Drop","Celebrity Co-sign"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Centurion › China-T1":      {"Parent":0.10,"Adult":0.30,"Child":0.60,"rd":"New","conflict":42,"life_script":"I know the codes before they become obvious","trigger_top":["Cultural Moment","Guochao","Scarcity Drop"],"trigger_null":["Logo Visibility","Price Hike"]},
    "Gen Z — Fashionista › Centurion › China-T2":      {"Parent":0.14,"Adult":0.26,"Child":0.60,"rd":"New","conflict":46,"life_script":"Luxury validates my trajectory","trigger_top":["KOL Co-sign","Cultural Moment","Gifting Ritual"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Centurion › China-T3":      {"Parent":0.20,"Adult":0.22,"Child":0.58,"rd":"New","conflict":50,"life_script":"This brand signals I have arrived","trigger_top":["KOL Co-sign","Logo Visibility","Gifting Ritual"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Fashionista › Centurion › ME":            {"Parent":0.14,"Adult":0.26,"Child":0.60,"rd":"New","conflict":44,"life_script":"I reflect the right cultural signals","trigger_top":["Exclusivity Signaling","Cultural Moment","Gifting Ritual"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Centurion › Japan":         {"Parent":0.22,"Adult":0.40,"Child":0.38,"rd":"Established","conflict":28,"life_script":"I understand what most people will never notice","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Logo Visibility","Hype Drop"]},
    "Gen Z — Fashionista › Centurion › South Korea":   {"Parent":0.08,"Adult":0.32,"Child":0.60,"rd":"New","conflict":40,"life_script":"My aesthetic is the cultural standard","trigger_top":["Idol Co-sign","Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign"]},

    # FASHIONISTA > CULTURAL ARCHITECT
    "Gen Z — Fashionista › Cultural Architect › EU-StTropez":   {"Parent":0.10,"Adult":0.35,"Child":0.55,"rd":"Established","conflict":35,"life_script":"I consume with intention and edge","trigger_top":["Cultural Moment","New Product Launch"],"trigger_null":["Mass Campaign","Price Hike"]},
    "Gen Z — Fashionista › Cultural Architect › EU-Mykonos":    {"Parent":0.07,"Adult":0.28,"Child":0.65,"rd":"New","conflict":40,"life_script":"My choices are my manifesto","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign"]},
    "Gen Z — Fashionista › Cultural Architect › EU-Portofino":  {"Parent":0.12,"Adult":0.38,"Child":0.50,"rd":"Established","conflict":30,"life_script":"Beauty with purpose","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Cultural Architect › EU-Taormina":   {"Parent":0.10,"Adult":0.33,"Child":0.57,"rd":"Established","conflict":33,"life_script":"I discovered this before it became obvious","trigger_top":["Cultural Moment","Craft Narrative"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Fashionista › Cultural Architect › EU-StMoritz":   {"Parent":0.15,"Adult":0.40,"Child":0.45,"rd":"Established","conflict":25,"life_script":"Depth over display","trigger_top":["Exclusivity Signaling","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Fashionista › Cultural Architect › EU-Capri":      {"Parent":0.13,"Adult":0.37,"Child":0.50,"rd":"Established","conflict":28,"life_script":"Italian soul, global vision","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Cultural Architect › EU-Courchevel": {"Parent":0.16,"Adult":0.40,"Child":0.44,"rd":"Established","conflict":24,"life_script":"Quality speaks without volume","trigger_top":["Exclusivity Signaling","Craft Narrative"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Cultural Architect › EU-ForteMarmi": {"Parent":0.18,"Adult":0.42,"Child":0.40,"rd":"Legacy","conflict":20,"life_script":"I know the codes before they become obvious","trigger_top":["Craft Narrative","Heritage Campaign"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Fashionista › Cultural Architect › EU-PortoCervo": {"Parent":0.12,"Adult":0.35,"Child":0.53,"rd":"Established","conflict":30,"life_script":"Selective, deliberate, unapologetic","trigger_top":["Cultural Moment","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Cultural Architect › EU-Ibiza":      {"Parent":0.06,"Adult":0.28,"Child":0.66,"rd":"New","conflict":42,"life_script":"My aesthetic is a political statement","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Cultural Architect › US":            {"Parent":0.08,"Adult":0.35,"Child":0.57,"rd":"New","conflict":38,"life_script":"I consume with intention","trigger_top":["Cultural Moment","Sustainability Narrative","Celebrity Co-sign"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Cultural Architect › China-T1":      {"Parent":0.12,"Adult":0.36,"Child":0.52,"rd":"Established","conflict":32,"life_script":"I set the cultural agenda","trigger_top":["Cultural Moment","Guochao","Craft Narrative"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Fashionista › Cultural Architect › China-T2":      {"Parent":0.15,"Adult":0.30,"Child":0.55,"rd":"New","conflict":36,"life_script":"Luxury validates my values","trigger_top":["KOL Co-sign","Cultural Moment","Gifting Ritual"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Cultural Architect › China-T3":      {"Parent":0.22,"Adult":0.24,"Child":0.54,"rd":"New","conflict":44,"life_script":"The right signal, authentically earned","trigger_top":["KOL Co-sign","Logo Visibility","Gifting Ritual"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Fashionista › Cultural Architect › ME":            {"Parent":0.16,"Adult":0.30,"Child":0.54,"rd":"New","conflict":40,"life_script":"I reflect the right cultural signals","trigger_top":["Cultural Moment","Exclusivity Signaling","Gifting Ritual"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Cultural Architect › Japan":         {"Parent":0.25,"Adult":0.42,"Child":0.33,"rd":"Established","conflict":22,"life_script":"I understand before I acquire","trigger_top":["Craft Narrative","Sustainability Narrative"],"trigger_null":["Logo Visibility","Hype Drop"]},
    "Gen Z — Fashionista › Cultural Architect › South Korea":   {"Parent":0.10,"Adult":0.36,"Child":0.54,"rd":"Established","conflict":34,"life_script":"My aesthetic is the standard others follow","trigger_top":["Cultural Moment","Idol Co-sign"],"trigger_null":["Heritage Campaign"]},

    # FASHIONISTA > ENTRY RITUALIST
    "Gen Z — Fashionista › Entry Ritualist › EU-StTropez":   {"Parent":0.05,"Adult":0.28,"Child":0.67,"rd":"New","conflict":55,"life_script":"This piece is my entry into the right world","trigger_top":["Scarcity Drop","New Product Launch"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-Mykonos":    {"Parent":0.04,"Adult":0.22,"Child":0.74,"rd":"New","conflict":60,"life_script":"Everyone needs to see this on me","trigger_top":["Scarcity Drop","Cultural Moment"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-Portofino":  {"Parent":0.07,"Adult":0.30,"Child":0.63,"rd":"New","conflict":48,"life_script":"One perfect piece says everything","trigger_top":["New Product Launch","Cultural Moment"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-Taormina":   {"Parent":0.06,"Adult":0.27,"Child":0.67,"rd":"New","conflict":50,"life_script":"The right piece at the right moment","trigger_top":["New Product Launch","Cultural Moment"],"trigger_null":["Heritage Campaign"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-StMoritz":   {"Parent":0.10,"Adult":0.32,"Child":0.58,"rd":"New","conflict":42,"life_script":"One piece. The right brand. That's enough.","trigger_top":["Exclusivity Signaling","New Product Launch"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-Capri":      {"Parent":0.08,"Adult":0.29,"Child":0.63,"rd":"New","conflict":46,"life_script":"This piece is my passport to the conversation","trigger_top":["New Product Launch","Cultural Moment"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-Courchevel": {"Parent":0.12,"Adult":0.33,"Child":0.55,"rd":"New","conflict":38,"life_script":"Entry done right","trigger_top":["New Product Launch","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-ForteMarmi": {"Parent":0.14,"Adult":0.35,"Child":0.51,"rd":"New","conflict":34,"life_script":"Quality over quantity, always","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-PortoCervo": {"Parent":0.09,"Adult":0.28,"Child":0.63,"rd":"New","conflict":44,"life_script":"The right piece opens the right doors","trigger_top":["Scarcity Drop","New Product Launch"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › EU-Ibiza":      {"Parent":0.04,"Adult":0.20,"Child":0.76,"rd":"New","conflict":62,"life_script":"I buy in before the moment peaks","trigger_top":["Scarcity Drop","Cultural Moment"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › US":            {"Parent":0.05,"Adult":0.25,"Child":0.70,"rd":"New","conflict":58,"life_script":"I buy in before the moment peaks","trigger_top":["Scarcity Drop","Celebrity Co-sign","New Product Launch"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › China-T1":      {"Parent":0.10,"Adult":0.32,"Child":0.58,"rd":"New","conflict":48,"life_script":"One piece. The right signal.","trigger_top":["Scarcity Drop","KOL Co-sign","Gifting Ritual"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › China-T2":      {"Parent":0.16,"Adult":0.27,"Child":0.57,"rd":"New","conflict":52,"life_script":"This signals I am on the right trajectory","trigger_top":["KOL Co-sign","Logo Visibility","Gifting Ritual"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Fashionista › Entry Ritualist › China-T3":      {"Parent":0.22,"Adult":0.23,"Child":0.55,"rd":"New","conflict":56,"life_script":"This brand signals I have arrived","trigger_top":["Logo Visibility","KOL Co-sign","Gifting Ritual"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Fashionista › Entry Ritualist › ME":            {"Parent":0.15,"Adult":0.27,"Child":0.58,"rd":"New","conflict":50,"life_script":"One piece that speaks for the family","trigger_top":["Gifting Ritual","Exclusivity Signaling","New Product Launch"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Entry Ritualist › Japan":         {"Parent":0.20,"Adult":0.38,"Child":0.42,"rd":"New","conflict":30,"life_script":"I earn the right piece through understanding","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Logo Visibility","Hype Drop"]},
    "Gen Z — Fashionista › Entry Ritualist › South Korea":   {"Parent":0.08,"Adult":0.30,"Child":0.62,"rd":"New","conflict":48,"life_script":"This piece is my cultural credential","trigger_top":["Idol Co-sign","New Product Launch","Scarcity Drop"],"trigger_null":["Heritage Campaign"]},

    # FASHIONISTA > PARADOX BUYER
    "Gen Z — Fashionista › Paradox Buyer › EU-StTropez":   {"Parent":0.06,"Adult":0.30,"Child":0.64,"rd":"New","conflict":72,"life_script":"I know better but I want it anyway","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-Mykonos":    {"Parent":0.04,"Adult":0.24,"Child":0.72,"rd":"New","conflict":78,"life_script":"Everyone is watching and I respond","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-Portofino":  {"Parent":0.08,"Adult":0.32,"Child":0.60,"rd":"New","conflict":65,"life_script":"I know the codes but emotion wins","trigger_top":["Cultural Moment","New Product Launch"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-Taormina":   {"Parent":0.07,"Adult":0.30,"Child":0.63,"rd":"New","conflict":68,"life_script":"I want to be ahead but I follow the moment","trigger_top":["Cultural Moment","New Product Launch"],"trigger_null":["Heritage Campaign"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-StMoritz":   {"Parent":0.12,"Adult":0.36,"Child":0.52,"rd":"Established","conflict":58,"life_script":"I know better, I spend anyway","trigger_top":["Exclusivity Signaling","Cultural Moment"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-Capri":      {"Parent":0.09,"Adult":0.33,"Child":0.58,"rd":"New","conflict":62,"life_script":"Rational mind, emotional wallet","trigger_top":["Cultural Moment","Exclusivity Signaling"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-Courchevel": {"Parent":0.13,"Adult":0.36,"Child":0.51,"rd":"Established","conflict":55,"life_script":"I overthink it then buy it","trigger_top":["Exclusivity Signaling","New Product Launch"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-ForteMarmi": {"Parent":0.15,"Adult":0.38,"Child":0.47,"rd":"Established","conflict":50,"life_script":"I question every purchase and make it anyway","trigger_top":["Exclusivity Signaling","Heritage Campaign"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-PortoCervo": {"Parent":0.10,"Adult":0.32,"Child":0.58,"rd":"New","conflict":64,"life_script":"I rationalize what I already want","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › EU-Ibiza":      {"Parent":0.04,"Adult":0.24,"Child":0.72,"rd":"New","conflict":76,"life_script":"FOMO wins every time","trigger_top":["Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign","Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › US":            {"Parent":0.05,"Adult":0.27,"Child":0.68,"rd":"New","conflict":74,"life_script":"I know it is hype. I still want it.","trigger_top":["Cultural Moment","Scarcity Drop","Celebrity Co-sign"],"trigger_null":["Heritage Campaign"]},
    "Gen Z — Fashionista › Paradox Buyer › China-T1":      {"Parent":0.10,"Adult":0.34,"Child":0.56,"rd":"New","conflict":62,"life_script":"I know the codes and still chase the moment","trigger_top":["Cultural Moment","Guochao","Scarcity Drop"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Fashionista › Paradox Buyer › China-T2":      {"Parent":0.16,"Adult":0.30,"Child":0.54,"rd":"New","conflict":66,"life_script":"Values and status in constant tension","trigger_top":["KOL Co-sign","Cultural Moment","Gifting Ritual"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › China-T3":      {"Parent":0.22,"Adult":0.26,"Child":0.52,"rd":"New","conflict":70,"life_script":"Individual want vs collective signal","trigger_top":["Logo Visibility","KOL Co-sign","Gifting Ritual"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Fashionista › Paradox Buyer › ME":            {"Parent":0.16,"Adult":0.30,"Child":0.54,"rd":"New","conflict":68,"life_script":"Family values, personal desire, constant tension","trigger_top":["Exclusivity Signaling","Gifting Ritual","Cultural Moment"],"trigger_null":["Price Hike"]},
    "Gen Z — Fashionista › Paradox Buyer › Japan":         {"Parent":0.24,"Adult":0.44,"Child":0.32,"rd":"Established","conflict":45,"life_script":"I research everything then trust my gut","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Logo Visibility","Hype Drop"]},
    "Gen Z — Fashionista › Paradox Buyer › South Korea":   {"Parent":0.09,"Adult":0.35,"Child":0.56,"rd":"New","conflict":60,"life_script":"I set the standard then follow the trend","trigger_top":["Idol Co-sign","Cultural Moment","Scarcity Drop"],"trigger_null":["Heritage Campaign"]},

    # CLASSIC > CENTURION
    "Gen Z — Classic › Centurion › EU-StTropez":   {"Parent":0.18,"Adult":0.42,"Child":0.40,"rd":"Established","conflict":28,"life_script":"I invest in experiences that define me","trigger_top":["Exclusivity Signaling","Cultural Moment"],"trigger_null":["Logo Visibility","Mass Campaign"]},
    "Gen Z — Classic › Centurion › EU-Mykonos":    {"Parent":0.14,"Adult":0.38,"Child":0.48,"rd":"New","conflict":35,"life_script":"Quality in the right context","trigger_top":["Exclusivity Signaling","Cultural Moment"],"trigger_null":["Logo Visibility","Mass Campaign"]},
    "Gen Z — Classic › Centurion › EU-Portofino":  {"Parent":0.20,"Adult":0.45,"Child":0.35,"rd":"Established","conflict":22,"life_script":"The right piece at the right place","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Price Hike"]},
    "Gen Z — Classic › Centurion › EU-Taormina":   {"Parent":0.18,"Adult":0.42,"Child":0.40,"rd":"Established","conflict":25,"life_script":"Beauty that lasts beyond the season","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Centurion › EU-StMoritz":   {"Parent":0.26,"Adult":0.46,"Child":0.28,"rd":"Legacy","conflict":18,"life_script":"I experience what others aspire to","trigger_top":["Exclusivity Signaling","Heritage Campaign"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Centurion › EU-Capri":      {"Parent":0.22,"Adult":0.44,"Child":0.34,"rd":"Established","conflict":20,"life_script":"Italian excellence, lived not performed","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Centurion › EU-Courchevel": {"Parent":0.28,"Adult":0.46,"Child":0.26,"rd":"Legacy","conflict":16,"life_script":"Luxury is a standard, not an aspiration","trigger_top":["Exclusivity Signaling","Heritage Campaign"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Centurion › EU-ForteMarmi": {"Parent":0.32,"Adult":0.46,"Child":0.22,"rd":"Legacy","conflict":14,"life_script":"We have always known quality","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility","Price Hike"]},
    "Gen Z — Classic › Centurion › EU-PortoCervo": {"Parent":0.20,"Adult":0.44,"Child":0.36,"rd":"Established","conflict":22,"life_script":"Selective by nature, not by effort","trigger_top":["Exclusivity Signaling","Cultural Moment"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Centurion › EU-Ibiza":      {"Parent":0.14,"Adult":0.40,"Child":0.46,"rd":"New","conflict":32,"life_script":"Experience first, object second","trigger_top":["Cultural Moment","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Centurion › US":            {"Parent":0.16,"Adult":0.44,"Child":0.40,"rd":"Established","conflict":30,"life_script":"I invest in quality that lasts","trigger_top":["Exclusivity Signaling","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Centurion › China-T1":      {"Parent":0.22,"Adult":0.46,"Child":0.32,"rd":"Established","conflict":20,"life_script":"I understand craft before I buy","trigger_top":["Craft Narrative","Guochao","Exclusivity Signaling"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Centurion › China-T2":      {"Parent":0.26,"Adult":0.40,"Child":0.34,"rd":"Established","conflict":28,"life_script":"Luxury that grows with me","trigger_top":["Gifting Ritual","Exclusivity Signaling","Craft Narrative"],"trigger_null":["Price Hike"]},
    "Gen Z — Classic › Centurion › China-T3":      {"Parent":0.30,"Adult":0.36,"Child":0.34,"rd":"New","conflict":36,"life_script":"I invest in signals that last","trigger_top":["Logo Visibility","Gifting Ritual","KOL Co-sign"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Classic › Centurion › ME":            {"Parent":0.28,"Adult":0.40,"Child":0.32,"rd":"Established","conflict":24,"life_script":"Quality as a family value","trigger_top":["Exclusivity Signaling","Gifting Ritual","Heritage Campaign"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Centurion › Japan":         {"Parent":0.36,"Adult":0.46,"Child":0.18,"rd":"Legacy","conflict":14,"life_script":"I understand what most will never notice","trigger_top":["Craft Narrative","Heritage Campaign"],"trigger_null":["Logo Visibility","Hype Drop","Mass Campaign"]},
    "Gen Z — Classic › Centurion › South Korea":   {"Parent":0.18,"Adult":0.46,"Child":0.36,"rd":"Established","conflict":26,"life_script":"Quality that earns cultural respect","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Heritage Campaign","Logo Visibility"]},

    # CLASSIC > CULTURAL ARCHITECT
    "Gen Z — Classic › Cultural Architect › EU-StTropez":   {"Parent":0.20,"Adult":0.46,"Child":0.34,"rd":"Established","conflict":22,"life_script":"I buy what I believe in","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › EU-Mykonos":    {"Parent":0.15,"Adult":0.42,"Child":0.43,"rd":"Established","conflict":28,"life_script":"Quality is my aesthetic statement","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Cultural Architect › EU-Portofino":  {"Parent":0.22,"Adult":0.48,"Child":0.30,"rd":"Legacy","conflict":18,"life_script":"Beauty with conscience","trigger_top":["Craft Narrative","Sustainability Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › EU-Taormina":   {"Parent":0.20,"Adult":0.45,"Child":0.35,"rd":"Established","conflict":20,"life_script":"I discovered this before it became obvious","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › EU-StMoritz":   {"Parent":0.28,"Adult":0.48,"Child":0.24,"rd":"Legacy","conflict":15,"life_script":"Depth over display, always","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › EU-Capri":      {"Parent":0.24,"Adult":0.46,"Child":0.30,"rd":"Legacy","conflict":16,"life_script":"Italian soul, enduring quality","trigger_top":["Craft Narrative","Heritage Campaign"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Cultural Architect › EU-Courchevel": {"Parent":0.30,"Adult":0.48,"Child":0.22,"rd":"Legacy","conflict":13,"life_script":"Excellence is non-negotiable","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › EU-ForteMarmi": {"Parent":0.34,"Adult":0.48,"Child":0.18,"rd":"Legacy","conflict":11,"life_script":"We have always known quality","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility","Price Hike"]},
    "Gen Z — Classic › Cultural Architect › EU-PortoCervo": {"Parent":0.22,"Adult":0.46,"Child":0.32,"rd":"Established","conflict":18,"life_script":"Curated, intentional, lasting","trigger_top":["Exclusivity Signaling","Craft Narrative"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Cultural Architect › EU-Ibiza":      {"Parent":0.16,"Adult":0.44,"Child":0.40,"rd":"Established","conflict":26,"life_script":"Values first, even here","trigger_top":["Cultural Moment","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › US":            {"Parent":0.18,"Adult":0.46,"Child":0.36,"rd":"Established","conflict":24,"life_script":"I consume with intention and quality","trigger_top":["Craft Narrative","Sustainability Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › China-T1":      {"Parent":0.24,"Adult":0.48,"Child":0.28,"rd":"Established","conflict":16,"life_script":"Craft before signal","trigger_top":["Craft Narrative","Guochao","Sustainability Narrative"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Cultural Architect › China-T2":      {"Parent":0.28,"Adult":0.42,"Child":0.30,"rd":"Established","conflict":22,"life_script":"Quality that reflects my values","trigger_top":["Gifting Ritual","Craft Narrative","Cultural Moment"],"trigger_null":["Price Hike"]},
    "Gen Z — Classic › Cultural Architect › China-T3":      {"Parent":0.32,"Adult":0.36,"Child":0.32,"rd":"New","conflict":30,"life_script":"The right signal, earned","trigger_top":["Gifting Ritual","Logo Visibility","KOL Co-sign"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Classic › Cultural Architect › ME":            {"Parent":0.30,"Adult":0.42,"Child":0.28,"rd":"Established","conflict":18,"life_script":"Quality as a family legacy","trigger_top":["Heritage Campaign","Gifting Ritual","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Cultural Architect › Japan":         {"Parent":0.38,"Adult":0.46,"Child":0.16,"rd":"Legacy","conflict":10,"life_script":"I understand before I acquire","trigger_top":["Craft Narrative","Sustainability Narrative","Heritage Campaign"],"trigger_null":["Logo Visibility","Hype Drop","Mass Campaign"]},
    "Gen Z — Classic › Cultural Architect › South Korea":   {"Parent":0.20,"Adult":0.48,"Child":0.32,"rd":"Established","conflict":20,"life_script":"Craft and culture, not hype","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Heritage Campaign","Logo Visibility"]},

    # CLASSIC > ENTRY RITUALIST
    "Gen Z — Classic › Entry Ritualist › EU-StTropez":   {"Parent":0.16,"Adult":0.44,"Child":0.40,"rd":"New","conflict":38,"life_script":"My first real piece. It has to be right.","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › EU-Mykonos":    {"Parent":0.12,"Adult":0.38,"Child":0.50,"rd":"New","conflict":44,"life_script":"Entry into quality, not hype","trigger_top":["New Product Launch","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Entry Ritualist › EU-Portofino":  {"Parent":0.18,"Adult":0.46,"Child":0.36,"rd":"New","conflict":32,"life_script":"One piece. Lasting. Italian.","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › EU-Taormina":   {"Parent":0.16,"Adult":0.43,"Child":0.41,"rd":"New","conflict":34,"life_script":"Beauty that I will keep forever","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › EU-StMoritz":   {"Parent":0.22,"Adult":0.46,"Child":0.32,"rd":"Established","conflict":26,"life_script":"Investment, not impulse","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › EU-Capri":      {"Parent":0.20,"Adult":0.45,"Child":0.35,"rd":"New","conflict":28,"life_script":"The piece that starts the collection","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Entry Ritualist › EU-Courchevel": {"Parent":0.25,"Adult":0.46,"Child":0.29,"rd":"Established","conflict":22,"life_script":"First piece. Right brand. Long hold.","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › EU-ForteMarmi": {"Parent":0.28,"Adult":0.46,"Child":0.26,"rd":"Established","conflict":18,"life_script":"Quality chosen once, kept forever","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › EU-PortoCervo": {"Parent":0.18,"Adult":0.44,"Child":0.38,"rd":"New","conflict":30,"life_script":"The right entry at the right moment","trigger_top":["Exclusivity Signaling","New Product Launch"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Entry Ritualist › EU-Ibiza":      {"Parent":0.12,"Adult":0.40,"Child":0.48,"rd":"New","conflict":40,"life_script":"Even here, quality over noise","trigger_top":["New Product Launch","Cultural Moment"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › US":            {"Parent":0.14,"Adult":0.44,"Child":0.42,"rd":"New","conflict":36,"life_script":"First real investment. Has to hold.","trigger_top":["Craft Narrative","Exclusivity Signaling","New Product Launch"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › China-T1":      {"Parent":0.20,"Adult":0.46,"Child":0.34,"rd":"New","conflict":28,"life_script":"Quality entry into the right codes","trigger_top":["Craft Narrative","Guochao","New Product Launch"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Entry Ritualist › China-T2":      {"Parent":0.24,"Adult":0.40,"Child":0.36,"rd":"New","conflict":34,"life_script":"First investment piece. Right signal.","trigger_top":["Gifting Ritual","New Product Launch","KOL Co-sign"],"trigger_null":["Price Hike"]},
    "Gen Z — Classic › Entry Ritualist › China-T3":      {"Parent":0.28,"Adult":0.34,"Child":0.38,"rd":"New","conflict":40,"life_script":"Entry that signals arrival","trigger_top":["Logo Visibility","Gifting Ritual","KOL Co-sign"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Classic › Entry Ritualist › ME":            {"Parent":0.26,"Adult":0.42,"Child":0.32,"rd":"New","conflict":30,"life_script":"A piece worthy of the family name","trigger_top":["Gifting Ritual","Exclusivity Signaling","Heritage Campaign"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Entry Ritualist › Japan":         {"Parent":0.32,"Adult":0.46,"Child":0.22,"rd":"New","conflict":18,"life_script":"I earn the right piece through understanding","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Logo Visibility","Hype Drop"]},
    "Gen Z — Classic › Entry Ritualist › South Korea":   {"Parent":0.16,"Adult":0.46,"Child":0.38,"rd":"New","conflict":30,"life_script":"Quality credential over cultural hype","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Heritage Campaign","Logo Visibility"]},

    # CLASSIC > PARADOX BUYER
    "Gen Z — Classic › Paradox Buyer › EU-StTropez":   {"Parent":0.18,"Adult":0.46,"Child":0.36,"rd":"Established","conflict":55,"life_script":"I research for weeks then trust my instinct","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › EU-Mykonos":    {"Parent":0.14,"Adult":0.42,"Child":0.44,"rd":"Established","conflict":60,"life_script":"I know quality but context pulls me","trigger_top":["Cultural Moment","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Paradox Buyer › EU-Portofino":  {"Parent":0.20,"Adult":0.48,"Child":0.32,"rd":"Established","conflict":48,"life_script":"Rational choice, emotional moment","trigger_top":["Craft Narrative","New Product Launch"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › EU-Taormina":   {"Parent":0.18,"Adult":0.45,"Child":0.37,"rd":"Established","conflict":50,"life_script":"I know the value but want the feeling","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › EU-StMoritz":   {"Parent":0.26,"Adult":0.48,"Child":0.26,"rd":"Legacy","conflict":42,"life_script":"I know exactly what to buy and still deliberate","trigger_top":["Heritage Campaign","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › EU-Capri":      {"Parent":0.22,"Adult":0.46,"Child":0.32,"rd":"Established","conflict":45,"life_script":"Italian quality deserves deliberation","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Paradox Buyer › EU-Courchevel": {"Parent":0.28,"Adult":0.48,"Child":0.24,"rd":"Legacy","conflict":38,"life_script":"I always know. I still wait.","trigger_top":["Heritage Campaign","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › EU-ForteMarmi": {"Parent":0.32,"Adult":0.48,"Child":0.20,"rd":"Legacy","conflict":34,"life_script":"Deliberate always. Certain eventually.","trigger_top":["Heritage Campaign","Craft Narrative"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › EU-PortoCervo": {"Parent":0.20,"Adult":0.46,"Child":0.34,"rd":"Established","conflict":46,"life_script":"I know what is right but take my time","trigger_top":["Exclusivity Signaling","Craft Narrative"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Paradox Buyer › EU-Ibiza":      {"Parent":0.14,"Adult":0.44,"Child":0.42,"rd":"Established","conflict":55,"life_script":"Even in chaos I choose quality","trigger_top":["Cultural Moment","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › US":            {"Parent":0.16,"Adult":0.46,"Child":0.38,"rd":"Established","conflict":56,"life_script":"I over-research and then trust quality","trigger_top":["Craft Narrative","Exclusivity Signaling"],"trigger_null":["Mass Campaign","Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › China-T1":      {"Parent":0.22,"Adult":0.48,"Child":0.30,"rd":"Established","conflict":44,"life_script":"I understand craft and still negotiate with desire","trigger_top":["Craft Narrative","Guochao","Exclusivity Signaling"],"trigger_null":["Logo Visibility"]},
    "Gen Z — Classic › Paradox Buyer › China-T2":      {"Parent":0.26,"Adult":0.42,"Child":0.32,"rd":"Established","conflict":50,"life_script":"Quality vs signal, always in tension","trigger_top":["Gifting Ritual","Craft Narrative","KOL Co-sign"],"trigger_null":["Price Hike"]},
    "Gen Z — Classic › Paradox Buyer › China-T3":      {"Parent":0.30,"Adult":0.36,"Child":0.34,"rd":"New","conflict":56,"life_script":"I want quality but need the signal","trigger_top":["Logo Visibility","Gifting Ritual","KOL Co-sign"],"trigger_null":["Craft Narrative"]},
    "Gen Z — Classic › Paradox Buyer › ME":            {"Parent":0.28,"Adult":0.44,"Child":0.28,"rd":"Established","conflict":48,"life_script":"Family values, personal tension, quality wins","trigger_top":["Heritage Campaign","Gifting Ritual","Exclusivity Signaling"],"trigger_null":["Mass Campaign"]},
    "Gen Z — Classic › Paradox Buyer › Japan":         {"Parent":0.36,"Adult":0.46,"Child":0.18,"rd":"Legacy","conflict":30,"life_script":"I already know. I still deliberate.","trigger_top":["Craft Narrative","Heritage Campaign"],"trigger_null":["Logo Visibility","Hype Drop","Mass Campaign"]},
    "Gen Z — Classic › Paradox Buyer › South Korea":   {"Parent":0.20,"Adult":0.48,"Child":0.32,"rd":"Established","conflict":44,"life_script":"Quality standard vs cultural moment, always","trigger_top":["Craft Narrative","Cultural Moment"],"trigger_null":["Heritage Campaign","Logo Visibility"]},
}


def run_simulation(campaign_type, n_vics, cities, budget, seed=42, brand_city_bias=None):
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
        city = assigned_cities[i]
        cf = cp.get("city_bias", {}).get(city, 1.0)
        if brand_city_bias:
            cf = cf * brand_city_bias.get(city, 1.0)
        pi = assigned_personas[i]
        alpha = cp["base_intent_alpha"] * p_intent[pi] * cf * budget_factor
        beta = cp["base_intent_beta"] / (p_intent[pi] * cf)
        intent = float(np.clip(rng.beta(alpha, beta), 0, 1))
        engagement = float(np.clip(rng.beta(3.0*p_eng[pi], 3.5) * cp["engagement_multiplier"] * cf * budget_factor, 0, 1))
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
    st.markdown('<div style="font-size:.5rem;letter-spacing:.1em;text-transform:uppercase;color:#666;margin-bottom:.4rem;">Type a brand</div>', unsafe_allow_html=True)
    BRAND_PROFILES = {
        "Gucci":           {"ego_override": {"Ultra-HNWI Collector":{"Parent":0.55,"Adult":0.25,"Child":0.20},"Aspirational Buyer":{"Parent":0.15,"Adult":0.25,"Child":0.60},"Heritage Loyalist":{"Parent":0.60,"Adult":0.30,"Child":0.10}}, "rd_default": "Established", "color": "#C8D400", "note": "Dual positioning — heritage codes and cultural edge"},
        "Bottega Veneta":  {"ego_override": {"Ultra-HNWI Collector":{"Parent":0.75,"Adult":0.20,"Child":0.05},"Private Client":{"Parent":0.30,"Adult":0.65,"Child":0.05},"Heritage Loyalist":{"Parent":0.80,"Adult":0.15,"Child":0.05}}, "rd_default": "Legacy", "color": "#111", "note": "Parent-dominant — Legacy depth, stealth anti-logo positioning"},
        "Dior":            {"ego_override": {"Ultra-HNWI Collector":{"Parent":0.65,"Adult":0.25,"Child":0.10},"Heritage Loyalist":{"Parent":0.70,"Adult":0.22,"Child":0.08},"Private Client":{"Parent":0.35,"Adult":0.55,"Child":0.10}}, "rd_default": "Legacy", "color": "#888", "note": "Heritage-dominant — savoir-faire, Parisian codes, Legacy default"},
        "Louis Vuitton":   {"ego_override": {"Ultra-HNWI Collector":{"Parent":0.60,"Adult":0.25,"Child":0.15},"Aspirational Buyer":{"Parent":0.20,"Adult":0.20,"Child":0.60},"Digital Native HNWI":{"Parent":0.15,"Adult":0.40,"Child":0.45}}, "rd_default": "Established", "color": "#C8D400", "note": "Dual portfolio — Parent for VICs, Child for aspirational and digital"},
        "The Attico":      {"ego_override": {"Trend Setter":{"Parent":0.05,"Adult":0.25,"Child":0.70},"Digital Native HNWI":{"Parent":0.05,"Adult":0.30,"Child":0.65},"Aspirational Buyer":{"Parent":0.08,"Adult":0.22,"Child":0.70}}, "rd_default": "New", "color": "#555", "note": "Child-dominant — cultural cool, emerging luxury, Gen Z / millennial anchor"},
        "Twinset":         {"ego_override": {"Aspirational Buyer":{"Parent":0.30,"Adult":0.35,"Child":0.35},"Private Client":{"Parent":0.25,"Adult":0.60,"Child":0.15},"Heritage Loyalist":{"Parent":0.45,"Adult":0.40,"Child":0.15}}, "rd_default": "Established", "color": "#888", "note": "Balanced Adult — accessible premium, rational purchase, mid-market luxury"},
        "Pinko":           {"ego_override": {"Aspirational Buyer":{"Parent":0.15,"Adult":0.25,"Child":0.60},"Trend Setter":{"Parent":0.10,"Adult":0.30,"Child":0.60},"Digital Native HNWI":{"Parent":0.10,"Adult":0.35,"Child":0.55}}, "rd_default": "New", "color": "#555", "note": "Child-dominant — trend-driven, FOMO-sensitive, aspirational entry point"},
        "Patrizia Pepe":   {"ego_override": {"Aspirational Buyer":{"Parent":0.20,"Adult":0.30,"Child":0.50},"Trend Setter":{"Parent":0.12,"Adult":0.33,"Child":0.55},"Digital Native HNWI":{"Parent":0.12,"Adult":0.38,"Child":0.50}}, "rd_default": "New", "color": "#555", "note": "Child-Adult mix — contemporary femininity, digital-native positioning"},
        "Velasca":         {"ego_override": {"Private Client":{"Parent":0.25,"Adult":0.68,"Child":0.07},"Ultra-HNWI Collector":{"Parent":0.40,"Adult":0.52,"Child":0.08},"Heritage Loyalist":{"Parent":0.50,"Adult":0.42,"Child":0.08}}, "rd_default": "Established", "color": "#C8D400", "note": "Adult-dominant — craft transparency, rational premium, direct-to-consumer trust"},
        "Max Mara":        {"ego_override": {"Private Client":{"Parent":0.35,"Adult":0.58,"Child":0.07},"Heritage Loyalist":{"Parent":0.62,"Adult":0.30,"Child":0.08},"Ultra-HNWI Collector":{"Parent":0.55,"Adult":0.35,"Child":0.10}}, "rd_default": "Legacy", "color": "#888", "note": "Parent-Adult — timeless investment dressing, low-noise luxury"},
        "Valentino":       {"ego_override": {"Ultra-HNWI Collector":{"Parent":0.60,"Adult":0.25,"Child":0.15},"Trend Setter":{"Parent":0.10,"Adult":0.25,"Child":0.65},"Aspirational Buyer":{"Parent":0.15,"Adult":0.20,"Child":0.65}}, "rd_default": "Established", "color": "#C8D400", "note": "Dual tension — Parent for couture VIC, Child for Pink PP cultural moment"},
        "Moncler":         {"ego_override": {"Digital Native HNWI":{"Parent":0.15,"Adult":0.40,"Child":0.45},"Trend Setter":{"Parent":0.10,"Adult":0.30,"Child":0.60},"Ultra-HNWI Collector":{"Parent":0.50,"Adult":0.35,"Child":0.15}}, "rd_default": "Established", "color": "#111", "note": "Child-Adult mix — experiential luxury, Genius drops, FOMO activation"},
        "Miu Miu":         {"ego_override": {"Trend Setter":{"Parent":0.05,"Adult":0.25,"Child":0.70},"Digital Native HNWI":{"Parent":0.05,"Adult":0.30,"Child":0.65},"Aspirational Buyer":{"Parent":0.08,"Adult":0.20,"Child":0.72}}, "rd_default": "New", "color": "#C8D400", "note": "Child-dominant — hyper-cultural relevance, viral aesthetics, Gen Z pinnacle"},
        "Chanel":          {"ego_override": {"Ultra-HNWI Collector":{"Parent":0.80,"Adult":0.15,"Child":0.05},"Heritage Loyalist":{"Parent":0.82,"Adult":0.14,"Child":0.04},"Private Client":{"Parent":0.55,"Adult":0.40,"Child":0.05}}, "rd_default": "Legacy", "color": "#111", "note": "Ultra Parent-dominant — identity anchor, savoir-faire absolute, pricing power maximum"},
        "Luisa Spagnoli":  {"ego_override": {"Heritage Loyalist":{"Parent":0.65,"Adult":0.28,"Child":0.07},"Private Client":{"Parent":0.30,"Adult":0.60,"Child":0.10},"Aspirational Buyer":{"Parent":0.35,"Adult":0.40,"Child":0.25}}, "rd_default": "Established", "color": "#888", "note": "Parent-Adult — Italian heritage, loyalist core, mid-luxury positioning"},
        "Kiko Milano":     {"ego_override": {"Aspirational Buyer":{"Parent":0.10,"Adult":0.30,"Child":0.60},"Digital Native HNWI":{"Parent":0.08,"Adult":0.42,"Child":0.50},"Trend Setter":{"Parent":0.08,"Adult":0.32,"Child":0.60}}, "rd_default": "New", "color": "#C8D400", "note": "Child-dominant — democratised beauty luxury, digital-first, high FOMO sensitivity"},
    }
    typed_brand = st.text_input("", placeholder="e.g. Hermès, Chanel, Dior...", key="typed_brand", label_visibility="collapsed")
    _typed = typed_brand.strip() if typed_brand else ""
    _matched = next((k for k in BRAND_PROFILES if k.lower() == _typed.lower()), None)
    selected_brand = _matched if _matched else (_typed if _typed else "Generic Luxury")
    brand_profile = BRAND_PROFILES.get(selected_brand, {"ego_override": None, "rd_default": "Established", "color": "#888", "note": "Custom brand — synthetic baseline applied"})
    if _typed:
        calibrated = _matched is not None
        note_color = "#C8D400" if calibrated else "#888"
        note_text = brand_profile["note"] if calibrated else f"Custom brand — synthetic baseline applied. Pre-calibrated brands: {', '.join(BRAND_PROFILES.keys())}"
        st.markdown(f'<div style="font-size:.58rem;color:{note_color};line-height:1.5;margin-bottom:.6rem;">{note_text}</div>', unsafe_allow_html=True)
    if "brand_profile" not in st.session_state or st.session_state.get("_last_brand") != selected_brand:
        st.session_state["brand_profile"] = brand_profile
        st.session_state["_last_brand"] = selected_brand
    st.markdown('<hr style="border-color:#333;margin:1rem 0;">', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:1.5rem;text-align:center;font-size:.65rem;font-weight:600;color:#555;letter-spacing:.1em;text-transform:uppercase;">Dress for Good</div>', unsafe_allow_html=True)


if "n_vics" not in st.session_state: st.session_state["n_vics"] = 5000
if "cities" not in st.session_state: st.session_state["cities"] = ALL_CITIES[:5]
if "budget" not in st.session_state: st.session_state["budget"] = 500000

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10 = st.tabs([
    "Campaign Simulator","Creative Testing","Product Launch","Price Optimisation",
    "Market Segmentation","Churn Prediction","Brand Perception",
    "VIC Psychographic Engine","VIC Focus Group","Claims Test",
])

with tab1:
    REGION_MAP = {
        "All markets":     ["Milano","Paris","London","New York","Los Angeles","Dubai","Riyadh","Tokyo","Shanghai","Singapore"],
        "Europe":          ["Milano","Paris","London","Zurich","Geneva","Monaco","Madrid","Amsterdam","Copenhagen","Stockholm"],
        "Middle East":     ["Dubai","Riyadh","Abu Dhabi","Doha","Kuwait City"],
        "Asia Pacific":    ["Tokyo","Shanghai","Beijing","Hong Kong","Singapore","Seoul","Sydney"],
        "South East Asia": ["Singapore","Bangkok","Kuala Lumpur","Jakarta","Manila"],
        "Americas":        ["New York","Los Angeles","Miami","São Paulo","Mexico City","Chicago","San Francisco"],
        "China":           ["Shanghai","Beijing","Chengdu","Guangzhou","Shenzhen"],
        "Africa & Levant": ["Dubai","Cairo","Casablanca","Johannesburg","Beirut"],
    }
    CITY_POOL = ["Milano","Paris","London","New York","Los Angeles","Dubai","Riyadh","Tokyo","Shanghai","Singapore"]
    ct_col1, ct_col2, ct_col3 = st.columns([1.4,1,1])
    with ct_col1:
        campaign_type = st.selectbox("Campaign type", options=list(CAMPAIGN_PARAMS.keys()), format_func=lambda x:CAMPAIGN_PARAMS[x]["label"])
    with ct_col2:
        region = st.selectbox("Region", list(REGION_MAP.keys()), key="region_tab1")
        region_cities = REGION_MAP[region]
    with ct_col3:
        sim_cities = [c for c in region_cities if c in CITY_POOL] or CITY_POOL[:3]
        city_options = ["All in region"] + sim_cities
        city_choice = st.selectbox("Major city", city_options, key="city_tab1")
        cities = sim_cities if city_choice == "All in region" else [city_choice] if city_choice in CITY_POOL else sim_cities
    n_vics = st.slider("VIC Pool Size", min_value=500, max_value=50000, value=5000, step=500, key="n_vics_tab1")
    budget = st.slider("Budget (EUR)", min_value=50000, max_value=5000000, value=500000, step=50000, key="budget_tab1")
    st.markdown("<br>",unsafe_allow_html=True)
    if st.button("Run Simulation", key="run_tab1"):
        _bp1 = st.session_state.get("brand_profile") or {}
        _brand_seed = hash(st.session_state.get("_last_brand","")) % 10000
        _brand_city_bias = _bp1.get("city_bias", None)
        with st.spinner("Running simulation..."):
            df = run_simulation(campaign_type, n_vics, cities, budget, seed=42+_brand_seed, brand_city_bias=_brand_city_bias)
            summary = compute_summary(df, budget)
        c1,c2,c3,c4,c5 = st.columns(5)
        kpis = [
            (f'{summary["buy_rate"]}%',"Buy rate","Beta-dist. intent model"),
            (f'{summary["buyers"]:,}',"Buyers","VICs with intent > threshold"),
            (f'EUR {summary["total_revenue"]/1000000:.1f}M',"Sim. Revenue","Synthetic proxy — not a forecast"),
            (f'{summary["roi"]:+.0f}%',"Sim. ROI Index","Comparative index only — not a financial projection"),
            (f'{summary["total_reach"]//1000000:.1f}M',"Reach","Sum influence scores"),
        ]
        for col,(val,label,note) in zip([c1,c2,c3,c4,c5],kpis):
            with col:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
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
        col_csv,col_xl = st.columns(2)
        csv_buf = io.StringIO(); df.to_csv(csv_buf,index=False)
        exc_buf = io.BytesIO()
        with pd.ExcelWriter(exc_buf, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="VIC Data")
            summary["city_summary"].to_excel(writer, index=False, sheet_name="City Summary")
            summary["persona_summary"].to_excel(writer, index=False, sheet_name="Persona Summary")
        exc_buf.seek(0)
        with col_csv:
            st.download_button("Export CSV",data=csv_buf.getvalue(),file_name=f"campaign_{campaign_type}.csv",mime="text/csv")
        with col_xl:
            st.download_button("Export Excel",data=exc_buf.read(),file_name=f"campaign_{campaign_type}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        _brand_name1 = st.session_state.get("_last_brand","")
        _brand_note1 = (st.session_state.get("brand_profile") or {}).get("note","")
        if _brand_name1 and _brand_name1 != "Generic Luxury":
            st.markdown(f"<div style='padding:.5rem 1rem;margin-bottom:.8rem;border-left:3px solid #C8D400;font-size:.78rem;color:#111;'><strong>{_brand_name1}</strong> — {_brand_note1}</div>", unsafe_allow_html=True)
        top_city = summary["city_summary"].iloc[0]["City"]
        top_persona = summary["persona_summary"].iloc[0]["Persona"]
        roi_read = "strong positive" if summary["roi"]>50 else "moderate" if summary["roi"]>0 else "negative"
        readout = (f"Simulation of {summary['total']:,} synthetic VIC agents across {', '.join(cities)} "
                   f"projects a {roi_read} ROI of {summary['roi']:+.0f}% on a EUR{budget:,.0f} investment. "
                   f"Conversion: {summary['buy_rate']}%. Top market: {top_city}. Dominant persona: {top_persona}.")
        st.markdown(f"<div style='font-family:Montserrat;font-size:.88rem;font-weight:300;color:#111;line-height:1.9;padding:1rem 0 1rem 1.2rem;border-left:3px solid #C8D400;'>{readout}</div>",unsafe_allow_html=True)
        st.markdown("<div style='font-family:Montserrat;font-size:.72rem;color:#999;margin-top:.8rem;padding:.6rem 1rem;border:1px solid #E8E8E4;'>⚠️ <strong>Simulation disclaimer</strong> — Revenue and ROI Index are synthetic outputs based on VIC agent modeling. They are comparative indices for scenario planning, not financial forecasts. Actual results depend on real CRM data, media mix, and market conditions.</div>", unsafe_allow_html=True)


with tab2:
    st.markdown("<div class='section-label'>Creative Testing</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#111;font-size:.9rem;margin-bottom:1.5rem;'>Test creative concepts against synthetic VIC panels before campaign launch.</p>",unsafe_allow_html=True)
    rng2 = np.random.default_rng(99)
    concepts = st.text_area("Enter creative concepts (one per line)", "Heritage storytelling\nProduct close-up\nLifestyle aspiration\nCelebrity endorsement", height=100)
    panel_size = st.number_input("VIC panel size", 200, 5000, 1000, 100, key="ct_panel")
    if st.button("Test Concepts", key="ct_run_tab2"):
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
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{best:.0f}%</div><div class='metric-label'>{metric.replace(' (%)','')}</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        fig_ct = go.Figure()
        for metric, color in [("Recall (%)","#111"),("Engagement (%)","#C8D400"),("Purchase Lift (%)","#888"),("Brand Fit (%)","#ccc")]:
            fig_ct.add_trace(go.Bar(name=metric.replace(" (%)",""), x=res_df["Concept"], y=res_df[metric], marker_color=color))
        fig_ct.update_layout(barmode="group", paper_bgcolor="#fff", plot_bgcolor="#fff", height=300,
            font=dict(family="Montserrat",color="#111"), legend=dict(font=dict(size=9)), margin=dict(l=10,r=10,t=20,b=10))
        fig_ct.update_xaxes(tickfont=dict(size=9,color="#111"), gridcolor="#E8E8E4")
        fig_ct.update_yaxes(tickfont=dict(size=9,color="#111"), gridcolor="#E8E8E4")
        st.plotly_chart(fig_ct, use_container_width=True)
        st.markdown(f"<div style='padding:1rem;border-left:3px solid #C8D400;font-size:.88rem;color:#111;'><strong>Winner:</strong> {winner} leads on purchase lift.</div>",unsafe_allow_html=True)
        st.dataframe(res_df.style.format({"Recall (%)":"{:.1f}","Purchase Lift (%)":"{:.1f}","Engagement (%)":"{:.1f}","Brand Fit (%)":"{:.1f}"}),use_container_width=True,hide_index=True)

with tab3:
    st.markdown("<div class='section-label'>Product Launch Simulator</div>",unsafe_allow_html=True)
    pl_col1, pl_col2 = st.columns(2)
    with pl_col1:
        product_name = st.text_input("Product name", "New Collection SS26")
        price_point = st.number_input("Price point (EUR)", 500, 50000, 2500, 500)
        launch_cities = st.multiselect("Launch markets", ALL_CITIES, ALL_CITIES[:3], key="pl_cities")
    with pl_col2:
        exclusivity = st.select_slider("Exclusivity level", ["Mass","Premium","Luxury","Ultra-Luxury"], "Luxury")
        launch_window = st.number_input("Launch window (weeks)", 1, 12, 4, key="pl_weeks")
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
        with c4: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(launch_cities or ['Milano'])}</div><div class='metric-label'>Markets</div></div>",unsafe_allow_html=True)
        fig_pl = go.Figure()
        fig_pl.add_trace(go.Scatter(x=weeks, y=adoption, mode="lines+markers", name="Adoption %",
            line=dict(color="#111",width=2), marker=dict(color="#C8D400",size=8)))
        fig_pl.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=250,
            font=dict(family="Montserrat",color="#111"),margin=dict(l=10,r=10,t=20,b=10),
            xaxis_title="Week",yaxis_title="Adoption (%)")
        fig_pl.update_xaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        fig_pl.update_yaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        st.plotly_chart(fig_pl, use_container_width=True)

with tab4:
    st.markdown("<div class='section-label'>Price Optimisation</div>",unsafe_allow_html=True)
    po_col1, po_col2 = st.columns(2)
    with po_col1:
        current_price = st.number_input("Current price (EUR)", 500, 100000, 3000, 500, key="po_price")
        pr_col1, pr_col2 = st.columns(2)
        with pr_col1: price_min = st.number_input("Price multiplier min", min_value=0.5, max_value=1.5, value=0.7, step=0.1, key="po_min")
        with pr_col2: price_max = st.number_input("Price multiplier max", min_value=0.6, max_value=2.0, value=1.5, step=0.1, key="po_max")
        price_range = (price_min, price_max)
    with po_col2:
        segment = st.selectbox("VIC segment", ["All segments","Ultra-HNWI Collector","Private Client","Aspirational Buyer"], key="po_seg")
        po_cities = st.multiselect("Markets", ALL_CITIES, ALL_CITIES[:3], key="po_cities")
    if st.button("Run Price Model", key="po_run"):
        prices = np.linspace(current_price*price_range[0], current_price*price_range[1], 20)
        elasticity = -1.8 if "Aspirational" in segment else -0.9 if "HNWI" in segment else -1.3
        base_demand = 1000
        demand = [max(0, base_demand * (p/current_price)**elasticity + np.random.normal(0,20)) for p in prices]
        revenue = [p*d for p,d in zip(prices,demand)]
        opt_idx = int(np.argmax(revenue)); opt_price = prices[opt_idx]; opt_rev = revenue[opt_idx]
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {opt_price:,.0f}</div><div class='metric-label'>Optimal price</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value'>{(opt_price/current_price-1)*100:+.0f}%</div><div class='metric-label'>vs current</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {opt_rev/1000:.0f}K</div><div class='metric-label'>Max revenue</div></div>",unsafe_allow_html=True)
        fig_po = go.Figure()
        fig_po.add_trace(go.Scatter(x=list(prices), y=revenue, mode="lines", name="Revenue", line=dict(color="#111",width=2)))
        fig_po.add_vline(x=opt_price, line_dash="dash", line_color="#C8D400", annotation_text=f"Optimal EUR{opt_price:,.0f}", annotation_font_color="#111")
        fig_po.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=250,font=dict(family="Montserrat",color="#111"),margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Price (EUR)",yaxis_title="Revenue (EUR)")
        fig_po.update_xaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        fig_po.update_yaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        st.plotly_chart(fig_po, use_container_width=True)

with tab5:
    st.markdown("<div class='section-label'>Market Segmentation</div>",unsafe_allow_html=True)
    ms_col1, ms_col2 = st.columns(2)
    with ms_col1: ms_cities = st.multiselect("Markets", ALL_CITIES, ALL_CITIES, key="ms_cities")
    with ms_col2: ms_campaign = st.selectbox("Campaign context", list(CAMPAIGN_PARAMS.keys()), format_func=lambda x:CAMPAIGN_PARAMS[x]["label"], key="ms_campaign")
    if st.button("Analyse Segments", key="ms_run"):
        rng_ms = np.random.default_rng(77)
        ms_data = []
        for city in (ms_cities or ALL_CITIES):
            for persona, share, intent, eng in VIC_PERSONAS:
                cf = CAMPAIGN_PARAMS[ms_campaign].get("city_bias", {}).get(city, 1.0)
                vic_count = round(share * 1000 * cf * rng_ms.uniform(0.85, 1.15))
                _bp5 = st.session_state.get("brand_profile") or {}
                _ov5 = (_bp5.get("ego_override") or {}).get(persona, None)
                _brand_boost = 1.15 if _ov5 else 1.0
                buy_r = round(intent * cf * rng_ms.uniform(0.8, 1.2) * _brand_boost * 100, 1)
                ms_data.append({"City": city, "Persona": persona, "VIC Count": vic_count, "Buy Rate (%)": buy_r, "Engagement (%)": round(eng * cf * 100, 1)})
        ms_df = pd.DataFrame(ms_data)
        pivot = ms_df.pivot_table(index="Persona", columns="City", values="Buy Rate (%)", aggfunc="mean").round(1)
        fig_ms = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=[[0,"#FFFFFF"],[0.5,"#888888"],[1,"#000000"]], showscale=True,
            hovertemplate="%{y} x %{x}<br>Buy Rate: %{z:.1f}%<extra></extra>",
            texttemplate="%{z:.0f}", textfont=dict(size=7, family="Montserrat")))
        fig_ms.update_layout(paper_bgcolor="#fff", height=400, font=dict(family="Montserrat",color="#111",size=9), margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_ms, use_container_width=True)
        st.dataframe(ms_df.style.format({"VIC Count":"{:,.0f}","Buy Rate (%)":"{:.1f}","Engagement (%)":"{:.1f}"}),use_container_width=True,hide_index=True)

with tab6:
    st.markdown("<div class='section-label'>Churn Prediction</div>",unsafe_allow_html=True)
    ch_col1, ch_col2 = st.columns(2)
    with ch_col1:
        ch_cities = st.multiselect("Markets", ALL_CITIES, ALL_CITIES[:4], key="ch_cities")
        ch_threshold = st.number_input("Churn risk threshold (%)", 30, 80, 50, 5, key="ch_threshold")
    with ch_col2:
        recency_weight = st.number_input("Recency weight", 0.1, 1.0, 0.5, 0.1, key="ch_recency")
        engagement_weight = st.number_input("Engagement weight", 0.1, 1.0, 0.5, 0.1, key="ch_eng")
    if st.button("Predict Churn", key="ch_run"):
        rng_ch = np.random.default_rng(55)
        ch_data = []
        for i in range(500):
            city = rng_ch.choice(ch_cities or ALL_CITIES[:4])
            persona = VIC_PERSONAS[rng_ch.integers(0, len(VIC_PERSONAS))][0]
            recency = rng_ch.integers(1, 365)
            eng_score = round(rng_ch.beta(3,4)*100, 1)
            _bp6 = st.session_state.get("brand_profile") or {}
            _rd6 = _bp6.get("rd_default","Established")
            _churn_mod = -8 if _rd6=="Legacy" else 5 if _rd6=="New" else 0
            churn_prob = min(100, recency_weight*(recency/365*100) + engagement_weight*(100-eng_score) + rng_ch.normal(0,5) + _churn_mod)
            ltv = round(rng_ch.uniform(2000, 50000), 0)
            ch_data.append({"City":city,"Persona":persona,"Days since purchase":recency,"Engagement (%)":eng_score,"Churn risk (%)":round(churn_prob,1),"LTV (EUR)":ltv})
        ch_df = pd.DataFrame(ch_data)
        at_risk = ch_df[ch_df["Churn risk (%)"] >= ch_threshold]
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(at_risk)}</div><div class='metric-label'>At-risk VICs</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(at_risk)/5:.0f}%</div><div class='metric-label'>Churn rate</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>EUR {at_risk['LTV (EUR)'].sum()/1000:.0f}K</div><div class='metric-label'>Revenue at risk</div></div>",unsafe_allow_html=True)
        fig_ch = go.Figure(go.Scatter(x=ch_df["Days since purchase"], y=ch_df["Churn risk (%)"],
            mode="markers", marker=dict(color=ch_df["Churn risk (%)"], colorscale=[[0,"#E8E8E4"],[0.5,"#888"],[1,"#111"]], size=6, showscale=False),
            text=ch_df["Persona"], hovertemplate="%{text}<br>Days: %{x}<br>Risk: %{y:.1f}%<extra></extra>"))
        fig_ch.add_hline(y=ch_threshold, line_dash="dash", line_color="#C8D400")
        fig_ch.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=280,font=dict(family="Montserrat",color="#111"),margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Days since last purchase",yaxis_title="Churn risk (%)")
        fig_ch.update_xaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        fig_ch.update_yaxes(gridcolor="#E8E8E4",tickfont=dict(size=9,color="#111"))
        st.plotly_chart(fig_ch, use_container_width=True)
        fmt_ch = {"Engagement (%)":"{:.1f}","Churn risk (%)":"{:.1f}","LTV (EUR)":"EUR{:,.0f}"}
        st.dataframe(at_risk.sort_values("Churn risk (%)",ascending=False).head(50).style.format(fmt_ch),use_container_width=True,hide_index=True)

with tab7:
    st.markdown("<div class='section-label'>Brand Perception Tracking</div>",unsafe_allow_html=True)
    bp_col1, bp_col2 = st.columns(2)
    with bp_col1:
        _sb7 = st.session_state.get("_last_brand","")
        _default_brand7 = _sb7 if _sb7 and _sb7 != "Generic Luxury" else "Your Brand"
        bp_brand = st.text_input("Brand name", _default_brand7)
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
        strongest = max(scores, key=scores.get); weakest = min(scores, key=scores.get)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{overall}</div><div class='metric-label'>Brand equity score</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value' style='font-size:1.2rem;'>{strongest}</div><div class='metric-label'>Strongest dimension</div></div>",unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value' style='font-size:1.2rem;'>{weakest}</div><div class='metric-label'>Opportunity area</div></div>",unsafe_allow_html=True)
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatterpolar(r=list(scores.values()), theta=dimensions, fill="toself",
            line_color="#111", fillcolor="rgba(200,212,0,0.15)", name=bp_brand))
        fig_bp.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=8,color="#111"),gridcolor="#E8E8E4"),
            angularaxis=dict(tickfont=dict(size=9,color="#111"),gridcolor="#E8E8E4")),
            paper_bgcolor="#fff", height=350, showlegend=True, font=dict(family="Montserrat",color="#111"), margin=dict(l=40,r=40,t=20,b=20))
        st.plotly_chart(fig_bp, use_container_width=True)
        city_df = pd.DataFrame(city_scores).T.reset_index().rename(columns={"index":"City"})
        fmt_bp = {d:"{:.1f}" for d in dimensions}
        st.dataframe(city_df.style.format(fmt_bp),use_container_width=True,hide_index=True)


with tab8:
    _selected_brand = st.session_state.get("_last_brand", "")
    _brand_color = st.session_state.get("brand_profile", {}).get("color", "#888")
    st.markdown(
        f"<div class='section-label'>VIC Psychographic Engine — TACLA Architecture v3 &nbsp;·&nbsp; "
        f"<span style='color:{_brand_color};'>{_selected_brand}</span></div>",
        unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#555;font-size:.85rem;margin-bottom:1.2rem;'>"
        "Each VIC agent is modeled as a dynamic system of three ego states (Parent, Adult, Child) "
        "with persona-specific Contextual Pattern Memory and an Orchestrator that activates the dominant "
        "state based on campaign trigger and relationship depth.</p>", unsafe_allow_html=True)

    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import random, copy
    random.seed(42)
    np.random.seed(42)

    RD_PROFILES = {
        "New": {"label":"New","color":"#888888","description":"Brand not yet internalized. Emotional aspiration drives engagement.","ego_shift":{"Parent":-0.10,"Adult":+0.05,"Child":+0.05},"purchase_mod":-8,"conflict_mod":+8,"churn_risk":"Low — no relationship to lose","brand_position":"aspirational object"},
        "Established": {"label":"Established","color":"#C8D400","description":"Brand evaluated rationally. VIC compares, benchmarks, negotiates.","ego_shift":{"Parent":+0.00,"Adult":+0.10,"Child":-0.10},"purchase_mod":+5,"conflict_mod":-3,"churn_risk":"Medium — rational exit possible if value perceived as declining","brand_position":"trusted reference"},
        "Legacy": {"label":"Legacy","color":"#111111","description":"Brand internalized as identity marker. VIC is a custodian, not a consumer.","ego_shift":{"Parent":+0.15,"Adult":-0.05,"Child":-0.10},"purchase_mod":+15,"conflict_mod":-10,"churn_risk":"Low but irreversible — if lost, brand is erased from identity script","brand_position":"identity anchor"},
    }

    VIC_PROFILES = {
        "Ultra-HNWI Collector": {"life_script":"I define the standard. Others follow.","driver":"Be Perfect","base":{"Parent":0.65,"Adult":0.25,"Child":0.10},"dominant":"Parent","expected_tx":"Parent","default_rd":"Legacy","patterns":{"Parent":["demands exclusivity proofs","references heritage lineage","corrects brand narratives"],"Adult":["compares provenance data","evaluates investment value","requests authentication"],"Child":["reacts with pride to scarcity signals","feels dismissed by mass messaging"]}},
        "Heritage Loyalist": {"life_script":"Tradition is the only luxury that lasts.","driver":"Be Strong","base":{"Parent":0.58,"Adult":0.28,"Child":0.14},"dominant":"Parent","expected_tx":"Parent","default_rd":"Legacy","patterns":{"Parent":["defends craftsmanship standards","resists innovation framing","values institutional authority"],"Adult":["tracks artisan credentials","verifies material sourcing","reads brand archives"],"Child":["nostalgic response to legacy campaigns","anxiety at modernisation signals"]}},
        "Private Client": {"life_script":"I make informed decisions others can't access.","driver":"Try Hard","base":{"Parent":0.20,"Adult":0.60,"Child":0.20},"dominant":"Adult","expected_tx":"Adult","default_rd":"Established","patterns":{"Parent":["sets personal standards for service level","expects protocol adherence"],"Adult":["price/quality benchmarking","evaluates ROI on experience","reads fine print"],"Child":["excitement at personalised access","frustration at generic treatment"]}},
        "Digital Native HNWI": {"life_script":"I discover before it becomes mainstream.","driver":"Hurry Up","base":{"Parent":0.15,"Adult":0.40,"Child":0.45},"dominant":"Child","expected_tx":"Child","default_rd":"Established","patterns":{"Parent":["brand accountability expectations","sustainability as values signal"],"Adult":["algorithmic research before purchase","cross-platform price check"],"Child":["FOMO activation on drops","shareability as purchase driver","reacts to peer validation"]}},
        "Aspirational Buyer": {"life_script":"One day I will belong here.","driver":"Please Others","base":{"Parent":0.25,"Adult":0.30,"Child":0.45},"dominant":"Child","expected_tx":"Child","default_rd":"New","patterns":{"Parent":["internalised social norms about luxury","guilt at price points"],"Adult":["extensive pre-purchase research","discount sensitivity"],"Child":["emotional response to aspirational imagery","identity projection onto brand"]}},
        "Trend Setter": {"life_script":"I shape culture, not follow it.","driver":"Be Strong","base":{"Parent":0.20,"Adult":0.30,"Child":0.50},"dominant":"Child","expected_tx":"Child","default_rd":"New","patterns":{"Parent":["cultural authority stance","dismisses derivative work"],"Adult":["trend analytics awareness","evaluates cultural capital ROI"],"Child":["spontaneous adoption of novelty","strong aesthetic emotional response"]}},
    }

    TRIGGER_TX_MAP = {
        "Exclusivity":     {"brand_ego":"Parent","label":"Brand speaks: Parent (authority/scarcity)"},
        "Price Hike":      {"brand_ego":"Parent","label":"Brand speaks: Parent (rules/positioning)"},
        "New Product":     {"brand_ego":"Child","label":"Brand speaks: Child (excitement/novelty)"},
        "Heritage Story":  {"brand_ego":"Parent","label":"Brand speaks: Parent (tradition/legacy)"},
        "Sustainability":  {"brand_ego":"Adult","label":"Brand speaks: Adult (facts/accountability)"},
        "Personalisation": {"brand_ego":"Adult","label":"Brand speaks: Adult (rational tailoring)"},
        "Scarcity Drop":   {"brand_ego":"Child","label":"Brand speaks: Child (FOMO/urgency)"},
        "Brand Collab":    {"brand_ego":"Child","label":"Brand speaks: Child (cultural energy)"},
    }

    def transaction_type(brand_ego, expected_tx):
        if brand_ego == expected_tx:
            return "Complementary", "#2D6A2D", "✓"
        return "Crossed", "#C0392B", "✗"

    def compute_ego_activation(base, trigger, persona_name, rd_key):
        w = copy.deepcopy(base)
        brand_ego = TRIGGER_TX_MAP[trigger]["brand_ego"]
        rd_profile = RD_PROFILES[rd_key]
        import streamlit as _st
        _bp = _st.session_state.get("brand_profile") or {}
        _override = _bp.get("ego_override", None)
        if _override and persona_name in _override:
            _ov = _override[persona_name]
            w = {"Parent":_ov.get("Parent",w["Parent"]),"Adult":_ov.get("Adult",w["Adult"]),"Child":_ov.get("Child",w["Child"])}
        trigger_shifts = {
            "Exclusivity":     {"Parent":+0.12,"Adult":-0.05,"Child":-0.07},
            "Price Hike":      {"Parent":+0.08,"Adult":+0.10,"Child":-0.18},
            "New Product":     {"Child":+0.15,"Adult":+0.05,"Parent":-0.20},
            "Heritage Story":  {"Parent":+0.15,"Adult":+0.00,"Child":-0.15},
            "Sustainability":  {"Adult":+0.18,"Parent":-0.05,"Child":-0.13},
            "Personalisation": {"Adult":+0.12,"Child":+0.08,"Parent":-0.20},
            "Scarcity Drop":   {"Child":+0.20,"Adult":-0.05,"Parent":-0.15},
            "Brand Collab":    {"Child":+0.18,"Adult":+0.02,"Parent":-0.20},
        }
        for ego, delta in trigger_shifts[trigger].items():
            w[ego] = max(0.05, min(0.90, w[ego] + delta))
        for ego, delta in rd_profile["ego_shift"].items():
            w[ego] = max(0.04, min(0.92, w[ego] + delta))
        total = sum(w.values()); w = {k:v/total for k,v in w.items()}
        noise = {"Parent":0.04,"Adult":0.02,"Child":0.05}
        for ego in w: w[ego] = max(0.04, w[ego] + random.gauss(0, noise[ego]))
        total = sum(w.values()); w = {k:v/total for k,v in w.items()}
        dominant = max(w, key=w.get)
        conflict = round(100*(1-max(w.values())) + rd_profile["conflict_mod"], 1)
        conflict = max(5.0, min(90.0, conflict))
        _vic_exp = _VIC_PROFILES_ACTIVE.get(persona_name, VIC_PROFILES.get(persona_name, {"expected_tx":"Child"})).get("expected_tx","Child")
        tx_type, _, _ = transaction_type(brand_ego, _vic_exp)
        base_prob = w[dominant]*100
        tx_bonus = 12 if tx_type=="Complementary" else -15
        rd_bonus = rd_profile["purchase_mod"]
        purchase_prob = round(min(95, max(5, base_prob+tx_bonus+rd_bonus+random.gauss(0,3))), 1)
        return w, dominant, conflict, purchase_prob


    # ── GEN Z SELECTOR ───────────────────────────────────────────────────────
    GEN_Z_MACRO_OPTIONS = ["Standard VIC archetypes", "Gen Z Fashionista", "Gen Z Classic"]
    genz_macro = st.selectbox("Gen Z segment (optional)", GEN_Z_MACRO_OPTIONS, key="genz_macro")
    _is_genz = genz_macro != "Standard VIC archetypes"
    if _is_genz:
        _gz_subtypes = ["Centurion", "Cultural Architect", "Entry Ritualist", "Paradox Buyer"]
        genz_subtype = st.selectbox("Psychological sub-type", _gz_subtypes, key="genz_subtype")
        _gz_regions_map = {
            "EU - St. Tropez":"EU-StTropez","EU - Mykonos":"EU-Mykonos",
            "EU - Portofino":"EU-Portofino","EU - Taormina":"EU-Taormina",
            "EU - St. Moritz":"EU-StMoritz","EU - Capri":"EU-Capri",
            "EU - Courchevel":"EU-Courchevel","EU - Forte dei Marmi":"EU-ForteMarmi",
            "EU - Porto Cervo":"EU-PortoCervo","EU - Ibiza":"EU-Ibiza",
            "US":"US",
            "China - Tier 1 (Shanghai/Beijing/Shenzhen)":"China-T1",
            "China - Tier 2 (Chengdu/Hangzhou/Nanjing)":"China-T2",
            "China - Tier 3 (Emerging cities)":"China-T3",
            "Middle East":"ME","Japan":"Japan","South Korea":"South Korea",
        }
        genz_region_label = st.selectbox("Region / Destination", list(_gz_regions_map.keys()), key="genz_region")
        genz_region_key = _gz_regions_map[genz_region_label]
        _macro_short = "Fashionista" if "Fashionista" in genz_macro else "Classic"
        _gz_key = f"Gen Z \u2014 {_macro_short} \u203a {genz_subtype} \u203a {genz_region_key}"
        _gz_data = GEN_Z_PROFILES.get(_gz_key)
        if _gz_data:
            _gb = {"Parent":_gz_data["Parent"],"Adult":_gz_data["Adult"],"Child":_gz_data["Child"]}
            _dom = max(_gb, key=_gb.get)
            _ec = {"Parent":"#111","Adult":"#C8D400","Child":"#888"}[_dom]
            _drv = "Hurry Up" if _gz_data["Child"]>0.5 else ("Be Perfect" if _gz_data["Parent"]>0.3 else "Try Hard")
            _etx = "Child" if _gz_data["Child"]>0.5 else ("Parent" if _gz_data["Parent"]>0.3 else "Adult")
            _gz_persona_name = f"Gen Z {_macro_short} - {genz_subtype}"
            st.markdown(
                f"<div style='margin:.6rem 0 1rem;padding:.8rem 1.2rem;background:#F5F5F3;"
                f"border-left:3px solid {_ec};font-size:.78rem;color:#111;line-height:1.8;'>"
                f"<strong>{_gz_key}</strong><br>"
                f"Life script: <em>\"{_gz_data['life_script']}\"</em><br>"
                f"Parent <strong>{_gz_data['Parent']:.0%}</strong> &middot; "
                f"Adult <strong>{_gz_data['Adult']:.0%}</strong> &middot; "
                f"Child <strong>{_gz_data['Child']:.0%}</strong> &middot; "
                f"Dominant: <strong style='color:{_ec};'>{_dom}</strong><br>"
                f"Conflict base: <strong>{_gz_data.get('conflict',45)}</strong> &middot; "
                f"Rel. Depth: <strong>{_gz_data.get('rd','New')}</strong><br>"
                f"<span style='color:#2D6A2D;'>Top: {', '.join(_gz_data.get('trigger_top',[]))}</span><br>"
                f"<span style='color:#C0392B;'>Null: {', '.join(_gz_data.get('trigger_null',[]))}</span>"
                f"</div>", unsafe_allow_html=True)
            _GZ_EXTRA = {
                _gz_persona_name: {
                    "life_script": _gz_data["life_script"],
                    "driver":      _drv,
                    "base":        _gb,
                    "dominant":    _dom,
                    "expected_tx": _etx,
                    "default_rd":  _gz_data.get("rd","New"),
                    "patterns": {
                        "Parent":["anchors to established codes","resists generic messaging","evaluates cultural authenticity"],
                        "Adult": ["researches before committing","evaluates value proposition critically","benchmarks across alternatives"],
                        "Child": ["responds to cultural moment activation","FOMO-triggered engagement","identity-driven impulse"],
                    },
                }
            }
        else:
            st.warning(f"Profile not found: {_gz_key}")
            _GZ_EXTRA = {}
    else:
        _GZ_EXTRA = {}
    _VIC_PROFILES_ACTIVE = {**VIC_PROFILES, **_GZ_EXTRA}
    st.markdown("<hr style='border-color:#E8E8E4;margin:.5rem 0 1rem;'>", unsafe_allow_html=True)
    # ── END GEN Z SELECTOR ───────────────────────────────────────────────────

    # ── UI CONTROLS ───────────────────────────────────────────────────────────
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 2])
    with col_ctrl1:
        tc_trigger = st.selectbox("Campaign Trigger", list(TRIGGER_TX_MAP.keys()), key="tc_trigger_v3")
    with col_ctrl2:
        rd_selected = st.selectbox("Relationship Depth", list(RD_PROFILES.keys()), index=1, key="rd_selector")
    with col_ctrl3:
        rd_info = RD_PROFILES[rd_selected]
        rd_html = ("<div style='margin-top:1.6rem;padding:.55rem 1rem;background:#F5F5F3;border-left:3px solid " +
                   rd_info['color'] + ";font-size:.78rem;color:#111;line-height:1.6;'><strong>" +
                   rd_info['label'] + "</strong> \u2014 " + rd_info['description'] +
                   " Brand position: <em>" + rd_info['brand_position'] + "</em>. Churn risk: <em>" +
                   rd_info['churn_risk'] + "</em>.</div>")
        st.markdown(rd_html, unsafe_allow_html=True)
    brand_ego_label = TRIGGER_TX_MAP[tc_trigger]["label"]
    st.markdown("<div style='margin-bottom:1rem;padding:.5rem 1rem;background:#F5F5F3;border-left:3px solid #111;font-size:.78rem;color:#555;'>" +
                brand_ego_label + " &nbsp;&middot;&nbsp; Relationship Depth modifies ego state baseline independently of CLV.</div>",
                unsafe_allow_html=True)

    # ── COMPUTE ───────────────────────────────────────────────────────────────
    rows = []
    for persona, profile in _VIC_PROFILES_ACTIVE.items():
        w, dominant, conflict, purchase_prob = compute_ego_activation(profile["base"], tc_trigger, persona, rd_selected)
        brand_ego = TRIGGER_TX_MAP[tc_trigger]["brand_ego"]
        tx_type, tx_color, tx_symbol = transaction_type(brand_ego, profile["expected_tx"])
        rows.append({
            "Persona": persona, "Driver": profile["driver"], "Rel. Depth": rd_selected,
            "Parent (%)": round(w["Parent"]*100,1), "Adult (%)": round(w["Adult"]*100,1), "Child (%)": round(w["Child"]*100,1),
            "Dominant Ego State": dominant, "Internal Conflict": conflict,
            "Purchase Probability (%)": purchase_prob, "Transaction Type": tx_type,
            "TX Color": tx_color, "Expected TX": profile["expected_tx"],
            "Active Pattern": random.choice(profile["patterns"][dominant]),
        })
    tc_df = pd.DataFrame(rows)

    avg_pp = tc_df["Purchase Probability (%)"].mean()
    avg_conf = tc_df["Internal Conflict"].mean()
    comp_count = len(tc_df[tc_df["Transaction Type"]=="Complementary"])
    total_count = len(tc_df)
    align_pct = round(comp_count/total_count*100)
    banner_color = "#2D6A2D" if align_pct>=50 else "#C0392B"

    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown("<div style='padding:.8rem 1rem;background:#F5F5F3;border-top:3px solid " + rd_info['color'] +
                    ";text-align:center;'><div style='font-size:.55rem;color:#888;text-transform:uppercase;letter-spacing:.08em;'>Avg Purchase Probability</div>" +
                    "<div style='font-size:1.6rem;font-weight:700;color:#111;'>" + str(round(avg_pp)) + "%</div>" +
                    "<div style='font-size:.7rem;color:#555;'>at " + rd_selected + " depth</div></div>", unsafe_allow_html=True)
    with col_b2:
        st.markdown("<div style='padding:.8rem 1rem;background:#F5F5F3;border-top:3px solid #C8D400;text-align:center;'>" +
                    "<div style='font-size:.55rem;color:#888;text-transform:uppercase;letter-spacing:.08em;'>Transaction Alignment</div>" +
                    "<div style='font-size:1.6rem;font-weight:700;color:" + banner_color + ";'>" + str(align_pct) + "%</div>" +
                    "<div style='font-size:.7rem;color:#555;'>" + str(comp_count) + "/" + str(total_count) + " complementary</div></div>", unsafe_allow_html=True)
    with col_b3:
        st.markdown("<div style='padding:.8rem 1rem;background:#F5F5F3;border-top:3px solid #888;text-align:center;'>" +
                    "<div style='font-size:.55rem;color:#888;text-transform:uppercase;letter-spacing:.08em;'>Avg Internal Conflict</div>" +
                    "<div style='font-size:1.6rem;font-weight:700;color:#111;'>" + str(round(avg_conf)) + "%</div>" +
                    "<div style='font-size:.7rem;color:#555;'>portfolio mean</div></div>", unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("<div class='section-label'>Ego State Distribution by VIC</div>", unsafe_allow_html=True)
        fig_bar = go.Figure()
        colors_ego = {"Parent":"#111111","Adult":"#C8D400","Child":"#888888"}
        for ego in ["Parent","Adult","Child"]:
            fig_bar.add_trace(go.Bar(name=ego, x=tc_df["Persona"], y=tc_df[ego+" (%)"], marker_color=colors_ego[ego], marker_line_width=0))
        fig_bar.update_layout(barmode="stack", paper_bgcolor="#fff", plot_bgcolor="#fff", height=280,
            margin=dict(l=10,r=10,t=10,b=80), font=dict(family="Montserrat",color="#111",size=9),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=8)),
            xaxis=dict(tickangle=-30,tickfont=dict(size=7)), yaxis=dict(gridcolor="#E8E8E4",ticksuffix="%"))
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_c2:
        st.markdown("<div class='section-label'>Conflict vs Purchase Probability</div>", unsafe_allow_html=True)
        fig_scatter = go.Figure()
        for _, row in tc_df.iterrows():
            msym = "circle" if row["Transaction Type"]=="Complementary" else "x"
            fig_scatter.add_trace(go.Scatter(
                x=[row["Internal Conflict"]], y=[row["Purchase Probability (%)"]],
                mode="markers+text",
                marker=dict(color=row["TX Color"],size=10,symbol=msym,line=dict(width=1.5,color=row["TX Color"])),
                text=[row["Persona"].split()[0]], textposition="top center", textfont=dict(size=7),
                showlegend=False,
                name=row["Persona"]))
        for label, color, sym in [("Complementary","#2D6A2D","circle"),("Crossed","#C0392B","x")]:
            fig_scatter.add_trace(go.Scatter(x=[None],y=[None],mode="markers",marker=dict(color=color,size=8,symbol=sym),name=label,showlegend=True))
        fig_scatter.update_layout(paper_bgcolor="#fff",plot_bgcolor="#fff",height=280,margin=dict(l=10,r=10,t=10,b=10),
            font=dict(family="Montserrat",color="#111",size=9),
            xaxis=dict(title="Internal Conflict (%)",gridcolor="#E8E8E4",tickfont=dict(size=8)),
            yaxis=dict(title="Purchase Probability (%)",gridcolor="#E8E8E4",tickfont=dict(size=8)),
            legend=dict(font=dict(size=8),orientation="h",yanchor="bottom",y=1.02))
        st.plotly_chart(fig_scatter, use_container_width=True)

    crossed_df = tc_df[tc_df["Transaction Type"]=="Crossed"]
    if not crossed_df.empty:
        st.markdown("<div class='section-label'>Crossed Transaction Analysis</div>", unsafe_allow_html=True)
        brand_ego_now = TRIGGER_TX_MAP[tc_trigger]["brand_ego"]
        for _, xrow in crossed_df.iterrows():
            rd_note = (" At Legacy depth: elevated churn risk." if rd_selected=="Legacy"
                       else " At New depth: missed acquisition signal." if rd_selected=="New" else "")
            xhtml = ("<div style='padding:.8rem 1rem;margin-bottom:.5rem;border-left:3px solid #C0392B;background:#FDECEA;font-size:.82rem;color:#111;'>" +
                     "<strong>" + xrow["Persona"] + "</strong> [" + rd_selected + "] \u2014 " +
                     "Campaign speaks <em>" + brand_ego_now + "</em> / VIC expects <em>" + xrow["Expected TX"] + "</em>. " +
                     "Active pattern: <em>" + xrow["Active Pattern"] + "</em>. " +
                     "Purchase probability: <strong>" + str(xrow["Purchase Probability (%)"]) + "%</strong>." + rd_note +
                     "<br><span style='color:#C0392B;font-size:.75rem;'>Reframe toward " + xrow["Expected TX"] + " register.</span></div>")
            st.markdown(xhtml, unsafe_allow_html=True)
    else:
        st.markdown("<div style='padding:.8rem 1rem;border-left:3px solid #2D6A2D;background:#EAF5EA;font-size:.82rem;color:#111;'>" +
                    "All VIC receive complementary transactions at " + rd_selected + " depth.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Strategic Readout</div>", unsafe_allow_html=True)
    top_persona = tc_df.loc[tc_df["Purchase Probability (%)"].idxmax(),"Persona"]
    parent_pct = round(len(tc_df[tc_df["Dominant Ego State"]=="Parent"])/len(tc_df)*100)
    adult_pct  = round(len(tc_df[tc_df["Dominant Ego State"]=="Adult"])/len(tc_df)*100)
    child_pct  = round(len(tc_df[tc_df["Dominant Ego State"]=="Child"])/len(tc_df)*100)
    rd_strategic = {
        "New": "New depth suppresses Parent and amplifies Child \u2014 emotional entry points over authority registers.",
        "Established": "Established depth activates Adult \u2014 rational-register messaging outperforms emotional triggers.",
        "Legacy": "Legacy depth shifts toward Parent \u2014 heritage and exclusivity triggers resonate most.",
    }
    conflict_read = ("High conflict signals ego state ambivalence." if avg_conf>35 else "Low conflict indicates clear ego state dominance.")
    readout_html = ("<div style='padding:1rem 1.2rem;border-left:3px solid #C8D400;font-size:.88rem;color:#111;line-height:1.9;'>" +
                    "Under a <strong>" + tc_trigger + "</strong> trigger at <strong>" + rd_selected + "</strong> depth: " +
                    "<strong>" + str(parent_pct) + "%</strong> Parent &middot; <strong>" + str(adult_pct) + "%</strong> Adult &middot; <strong>" + str(child_pct) + "%</strong> Child dominant. " +
                    "Avg conflict: <strong>" + str(round(avg_conf)) + "%</strong>. " + conflict_read + " " +
                    "Highest conversion: <strong>" + top_persona + "</strong>. " +
                    "Alignment: <strong>" + str(align_pct) + "%</strong>. " + rd_strategic[rd_selected] + "</div>")
    st.markdown(readout_html, unsafe_allow_html=True)

    st.markdown("<div class='section-label'>VIC Psychographic Data</div>", unsafe_allow_html=True)
    display_df = tc_df[["Persona","Driver","Rel. Depth","Dominant Ego State","Transaction Type",
                         "Parent (%)","Adult (%)","Child (%)","Internal Conflict","Purchase Probability (%)","Active Pattern"]].copy()
    def style_tx(val):
        if val=="Complementary": return "color:#2D6A2D;font-weight:600"
        if val=="Crossed": return "color:#C0392B;font-weight:600"
        return ""
    fmt_t8 = {"Parent (%)":"{:.1f}","Adult (%)":"{:.1f}","Child (%)":"{:.1f}","Internal Conflict":"{:.1f}","Purchase Probability (%)":"{:.1f}"}
    st.dataframe(display_df.style.format(fmt_t8).map(style_tx, subset=["Transaction Type"]), use_container_width=True, height=280, hide_index=True)
    st.markdown("<div style='margin-top:1.8rem;padding:1.2rem 1.4rem;background:#F5F5F3;font-size:.55rem;color:#888;line-height:2;'>"
                "<strong style='color:#111;text-transform:uppercase;font-size:.5rem;letter-spacing:.1em;'>Methodology \u2014 TACLA Architecture v3 + Gen Z Extension v16</strong><br><br>"
                "Each VIC agent modeled across Parent/Adult/Child ego states with Relationship Depth modulation. "
                "Gen Z Extension: 136 profiles across 2 macro x 4 sub-types x 17 regions. "
                "References: Berne (1961, 1964, 1972). Stewart &amp; Joines (2012). Dress for Good AI Studio (2025).</div>",
                unsafe_allow_html=True)


with tab9:
    _fg_brand = st.session_state.get("_last_brand", "")
    _fg_bp = st.session_state.get("brand_profile") or {}
    _fg_brand_note = _fg_bp.get("note", "")
    st.markdown("<div class='section-label'>VIC Focus Group \u2014 Synthetic Qualitative Research</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;font-size:.85rem;margin-bottom:1.2rem;'>Simulate a qualitative interview with a synthetic VIC agent using the TACLA ego state framework.</p>", unsafe_allow_html=True)
    fg_col1, fg_col2 = st.columns(2)
    with fg_col1:
        fg_persona = st.selectbox("VIC Archetype", [p[0] for p in VIC_PERSONAS], key="fg_persona")
        fg_trigger = st.selectbox("Campaign trigger", list(TRIGGER_TX_MAP.keys()), key="fg_trigger")
    with fg_col2:
        fg_rd = st.selectbox("Relationship Depth", ["New","Established","Legacy"], index=1, key="fg_rd")
        fg_language = st.selectbox("Response language", ["English","Italian","French","Arabic","Japanese","Mandarin"], key="fg_language")
    fg_question = st.text_area("Your question to the VIC", placeholder="e.g. What do you think about the new Gucci collection?", height=80, key="fg_question")
    if st.button("Run Focus Group", key="fg_run"):
        if not fg_question.strip():
            st.warning("Please enter a question.")
        else:
            _ego_profiles = {
                "Ultra-HNWI Collector": {"Parent":0.65,"Adult":0.25,"Child":0.10,"life_script":"I deserve the best \u2014 status is everything"},
                "Brand Ambassador": {"Parent":0.30,"Adult":0.35,"Child":0.35,"life_script":"I define trends before they exist"},
                "Aspirational Buyer": {"Parent":0.20,"Adult":0.30,"Child":0.50,"life_script":"I want to belong to a world I admire"},
                "Trend Setter Influencer": {"Parent":0.10,"Adult":0.30,"Child":0.60,"life_script":"I live for the new and the now"},
                "Private Client": {"Parent":0.40,"Adult":0.55,"Child":0.05,"life_script":"I value discretion and craftsmanship above all"},
                "Digital Native": {"Parent":0.10,"Adult":0.45,"Child":0.45,"life_script":"I research everything before I commit"},
                "Heritage Loyalist": {"Parent":0.70,"Adult":0.25,"Child":0.05,"life_script":"I buy legacy, not fashion"},
                "Gulf HNWI": {"Parent":0.55,"Adult":0.30,"Child":0.15,"life_script":"Luxury is my cultural language"},
                "Asia Pacific VIC": {"Parent":0.45,"Adult":0.40,"Child":0.15,"life_script":"I invest in brands that signal global sophistication"},
            }
            _p = _ego_profiles.get(fg_persona, _ego_profiles["Private Client"])
            _rd_desc = RD_PROFILES.get(fg_rd, {}).get("description", "")
            _dominant = max(_p, key=lambda k: _p[k] if k in ["Parent","Adult","Child"] else 0)
            _dominant_map = {
                "Parent": "values, status, tradition \u2014 responds to heritage, authority, exclusivity signals",
                "Adult": "rational, analytical \u2014 responds to value proposition, quality proof, transparent information",
                "Child": "emotional, impulsive \u2014 responds to desire, FOMO, aesthetic excitement, social validation"
            }
            _brand_context = "Brand: " + _fg_brand + ". " + _fg_brand_note if _fg_brand else "Generic luxury brand"
            _trigger_desc = TRIGGER_TX_MAP.get(fg_trigger, {}).get("label", fg_trigger)
            system_prompt = ("You are a synthetic VIC (Very Important Client) participating in a luxury brand focus group.\n\n"
                "You are: " + fg_persona + "\nYour life script: " + _p.get("life_script","") + "\n"
                "Your dominant ego state: " + _dominant + " \u2014 " + _dominant_map.get(_dominant,"") + "\n"
                "Ego state weights \u2014 Parent: " + str(round(_p["Parent"]*100)) + "%, Adult: " + str(round(_p["Adult"]*100)) + "%, Child: " + str(round(_p["Child"]*100)) + "%\n"
                "Your relationship with the brand: " + fg_rd + " \u2014 " + _rd_desc + "\n"
                "Campaign trigger context: " + fg_trigger + " \u2014 " + _trigger_desc + "\n"
                + _brand_context + "\n\n"
                "Respond in first person as this VIC archetype. Stay in character throughout.\n"
                "Respond in " + fg_language + ".\n"
                "Be specific, authentic, and nuanced. Length: 3-5 sentences. Senior luxury consumer voice.")
            with st.spinner("Generating VIC response..."):
                try:
                    import requests as _req
                    try:
                        _api_key = st.secrets["ANTHROPIC_API_KEY"]
                    except Exception as _ke:
                        st.error("Secret not found: " + str(_ke) + ". Add ANTHROPIC_API_KEY to Streamlit secrets.")
                        st.stop()
                    _resp = _req.post("https://api.anthropic.com/v1/messages",
                        headers={"Content-Type":"application/json","x-api-key":_api_key,"anthropic-version":"2023-06-01"},
                        json={"model":"claude-sonnet-4-5","max_tokens":1000,"system":system_prompt,"messages":[{"role":"user","content":fg_question}]},
                        timeout=30)
                    _data = _resp.json()
                    if _data.get("content"):
                        _answer = _data["content"][0]["text"]
                    else:
                        _err = _data.get("error", {})
                        _answer = "API error " + str(_resp.status_code) + ": " + _err.get("message", str(_data))
                    st.markdown("<div style='background:#F5F5F3;border-left:3px solid #C8D400;padding:1.2rem 1.4rem;margin-top:1rem;'>" +
                                "<div style='font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:#999;margin-bottom:.6rem;'>" +
                                fg_persona + " \xb7 " + fg_rd + " \xb7 " + fg_trigger + " \xb7 " + fg_language + "</div>" +
                                "<div style='font-size:.92rem;font-family:Montserrat,sans-serif;color:#111;line-height:1.8;'>" + _answer + "</div></div>",
                                unsafe_allow_html=True)
                    eg_col1, eg_col2, eg_col3 = st.columns(3)
                    for col, state, val, color in [(eg_col1,"Parent",_p["Parent"],"#111"),(eg_col2,"Adult",_p["Adult"],"#555"),(eg_col3,"Child",_p["Child"],"#C8D400")]:
                        with col:
                            st.markdown("<div style='background:#fff;border:1px solid #E8E8E4;padding:.8rem 1rem;text-align:center;'>" +
                                        "<div style='font-family:Montserrat;font-size:1.6rem;font-weight:700;color:" + color + ";line-height:1;'>" + str(round(val*100)) + "%</div>" +
                                        "<div style='font-family:Montserrat;font-size:.55rem;letter-spacing:.1em;text-transform:uppercase;color:#999;margin-top:.4rem;'>" + state + " ego state</div></div>",
                                        unsafe_allow_html=True)
                    st.markdown("<div style='font-size:.65rem;color:#bbb;margin-top:.8rem;'>Synthetic VIC response \u2014 TACLA psychographic engine. Not a real consumer. Directional insight only.</div>", unsafe_allow_html=True)
                except Exception as _e:
                    import traceback
                    st.error("API error: " + str(_e))
                    st.code(traceback.format_exc())

with tab10:
    _ct_brand = st.session_state.get("_last_brand", "")
    _ct_bp = st.session_state.get("brand_profile") or {}
    _ct_note = _ct_bp.get("note", "")
    st.markdown("<div class='section-label'>Claims Test \u2014 Synthetic VIC Panel</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;font-size:.85rem;margin-bottom:1.2rem;'>Test up to 3 campaign headlines against a synthetic VIC panel scored by purchase intent, emotional resonance, and ego state alignment.</p>", unsafe_allow_html=True)
    ct_col1, ct_col2 = st.columns(2)
    with ct_col1:
        ct_campaign = st.selectbox("Campaign context", options=list(CAMPAIGN_PARAMS.keys()), format_func=lambda x:CAMPAIGN_PARAMS[x]["label"], key="ct_campaign")
    with ct_col2:
        ct_rd = st.selectbox("Relationship Depth", ["New","Established","Legacy"], index=1, key="ct_rd")
    ct_lang = st.selectbox("Response language", ["English","Italian","French","Arabic","Japanese"], key="ct_lang")
    st.markdown("<div style='margin:.8rem 0 .4rem;font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:#666;'>Claims / Headlines</div>", unsafe_allow_html=True)
    claim1 = st.text_input("Claim 1", placeholder="e.g. Crafted for those who need no introduction", key="claim1")
    claim2 = st.text_input("Claim 2", placeholder="e.g. The collection that defies the obvious", key="claim2")
    claim3 = st.text_input("Claim 3", placeholder="e.g. Bold. Unapologetic. Yours.", key="claim3")
    claims = [c for c in [claim1, claim2, claim3] if c.strip()]
    if st.button("Run Claims Test", key="ct_run"):
        if not claims:
            st.warning("Enter at least one claim.")
        else:
            import numpy as np, pandas as pd, requests as _req, json, re
            EGO_CT = {
                "Ultra-HNWI Collector":{"Parent":0.65,"Adult":0.25,"Child":0.10},
                "Brand Ambassador":{"Parent":0.30,"Adult":0.35,"Child":0.35},
                "Aspirational Buyer":{"Parent":0.20,"Adult":0.30,"Child":0.50},
                "Trend Setter Influencer":{"Parent":0.10,"Adult":0.30,"Child":0.60},
                "Private Client":{"Parent":0.40,"Adult":0.55,"Child":0.05},
                "Digital Native":{"Parent":0.10,"Adult":0.45,"Child":0.45},
                "Heritage Loyalist":{"Parent":0.70,"Adult":0.25,"Child":0.05},
                "Gulf HNWI":{"Parent":0.55,"Adult":0.30,"Child":0.15},
                "Asia Pacific VIC":{"Parent":0.45,"Adult":0.40,"Child":0.15},
            }
            RD_MULT = {"New":0.85,"Established":1.0,"Legacy":1.15}
            rd_mult = RD_MULT.get(ct_rd, 1.0)
            _brand_ov = _ct_bp.get("ego_override") or {}
            results = []
            with st.spinner("Scoring claims against VIC panel..."):
                for claim in claims:
                    for persona, share, base_intent, base_eng in VIC_PERSONAS:
                        ep = EGO_CT.get(persona, {"Parent":0.33,"Adult":0.34,"Child":0.33})
                        if persona in _brand_ov:
                            ep = {**ep, **_brand_ov[persona]}
                        dominant = max(["Parent","Adult","Child"], key=lambda k: ep.get(k,0))
                        score_prompt = ("You are evaluating a luxury campaign claim for a specific consumer archetype.\n"
                            "Brand: " + (_ct_brand if _ct_brand else "Premium luxury brand") + "\n"
                            "Claim: \"" + claim + "\"\n"
                            "Archetype: " + persona + " | Dominant ego state: " + dominant + " (" + str(round(ep.get(dominant,0.33)*100)) + "%)\n"
                            "Relationship depth: " + ct_rd + " | Campaign: " + CAMPAIGN_PARAMS[ct_campaign]["label"] + "\n\n"
                            "Score 0-100 each. Respond ONLY with JSON:\n"
                            "{\"purchase_intent\":<0-100>,\"emotional_resonance\":<0-100>,\"ego_alignment\":<0-100>,\"reaction\":\"<8 words in " + ct_lang + ">\"}")
                        try:
                            _api_key_ct = st.secrets.get("ANTHROPIC_API_KEY", "")
                            _resp = _req.post("https://api.anthropic.com/v1/messages",
                                headers={"Content-Type":"application/json","x-api-key":_api_key_ct,"anthropic-version":"2023-06-01"},
                                json={"model":"claude-sonnet-4-20250514","max_tokens":150,"messages":[{"role":"user","content":score_prompt}]})
                            _text = _resp.json().get("content",[{}])[0].get("text","{}")
                            _m = re.search(r'\{.*\}', _text, re.DOTALL)
                            _s = json.loads(_m.group()) if _m else {}
                        except:
                            _s = {}
                        pi_score = _s.get("purchase_intent",50); er_score = _s.get("emotional_resonance",50); ea_score = _s.get("ego_alignment",50)
                        results.append({"Claim":claim[:35]+"..." if len(claim)>35 else claim,"Persona":persona,
                            "Purchase Intent":round(pi_score,0),"Emotional Resonance":round(er_score,0),"Ego Alignment":round(ea_score,0),
                            "Reaction":_s.get("reaction","\u2014"),"Weighted":round((pi_score+er_score+ea_score)/3*share*rd_mult,2)})
            df_ct = pd.DataFrame(results)
            summary_ct = df_ct.groupby("Claim").agg(Intent=("Purchase Intent","mean"),Resonance=("Emotional Resonance","mean"),Ego=("Ego Alignment","mean"),Score=("Weighted","sum")).reset_index().sort_values("Score",ascending=False).reset_index(drop=True)
            st.markdown("<br><div class='section-label'>Claim ranking</div>", unsafe_allow_html=True)
            medals = ["\U0001f947","\U0001f948","\U0001f949"]
            for idx, row in summary_ct.iterrows():
                border = "3px solid #C8D400" if idx==0 else "1px solid #E8E8E4"
                medal = medals[idx] if idx<3 else ""
                st.markdown("<div style='border:" + border + ";padding:1rem 1.2rem;margin-bottom:.6rem;'>" +
                            "<div style='font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;color:#999;'>" + medal + " Claim</div>" +
                            "<div style='font-size:.95rem;font-weight:600;color:#111;margin:.3rem 0 .6rem;'>&ldquo;" + row["Claim"] + "&rdquo;</div>" +
                            "<div style='display:flex;gap:2rem;font-size:.75rem;color:#555;'>" +
                            "<span>Intent <strong style='color:#111'>" + str(round(row["Intent"])) + "</strong></span>" +
                            "<span>Resonance <strong style='color:#111'>" + str(round(row["Resonance"])) + "</strong></span>" +
                            "<span>Score <strong style='color:#C8D400'>" + str(round(row["Score"],1)) + "</strong></span></div></div>",
                            unsafe_allow_html=True)
            st.dataframe(df_ct[["Persona","Claim","Purchase Intent","Emotional Resonance","Ego Alignment","Reaction"]], use_container_width=True, hide_index=True)
            st.markdown("<div style='font-size:.65rem;color:#bbb;margin-top:.8rem;'>Synthetic scoring \u2014 directional proxy only. Validate against real consumer data before go-to-market decisions.</div>", unsafe_allow_html=True)
