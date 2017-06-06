"""Unsorted variables related to leaf model"""

from essm.variables import Variable
from essm.variables.units import joule, kelvin, kilogram, meter, mole, pascal, second

class a_s(Variable):
    """Fraction of one-sided leaf area covered by stomata (1 if stomata are on one side only, 2 if they are on both sides)"""
    name = 'a_s'
    unit = 1
    latex_name = r"a_s"
       



class a_sh(Variable):
    """Fraction of projected area exchanging sensible heat with the air (2)"""
    name = 'a_sh'
    unit = 1
    latex_name = r"a_{sh}"
    default = 2   



class C_wa(Variable):
    """Concentration of water in the free air """
    name = 'C_wa'
    unit = mole/meter**3
    latex_name = r"C_{wa}"
       



class C_wl(Variable):
    """Concentration of water in the leaf air space """
    name = 'C_wl'
    unit = mole/meter**3
    latex_name = r"C_{wl}"
       



class E_lmol(Variable):
    """Transpiration rate in molar units"""
    name = 'E_lmol'
    unit = mole/(meter**2*second)
    latex_name = r"E_{l,mol}"
       



class E_l(Variable):
    """Latent heat flux from leaf"""
    name = 'E_l'
    unit = joule/(meter**2*second)
    latex_name = r"E_l"
       



class epsilon_l(Variable):
    """Longwave emmissivity of the leaf surface (1.0)"""
    name = 'epsilon_l'
    unit = 1
    latex_name = r"\epsilon_l"
    default = 1   



class g_bw(Variable):
    """Boundary layer conductance to water vapour """
    name = 'g_bw'
    unit = meter/second
    latex_name = r"g_{bw}"
       



class g_bwmol(Variable):
    """Boundary layer conductance to water vapour """
    name = 'g_bwmol'
    unit = mole/(meter**2*second)
    latex_name = r"g_{bw,mol}"
       



class g_sw(Variable):
    """Stomatal conductance to water vapour"""
    name = 'g_sw'
    unit = meter/second
    latex_name = r"g_{sw}"
       



class g_swmol(Variable):
    """Stomatal conductance to water vapour"""
    name = 'g_swmol'
    unit = mole/(meter**2*second)
    latex_name = r"g_{sw,mol}"
       



class g_tw(Variable):
    """Total leaf conductance to water vapour"""
    name = 'g_tw'
    unit = meter/second
    latex_name = r"g_{tw}"
       



class g_twmol(Variable):
    """Total leaf layer conductance to water vapour"""
    name = 'g_twmol'
    unit = mole/(meter**2*second)
    latex_name = r"g_{tw,mol}"
       



class H_l(Variable):
    """Sensible heat flux from leaf"""
    name = 'H_l'
    unit = joule/(meter**2*second)
    latex_name = r"H_l"
       



class L_l(Variable):
    """Characteristic length scale for convection (size of leaf)"""
    name = 'L_l'
    unit = meter
    latex_name = r"L_l"
       



class P_wl(Variable):
    """Vapour pressure inside the leaf"""
    name = 'P_wl'
    unit = pascal
    latex_name = r"P_{wl}"
       



class r_bw(Variable):
    """Boundary layer resistance to water vapour, inverse of $g_{bw}$"""
    name = 'r_bw'
    unit = second/meter
    latex_name = r"r_{bw}"
       



class r_sw(Variable):
    """Stomatal resistance to water vapour, inverse of $g_{sw}$"""
    name = 'r_sw'
    unit = second/meter
    latex_name = r"r_{sw}"
       



class r_tw(Variable):
    """Total leaf resistance to water vapour, $r_{bv} + r_{sv}$"""
    name = 'r_tw'
    unit = second/meter
    latex_name = r"r_{tw}"
       



class rho_al(Variable):
    """Density of air at the leaf surface"""
    name = 'rho_al'
    unit = kilogram/meter**3
    latex_name = r"\rho_{al}"
       



class R_ll(Variable):
    """Longwave radiation away from leaf"""
    name = 'R_ll'
    unit = joule/(meter**2*second)
    latex_name = r"R_{ll}"
       



class T_l(Variable):
    """Leaf temperature"""
    name = 'T_l'
    unit = kelvin
    latex_name = r"T_l"
       



class T_w(Variable):
    """Radiative temperature of objects surrounding the leaf"""
    name = 'T_w'
    unit = kelvin
    latex_name = r"T_w"
       


__all__ = (
    'a_s',
    'a_sh',
    'C_wa',
    'C_wl',
    'E_lmol',
    'E_l',
    'epsilon_l',
    'g_bw',
    'g_bwmol',
    'g_sw',
    'g_swmol',
    'g_tw',
    'g_twmol',
    'H_l',
    'L_l',
    'P_wl',
    'r_bw',
    'r_sw',
    'r_tw',
    'rho_al',
    'R_ll',
    'T_l',
    'T_w',
)