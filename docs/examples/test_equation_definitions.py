# -*- coding: utf-8 -*-
#
# This file is for use with essm.
# Copyright (C) 2020 ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
"""Equations defined in api_features.ipynb and dependencies."""

from __future__ import division

from sympy import Abs, Eq, Integral, Piecewise, exp, sqrt
from sympy.physics.units import joule, kelvin, meter, pascal, second

from essm import Eq, sqrt
from essm.equations import Equation
from essm.variables import Variable
from test_variable_definitions import (
    M_N2, M_O2, P_N2, P_O2, C_wa, D_va, Delta_Pwa, Le, M_w, Nu, P_a, P_g, P_wa,
    P_wa1, Pr, R_mol, Re, Re_c, T_a, T_a1, T_a2, T_g, V_g, alpha_a, k_a,
    lambda_E, n_g, n_w, nu_a, p_CC1, p_CC2, rho_a, x_N2, x_O2
)


class eq_Le(Equation):
    """Le as function of alpha_a and D_va.

    (Eq. B3 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(Le, alpha_a / D_va)


class eq_Cwa(Equation):
    """C_wa as a function of P_wa and T_a.

    (Eq. B9 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(C_wa, P_wa / (R_mol * T_a))


class eq_Nu_forced_all(Equation):
    """Nu as function of Re and Re_c under forced conditions.

    (Eqs. B13--B15 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(
        Nu, -Pr ** (1 / 3) * (
            -37 * Re ** (4 / 5) + 37 * (Re + Re_c - Abs(Re - Re_c) / 2) **
            (4 / 5) - 664 * sqrt(Re + Re_c - Abs(Re - Re_c) / 2)
        ) / 1000
    )


class eq_Dva(Equation):
    """D_va as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_Dva2(Variable):
        """Internal parameter of eq_Dva."""

        name = 'p_Dva2'
        unit = meter ** 2 / second
        assumptions = {'real': True}
        latex_name = 'p_2'
        default = 1.96e-05

    class p_Dva1(Variable):
        """Internal parameter of eq_Dva."""

        name = 'p_Dva1'
        unit = meter ** 2 / (kelvin * second)
        assumptions = {'real': True}
        latex_name = 'p_1'
        default = 1.49e-07

    expr = Eq(D_va, T_a * p_Dva1 - p_Dva2)


class eq_alphaa(Equation):
    """alpha_a as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_alpha2(Variable):
        """Internal parameter of eq_alphaa."""

        name = 'p_alpha2'
        unit = meter ** 2 / second
        assumptions = {'real': True}
        latex_name = 'p_2'
        default = 1.73e-05

    class p_alpha1(Variable):
        """Internal parameter of eq_alphaa."""

        name = 'p_alpha1'
        unit = meter ** 2 / (kelvin * second)
        assumptions = {'real': True}
        latex_name = 'p_1'
        default = 1.32e-07

    expr = Eq(alpha_a, T_a * p_alpha1 - p_alpha2)


class eq_ka(Equation):
    """k_a as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_ka1(Variable):
        """Internal parameter of eq_ka."""

        name = 'p_ka1'
        unit = joule / (kelvin ** 2 * meter * second)
        assumptions = {'real': True}
        latex_name = 'p_1'
        default = 6.84e-05

    class p_ka2(Variable):
        """Internal parameter of eq_ka."""

        name = 'p_ka2'
        unit = joule / (kelvin * meter * second)
        assumptions = {'real': True}
        latex_name = 'p_2'
        default = 0.00563

    expr = Eq(k_a, T_a * p_ka1 + p_ka2)


class eq_nua(Equation):
    """nu_a as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_nua2(Variable):
        """Internal parameter of eq_nua."""

        name = 'p_nua2'
        unit = meter ** 2 / second
        assumptions = {'real': True}
        latex_name = 'p_2'
        default = 1.13e-05

    class p_nua1(Variable):
        """Internal parameter of eq_nua."""

        name = 'p_nua1'
        unit = meter ** 2 / (kelvin * second)
        assumptions = {'real': True}
        latex_name = 'p_1'
        default = 9e-08

    expr = Eq(nu_a, T_a * p_nua1 - p_nua2)


class eq_rhoa_Pwa_Ta(Equation):
    """rho_a as a function of P_wa and T_a.

    (Eq. B20 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(rho_a, (M_N2 * P_N2 + M_O2 * P_O2 + M_w * P_wa) / (R_mol * T_a))


class eq_Pa(Equation):
    """Calculate air pressure.

    From partial pressures of N2, O2 and H2O, following Dalton's law of
    partial pressures.
    """

    expr = Eq(P_a, P_N2 + P_O2 + P_wa)


class eq_PN2_PO2(Equation):
    """Calculate P_N2 as a function of P_O2.

    It follows Dalton's law of partial pressures.
    """

    expr = Eq(P_N2, P_O2 * x_N2 / x_O2)


class eq_ideal_gas_law(Equation):
    """Ideal gas law."""

    expr = Eq(P_g * V_g, R_mol * T_g * n_g)


class eq_Pwa_CC(Equation):
    """Clausius-Clapeyron P_wa as function of T_g.

    Eq. B3 in :cite{hartmann_global_1994}
    """

    class p_CC1(Variable):
        """Internal parameter of eq_Pwa_CC."""

        name = 'p_CC1'
        unit = pascal
        assumptions = {'real': True}
        latex_name = '611'
        default = 611.0

    class p_CC2(Variable):
        """Internal parameter of eq_Pwa_CC."""

        name = 'p_CC2'
        unit = kelvin
        assumptions = {'real': True}
        latex_name = '273'
        default = 273.0

    expr = Eq(
        P_wa, p_CC1 * exp(-M_w * lambda_E * (-1 / p_CC2 + 1 / T_g) / R_mol)
    )


class eq1(Equation):
    """Test"""

    expr = Eq(
        P_wa,
        Piecewise((0, T_a < 0), (
            p_CC1 * exp(-M_w * lambda_E * (-1 / p_CC2 + 1 / T_g) / R_mol), True
        ))
    )


class eq_Pwa_Delta(Equation):
    """P_wa deduced from the integral of Delta"""

    expr = Eq(P_wa, P_wa1 + Integral(Delta_Pwa, (T_g, T_a1, T_a2)))


class eq_PO2(eq_Pa.definition, eq_PN2_PO2.definition):
    """Calculate P_O2 as a function of P_a, P_N2 and P_wa."""

    expr = Eq(P_O2, (P_a * x_O2 - P_wa * x_O2) / (x_N2 + x_O2))


class eq_PN2(eq_Pa.definition, eq_PN2_PO2.definition):
    """Calculate P_N2 as a function of P_a, P_O2 and P_wa."""

    expr = Eq(P_N2, (P_a * x_N2 - P_wa * x_N2) / (x_N2 + x_O2))


class eq_rhoa(eq_PN2.definition, eq_rhoa_Pwa_Ta.definition, eq_PO2.definition):
    """Calculate rho_a from T_a, P_a and P_wa."""

    expr = Eq(
        rho_a, (
            x_N2 * (M_N2 * P_a - P_wa * (M_N2 - M_w)) + x_O2 *
            (M_O2 * P_a - P_wa * (M_O2 - M_w))
        ) / (R_mol * T_a * x_N2 + R_mol * T_a * x_O2)
    )


class eq_Pg(eq_ideal_gas_law.definition):
    """Calculate pressure of ideal gas."""

    expr = Eq(P_g, R_mol * T_g * n_g / V_g)


class eq_Pwa_nw(eq_Pg.definition):
    """Calculate vapour pressure from amount of water in gas."""

    expr = Eq(P_wa, R_mol * T_g * n_w / V_g)


__all__ = (
    'eq_Le',
    'eq_Cwa',
    'eq_Nu_forced_all',
    'eq_Dva',
    'eq_alphaa',
    'eq_ka',
    'eq_nua',
    'eq_rhoa_Pwa_Ta',
    'eq_Pa',
    'eq_PN2_PO2',
    'eq_ideal_gas_law',
    'eq_Pwa_CC',
    'eq1',
    'eq_Pwa_Delta',
    'eq_PO2',
    'eq_PN2',
    'eq_rhoa',
    'eq_Pg',
    'eq_Pwa_nw',
)
