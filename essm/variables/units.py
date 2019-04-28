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
from sympy import Symbol
from sympy.physics.units import Dimension, Quantity, find_unit
from sympy.physics.units.dimensions import (amount_of_substance, capacitance,
                                            charge, conductance, dimsys_SI,
                                            energy, force, frequency,
                                            inductance, luminous_intensity,
                                            magnetic_density, magnetic_flux,
                                            power, pressure, temperature, time,
                                            voltage)
from sympy.physics.units.systems import SI

candela = u.candela
coulomb = u.coulomb
farad = u.farad
gray = u.gray
henry = u.henry
joule = u.joule
katal = u.katal
kelvin = u.kelvin
kilogram = u.kilogram
lux = u.lux
meter = u.meter
mol = mole = u.mol
newton = u.newton
ohm = u.ohm
pascal = u.pascal
second = u.second
siemens = u.siemens
tesla = u.tesla
volt = u.volt
watt = u.watt
weber = u.weber

SI_BASE_DIMENSIONS = {
    Quantity.get_dimensional_expr(d): d
    for d in SI._base_units
}

SI_EXTENDED_UNITS = list(SI._base_units) + [
    kelvin, candela, lux, mol, newton, pascal, joule, watt, coulomb, volt,
    farad, ohm, siemens, weber, tesla, henry
]
SI_EXTENDED_DIMENSIONS = {
    Quantity.get_dimensional_expr(d): d
    for d in SI_EXTENDED_UNITS
}


def markdown(unit):
    """Return markdown representation of a unit."""
    from sympy.printing import StrPrinter
    from operator import itemgetter
    # displays short units (m instead of meter)
    StrPrinter._print_Quantity = lambda self, expr: str(expr.abbrev)
    if unit.is_Pow:
        item = unit.args
        return '{0}$^{{{1}}}$'.format(item[0], item[1])
    if unit.is_Mul:
        str1 = ''
        tuples = []
        allargs = unit.args
        for arg in allargs:
            if arg.is_Pow:
                args = arg.args
                tuples.append((str(args[0]), args[1]))
            if isinstance(arg, Quantity):
                tuples.append((str(arg), 1))
        tuples.sort(key=itemgetter(1), reverse=True)
        tuples.sort(key=itemgetter(0))
        for item in tuples:
            if item[1] == 1:
                str1 = str1 + ' ' + item[0]
            else:
                str1 = str1 + ' {0}$^{{{1}}}$'.format(item[0], item[1])
        return str1.strip()
    else:
        return str(unit)


def unit_symbols(expr):
    """Return unit symbols."""
    from essm.variables._core import BaseVariable, Variable

    for variable in expr.atoms(BaseVariable):
        for unit in variable.definition.unit.atoms(Quantity):
            yield unit


def derive_unit(expr, name=None):
    """Derive SI unit from an expression, omitting scale factors."""
    from essm.variables import Variable
    from essm.variables.utils import extract_variables

    dim = Variable.get_dimensional_expr(expr)
    return dim.subs(SI_EXTENDED_DIMENSIONS)


def derive_baseunit(expr, name=None):
    """Derive SI base unit from an expression, omitting scale factors."""
    from essm.variables import Variable
    from essm.variables.utils import extract_variables
    from sympy.physics.units import Dimension
    from sympy.physics.units.dimensions import dimsys_SI

    variables = extract_variables(expr)
    for var1 in variables:
        q1 = Quantity('q_' + str(var1))
        q1.set_dimension(
            Dimension(Quantity.get_dimensional_expr(
                derive_baseunit(var1.definition.unit)))
        )
        q1.set_scale_factor(var1.definition.unit)
        expr = expr.xreplace({var1: q1})
    dim = Dimension(Quantity.get_dimensional_expr(expr))
    return functools.reduce(
        operator.mul, (
            SI_BASE_DIMENSIONS[Symbol(d)] ** p
            for d, p in dimsys_SI.get_dimensional_dependencies(dim).items()
        ), 1
    )


def derive_base_dimension(dim):
    """Derive base dimension of dimension"""
    return functools.reduce(
        operator.mul, (
            Symbol(d) ** p
            for d, p in dimsys_SI.get_dimensional_dependencies(dim).items()
        ), 1
    )

def collect_factor_and_basedimension(expr):
    """Return tuple with factor expression and dimension expression."""
    from essm.variables._core import BaseVariable, Variable
    if isinstance(expr, BaseVariable):
        expr = expr.definition.unit 
    if isinstance(expr, Quantity):
        return expr.scale_factor, derive_base_dimension(expr.dimension)
    elif isinstance(expr, Mul):
        factor = 1
        dimension = Dimension(1)
        for arg in expr.args:
            arg_factor, arg_dim = collect_factor_and_basedimension(arg)
            factor *= arg_factor
            dimension *= arg_dim
        return factor, dimension
    elif isinstance(expr, Pow):
        factor, dim = collect_factor_and_basedimension(expr.base)
        exp_factor, exp_dim = collect_factor_and_basedimension(expr.exp)
        if exp_dim.is_dimensionless:
            exp_dim = 1
        return factor ** exp_factor, dim ** (exp_factor * exp_dim)
    elif isinstance(expr, Add):
        factor, dim = collect_factor_and_basedimension(expr.args[0])           
        for addend in expr.args[1:]:
            print(addend)
            addend_factor, addend_dim = \
                collect_factor_and_basedimension(addend)
            print(addend_factor, addend_dim)
            if dim != addend_dim:
                print('factor, dim:')
                print((addend_factor, addend_dim))
                raise ValueError(
                    'Dimension of "{0}" is {1}, '
                    'but it should be {2}'.format(
                        addend, addend_dim, dim.name))
            factor += addend_factor
        return factor, dim
    elif isinstance(expr, Derivative):
        factor, dim = collect_factor_and_basedimension(expr.args[0])
        for independent, count in expr.variable_count:
            ifactor, idim = collect_factor_and_basedimension(independent)
            factor /= ifactor**count
            dim /= idim**count
        return factor, dim
    elif isinstance(expr, Function):
        fds = [collect_factor_and_basedimension(
            arg) for arg in expr.args]
        return (expr.func(*(f[0] for f in fds)),
                expr.func(*(d[1] for d in fds)))               
    elif isinstance(expr, Dimension):
        return 1, expr
    else:
        return expr, Dimension(1)

__all__ = (
    'derive_baseunit', 'derive_basedimension', 'derive_unit', 'markdown',
    'joule', 'kelvin', 'kilogram', 'meter', 'mole', 'pascal', 'second',
    'unit_symbols', 'watt'
)
