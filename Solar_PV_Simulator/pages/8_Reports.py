import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
from components.common import context,header,perf,IMPORTED,HISTORICAL
from analysis import prepare_weather,energy_wh
ctx=context(); d=perf(ctx); header("Reports & data","Import archived weather datasets and export simulation results.")
upload=st.file_uploader("Import weather CSV",type=["csv"])
if upload:
 try:
  checked=prepare_weather(pd.read_csv(upload))
  name=Path(upload.name).stem.replace(" ","_")
  checked.to_csv(IMPORTED/f"{name}.csv",index=False)
  st.success(f"Imported {len(checked)} rows. Select Imported / {name} in the sidebar.")
  st.dataframe(checked.head(),use_container_width=True)
 except Exception as ex: st.error(f"CSV validation failed: {ex}")
st.markdown("#### Optional NASA POWER archived weather download")
with st.form("nasa"):
 lat=st.number_input("Latitude",value=23.8103,format="%.4f")
 lon=st.number_input("Longitude",value=90.4125,format="%.4f")
 start=st.text_input("Start date (YYYY-MM-DD)","2024-01-01")
 end=st.text_input("End date (YYYY-MM-DD)","2024-01-03")
 submit=st.form_submit_button("Download archived data")
if submit:
 try:
  from historical_data import download_nasa_power
  hist,_=download_nasa_power(lat,lon,start,end,HISTORICAL/"nasa_power.csv")
  st.success(f"Saved {len(hist)} records. Select Historical / nasa_power in sidebar.")
 except Exception as ex: st.error(str(ex))
st.divider()
st.download_button("PV performance CSV",d.to_csv(index=False).encode(),"pv_performance.csv")
st.download_button("Active weather CSV",ctx["weather"].to_csv(index=False).encode(),"weather_dataset.csv")
if st.button("Prepare PDF report",type="primary"):
 try:
  from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table
  from reportlab.lib.styles import getSampleStyleSheet
  from reportlab.lib.pagesizes import A4
  from reportlab.lib import colors
  buf=BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4); styles=getSampleStyleSheet()
  peak=d.loc[d.pmax.idxmax()]
  story=[Paragraph("Solar PV Studio — Simulation Report",styles["Title"]),
   Paragraph(f"Dataset: {ctx['dataset']} | PV model: single diode",styles["Normal"]),Spacer(1,14)]
  table=Table([["Metric","Value"],["Peak available power",f"{d.pmax.max():.2f} W"],
   ["MPP voltage at peak",f"{peak.vmp:.2f} V"],["MPP current at peak",f"{peak.imp:.2f} A"],
   ["Integrated energy",f"{energy_wh(d,'pmax'):.2f} Wh"],["Mean irradiance",f"{d.irradiance.mean():.1f} W/m²"]])
  table.setStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17334a")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
   ("GRID",(0,0),(-1,-1),.4,colors.grey),("PADDING",(0,0),(-1,-1),7)])
  story += [table,Spacer(1,14),Paragraph("Model notes",styles["Heading2"]),
   Paragraph("Single-diode PV model with irradiance and temperature dependence. Numerical root finding uses bisection/Newton-Raphson. Energy is integrated with the trapezoidal rule. The averaged boost converter does not model switching ripple or transient states.",styles["BodyText"])]
  doc.build(story); buf.seek(0)
  st.download_button("Download PDF report",buf.getvalue(),"solar_pv_report.pdf","application/pdf")
 except Exception as ex: st.error(f"PDF creation failed: {ex}")
