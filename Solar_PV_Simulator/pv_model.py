import numpy as np
from config import PanelParams
from numerical_methods import bisection

class SingleDiodePV:
    """Single-diode model: I=Iph-I0(exp((V+I*Rs)/a)-1)-(V+I*Rs)/Rsh."""
    def __init__(self, panel=None):
        self.panel = panel or PanelParams()
        p = self.panel
        self.vt_ref = 1.380649e-23 * 298.15 / 1.602176634e-19
        self.a_ref = p.diode_ideality * p.cells_series * self.vt_ref
        self.i0_ref = p.isc / max(np.exp(min(p.voc/self.a_ref, 80))-1, 1e-30)
        self.iph_ref = p.isc * (1 + p.rs/p.rsh) + self.i0_ref*(np.exp(min(p.isc*p.rs/self.a_ref,80))-1)
    def parameters_at(self, irradiance, cell_temp):
        p=self.panel
        g=max(float(irradiance),0.0); tk=float(cell_temp)+273.15
        iph=(self.iph_ref + p.alpha_isc*(tk-298.15))*(g/1000.0)
        vt=1.380649e-23*tk/1.602176634e-19
        a=p.diode_ideality*p.cells_series*vt
        eg=1.12*1.602176634e-19
        i0=self.i0_ref*(tk/298.15)**3*np.exp(np.clip(eg/(p.diode_ideality*1.380649e-23)*(1/298.15-1/tk),-80,80))
        return max(iph,0), max(i0,1e-30), a
    def current_at_voltage(self, voltage, irradiance, cell_temp):
        p=self.panel; iph,i0,a=self.parameters_at(irradiance,cell_temp)
        if irradiance <= 0: return 0.0
        def f(i):
            z=np.clip((voltage+i*p.rs)/a,-100,100)
            return iph-i0*np.expm1(z)-(voltage+i*p.rs)/p.rsh-i
        lo,hi=0.0,max(iph*1.1+0.1,0.2)
        try: return max(0.0,bisection(f,lo,hi,tol=1e-7,max_iter=100)[0])
        except ValueError: return 0.0
    def curve(self, irradiance=1000, cell_temp=25, points=300):
        p=self.panel
        if irradiance <= 0:
            v=np.linspace(0,p.voc,points); i=np.zeros_like(v)
        else:
            iph,_,_=self.parameters_at(irradiance,cell_temp)
            voc_est=max(0.0,p.voc + p.beta_voc*(cell_temp-25) + 0.025*np.log(max(irradiance,1)/1000))
            v=np.linspace(0,voc_est,points)
            i=np.array([self.current_at_voltage(x,irradiance,cell_temp) for x in v])
        power=v*i; k=int(np.argmax(power))
        isc=float(i[0]); voc=float(v[np.where(i<=max(isc*0.002,1e-5))[0][0]]) if np.any(i<=max(isc*0.002,1e-5)) else float(v[-1])
        vmp=float(v[k]); imp=float(i[k]); pmax=float(power[k])
        ff=pmax/max(voc*isc,1e-12)
        efficiency=100*pmax/max(float(irradiance)*p.area/1000,1e-12) if irradiance>0 else 0
        return {"voltage":v,"current":i,"power":power,"voc":voc,"isc":isc,
                "vmp":vmp,"imp":imp,"pmax":pmax,"ff":ff,"efficiency":efficiency}
