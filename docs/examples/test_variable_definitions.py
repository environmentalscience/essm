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
"""Variables defined in api_features.ipynb and dependencies."""

from sympy.physics.units import (
    joule, kelvin, kilogram, meter, mole, pascal, second, watt
)

from essm.variables import Variable


class alpha_a(Variable):
    """Thermal diffusivity of dry air."""

    name = 'alpha_a'
    unit = meter ** 2 / second
    assumptions = {'real': True}
    latex_name = '\\alpha_a'


class c_pa(Variable):
    """Specific heat of dry air."""

    name = 'c_pa'
    unit = joule / (kelvin * kilogram)
    assumptions = {'real': True}
    latex_name = 'c_{pa}'
    default = 1010.0


class c_pamol(Variable):
    """Molar specific heat of dry air.

    https://en.wikipedia.org/wiki/Heat_capacity#Specific_heat_capacity
    """

    name = 'c_pamol'
    unit = joule / (kelvin * mole)
    assumptions = {'real': True}
    latex_name = 'c_{pa,mol}'
    default = 29.19


class c_pv(Variable):
    """Specific heat of water vapour at 300 K.

    http://www.engineeringtoolbox.com/water-vapor-d_979.html
    """

    name = 'c_pv'
    unit = joule / (kelvin * kilogram)
    assumptions = {'real': True}
    latex_name = 'c_{pv}'
    default = 1864


class C_wa(Variable):
    """Concentration of water in air."""

    name = 'C_wa'
    unit = mole / meter ** 3
    assumptions = {'real': True}
    latex_name = 'C_{wa}'


class D_va(Variable):
    """Binary diffusion coefficient of water vapour in air."""

    name = 'D_va'
    unit = meter ** 2 / second
    assumptions = {'real': True}
    latex_name = 'D_{va}'


class g(Variable):
    """Gravitational acceleration."""

    name = 'g'
    unit = meter / second ** 2
    assumptions = {'real': True}
    latex_name = 'g'
    default = 9.81


class Gr(Variable):
    """Grashof number."""

    name = 'Gr'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'N_{Gr_L}'


class h_c(Variable):
    """Average 1-sided convective heat transfer coefficient."""

    name = 'h_c'
    unit = joule / (kelvin * meter ** 2 * second)
    assumptions = {'real': True}
    latex_name = 'h_c'


class k_a(Variable):
    """Thermal conductivity of dry air."""

    name = 'k_a'
    unit = joule / (kelvin * meter * second)
    assumptions = {'real': True}
    latex_name = 'k_a'


class lambda_E(Variable):
    """Latent heat of evaporation."""

    name = 'lambda_E'
    unit = joule / kilogram
    assumptions = {'real': True}
    latex_name = '\\lambda_E'
    default = 2450000.0


class Le(Variable):
    """Lewis number."""

    name = 'Le'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'N_{Le}'


class M_air(Variable):
    """Molar mass of air.

    http://www.engineeringtoolbox.com/molecular-mass-air-d_679.html
    """

    name = 'M_air'
    unit = kilogram / mole
    assumptions = {'real': True}
    latex_name = 'M_{air}'
    default = 0.02897


class M_N2(Variable):
    """Molar mass of nitrogen."""

    name = 'M_N2'
    unit = kilogram / mole
    assumptions = {'real': True}
    latex_name = 'M_{N_2}'
    default = 0.028


class M_O2(Variable):
    """Molar mass of oxygen."""

    name = 'M_O2'
    unit = kilogram / mole
    assumptions = {'real': True}
    latex_name = 'M_{O_2}'
    default = 0.032


class M_w(Variable):
    """Molar mass of water."""

    name = 'M_w'
    unit = kilogram / mole
    assumptions = {'real': True}
    latex_name = 'M_w'
    default = 0.018


class nu_a(Variable):
    """Kinematic viscosity of dry air."""

    name = 'nu_a'
    unit = meter ** 2 / second
    assumptions = {'real': True}
    latex_name = '\\nu_a'


class Nu(Variable):
    """Average Nusselt number over given length."""

    name = 'Nu'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'N_{Nu_L}'


class P_a(Variable):
    """Air pressure."""

    name = 'P_a'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_a'


class Pr(Variable):
    """Prandtl number (0.71 for air)."""

    name = 'Pr'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'N_{Pr}'


class P_N2(Variable):
    """Partial pressure of nitrogen."""

    name = 'P_N2'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_{N2}'


class P_O2(Variable):
    """Partial pressure of oxygen."""

    name = 'P_O2'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_{O2}'


class P_wa(Variable):
    """Partial pressure of water vapour in air."""

    name = 'P_wa'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_{wa}'


class P_was(Variable):
    """Saturation water vapour pressure at air temperature."""

    name = 'P_was'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_{was}'


class R_d(Variable):
    """Downwelling global radiation."""

    name = 'R_d'
    unit = watt / meter ** 2
    assumptions = {'real': True}
    latex_name = 'R_d'


class Re_c(Variable):
    """Critical Reynolds number for the onset of turbulence."""

    name = 'Re_c'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'N_{Re_c}'


class Re(Variable):
    """Average Reynolds number over given length."""

    name = 'Re'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'N_{Re_L}'


class rho_a(Variable):
    """Density of dry air."""

    name = 'rho_a'
    unit = kilogram / meter ** 3
    assumptions = {'real': True}
    latex_name = '\\rho_a'


class R_u(Variable):
    """Upwelling global radiation."""

    name = 'R_u'
    unit = watt / meter ** 2
    assumptions = {'real': True}
    latex_name = 'R_u'


class R_mol(Variable):
    """Molar gas constant."""

    name = 'R_mol'
    unit = joule / (kelvin * mole)
    assumptions = {'real': True}
    latex_name = 'R_{mol}'
    default = 8.314472


