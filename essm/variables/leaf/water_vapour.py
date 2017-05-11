"""Leaf water vapour exchange and energy balance."""

from __future__ import absolute_import

from sage.symbolic.units import units

from .._core import Variable, register

# Used units
meter = units.length.meter

@register
class B_l(Variable):
    """Boundary layer thickness"""

    unit = meter
