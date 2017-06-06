"""Unsorted equations related to leaf model"""

from essm.variables.physics.thermodynamics import D_va, Le, M_w, R_mol, R_s, Sh, T_a, c_pa, h_c, lambda_E, rho_a, sigm
from sage.all import e, pi
from essm.variables.units import kelvin, pascal
from essm.variables.leaf.unsorted import C_wa, C_wl, E_l, E_lmol, H_l, L_l, P_wl, R_ll, T_l, T_w, a_s, a_sh, epsilon_l, g_bw, g_sw, g_tw
from essm.variables import Variable
from essm.equations import Equation

class eq_Rs_enbal(Equation):
    """Calculate R_s from energy balance."""
    
    expr = R_s == E_l + H_l + R_ll


class eq_Rll(Equation):
    """R_ll as function of T_l and T_w."""
    
    expr = R_ll == (T_l**4 - T_w**4)*a_sh*epsilon_l*sigm


class eq_Hl(Equation):
    """H_l as function of T_l."""
    
    expr = H_l == -(T_a - T_l)*a_sh*h_c


class eq_El(Equation):
    """E_l as function of E_lmol."""
    
    expr = E_l == E_lmol*M_w*lambda_E


class eq_Elmol(Equation):
    """E_lmol as functino of g_tw and C_wl."""
    
    expr = E_lmol == -(C_wa - C_wl)*g_tw


class eq_gtw(Equation):
    """g_tw from g_sw and g_bw."""
    
    expr = g_tw == (1/(1/g_bw + 1/g_sw))


class eq_gbw(Equation):
    """g_bw as function of Sh and L_l."""
    
    expr = g_bw == D_va*Sh/L_l


class eq_gbw_hc(Equation):
    """g_bw as function of h_c."""
    
    expr = g_bw == a_s*h_c/(Le**(2/3)*c_pa*rho_a)


class eq_Cwl(Equation):
    """C_wl as function of P_wl and T_l."""
    
    expr = C_wl == P_wl/(R_mol*T_l)


class eq_Pwl(Equation):
    """Clausius-Clapeyron P_wl as function of T_l. \citep[Eq. B.3]{hartmann_global_1994}"""
        
    class p_CC1(Variable):
        """Internal parameter of eq_Pwl."""
        name = 'p_CC1'
        unit = pascal
        domain = 'real'
        latex_name = 'p_CC1'
        default = 611.   
    
    
    
    class p_CC2(Variable):
        """Internal parameter of eq_Pwl."""
        name = 'p_CC2'
        unit = kelvin
        domain = 'real'
        latex_name = 'p_CC2'
        default = 273.   
    
    expr = P_wl == p_CC1*e**(-M_w*lambda_E*(1/T_l - 1/p_CC2)/R_mol)


__all__ = (
    'eq_Rs_enbal',
    'eq_Rll',
    'eq_Hl',
    'eq_El',
    'eq_Elmol',
    'eq_gtw',
    'eq_gbw',
    'eq_gbw_hc',
    'eq_Cwl',
    'eq_Pwl',
)