from dataclasses import dataclass

@dataclass
class PanelParams:
    name: str = "250 W Illustrative Module"
    p_rated: float = 250.0
    voc: float = 37.5
    isc: float = 8.7
    vmp: float = 30.5
    imp: float = 8.2
    area: float = 1.65
    cells_series: int = 60
    rs: float = 0.25
    rsh: float = 250.0
    diode_ideality: float = 1.2
    alpha_isc: float = 0.0005
    beta_voc: float = -0.0032
    noct: float = 45.0
    @property
    def eta_ref(self):
        return self.p_rated / (1000.0 * self.area)
