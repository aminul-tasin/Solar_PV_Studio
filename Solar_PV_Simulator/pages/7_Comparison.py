import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components.common import context,header,plot_theme,SYNTHETIC
from analysis import add_pv_performance,energy_wh
from converter import direct_pv_to_resistive_load
ctx=context(); header("Comparison & optimization","Compare environmental scenarios and investigate load matching.")
fig=go.Figure(); rows=[]
for s in ["sunny","cloudy","foggy","rainy"]:
 df=add_pv_performance(ctx["pv"],pd.read_csv(SYNTHETIC/f"{s}.csv"))
 fig.add_scatter(x=df.timestamp,y=df.pmax,name=s.title())
 rows.append({"Weather":s.title(),"Mean irradiance (W/m²)":df.irradiance.mean(),
              "Peak power (W)":df.pmax.max(),"Energy (Wh)":energy_wh(df,"pmax")})
fig.update_layout(title="PV power by weather scenario",xaxis_title="Time",yaxis_title="Power (W)")
st.plotly_chart(plot_theme(fig),use_container_width=True)
st.dataframe(pd.DataFrame(rows).round(2),use_container_width=True,hide_index=True)
st.markdown("#### Direct-load resistance sweep")
lo,hi=st.slider("Load resistance range (Ω)",2,100,(5,60))
step=st.select_slider("Resistance step (Ω)",options=[1,2,5,10],value=5)
sample=ctx["weather"].iloc[::max(1,len(ctx["weather"])//100)].reset_index(drop=True)
sweep=[]
for r in range(lo,hi+1,step):
 d=direct_pv_to_resistive_load(ctx["pv"],sample,r)
 sweep.append((r,energy_wh(d,"load_power")))
sf=pd.DataFrame(sweep,columns=["Resistance (Ω)","Energy (Wh)"])
fig=go.Figure(go.Scatter(x=sf.iloc[:,0],y=sf.iloc[:,1],mode="lines+markers"))
fig.update_layout(title="Delivered energy versus load resistance",xaxis_title="Resistance (Ω)",yaxis_title="Energy (Wh)")
st.plotly_chart(plot_theme(fig),use_container_width=True)
best=sf.loc[sf["Energy (Wh)"].idxmax()]
st.success(f"Best tested resistance: {best.iloc[0]} Ω, yielding {best.iloc[1]:.2f} Wh in this dataset.")
