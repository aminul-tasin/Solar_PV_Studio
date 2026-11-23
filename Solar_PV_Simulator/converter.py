import numpy as np
import pandas as pd
from analysis import prepare_weather

def direct_pv_to_resistive_load(pv, weather, resistance):
    if resistance<=0: raise ValueError("Load resistance must be positive.")
    d=prepare_weather(weather); rows=[]
    for r in d.itertuples():
        c=pv.curve(r.irradiance,r.cell_temp,points=260)
        # Intersect PV I-V curve with I=V/R.
        diff=c["current"]-c["voltage"]/resistance
        k=int(np.argmin(np.abs(diff))); v=float(c["voltage"][k]); i=float(c["current"][k])
        rows.append({"timestamp":r.timestamp,"pv_voltage":v,"pv_current":i,"load_power":v*i})
    return pd.DataFrame(rows)

def boost_mppt_to_load(pv,weather,resistance,efficiency,tracker):
    if resistance<=0: raise ValueError("Load resistance must be positive.")
    if not 0<efficiency<=1: raise ValueError("Efficiency must be between 0 and 1.")
    d=prepare_weather(weather).reset_index(drop=True)
    t=tracker.reset_index(drop=True)
    pin=t["tracked_power"].to_numpy()
    # Ideal boost relation Vout = Vin/(1-D); choose a modest DC bus target.
    vin=np.maximum(t["tracked_voltage"].to_numpy(),1e-6)
    vout=np.maximum(48.0,vin*1.15)
    duty=np.clip(1-vin/vout,0,.85)
    pout=pin*efficiency
    vload=np.sqrt(np.maximum(pout*resistance,0))
    iload=vload/resistance
    return pd.DataFrame({"timestamp":d.timestamp,"pv_voltage":vin,"pv_current":t.tracked_current,
        "pv_input_power":pin,"duty_cycle":duty,"load_voltage":vload,
        "load_current":iload,"load_power":pout})
