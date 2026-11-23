import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dataset_generator import generate_weather_dataset
from components.common import context,header,plot_theme,SYNTHETIC
from analysis import add_pv_performance,energy_wh
ctx=context(); header("Weather simulation lab","Explore sunny, cloudy, foggy and rainy preloaded profiles.")
scenario=st.selectbox("Generate scenario",["sunny","cloudy","foggy","rainy"])
date=st.date_input("Profile date",value=pd.Timestamp("2026-06-15").date())
seed=st.number_input("Random seed",0,99999,7)
if st.button("Generate and save scenario",type="primary"):
 generate_weather_dataset(scenario,str(date),int(seed)).to_csv(SYNTHETIC/f"{scenario}.csv",index=False)
 st.cache_data.clear(); st.success("Scenario saved. Select it in the sidebar to activate.")
fig=go.Figure(); summary=[]
for s in ["sunny","cloudy","foggy","rainy"]:
 df=pd.read_csv(SYNTHETIC/f"{s}.csv"); p=add_pv_performance(ctx["pv"],df)
 fig.add_scatter(x=p.timestamp,y=p.pmax,name=s.title())
 summary.append({"Weather":s.title(),"Mean irradiance":p.irradiance.mean(),
                 "Peak PV power (W)":p.pmax.max(),"Energy (Wh)":energy_wh(p,"pmax")})
fig.update_layout(title="Maximum power by weather scenario",xaxis_title="Time",yaxis_title="Power (W)")
st.plotly_chart(plot_theme(fig),use_container_width=True)
st.dataframe(pd.DataFrame(summary).round(2),use_container_width=True,hide_index=True)
st.markdown("#### Active weather data")
st.dataframe(ctx["weather"],use_container_width=True,hide_index=True)
st.download_button("Download active dataset",ctx["weather"].to_csv(index=False).encode(),"weather_data.csv")
