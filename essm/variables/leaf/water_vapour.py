"""Leaf water vapour exchange and energy balance."""

from __future__ import absolute_import

from sage.symbolic.units import units

from .._core import Variable

# Used units
meter = units.length.meter


class B_l(Variable):
    """Boundary layer thickness"""

    unit = meter


__all__ = ('B_l', )
