# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017 ETH Zurich, Swiss Data Science Center.
# Copyright (C) 2018 LIST (Luxembourg Institute of Science and Technology).
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

from essm.equations._core import BaseEquation
from essm.variables._core import BaseVariable
from sympy import Eq, preorder_traversal
from sympy.core.expr import Expr

from .units import markdown


class ListTable(list):
    """Override list class to render HTML Table in Jupyter notbook.

    Takes a 2-dimensional list of the form ``[[1, 2, 3], [4, 5, 6]],``
    and renders an HTML Table in IPython Notebook.

    Source: https://calebmadrigal.com/display-list-as-table-in-ipython-notebook

    Example:

    >>> table = ListTable()
    >>> table.append(['Column1', 'Column2'])
    >>> table.append(['1', '2'])
    >>> table
    [['Column1', 'Column2'], ['1', '2']]
    """

    def _repr_html_(self):
        html = ["<table>"]
        for row in self:
            html.append("<tr>")
            for col in row:
                html.append("<td>{0}</td>".format(col))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)


def generate_metadata_table(variables=None, include_header=True):
    """Generate table of variables, default values and units.

    If variables not provided in list ``variables``, table will contain
    all variables in ``Variables.__registry__``.
    """
    from ._core import Variable
    table = ListTable()
    variables = variables or Variable.__registry__.keys()
    if include_header:
        table.append(
            ('Symbol', 'Name', 'Description', 'Default value', 'Units')
        )

    for variable in sorted(variables,
                           key=lambda x: x.definition.latex_name.lower()):
        symbol = '$' + variable.definition.latex_name + '$'
        name = str(variable)
        doc = variable.__doc__
        val = str(Variable.__defaults__.get(variable, '-'))

        table.append(
            (symbol, name, doc, val, markdown(variable.definition.unit))
        )
    return table


def extract_variables(expr):
    """Traverse through expression and return set of variables."""
    return {
        arg
        for arg in preorder_traversal(expr) if isinstance(arg, BaseVariable)
    }


def replace_variables(expr, variables=None):
    """Replace all base variables in expression by ``variables``."""
    if not isinstance(expr, Expr):  # stop recursion
        return expr
    symbols = {
        key: getattr(key, '_name', key)
        for key in extract_variables(expr)
    }
    variables = {
        getattr(key, '_name', key): replace_variables(value)
        for key, value in (variables or {}).items()
    }
    if isinstance(expr, BaseEquation):
        return Eq(
            expr.lhs.xreplace(symbols).xreplace(variables),
            expr.rhs.xreplace(symbols).xreplace(variables)
        )
    return expr.xreplace(symbols).xreplace(variables)


def replace_defaults(expr):
    """Replace variables in expression by their default values."""
    if hasattr(expr, 'lhs'):
        expr1 = expr.lhs
        lhs = expr1.replace(
            lambda expr1: isinstance(expr1, BaseVariable), lambda expr1: expr1.
            definition.unit * expr1.definition.default
            if hasattr(expr1.definition, 'default') else expr1
        )
        expr1 = expr.rhs
        rhs = expr1.replace(
            lambda expr1: isinstance(expr1, BaseVariable), lambda expr1: expr1.
            definition.unit * expr1.definition.default
            if hasattr(expr1.definition, 'default') else expr1
        )
        return Eq(lhs, rhs)
    else:
        expr1 = expr
        return expr1.replace(
            lambda expr1: isinstance(expr1, BaseVariable), lambda expr1: expr1.
            definition.unit * expr1.definition.default
            if hasattr(expr1.definition, 'default') else expr1
        )
