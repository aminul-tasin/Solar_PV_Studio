from pathlib import Path
import numpy as np
import pandas as pd

def generate_weather_dataset(scenario="sunny", date="2026-06-15", seed=7, periods=144, freq="10min"):
    rng=np.random.default_rng(seed)
    times=pd.date_range(f"{date} 05:00",periods=periods,freq=freq)
    hour=times.hour.to_numpy()+times.minute.to_numpy()/60
    daylight=np.clip(np.sin(np.pi*(hour-5.0)/14.0),0,None)
    base=950*daylight
    factors={"sunny":1.0,"cloudy":0.58,"foggy":0.32,"rainy":0.22}
    if scenario not in factors: raise ValueError("Unknown scenario")
    if scenario=="cloudy":
        cloud=0.55+0.35*np.sin(np.linspace(0,8*np.pi,periods))**2
    elif scenario=="foggy": cloud=np.linspace(.45,.75,periods)
    elif scenario=="rainy": cloud=.45+.25*np.sin(np.linspace(0,5*np.pi,periods))
    else: cloud=np.ones(periods)
    irr=np.clip(base*factors[scenario]*cloud+rng.normal(0,18,periods),0,1100)
    ambient=23+8*daylight+rng.normal(0,1.2,periods)
    wind=np.clip(1.5+rng.normal(0,.5,periods),0,6)
    cell=ambient+(45-20)/800*irr/(1+0.04*wind)
    return pd.DataFrame({"timestamp":times,"irradiance":irr,"ambient_temp":ambient,
                         "cell_temp":cell,"wind_speed":wind})

def generate_all(folder):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    for s in ["sunny","cloudy","foggy","rainy"]:
        generate_weather_dataset(s).to_csv(folder/f"{s}.csv",index=False)
