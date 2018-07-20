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
"""Leaf energy and water balance equations."""

from __future__ import division

from essm import Eq, e
from essm.equations import Equation
from essm.variables import Variable
from essm.variables.leaf.energy_water import (C_wl, E_l, E_lmol, Gr, H_l, L_l,
                                              P_wl, R_ll, T_l, T_w, a_s, a_sh,
                                              epsilon_l, g_bw, g_sw, g_tw,
                                              g_twmol, h_c, rho_al)
from essm.variables.physics.thermodynamics import (C_wa, Le, M_w, Nu, P_a,
                                                   P_wa, R_mol, R_s, Re, T_a,
                                                   c_pa, g, k_a, lambda_E,
                                                   nu_a, rho_a, sigm, v_w)
from essm.variables.units import kelvin, pascal


class eq_Rs_enbal(Equation):
    """Calculate R_s from energy balance.

    (Eq. 1 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(R_s, E_l + H_l + R_ll)


class eq_Rll(Equation):
    """R_ll as function of T_l and T_w.

    (Eq. 2 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(R_ll, (T_l ** 4 - T_w ** 4) * a_sh * epsilon_l * sigm)


class eq_Hl(Equation):
    """H_l as function of T_l.

    (Eq. 3 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(H_l, -(T_a - T_l) * a_sh * h_c)


class eq_El(Equation):
    """E_l as function of E_lmol.

    (Eq. 4 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(E_l, E_lmol * M_w * lambda_E)


class eq_Elmol(Equation):
    """E_lmol as functino of g_tw and C_wl.

    (Eq. 5 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(E_lmol, -(C_wa - C_wl) * g_tw)


class eq_gtw(Equation):
    """g_tw from g_sw and g_bw.

    (Eq. 6 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(g_tw, (1 / (1 / g_bw + 1 / g_sw)))


class eq_gbw_hc(Equation):
    """g_bw as function of h_c.

    (Eq. B2 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(g_bw, a_s * h_c / (Le ** (2 / 3) * c_pa * rho_a))


class eq_Cwl(Equation):
    """C_wl as function of P_wl and T_l.

    (Eq. B4 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(C_wl, P_wl / (R_mol * T_l))


class eq_Pwl(Equation):
    """Clausius-Clapeyron P_wl as function of T_l.

    (Eq. B3 in :cite:`hartmann_global_1994`)
    """

    class p_CC1(Variable):
        """Internal parameter of eq_Pwl."""

        name = 'p_CC1'
        unit = pascal
        domain = 'real'
        latex_name = 'p_1'
        default = 611.

    class p_CC2(Variable):
        """Internal parameter of eq_Pwl."""

        name = 'p_CC2'
        unit = kelvin
        domain = 'real'
        latex_name = 'p_2'
        default = 273.

    expr = Eq(
        P_wl, p_CC1 * e ** (-M_w * lambda_E * (1 / T_l - 1 / p_CC2) / R_mol)
    )


class eq_Elmol_conv(Equation):
    """E_lmol as function of g_twmol and P_wl.

    (Eq. B6 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(E_lmol, -(P_wa - P_wl) * g_twmol / P_a)


class eq_gtwmol_gtw(eq_Elmol.definition, eq_Cwl.definition,
                    eq_Elmol_conv.definition):
    """g_twmol as a function of g_tw.

    It uses eq_Elmol, eq_Cwl and eq_Elmol_conv.
    """

    expr = Eq(
        g_twmol, -(P_a * P_wl * T_a - P_a * P_wa * T_l) * g_tw /
        ((P_wa - P_wl) * R_mol * T_a * T_l)
    )


class eq_gtwmol_gtw_iso(eq_gtwmol_gtw.definition):
    """g_twmol as a function of g_tw at isothermal conditions."""

    expr = Eq(g_twmol, P_a * g_tw / (R_mol * T_a))


class eq_hc(Equation):
    """h_c as a function of Nu and L_l.

    (Eq. B10 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(h_c, Nu * k_a / L_l)


class eq_Re(Equation):
    """Re as a function of v_w and L_l.

    (Eq. B11 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(Re, L_l * v_w / nu_a)


class eq_Gr(Equation):
    """Gr as function of air density within and outside of leaf.

    (Eq. B12 in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(Gr, L_l ** 3 * g * (rho_a - rho_al) / (nu_a ** 2 * rho_al))


__all__ = (
    'eq_Rs_enbal',
    'eq_Rll',
    'eq_Hl',
    'eq_El',
    'eq_Elmol',
    'eq_gtw',
    'eq_gbw_hc',
    'eq_Cwl',
    'eq_Pwl',
    'eq_Elmol_conv',
    'eq_gtwmol_gtw',
    'eq_gtwmol_gtw_iso',
    'eq_hc',
    'eq_Re',
    'eq_Gr',
)
