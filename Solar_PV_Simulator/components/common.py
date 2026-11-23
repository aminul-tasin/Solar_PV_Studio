from pathlib import Path
import streamlit as st
import pandas as pd
from components.styles import DARK_CSS,LIGHT_CSS
from config import PanelParams
from pv_model import SingleDiodePV
from analysis import prepare_weather,add_pv_performance

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
SYNTHETIC=DATA/"synthetic"
HISTORICAL=DATA/"historical"
IMPORTED=DATA/"imports"

def theme():
    st.markdown(DARK_CSS if st.session_state.get("theme","Dark")=="Dark" else LIGHT_CSS,unsafe_allow_html=True)

def datasets():
    for p in [SYNTHETIC,HISTORICAL,IMPORTED]: p.mkdir(parents=True,exist_ok=True)
    return {f"Synthetic / {p.stem.title()}":p for p in sorted(SYNTHETIC.glob("*.csv"))} | \
           {f"Historical / {p.stem}":p for p in sorted(HISTORICAL.glob("*.csv"))} | \
           {f"Imported / {p.stem}":p for p in sorted(IMPORTED.glob("*.csv"))}

@st.cache_data
def read_csv(path,mtime): return pd.read_csv(path)

def context():
    from dataset_generator import generate_all
    if not list(SYNTHETIC.glob("*.csv")): generate_all(SYNTHETIC)
    opts=datasets()
    choice=st.session_state.get("dataset","Synthetic / Sunny")
    path=opts.get(choice,next(iter(opts.values())))
    weather=prepare_weather(read_csv(str(path),path.stat().st_mtime_ns))
    if st.session_state.get("panel_kind")=="Custom":
        panel=PanelParams(name="Custom module",p_rated=st.session_state.get("rated",250),
          voc=st.session_state.get("voc",37.5),isc=st.session_state.get("isc",8.7),
          vmp=st.session_state.get("vmp",30.5),imp=st.session_state.get("imp",8.2),
          area=st.session_state.get("area",1.65))
    else: panel=PanelParams()
    return {"weather":weather,"pv":SingleDiodePV(panel),"panel":panel,"dataset":choice,"path":path}

def header(title,subtitle):
    st.markdown(f'<div class="eyebrow">SOLAR PV STUDIO / ENGINEERING WORKSPACE</div><div class="page-title">{title}</div><div class="subtle">{subtitle}</div>',unsafe_allow_html=True)
    st.write("")

def perf(ctx): return add_pv_performance(ctx["pv"],ctx["weather"])

def plot_theme(fig,height=390):
    fig.update_layout(template="plotly_dark" if st.session_state.get("theme","Dark")=="Dark" else "plotly_white",
      height=height,margin=dict(l=15,r=15,t=55,b=20),paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",hovermode="x unified",
      legend=dict(orientation="h",y=1.02,x=0))
    return fig
