import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.common import context,header,plot_theme
from mppt import simulate_po,simulate_inccond,tracking_efficiency
ctx=context(); header("MPPT laboratory","Compare Perturb & Observe and Incremental Conductance tracking.")
alg=st.selectbox("Algorithm",["Compare both","P&O","Incremental Conductance"])
n=st.slider("Weather samples",10,min(721,len(ctx["weather"])),min(180,len(ctx["weather"])),10)
step=st.number_input("Voltage step (V)",.05,2.,float(st.session_state.mppt_step),.05)
if st.button("Run MPPT simulation",type="primary"):
 w=ctx["weather"].iloc[:n].reset_index(drop=True)
 st.session_state.mppt_po=simulate_po(ctx["pv"],w,step) if alg!="Incremental Conductance" else None
 st.session_state.mppt_ic=simulate_inccond(ctx["pv"],w,step) if alg!="P&O" else None
po=st.session_state.get("mppt_po"); ic=st.session_state.get("mppt_ic")
if po is None and ic is None: st.info("Run a simulation to display MPPT tracking results.")
else:
 fig=go.Figure()
 base=po if po is not None else ic
 fig.add_scatter(x=base.timestamp,y=base.available_mpp_power,name="Available MPP",line=dict(dash="dash"))
 if po is not None: fig.add_scatter(x=po.timestamp,y=po.tracked_power,name="P&O")
 if ic is not None: fig.add_scatter(x=ic.timestamp,y=ic.tracked_power,name="Incremental Conductance")
 fig.update_layout(title="MPPT tracking power",xaxis_title="Time",yaxis_title="Power (W)")
 st.plotly_chart(plot_theme(fig),use_container_width=True)
 a,b=st.columns(2)
 if po is not None: a.metric("P&O tracking efficiency",f"{tracking_efficiency(po):.2f}%")
 if ic is not None: b.metric("IncCond tracking efficiency",f"{tracking_efficiency(ic):.2f}%")
 frames=[x for x in [po,ic] if x is not None]; result=pd.concat(frames,ignore_index=True)
 st.dataframe(result,use_container_width=True,hide_index=True)
 st.download_button("Export MPPT results",result.to_csv(index=False).encode(),"mppt_results.csv")
st.caption("Educational sampled-data MPPT. It is not a switching-frequency hardware controller.")
