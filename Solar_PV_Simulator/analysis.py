import numpy as np
import pandas as pd

def prepare_weather(df):
    d=df.copy()
    required={"timestamp","irradiance","ambient_temp"}
    missing=required-set(d.columns)
    if missing: raise ValueError("CSV missing required columns: "+", ".join(sorted(missing)))
    d["timestamp"]=pd.to_datetime(d["timestamp"])
    for c in ["irradiance","ambient_temp"]:
        d[c]=pd.to_numeric(d[c],errors="coerce")
    if "wind_speed" not in d: d["wind_speed"]=1.5
    d["wind_speed"]=pd.to_numeric(d["wind_speed"],errors="coerce").fillna(1.5)
    if "cell_temp" not in d:
        d["cell_temp"]=d["ambient_temp"]+(45-20)/800*d["irradiance"]/(1+.04*d["wind_speed"])
    d["cell_temp"]=pd.to_numeric(d["cell_temp"],errors="coerce")
    d=d.dropna(subset=["timestamp","irradiance","ambient_temp","cell_temp"]).sort_values("timestamp").reset_index(drop=True)
    d["irradiance"]=d["irradiance"].clip(0,1400)
    return d

def add_pv_performance(pv, weather):
    d=prepare_weather(weather); rows=[]
    for r in d.itertuples():
        c=pv.curve(r.irradiance,r.cell_temp,points=160)
        rows.append([c["vmp"],c["imp"],c["pmax"],c["ff"],c["efficiency"]])
    d[["vmp","imp","pmax","fill_factor","panel_efficiency"]]=rows
    return d

def energy_wh(df, power_col):
    if len(df)<2: return 0.0
    t=pd.to_datetime(df["timestamp"])
    hours=(t.astype("int64").to_numpy()/3.6e12)
    return float(np.trapezoid(df[power_col].to_numpy(dtype=float),hours))
