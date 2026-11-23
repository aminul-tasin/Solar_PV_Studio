import streamlit as st
import numpy as np
import plotly.graph_objects as go
from components.common import context,header,plot_theme
from numerical_methods import bisection,newton_raphson
from analysis import energy_wh
ctx=context(); header("Numerical techniques lab","Demonstrate root finding, numerical differentiation and integration.")
tabs=st.tabs(["Newton–Raphson","Bisection","Differentiation","Trapezoidal integration"])
with tabs[0]:
 v=st.number_input("PV voltage (V)",0.,float(ctx["panel"].voc),20.)
 g=st.number_input("Irradiance (W/m²)",0.,1200.,1000.,key="ng")
 temp=st.number_input("Cell temperature (°C)",-10.,90.,25.,key="nt")
 if st.button("Solve using Newton–Raphson"):
  p=ctx["panel"]; iph,i0,a=ctx["pv"].parameters_at(g,temp)
  f=lambda i: iph-i0*np.expm1(np.clip((v+i*p.rs)/a,-100,100))-(v+i*p.rs)/p.rsh-i
  df=lambda i: -i0*np.exp(np.clip((v+i*p.rs)/a,-100,100))*p.rs/a-p.rs/p.rsh-1
  try:
   root,it=newton_raphson(f,df,min(iph,p.isc)); st.success(f"Current = {root:.7f} A in {it} iterations")
  except Exception as ex: st.error(str(ex))
with tabs[1]:
 v=st.number_input("Voltage (V)",0.,float(ctx["panel"].voc),20.,key="bv")
 g=st.number_input("Irradiance (W/m²)",0.,1200.,1000.,key="bg")
 temp=st.number_input("Cell temperature (°C)",-10.,90.,25.,key="bt")
 if st.button("Solve using Bisection"):
  p=ctx["panel"]; iph,i0,a=ctx["pv"].parameters_at(g,temp)
  f=lambda i: iph-i0*np.expm1(np.clip((v+i*p.rs)/a,-100,100))-(v+i*p.rs)/p.rsh-i
  try: root,it=bisection(f,0,max(iph*1.2+.1,.2)); st.success(f"Current = {root:.7f} A in {it} iterations")
  except Exception as ex: st.error(str(ex))
with tabs[2]:
 row=ctx["weather"].iloc[len(ctx["weather"])//2]; c=ctx["pv"].curve(row.irradiance,row.cell_temp,350)
 derivative=np.gradient(c["power"],c["voltage"])
 fig=go.Figure(go.Scatter(x=c["voltage"],y=derivative,name="dP/dV"))
 fig.add_hline(y=0,line_dash="dash"); fig.update_layout(title="Numerical derivative of P–V curve",xaxis_title="Voltage (V)",yaxis_title="dP/dV (W/V)")
 st.plotly_chart(plot_theme(fig),use_container_width=True)
 st.caption("At the maximum-power point, dP/dV is approximately zero.")
with tabs[3]:
 powers=[ctx["pv"].curve(r.irradiance,r.cell_temp,150)["pmax"] for r in ctx["weather"].itertuples()]
 df=ctx["weather"].copy(); df["power_w"]=powers
 st.metric("Integrated energy",f"{energy_wh(df,'power_w'):.3f} Wh")
 st.latex(r"E\\approx\\sum_{i=1}^{n-1}\\frac{P_i+P_{i+1}}{2}\\Delta t_i")
