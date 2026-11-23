import streamlit as st
from components.common import context,header,perf,plot_theme
import plotly.graph_objects as go
from analysis import energy_wh
ctx=context(); d=perf(ctx)
header("Simulation dashboard","Monitor PV output, environmental conditions and energy yield.")
st.caption(f"ACTIVE DATASET  ·  {ctx['dataset']}     |     MODEL  ·  SINGLE DIODE     |     SAMPLES  ·  {len(d)}")
a,b,c,e,f=st.columns(5)
a.metric("Peak PV power",f"{d.pmax.max():.1f} W")
r=d.loc[d.pmax.idxmax()]
b.metric("MPP voltage",f"{r.vmp:.2f} V"); c.metric("MPP current",f"{r.imp:.2f} A")
e.metric("Mean efficiency",f"{d.panel_efficiency.mean():.1f}%")
f.metric("Available energy",f"{energy_wh(d,'pmax'):.1f} Wh")
left,right=st.columns(2)
for col,y,title,ylab in [(left,"pmax","Maximum available PV power","Power (W)"),(right,"irradiance","Solar irradiance","W/m²")]:
    fig=go.Figure(go.Scatter(x=d.timestamp,y=d[y],mode="lines",name=title,line=dict(width=2)))
    fig.update_layout(title=title,xaxis_title="Time",yaxis_title=ylab)
    col.plotly_chart(plot_theme(fig),use_container_width=True)
fig=go.Figure()
fig.add_scatter(x=d.timestamp,y=d.cell_temp,name="Cell temperature")
fig.add_scatter(x=d.timestamp,y=d.ambient_temp,name="Ambient temperature")
fig.update_layout(title="Thermal profile",xaxis_title="Time",yaxis_title="°C")
st.plotly_chart(plot_theme(fig),use_container_width=True)
st.markdown("#### PV module specifications")
st.write({"Module":ctx["panel"].name,"Rated power (W)":ctx["panel"].p_rated,
          "Voc (V)":ctx["panel"].voc,"Isc (A)":ctx["panel"].isc,
          "Series cells":ctx["panel"].cells_series,"Area (m²)":ctx["panel"].area})
