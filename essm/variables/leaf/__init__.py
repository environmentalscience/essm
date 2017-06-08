"""Leaf related variables."""

from __future__ import absolute_import

# Trick to force the variable registration
from . import radiation, water_vapour

__all__ = ('radiation', 'water_vapour', )
