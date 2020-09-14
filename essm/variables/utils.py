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
"""Utility function for variables, expressions and equations."""

from essm.equations._core import BaseEquation, EquationMeta
from essm.variables._core import BaseVariable
from sympy import Eq, latex, preorder_traversal
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


def generate_metadata_table(variables=None, include_header=True, cols=None):
    """Generate table of variables, default values and units.

    If variables not provided in list ``variables``, table will contain
    all variables in ``Variables.__registry__``.
    It is possible to remove columns by providing a tuple with a subste of:
    cols=('Symbol', 'Name', 'Description', 'Definition',
                'Default value', 'Units')
    """
    from ._core import Variable
    all_cols = ('Symbol', 'Name', 'Description', 'Definition',
                'Default value', 'Units')
    cols = cols or all_cols
    table = ListTable()
    variables = variables or Variable.__registry__.keys()
    if include_header:
        table.append(cols)

    for variable in sorted(variables,
                           key=lambda x: x.definition.latex_name.lower()):
        symbol = '$' + variable.definition.latex_name + '$'
        name = str(variable)
        doc = variable.__doc__
        defn1 = Variable.__expressions__.get(variable, '')
        if len(str(defn1)) > 1:
            defn = '$' + latex(defn1) + '$'
        else:
            defn = ''
        val = str(Variable.__defaults__.get(variable, '-'))
        unit = markdown(variable.definition.unit)
        dict_col = {}
        dict_col['Symbol'] = symbol
        dict_col['Name'] = name
        dict_col['Description'] = doc
        dict_col['Definition'] = defn
        dict_col['Default value'] = val
        dict_col['Units'] = unit

        table.append(
            tuple(dict_col[item] for item in cols)
        )
    return table


def extract_variables(expr):
    """Traverse through expression and return set of variables."""
    return {
        arg
        for arg in preorder_traversal(expr) if isinstance(arg, BaseVariable)
    }


def get_allparents(equation, allparents=None):
    """Return set of parents of equation recursively."""
    if not allparents:
        allparents = set()
    if isinstance(equation, BaseEquation):
        parents = equation.definition.__bases__
    else:
        parents = equation.__bases__
    for parent in parents:
        if hasattr(parent, 'name'):
            allparents.update([parent.name])
            get_allparents(parent, allparents)
    return allparents


def get_parents(equation):
    """Return set of parents of equation."""
    allparents = set()
    parents = equation.definition.__bases__
    for parent in parents:
        if hasattr(parent, 'name'):
            allparents.update([parent.name])
    return allparents


def replace_variables(expr, variables=None):
    """Replace all base variables in expression by ``variables``."""
    if not isinstance(expr, Expr)\
       and not isinstance(expr, BaseEquation):  # stop recursion
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


def subs_eq(expr, *args):
    r"""Return a new expression with args consecutively substituted into expr.

    If expr is an equality, substitution is performed on both sides. If args
    contain equations, substitution is performed as .subs(eqn.lhs, eqn.rhs)
    for each eqn.

    **Examples:**

        >>> from essm.variables.physics.thermodynamics import (T_a)
        >>> from essm.variables.leaf.energy_water import (T_l)
        >>> from essm.equations.leaf.energy_water import (
        ... eq_Rs_enbal, eq_El, eq_Elmol, eq_Hl, eq_Rll )
        >>> subs_eq(eq_Rs_enbal, [eq_El, eq_Hl], eq_Elmol,
        ... {T_l: 301., T_a: 300.})
        Eq(R_s, M_w*g_tw*lambda_E*(-C_wa + C_wl) + R_ll + 1.0*a_sh*h_c)
        >>> subs_eq(eq_Rs_enbal.rhs, [eq_El, eq_Hl], eq_Elmol)
        M_w*g_tw*lambda_E*(-C_wa + C_wl) + R_ll + a_sh*h_c*(-T_a + T_l)

    """
    if isinstance(expr, Eq):
        lhs = expr.lhs
        rhs = expr.rhs
    else:
        lhs = None
        rhs = expr
    for arg in args:
        if isinstance(arg, Eq):
            arg = {arg.lhs: arg.rhs}
        if isinstance(arg, list) or isinstance(arg, tuple):
            arg = {s1.lhs: s1.rhs for s1 in arg}
        if lhs:
            lhs = lhs.subs(arg)
        rhs = rhs.subs(arg)
    if lhs:
        return Eq(lhs, rhs)
    else:
        return rhs
