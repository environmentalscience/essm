"""Chamber insulation material."""

from __future__ import absolute_import

from sage.symbolic.units import units

from .._core import Variable

# Used units
joule = units.energy.joule
kilogram = units.mass.kilogram
kelvin = units.temperature.kelvin
meter = units.length.meter
second = units.time.second


class c_pi(Variable):
    """Heat capacity of insulation material."""

    unit = joule / kilogram / kelvin
    latex_name = 'c_{pi}'


class lambda_i(Variable):
    """Heat conductivity of insulation material"""

    unit = joule / second / meter / kelvin


class rho_i(Variable):
    """Density of insulation material"""

    unit = kilogram / meter ** 3


class L_i(Variable):
    """Thickness of insulation material"""

    unit = meter


class A_i(Variable):
    """Conducting area of insulation material"""

    unit = meter ** 2


class Q_i(Variable):
    """Heat conduction through insulation material"""

    unit = joule / second


class dT_i(Variable):
    """Temperature increment of insulation material"""

    unit = kelvin

__all__ = (
    'c_pi',
    'lambda_i',
    'rho_i',
    'L_i',
    'A_i',
    'Q_i',
    'dT_i',
)
