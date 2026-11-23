import requests
import pandas as pd

def download_nasa_power(latitude,longitude,start_date,end_date,output_file=None):
    url="https://power.larc.nasa.gov/api/temporal/hourly/point"
    params={"parameters":"ALLSKY_SFC_SW_DWN,T2M,WS10M","community":"RE",
            "longitude":longitude,"latitude":latitude,"start":start_date.replace("-",""),
            "end":end_date.replace("-",""),"format":"JSON"}
    response=requests.get(url,params=params,timeout=45); response.raise_for_status()
    payload=response.json()["properties"]["parameter"]
    irr=payload["ALLSKY_SFC_SW_DWN"]; temp=payload["T2M"]; wind=payload["WS10M"]
    keys=sorted(set(irr)&set(temp)&set(wind))
    df=pd.DataFrame({"timestamp":pd.to_datetime(keys,format="%Y%m%d%H"),
        "irradiance":[irr[k] for k in keys],"ambient_temp":[temp[k] for k in keys],
        "wind_speed":[wind[k] for k in keys]})
    if output_file: df.to_csv(output_file,index=False)
    return df,output_file
