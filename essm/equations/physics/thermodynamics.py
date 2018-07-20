# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017 ETH Zurich, Swiss Data Science Center.
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
"""General and atmospheric thermodynamics equations."""

from __future__ import division

from essm import Eq, sqrt
from essm.equations import Equation
from essm.variables import Variable
from essm.variables.physics.thermodynamics import (M_N2, M_O2, P_N2, P_O2,
                                                   C_wa, D_va, Le, M_w, Nu,
                                                   P_a, P_wa, Pr, R_mol, Re,
                                                   Re_c, T_a, alpha_a, k_a,
                                                   nu_a, rho_a, x_N2, x_O2)
from essm.variables.units import joule, kelvin, meter, second


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
        Nu, -1 / 1000 * Pr ** (1 / 3) * (
            37 * (Re + Re_c - 1 / 2 * abs(Re - Re_c)) ** (4 / 5) - 37 * Re **
            (4 / 5) - 664 * sqrt(Re + Re_c - 1 / 2 * abs(Re - Re_c))
        )
    )


class eq_Dva(Equation):
    """D_va as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_Dva1(Variable):
        """Internal parameter of eq_Dva."""

        name = 'p_Dva1'
        unit = meter ** 2 / (kelvin * second)
        domain = 'real'
        latex_name = 'p_1'
        default = 1.49e-07

    class p_Dva2(Variable):
        """Internal parameter of eq_Dva."""

        name = 'p_Dva2'
        unit = meter ** 2 / second
        domain = 'real'
        latex_name = 'p_2'
        default = 1.96e-05

    expr = Eq(D_va, T_a * p_Dva1 - p_Dva2)


class eq_alphaa(Equation):
    """alpha_a as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_alpha1(Variable):
        """Internal parameter of eq_alphaa."""

        name = 'p_alpha1'
        unit = meter ** 2 / (kelvin * second)
        domain = 'real'
        latex_name = 'p_1'
        default = 1.32e-07

    class p_alpha2(Variable):
        """Internal parameter of eq_alphaa."""

        name = 'p_alpha2'
        unit = meter ** 2 / second
        domain = 'real'
        latex_name = 'p_2'
        default = 1.73e-05

    expr = Eq(alpha_a, T_a * p_alpha1 - p_alpha2)


class eq_ka(Equation):
    """k_a as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_ka1(Variable):
        """Internal parameter of eq_ka."""

        name = 'p_ka1'
        unit = joule / (kelvin ** 2 * meter * second)
        domain = 'real'
        latex_name = 'p_1'
        default = 6.84e-05

    class p_ka2(Variable):
        """Internal parameter of eq_ka."""

        name = 'p_ka2'
        unit = joule / (kelvin * meter * second)
        domain = 'real'
        latex_name = 'p_2'
        default = 5.63e-03

    expr = Eq(k_a, T_a * p_ka1 + p_ka2)


class eq_nua(Equation):
    """nu_a as a function of air temperature.

    (Table A.3 in :cite:`monteith_principles_2007`)
    """

    class p_nua1(Variable):
        """Internal parameter of eq_nua."""

        name = 'p_nua1'
        unit = meter ** 2 / (kelvin * second)
        domain = 'real'
        latex_name = 'p_1'
        default = 9.e-08

    class p_nua2(Variable):
        """Internal parameter of eq_nua."""

        name = 'p_nua2'
        unit = meter ** 2 / second
        domain = 'real'
        latex_name = 'p_2'
        default = 1.13e-05

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


class eq_PO2(eq_Pa.definition, eq_PN2_PO2.definition):
    """Calculate P_O2 as a function of P_a, P_N2 and P_wa."""

    expr = Eq(P_O2, (P_a * x_O2 - P_wa * x_O2) / (x_N2 + x_O2))


class eq_PN2(eq_Pa.definition, eq_PN2_PO2.definition):
    """Calculate P_N2 as a function of P_a, P_O2 and P_wa."""

    expr = Eq(P_N2, (P_a * x_N2 - P_wa * x_N2) / (x_N2 + x_O2))


class eq_rhoa(eq_rhoa_Pwa_Ta.definition, eq_PN2.definition, eq_PO2.definition):
    """Calculate rho_a from T_a, P_a and P_wa."""

    expr = Eq(
        rho_a, ((M_N2 * P_a - (M_N2 - M_w) * P_wa) * x_N2 +
                (M_O2 * P_a - (M_O2 - M_w) * P_wa) * x_O2) /
        (R_mol * T_a * x_N2 + R_mol * T_a * x_O2)
    )


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
    'eq_PO2',
    'eq_PN2',
    'eq_rhoa',
)
