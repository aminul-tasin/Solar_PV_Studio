import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.common import context,header,plot_theme
from mppt import simulate_po,simulate_inccond
from converter import direct_pv_to_resistive_load,boost_mppt_to_load
from analysis import energy_wh
ctx=context(); header("MPPT-to-load system","Compare direct resistive loading with an MPPT-controlled averaged boost converter.")
alg=st.radio("MPPT controller",["P&O","Incremental Conductance"],horizontal=True)
n=st.slider("Weather samples",10,min(721,len(ctx["weather"])),min(180,len(ctx["weather"])),10)
if st.button("Run load-system simulation",type="primary"):
 w=ctx["weather"].iloc[:n].reset_index(drop=True)
 track=simulate_po(ctx["pv"],w,st.session_state.mppt_step) if alg=="P&O" else simulate_inccond(ctx["pv"],w,st.session_state.mppt_step)
 st.session_state.direct=direct_pv_to_resistive_load(ctx["pv"],w,st.session_state.load_r)
 st.session_state.boost=boost_mppt_to_load(ctx["pv"],w,st.session_state.load_r,st.session_state.converter_eta/100,track)
if "direct" in st.session_state and "boost" in st.session_state:
 d=st.session_state.direct; b=st.session_state.boost
 fig=go.Figure(); fig.add_scatter(x=d.timestamp,y=d.load_power,name="Direct PV → load")
 fig.add_scatter(x=b.timestamp,y=b.load_power,name="MPPT + boost → load")
 fig.update_layout(title="Load power delivered",xaxis_title="Time",yaxis_title="Power (W)")
 st.plotly_chart(plot_theme(fig),use_container_width=True)
 a,c,e=st.columns(3); a.metric("Direct energy",f"{energy_wh(d,'load_power'):.2f} Wh")
 c.metric("MPPT load energy",f"{energy_wh(b,'load_power'):.2f} Wh")
 e.metric("Mean duty cycle",f"{100*b.duty_cycle.mean():.1f}%")
 st.dataframe(b,use_container_width=True,hide_index=True)
 st.download_button("Export load results",b.to_csv(index=False).encode(),"load_results.csv")
st.markdown("#### Power conversion chain")
st.markdown("**PV panel → MPPT controller → averaged boost converter → DC resistive load**")
st.caption("Averaged converter approximation; no PWM ripple, switching losses or transient circuit states.")
