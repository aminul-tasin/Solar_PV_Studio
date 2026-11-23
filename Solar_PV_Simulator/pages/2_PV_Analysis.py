import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.common import context,header,plot_theme
ctx=context(); w=ctx["weather"]
header("PV performance analysis","Inspect I–V and P–V characteristics at selected weather conditions.")
i=st.slider("Weather sample",0,len(w)-1,len(w)//2)
x,y=st.columns(2)
g=x.number_input("Irradiance override (W/m²)",0.,1200.,float(w.iloc[i].irradiance),10.)
t=y.number_input("Cell temperature override (°C)",-10.,90.,float(w.iloc[i].cell_temp),1.)
c=ctx["pv"].curve(g,t,500)
fig=go.Figure(); fig.add_scatter(x=c["voltage"],y=c["current"],name="I–V",line=dict(width=3))
fig.add_scatter(x=[c["vmp"]],y=[c["imp"]],mode="markers",name="MPP",marker=dict(size=11))
fig.update_layout(title="Current–Voltage characteristic",xaxis_title="Voltage (V)",yaxis_title="Current (A)")
f2=go.Figure(); f2.add_scatter(x=c["voltage"],y=c["power"],name="P–V",fill="tozeroy")
f2.add_scatter(x=[c["vmp"]],y=[c["pmax"]],mode="markers",name="MPP",marker=dict(size=11))
f2.update_layout(title="Power–Voltage characteristic",xaxis_title="Voltage (V)",yaxis_title="Power (W)")
a,b=st.columns(2); a.plotly_chart(plot_theme(fig),use_container_width=True); b.plotly_chart(plot_theme(f2),use_container_width=True)
m=st.columns(6)
for col,label,val in zip(m,["Voc","Isc","Vmp","Imp","Pmax","Fill factor"],
 [c["voc"],c["isc"],c["vmp"],c["imp"],c["pmax"],c["ff"]]):
 col.metric(label,f"{val:.3f}" if label=="Fill factor" else f"{val:.2f}")
st.metric("Estimated module efficiency",f"{c['efficiency']:.2f}%")
with st.expander("Single-diode equation"):
 st.latex(r"I=I_{ph}-I_0\\left[\\exp\\left(\\frac{V+IR_s}{a}\\right)-1\\right]-\\frac{V+IR_s}{R_{sh}}")
 st.write("The photocurrent depends primarily on irradiance; diode saturation current and thermal voltage depend on cell temperature.")
st.download_button("Export curve CSV",pd.DataFrame({"voltage_V":c["voltage"],"current_A":c["current"],"power_W":c["power"]}).to_csv(index=False).encode(),"pv_curves.csv")
