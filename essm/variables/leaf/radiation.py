"""Leaf radiation balance."""

from __future__ import absolute_import

from sage.symbolic.units import units

from .._core import Variable, register

# Used units
joule = units.energy.joule
kilogram = units.mass.kilogram
kelvin = units.temperature.kelvin
meter = units.length.meter
second = units.time.second
watt = units.power.watt


@register
class alpha_l(Variable):
    """Leaf albedo, fraction of shortwave radiation reflected by the leaf"""

    unit = watt / watt


@register
class R_d(Variable):
    """Downwelling global radiation"""

    unit = joule / second / meter ** 2


@register
class R_la(Variable):
    """Longwave radiation absorbed by leaf"""

    unit = joule / second / meter ** 2
    latex_name = 'R_{la}'


@register
class R_ld(Variable):
    """Downwards emitted/reflected global radiation from leaf"""

    unit = joule / second / meter ** 2
    latex_name = 'R_{ld}'


@register
class R_lu(Variable):
    """Upwards emitted/reflected global radiation from leaf"""

    unit = joule / second / meter ** 2
    latex_name = 'R_{lu}'


@register
class R_u(Variable):
    """Upwelling global radiation"""

    unit = joule / second / meter ** 2


@register
class S_a(Variable):
    """Radiation sensor above leaf reading"""

    unit = joule / second / meter ** 2


@register
class S_b(Variable):
    """Radiation sensor below leaf reading"""

    unit = joule / second / meter ** 2


@register
class S_s(Variable):
    """Radiation sensor beside leaf reading"""

    unit = joule / second / meter ** 2
