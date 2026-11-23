import numpy as np
import pandas as pd

def _track(pv, weather, method="po", step_v=.35):
    d=weather.reset_index(drop=True).copy()
    v=float(pv.panel.vmp); rows=[]
    prev_p=None; prev_v=None; direction=1
    for r in d.itertuples():
        c=pv.curve(float(r.irradiance),float(r.cell_temp),points=220)
        if method=="po":
            if prev_p is not None:
                if c["pmax"] < prev_p: direction *= -1
            v=np.clip(v+direction*step_v,0,c["voc"])
        else:
            # Incremental-conductance direction inferred from dP/dV at current operating point.
            idx=int(np.argmin(np.abs(c["voltage"]-v)))
            slope=np.gradient(c["power"],c["voltage"])[idx]
            v=np.clip(v+np.sign(slope)*step_v,0,c["voc"])
        j=int(np.argmin(np.abs(c["voltage"]-v)))
        pv_power=float(c["power"][j])
        rows.append({"timestamp":r.timestamp,"available_mpp_power":c["pmax"],
                     "tracked_voltage":float(c["voltage"][j]),"tracked_current":float(c["current"][j]),
                     "tracked_power":pv_power})
        prev_p=c["pmax"]; prev_v=v
    out=pd.DataFrame(rows)
    out["algorithm"]="P&O" if method=="po" else "Incremental Conductance"
    return out

def simulate_po(pv,weather,step_v=.35): return _track(pv,weather,"po",step_v)
def simulate_inccond(pv,weather,step_v=.35): return _track(pv,weather,"inc",step_v)
def tracking_efficiency(result):
    den=result["available_mpp_power"].sum()
    return 100*result["tracked_power"].sum()/den if den else 0.0
