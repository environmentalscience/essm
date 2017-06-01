"""General physics variables."""

from __future__ import absolute_import

from essm.variables import Variable
from essm.variables.units import joule, kelvin, kilogram, meter, \
    mole, pascal, second


class alpha_a(Variable):
    """Thermal diffusivity of dry air"""
    name = 'alpha_a'
    domain = 'real'
    unit = meter**2 / second
    latex_name = r"\alpha_a"


class c_pa(Variable):
    """Specific heat of dry air. """
    name = 'c_pa'
    domain = 'real'
    unit = joule / (kelvin * kilogram)
    latex_name = r"c_{pa}"
    default = 1010


class c_pamol(Variable):
    """Molar specific heat of dry air."""
    name = 'c_pamol'
    domain = 'real'
    unit = joule / (kelvin * mole)
    latex_name = r"c_{pa,mol}"
    default = 29.19


class D_va(Variable):
    """Binary diffusion coefficient of water vapour in air"""
    name = 'D_va'
    domain = 'real'
    unit = meter**2 / second
    latex_name = r"D_{va}"


class g(Variable):
    """Gravitational acceleration (9.81)"""
    name = 'g'
    domain = 'real'
    unit = meter / second**2
    latex_name = r"g"
    default = 9.81


class Gr(Variable):
    """Grashof number"""
    name = 'Gr'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Gr_L}"


class k_a(Variable):
    """Thermal conductivity of dry air"""
    name = 'k_a'
    domain = 'real'
    unit = joule / (kelvin * meter * second)
    latex_name = r"k_a"


class lambda_E(Variable):
    """Latent heat of evaporation (2.45e6)"""
    name = 'lambda_E'
    domain = 'real'
    unit = joule / kilogram
    latex_name = r"\lambda_E"
    default = 2.45e6


class Le(Variable):
    """Lewis number"""
    name = 'Le'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Le}"


class M_N2(Variable):
    """Molar mass of nitrogen (0.028)"""
    name = 'M_N2'
    domain = 'real'
    unit = kilogram / mole
    latex_name = r"M_{N_2}"
    default = 0.028


class M_O2(Variable):
    """Molar mass of oxygen (0.032)"""
    name = 'M_O2'
    domain = 'real'
    unit = kilogram / mole
    latex_name = r"M_{O_2}"
    default = 0.032


class M_w(Variable):
    """Molar mass of water (0.018)"""
    name = 'M_w'
    domain = 'real'
    unit = kilogram / mole
    latex_name = r"M_w"
    default = 0.018


class nu_a(Variable):
    """Kinematic viscosity of dry air"""
    name = 'nu_a'
    domain = 'real'
    unit = meter**2 / second
    latex_name = r"\nu_a"


class Nu(Variable):
    """Nusselt number"""
    name = 'Nu'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Nu_L}"


class P_a(Variable):
    """Air pressure"""
    name = 'P_a'
    domain = 'real'
    unit = pascal
    latex_name = r"P_a"


class Pr(Variable):
    """Prandtl number (0.71)"""
    name = 'Pr'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Pr}"
    default = 0.71


class Re_c(Variable):
    """Critical Reynolds number for the onset of turbulence"""
    name = 'Re_c'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Re_c}"


class Re(Variable):
    """Reynolds number"""
    name = 'Re'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Re_L}"


class rho_a(Variable):
    """Density of dry air"""
    name = 'rho_a'
    domain = 'real'
    unit = kilogram / meter**3
    latex_name = r"\rho_a"


class R_mol(Variable):
    """Molar gas constant (8.314472)"""
    name = 'R_mol'
    domain = 'real'
    unit = joule / (kelvin * mole)
    latex_name = r"R_{mol}"
    default = 8.314472


class Sh(Variable):
    """Sherwood number"""
    name = 'Sh'
    domain = 'real'
    unit = 1
    latex_name = r"N_{Sh_L}"


class sigm(Variable):
    """Stefan-Boltzmann constant (5.67e-8)"""
    name = 'sigm'
    domain = 'real'
    unit = joule / (kelvin**4 * meter**2 * second)
    latex_name = r"\sigma"
    default = 5.67e-8