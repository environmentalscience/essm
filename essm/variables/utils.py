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

from .units import markdown
from _core import BaseVariable
from sympy import preorder_traversal


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


def get_vars(expr):
    """Traverses through expression and returns set of variables as list."""
    vars = []
    for arg in preorder_traversal(expr):
        if isinstance(arg, BaseVariable):
            vars.append(arg)
    return list(set(vars))


def subs_vars(expr, vdict={}):
    '''Replaces all variables in expression by
    their names and then by their expressions in vdict
    (keys in vdict are variables)'''
    def replace_names(expr):
        '''Replaces all variables in expression by their names.'''
        try:
            return expr.replace(
                lambda expr: isinstance(expr, BaseVariable),
                lambda expr: expr._name)
        except:
            return expr

    expr1 = replace_names(expr)
    sdict = dict(
        (key._name, replace_names(vdict[key]))
        for key in vdict.keys()
    )
    return expr1.xreplace(sdict)
