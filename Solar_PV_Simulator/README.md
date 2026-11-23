# Solar PV Studio — Engineering GUI

A Streamlit multipage offline simulator for PV performance, weather scenarios, MPPT and MPPT-to-load analysis.

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Python 3.10+ recommended.

## Interface
- Dark / Light theme switcher
- Professional engineering visual style
- Persistent sidebar with global dataset, panel, load, converter-efficiency and MPPT-step controls
- Dashboard, PV Analysis, Weather Lab, MPPT Lab, Load System, Numerical Lab, Comparison, Reports & Data

## Included capabilities
- Single-diode PV model with irradiance and cell-temperature dependence
- I–V / P–V curves, Voc, Isc, MPP, fill factor and estimated efficiency
- Preloaded synthetic sunny, cloudy, foggy and rainy CSV datasets
- User-imported weather CSV support and optional NASA POWER historical archive downloader
- P&O and Incremental Conductance MPPT demonstrations
- Direct resistive load and averaged boost converter model
- Newton–Raphson, Bisection, numerical differentiation and trapezoidal integration
- Interactive Plotly charts; CSV and PDF exports

## Weather CSV schema
Required: `timestamp`, `irradiance` (W/m²), `ambient_temp` (°C).
Optional: `cell_temp` (°C), `wind_speed` (m/s).

## Model limitations (important for lab reporting)
- The included 250 W module is illustrative, not a manufacturer's certified datasheet model.
- Single-diode parameters are estimated from Voc/Isc with assumed Rs/Rsh/ideality; the nominal Vmp/Imp are not independently fitted.
- Cell temperature is estimated with a simplified NOCT-style relationship.
- MPPT routines are sampled-data educational demonstrations, not high-frequency controller firmware.
- Boost converter is an averaged steady-state approximation with fixed efficiency. No PWM ripple, switching loss or transient inductor/capacitor dynamics.
- Synthetic weather scenarios are illustrative profiles, not measured meteorological observations.
- NASA POWER download is optional and requires internet; saved data can subsequently be used offline.
