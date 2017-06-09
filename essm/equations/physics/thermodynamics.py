"""General and atmospheric thermodynamics equations."""

from __future__ import division

from essm.equations import Equation
from essm.variables import Variable
from essm.variables.leaf.unsorted import C_wa, L_l, rho_al
from essm.variables.physics.thermodynamics import (
    M_N2, M_O2, P_N2, P_O2, D_va, Gr, Le, M_w, Nu, P_a, P_wa, Pr, R_mol, Re,
    Re_c, T_a, alpha_a, g, h_c, k_a, nu_a, rho_a, v_w, x_N2, x_O2)
from essm.variables.units import joule, kelvin, meter, second
from sage.all import sqrt


class eq_Le(Equation):
    """Le as function of alpha_a and D_va."""

    expr = Le == alpha_a / D_va


class eq_Cwa(Equation):
    """C_wa as a function of P_wa and T_a."""

    expr = C_wa == P_wa / (R_mol * T_a)


class eq_hc(Equation):
    """h_c as a function of Nu and L_l."""

    expr = h_c == Nu * k_a / L_l


class eq_Re(Equation):
    """Re as a function of v_w and L_l."""

    expr = Re == L_l * v_w / nu_a


class eq_Gr(Equation):
    """Gr as function of air density within and outside of leaf."""

    expr = Gr == L_l**3 * g * (rho_a - rho_al) / (nu_a**2 * rho_al)


class eq_Nu_forced_all(Equation):
    """Nu as function of Re and Re_c under forced conditions."""

    expr = Nu == Pr**(1 / 3) * (
        -0.0370000000000000 * (Re + Re_c - 1 / 2 * abs(Re - Re_c))**
        (4 / 5) + 0.0370000000000000 * Re**
        (4 / 5) + 0.664000000000000 * sqrt(Re + Re_c - 1 / 2 * abs(Re - Re_c)))


class eq_Dva(Equation):
    """D_va as a function of air temperature"""

    class p_Dva1(Variable):
        """Internal parameter of eq_Dva."""
        name = 'p_Dva1'
        unit = meter**2 / (kelvin * second)
        domain = 'real'
        latex_name = 'p_Dva1'
        default = 1.49e-07

    class p_Dva2(Variable):
        """Internal parameter of eq_Dva."""
        name = 'p_Dva2'
        unit = meter**2 / second
        domain = 'real'
        latex_name = 'p_Dva2'
        default = 1.96e-05

    expr = D_va == T_a * p_Dva1 - p_Dva2


class eq_alphaa(Equation):
    """alpha_a as a function of air temperature"""

    class p_alpha1(Variable):
        """Internal parameter of eq_alphaa."""
        name = 'p_alpha1'
        unit = meter**2 / (kelvin * second)
        domain = 'real'
        latex_name = 'p_alpha1'
        default = 1.32e-07

    class p_alpha2(Variable):
        """Internal parameter of eq_alphaa."""
        name = 'p_alpha2'
        unit = meter**2 / second
        domain = 'real'
        latex_name = 'p_alpha2'
        default = 1.73e-05

    expr = alpha_a == T_a * p_alpha1 - p_alpha2


class eq_ka(Equation):
    """k_a as a function of air temperature"""

    class p_ka1(Variable):
        """Internal parameter of eq_ka."""
        name = 'p_ka1'
        unit = joule / (kelvin**2 * meter * second)
        domain = 'real'
        latex_name = 'p_ka1'
        default = 6.84e-05

    class p_ka2(Variable):
        """Internal parameter of eq_ka."""
        name = 'p_ka2'
        unit = joule / (kelvin * meter * second)
        domain = 'real'
        latex_name = 'p_ka2'
        default = 5.63e-03

    expr = k_a == T_a * p_ka1 + p_ka2


class eq_nua(Equation):
    """nu_a as a function of air temperature"""

    class p_nua1(Variable):
        """Internal parameter of eq_nua."""
        name = 'p_nua1'
        unit = meter**2 / (kelvin * second)
        domain = 'real'
        latex_name = 'p_nua1'
        default = 9.e-08

    class p_nua2(Variable):
        """Internal parameter of eq_nua."""
        name = 'p_nua2'
        unit = meter**2 / second
        domain = 'real'
        latex_name = 'p_nua2'
        default = 1.13e-05

    expr = nu_a == T_a * p_nua1 - p_nua2


class eq_rhoa_Pwa_Ta(Equation):
    """rho_a as a function of P_wa and T_a."""

    expr = rho_a == (M_N2 * P_N2 + M_O2 * P_O2 + M_w * P_wa) / (R_mol * T_a)


class eq_Pa(Equation):
    """Calculate air pressure from partial pressures of N2, O2 and H2O."""

    expr = P_a == P_N2 + P_O2 + P_wa


class eq_PN2_PO2(Equation):
    """Calculate P_N2 as a function of P_O2."""

    expr = P_N2 == P_O2 * x_N2 / x_O2


class eq_PO2(eq_Pa, eq_PN2_PO2):
    """Calculate P_O2 as a function of P_a, P_N2 and P_wa."""

    expr = P_O2 == (P_a * x_O2 - P_wa * x_O2) / (x_N2 + x_O2)


class eq_PN2(eq_Pa, eq_PN2_PO2):
    """Calculate P_N2 as a function of P_a, P_O2 and P_wa."""

    expr = P_N2 == (P_a * x_N2 - P_wa * x_N2) / (x_N2 + x_O2)


class eq_rhoa(eq_rhoa_Pwa_Ta, eq_PN2, eq_PO2):
    """Calculate rho_a from T_a, P_a and P_wa."""

    expr = rho_a == ((M_N2 * P_a - (M_N2 - M_w) * P_wa) * x_N2 +
                     (M_O2 * P_a - (M_O2 - M_w) * P_wa) * x_O2) / (
                         R_mol * T_a * x_N2 + R_mol * T_a * x_O2)


__all__ = (
    'eq_Le', 'eq_Cwa', 'eq_hc', 'eq_Re', 'eq_Gr', 'eq_Nu_forced_all', 'eq_Dva',
    'eq_alphaa', 'eq_ka', 'eq_nua', 'eq_rhoa_Pwa_Ta', 'eq_Pa', 'eq_PN2_PO2',
    'eq_PO2', 'eq_PN2', 'eq_rhoa', )
