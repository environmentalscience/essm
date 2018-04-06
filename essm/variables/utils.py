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
"""Utility function for variables."""

from sympy import Eq, preorder_traversal
from sympy.core.expr import Expr
from sympy.physics.units import Dimension
from sympy.physics.units.dimensions import dimsys_default

from essm.equations._core import BaseEquation
from essm.variables import Variable
from essm.variables._core import BaseVariable

from .units import markdown


def generate_metadata_table(variables=None, include_header=True):
    """Generate table of variables, default values and units.

    If variables not provided in list ``variables``, table will contain
    all variables in ``Variables.__registry__``.
    """
    from ._core import Variable
    variables = variables or Variable.__registry__.keys()
    if include_header:
        yield ('Symbol', 'Name', 'Description', 'Default value', 'Units')

    for variable in sorted(variables, key=lambda x: x._latex_().lower()):
        symbol = '$' + variable._latex_() + '$'
        name = str(variable)
        doc = variable.__doc__
        val = str(Variable.__defaults__.get(variable, '-'))

        yield (symbol, name, doc, val, markdown(variable.short_unit))


def extract_variables(expr):
    """Traverse through expression and return set of variables."""
    return {arg for arg in preorder_traversal(expr)
            if isinstance(arg, BaseVariable)}


def replace_variables(expr, variables=None):
    """Replace all base variables in expression by ``variables``."""
    if not isinstance(expr, Expr):  # stop recursion
        return expr
    symbols = {key: getattr(key, '_name', key)
               for key in extract_variables(expr)}
    variables = {getattr(key, '_name', key): replace_variables(value)
                 for key, value in (variables or {}).items()}
    if isinstance(expr, BaseEquation):
        return Eq(expr.lhs.xreplace(symbols).xreplace(variables),
                  expr.rhs.xreplace(symbols).xreplace(variables))
    return expr.xreplace(symbols).xreplace(variables)


def replace_defaults(expr):
    """Replace variables in expression by their default values."""
    if hasattr(expr, 'lhs'):
        expr1 = expr.lhs
        lhs = expr1.replace(
            lambda expr1: isinstance(expr1, BaseVariable),
            lambda expr1: expr1.definition.unit*expr1.definition.default
            if hasattr(expr1.definition, 'default') else expr1)
        expr1 = expr.rhs
        rhs = expr1.replace(
            lambda expr1: isinstance(expr1, BaseVariable),
            lambda expr1: expr1.definition.unit*expr1.definition.default
            if hasattr(expr1.definition, 'default') else expr1)
        return Eq(lhs, rhs)
    else:
        expr1 = expr
        return expr1.replace(
            lambda expr1: isinstance(expr1, BaseVariable),
            lambda expr1: expr1.definition.unit*expr1.definition.default
            if hasattr(expr1.definition, 'default') else expr1)


def check_unit(expr):
    # Construction postprocessor for the addition,
    # checks for dimension mismatches of the addends, thus preventing
    # expressions like `meter + second` to be created.

    deset = {
        tuple(sorted(dimsys_default.get_dimensional_dependencies(
            Dimension(Variable.get_dimensional_expr(i) if not i.is_number else 1
        )).items()))
        for i in expr.args
        #if i.free_symbols == set()  # do not raise if there are symbols
                    # (free symbols could contain the units corrections)
    }
    # If `deset` has more than one element, then some dimensions do not
    # match in the sum:
    if len(deset) > 1:
        raise ValueError("summation of quantities of incompatible dimensions")
    return expr