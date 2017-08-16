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

import functools
import operator
import sympy.physics.units as u
from sympy.physics.units import find_unit, Dimension, Quantity

from .SI import SI

joule = u.joule
kelvin = u.kelvin
kilogram = u.kilogram
meter = u.meter
mole = u.mole
pascal = u.pascal
second = u.second
watt = u.watt
BASEUNITS = set(str(unit) for unit in SI._base_units)


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
    """Derive SI-unit from an expression, omitting scale factors."""
    # Get dimensions of expr
    dim_expr = Quantity.get_dimensional_expr(expr)

    # Generate dictionary with standard units to substitute into dim_expr
    units = {}
    for dim in dim_expr.free_symbols:
        dimension1 = Dimension(dim)

        # Get base dimensions (e.g. length**3 instead of volume)
        dimensional_dependencies = dimension1.get_dimensional_dependencies()

        # Generate dictionary with standard units of each base dimension
        units1 = []
        for dim1 in dimensional_dependencies.keys():
            unit = list(set(find_unit(dim1)) & (BASEUNITS))[0]
            units1.append(eval('u.' + unit) ** dimensional_dependencies[dim1])
        units_dim = functools.reduce(operator.mul, units1)
        units[dim] = units_dim
    return dim_expr.subs(units)


__all__ = (
    'derive_unit', 'derive_quantity', 'markdown', 'joule', 'kelvin',
    'kilogram', 'meter', 'mole', 'pascal', 'second', 'unit_symbols', 'watt')
