import streamlit as st
from components.common import theme,datasets
from dataset_generator import generate_all
from pathlib import Path

st.set_page_config(page_title="Solar PV Studio",page_icon="☀️",layout="wide",initial_sidebar_state="expanded")
ROOT=Path(__file__).resolve().parent
generate_all(ROOT/"data"/"synthetic")
defaults={"theme":"Dark","dataset":"Synthetic / Sunny","panel_kind":"250 W Illustrative",
          "load_r":20.0,"converter_eta":95,"mppt_step":0.35}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v

with st.sidebar:
    st.markdown('<div style="font-size:29px">☀️</div><div class="brand">SOLAR PV STUDIO</div><div class="brand-sub">ENGINEERING SIMULATOR</div>',unsafe_allow_html=True)
    st.caption("PERFORMANCE · OPTIMIZATION · ANALYSIS")
    st.divider()
    st.markdown("#### GLOBAL CONTROLS")
    st.selectbox("Appearance",["Dark","Light"],key="theme")
    theme()
    opts=datasets()
    names=list(opts)
    default=names.index(st.session_state.dataset) if st.session_state.dataset in names else 0
    st.selectbox("Weather dataset",names,index=default,key="dataset")
    st.selectbox("PV module",["250 W Illustrative","Custom"],key="panel_kind")
    if st.session_state.panel_kind=="Custom":
        st.number_input("Rated power (W)",50.,1000.,250.,key="rated")
        st.number_input("Voc (V)",10.,100.,37.5,key="voc")
        st.number_input("Isc (A)",1.,30.,8.7,key="isc")
        st.number_input("Vmp (V)",5.,90.,30.5,key="vmp")
        st.number_input("Imp (A)",1.,30.,8.2,key="imp")
        st.number_input("Area (m²)",.2,5.,1.65,key="area")
    st.number_input("Load resistance (Ω)",2.,100.,key="load_r")
    st.slider("Converter efficiency (%)",70,99,key="converter_eta")
    st.slider("MPPT step (V)",.05,2.,key="mppt_step")
    st.divider()
    st.success("OFFLINE SIMULATION READY")
    st.caption("Preloaded local CSV data. Historical download is optional.")

pages=[
 st.Page("pages/1_Dashboard.py",title="Dashboard",icon="📊",default=True),
 st.Page("pages/2_PV_Analysis.py",title="PV Analysis",icon="☀️"),
 st.Page("pages/3_Weather_Lab.py",title="Weather Lab",icon="☁️"),
 st.Page("pages/4_MPPT_Lab.py",title="MPPT Lab",icon="🎯"),
 st.Page("pages/5_Load_System.py",title="Load System",icon="⚡"),
 st.Page("pages/6_Numerical_Lab.py",title="Numerical Lab",icon="∑"),
 st.Page("pages/7_Comparison.py",title="Comparison",icon="⇄"),
 st.Page("pages/8_Reports.py",title="Reports & Data",icon="📄")]
st.navigation(pages,position="sidebar").run()