class R_s(Variable):
    """Solar shortwave flux per area."""

    name = 'R_s'
    unit = joule / (meter ** 2 * second)
    assumptions = {'real': True}
    latex_name = 'R_s'


class sigm(Variable):
    """Stefan-Boltzmann constant."""

    name = 'sigm'
    unit = joule / (kelvin ** 4 * meter ** 2 * second)
    assumptions = {'real': True}
    latex_name = '\\sigma'
    default = 5.67e-08


class T0(Variable):
    """Freezing point in Kelvin."""

    name = 'T0'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = 'T_0'
    default = 273.15


class T_a(Variable):
    """Air temperature."""

    name = 'T_a'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = 'T_a'


class v_w(Variable):
    """Wind velocity."""

    name = 'v_w'
    unit = meter / second
    assumptions = {'real': True}
    latex_name = 'v_w'


class x_N2(Variable):
    """Mole fraction of nitrogen in dry air."""

    name = 'x_N2'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'x_{N2}'
    default = 0.79


class x_O2(Variable):
    """Mole fraction of oxygen in dry air."""

    name = 'x_O2'
    unit = 1
    assumptions = {'real': True}
    latex_name = 'x_{O2}'
    default = 0.21


class p_Dva1(Variable):
    """Internal parameter of eq_Dva."""

    name = 'p_Dva1'
    unit = meter ** 2 / (kelvin * second)
    assumptions = {'real': True}
    latex_name = 'p_1'
    default = 1.49e-07


class p_Dva2(Variable):
    """Internal parameter of eq_Dva."""

    name = 'p_Dva2'
    unit = meter ** 2 / second
    assumptions = {'real': True}
    latex_name = 'p_2'
    default = 1.96e-05


class p_alpha1(Variable):
    """Internal parameter of eq_alphaa."""

    name = 'p_alpha1'
    unit = meter ** 2 / (kelvin * second)
    assumptions = {'real': True}
    latex_name = 'p_1'
    default = 1.32e-07


class p_alpha2(Variable):
    """Internal parameter of eq_alphaa."""

    name = 'p_alpha2'
    unit = meter ** 2 / second
    assumptions = {'real': True}
    latex_name = 'p_2'
    default = 1.73e-05


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


class p_nua1(Variable):
    """Internal parameter of eq_nua."""

    name = 'p_nua1'
    unit = meter ** 2 / (kelvin * second)
    assumptions = {'real': True}
    latex_name = 'p_1'
    default = 9e-08


class p_nua2(Variable):
    """Internal parameter of eq_nua."""

    name = 'p_nua2'
    unit = meter ** 2 / second
    assumptions = {'real': True}
    latex_name = 'p_2'
    default = 1.13e-05


class P_g(Variable):
    """Pressure of gas."""

    name = 'P_g'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_g'


class V_g(Variable):
    """Volume of gas."""

    name = 'V_g'
    unit = meter ** 3
    assumptions = {'real': True}
    latex_name = 'V_g'


class n_g(Variable):
    """Amount of gas."""

    name = 'n_g'
    unit = mole
    assumptions = {'real': True}
    latex_name = 'n_g'


class n_w(Variable):
    """Amount of water."""

    name = 'n_w'
    unit = mole
    assumptions = {'real': True}
    latex_name = 'n_w'


class T_g(Variable):
    """Temperature of gas."""

    name = 'T_g'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = 'T_g'


class Delta_Pwa(Variable):
    """Slope of saturated vapour pressure, $\partial P_{wa} / \partial T_g$"""

    name = 'Delta_Pwa'
    unit = pascal / kelvin
    assumptions = {'real': True}
    latex_name = '\\Delta'


class x(Variable):
    """Positive real variable."""

    name = 'x'
    unit = 1
    assumptions = {'positive': True, 'real': True}
    latex_name = 'x'


class p_CC1(Variable):
    """Internal parameter of eq_Pwl."""

    name = 'p_CC1'
    unit = pascal
    assumptions = {'real': True}
    latex_name = '611'
    default = 611.0


class p_CC2(Variable):
    """Internal parameter of eq_Pwl."""

    name = 'p_CC2'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = '273'
    default = 273.0


class T_a1(Variable):
    """Air temperature"""

    name = 'T_a1'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = 'T_{a1}'


class T_a2(Variable):
    """Air temperature"""

    name = 'T_a2'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = 'T_{a2}'


class P_wa1(Variable):
    """P_wa at T1"""

    name = 'P_wa1'
    unit = pascal
    assumptions = {'real': True}
    latex_name = 'P_{wa1}'


__all__ = (
    'alpha_a',
    'c_pa',
    'c_pamol',
    'c_pv',
    'C_wa',
    'D_va',
    'g',
    'Gr',
    'h_c',
    'k_a',
    'lambda_E',
    'Le',
    'M_air',
    'M_N2',
    'M_O2',
    'M_w',
    'nu_a',
    'Nu',
    'P_a',
    'Pr',
    'P_N2',
    'P_O2',
    'P_wa',
    'P_was',
    'R_d',
    'Re_c',
    'Re',
    'rho_a',
    'R_u',
    'R_mol',
    'R_s',
    'sigm',
    'T0',
    'T_a',
    'v_w',
    'x_N2',
    'x_O2',
    'p_Dva1',
    'p_Dva2',
    'p_alpha1',
    'p_alpha2',
    'p_ka1',
    'p_ka2',
    'p_nua1',
    'p_nua2',
    'P_g',
    'V_g',
    'n_g',
    'n_w',
    'T_g',
    'Delta_Pwa',
    'x',
    'p_CC1',
    'p_CC2',
    'T_a1',
    'T_a2',
    'P_wa1',
)
