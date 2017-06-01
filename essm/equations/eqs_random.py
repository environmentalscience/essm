"""Test."""

from essm.equations import Equation
from essm.variables.leaf.unsorted import (
    C_wa, C_wl, E_l, E_lmol, H_l, L_l, P_wl, R_ll, R_s, T_a, T_l, T_w, a_s,
    a_sh, epsilon_l, g_bw, g_sw, g_tw, h_c)
from essm.variables.physics.thermodynamics import (
    D_va, Le, M_w, R_mol, Sh, alpha_a, c_pa, lambda_E, rho_a, sigm)


class eq_Rs_enbal(Equation):
    """Calculate R_s from energy balance."""
    expr = R_s == E_l + H_l + R_ll


class eq_Rll(Equation):
    """R_ll as function of T_l and T_w."""
    expr = R_ll == (T_l**4 - T_w**4) * a_sh * epsilon_l * sigm


class eq_Hl(Equation):
    """H_l as function of T_l."""
    expr = H_l == -(T_a - T_l) * a_sh * h_c


class eq_El(Equation):
    """E_l as function of E_lmol."""
    expr = E_l == E_lmol * M_w * lambda_E


class eq_Elmol(Equation):
    """E_lmol as functino of g_tw and C_wl."""
    expr = E_lmol == -(C_wa - C_wl) * g_tw


class eq_gtw(Equation):
    """g_tw from g_sw and g_bw."""
    expr = g_tw == (1 / (1 / g_bw + 1 / g_sw))


class eq_gbw(Equation):
    """g_bw as function of Sh and L_l."""
    expr = g_bw == D_va * Sh / L_l


class eq_gbw_hc(Equation):
    """g_bw as function of h_c."""
    expr = g_bw == a_s * h_c / (Le**(2 / 3) * c_pa * rho_a)


class eq_Le(Equation):
    """Le as function of alpha_a and D_va."""
    expr = Le == alpha_a / D_va


class eq_Cwl(Equation):
    """C_wl as function of P_wl and T_l."""
    expr = C_wl == P_wl / (R_mol * T_l)


__all__ = ('eq_Rs_enbal', 'eq_Rll', 'eq_Hl', 'eq_El', 'eq_Elmol', 'eq_gtw',
           'eq_gbw', 'eq_gbw_hc', 'eq_Le', 'eq_Cwl', )
