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
"""Define unit symbols."""

import sympy.physics.units as u
from sympy.physics.units import Quantity
from sympy.physics.units.systems import natural

joule = u.joule
kelvin = u.kelvin
kilogram = u.kilogram
meter = u.meter
mole = u.mole
pascal = u.pascal
second = u.second
watt = u.watt


def markdown(unit):
    """Return markdown representation of a unit."""
    return str(unit)


def unit_symbols(expr):
    """Return unit symbols."""
    from essm.variables._core import BaseVariable, Variable

    for variable in expr.atoms(BaseVariable):
        for unit in variable.definition.unit.atoms(Quantity):
            yield unit


def derive_quantity(expr, name=None):
    """Derive a quantity from an expression."""
    factor, dimension = Quantity._collect_factor_and_dimension(expr)
    return Quantity(name or str(expr), dimension, factor)


def derive_unit(expr, name=None):
    """Derive a unit from an expression."""
    return natural.print_unit_base(derive_quantity(expr, name=name))


__all__ = (
    'derive_unit', 'derive_quantity', 'markdown', 'joule', 'kelvin',
    'kilogram', 'meter', 'mole', 'pascal', 'second', 'unit_symbols', 'watt')
