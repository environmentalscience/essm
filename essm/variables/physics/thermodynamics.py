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
"""General and atmospheric thermodynamics variables."""

from essm.variables import Variable
from essm.variables.units import (
    joule, kelvin, kilogram, meter, mole, pascal, second)


class alpha_a(Variable):
    """Thermal diffusivity of dry air."""
    name = 'alpha_a'
    unit = meter**2 / second
    domain = 'real'
    latex_name = '\\alpha_a'


class c_pa(Variable):
    """Specific heat of dry air."""
    name = 'c_pa'
    unit = joule / (kelvin * kilogram)
    domain = 'real'
    latex_name = 'c_{pa}'
    default = 1010.00000000000


class c_pamol(Variable):
    """Molar specific heat of dry air."""
    name = 'c_pamol'
    unit = joule / (kelvin * mole)
    domain = 'real'
    latex_name = 'c_{pa,mol}'
    default = 29.1900000000000


class D_va(Variable):
    """Binary diffusion coefficient of water vapour in air."""
    name = 'D_va'
    unit = meter**2 / second
    domain = 'real'
    latex_name = 'D_{va}'


class g(Variable):
    """Gravitational acceleration."""
    name = 'g'
    unit = meter / second**2
    domain = 'real'
    latex_name = 'g'
    default = 9.81000000000000


class Gr(Variable):
    """Grashof number."""
    name = 'Gr'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Gr_L}'


class h_c(Variable):
    """Average 1-sided convective transfer coefficient."""
    name = 'h_c'
    unit = joule / (kelvin * meter**2 * second)
    domain = 'real'
    latex_name = 'h_c'


class k_a(Variable):
    """Thermal conductivity of dry air."""
    name = 'k_a'
    unit = joule / (kelvin * meter * second)
    domain = 'real'
    latex_name = 'k_a'


class lambda_E(Variable):
    """Latent heat of evaporation."""
    name = 'lambda_E'
    unit = joule / kilogram
    domain = 'real'
    latex_name = '\\lambda_E'
    default = 2.45000000000000e6


class Le(Variable):
    """Lewis number."""
    name = 'Le'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Le}'


class M_N2(Variable):
    """Molar mass of nitrogen."""
    name = 'M_N2'
    unit = kilogram / mole
    domain = 'real'
    latex_name = 'M_{N_2}'
    default = 0.0280000000000000


class M_O2(Variable):
    """Molar mass of oxygen."""
    name = 'M_O2'
    unit = kilogram / mole
    domain = 'real'
    latex_name = 'M_{O_2}'
    default = 0.0320000000000000


class M_w(Variable):
    """Molar mass of water."""
    name = 'M_w'
    unit = kilogram / mole
    domain = 'real'
    latex_name = 'M_w'
    default = 0.0180000000000000


class nu_a(Variable):
    """Kinematic viscosity of dry air."""
    name = 'nu_a'
    unit = meter**2 / second
    domain = 'real'
    latex_name = '\\nu_a'


class Nu(Variable):
    """Nusselt number."""
    name = 'Nu'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Nu_L}'


class P_a(Variable):
    """Air pressure."""
    name = 'P_a'
    unit = pascal
    domain = 'real'
    latex_name = 'P_a'


class Pr(Variable):
    """Prandtl number (0.71 for air)."""
    name = 'Pr'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Pr}'


class P_N2(Variable):
    """Partial pressure of nitrogen."""
    name = 'P_N2'
    unit = pascal
    domain = 'real'
    latex_name = 'P_{N2}'


class P_O2(Variable):
    """Partial pressure of oxygen."""
    name = 'P_O2'
    unit = pascal
    domain = 'real'
    latex_name = 'P_{O2}'


class P_wa(Variable):
    """Vapour pressure in the atmosphere."""
    name = 'P_wa'
    unit = pascal
    domain = 'real'
    latex_name = 'P_{wa}'


class P_was(Variable):
    """Saturation vapour pressure at air temperature."""
    name = 'P_was'
    unit = pascal
    domain = 'real'
    latex_name = 'P_{was}'


class Re_c(Variable):
    """Critical Reynolds number for the onset of turbulence."""
    name = 'Re_c'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Re_c}'


class Re(Variable):
    """Reynolds number."""
    name = 'Re'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Re_L}'


class rho_a(Variable):
    """Density of dry air."""
    name = 'rho_a'
    unit = kilogram / meter**3
    domain = 'real'
    latex_name = '\\rho_a'


class R_mol(Variable):
    """Molar gas constant."""
    name = 'R_mol'
    unit = joule / (kelvin * mole)
    domain = 'real'
    latex_name = 'R_{mol}'
    default = 8.31447200000000


class R_s(Variable):
    """Solar shortwave flux per area."""
    name = 'R_s'
    unit = joule / (meter**2 * second)
    domain = 'real'
    latex_name = 'R_s'


class Sh(Variable):
    """Sherwood number."""
    name = 'Sh'
    unit = 1 / 1
    domain = 'real'
    latex_name = 'N_{Sh_L}'


class sigm(Variable):
    """Stefan-Boltzmann constant."""
    name = 'sigm'
    unit = joule / (kelvin**4 * meter**2 * second)
    domain = 'real'
    latex_name = '\\sigma'
    default = 5.67000000000000e-8


class T_a(Variable):
    """Air temperature."""
    name = 'T_a'
    unit = kelvin
    domain = 'real'
    latex_name = 'T_a'


class v_w(Variable):
    """Wind velocity."""
    name = 'v_w'
    unit = meter / second
    domain = 'real'
    latex_name = 'v_w'


class x_N2(Variable):
    """Mole fraction of nitrogen in dry air."""
    name = 'x_N2'
    unit = 1
    domain = 'real'
    latex_name = 'x_{N2}'
    default = 0.790000000000000


class x_O2(Variable):
    """Mole fraction of oxygen in dry air."""
    name = 'x_O2'
    unit = 1
    domain = 'real'
    latex_name = 'x_{N2}'
    default = 0.210000000000000


__all__ = (
    'alpha_a', 'c_pa', 'c_pamol', 'D_va', 'g', 'Gr', 'h_c', 'k_a', 'lambda_E',
    'Le', 'M_N2', 'M_O2', 'M_w', 'nu_a', 'Nu', 'P_a', 'Pr', 'P_N2', 'P_O2',
    'P_wa', 'P_was', 'Re_c', 'Re', 'rho_a', 'R_mol', 'R_s', 'Sh', 'sigm',
    'T_a', 'v_w', 'x_N2', 'x_O2', )
