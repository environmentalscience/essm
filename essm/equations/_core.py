# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017-2019 ETH Zurich, Swiss Data Science Center.
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
"""Core equation type. Contains class definitions related to equations."""

from __future__ import absolute_import

import warnings

import six
from sympy.core.relational import Eq

from ..bases import RegistryType
from ..transformer import build_instance_expression
from ..variables import Variable
from ..variables._core import BaseVariable, Variable


class EquationMeta(RegistryType):
    r"""Equation interface.

    Defines an equation with a docstring and internal variables,
    if needed.

    Example:

    .. code-block:: python

        from ..variables.units import meter, second
        class test(Equation):
            '''Test equation.'''

            class d(Variable):
                '''Internal variable.'''
                unit = meter

            class t(Variable):
                '''Internal variable.'''
                unit = second

            class v(Variable):
                '''Internal variable.'''
                unit = meter/second

            expr = v == d / t

    :raises ValueError: if the units are inconsistent.

        Example:

        .. testcode:: python

           from ..variables.units import meter, second
           class test(Equation):
               '''Test equation with inconsistent units.'''

               class d(Variable):
                   '''Internal variable.'''
                   unit = meter

               class t(Variable):
                   '''Internal variable.'''
                   unit = second

               class v(Variable):
                   '''Internal variable.'''
                   unit = meter/second

               expr = v == d * t

        Since the units of v and d*t are not the same, this returns:

        .. testoutput::

           ValueError: Invalid expression units: meter/second == meter*second
    """

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            dct.setdefault('name', name)
            expr = dct.pop('expr')

            instance = super(EquationMeta,
                             cls).__new__(cls, name, parents, dct)
            expr = build_instance_expression(instance, expr)
            instance.expr = expr = BaseEquation(instance, expr)
            instance[expr] = instance

            return expr

        return super(EquationMeta, cls).__new__(cls, name, parents, dct)


@six.add_metaclass(EquationMeta)
class Equation(object):
    """Base type for all equations."""

    __registry__ = {}

    @classmethod
    def args(cls):
        """Return equation arguments from registry if exist."""
        return tuple(
            Variable.__registry__.get(arg, arg)
            for arg in cls.expr.atoms(BaseVariable)
        )


class BaseEquation(Eq):
    """Add definition and short unit."""

    def __new__(cls, definition, expr):
        if not isinstance(expr, Eq):
            return expr
        # The below raises an error if units are not consistent
        Variable.collect_factor_and_basedimension(expr.lhs + expr.rhs)
        self = super(BaseEquation, cls).__new__(cls, *expr.args)
        self.definition = definition
        return self

    @property
    def __doc__(self):
        return self.definition.__doc__

    def __add__(self, other):
        """Combine two equations."""
        if not isinstance(other, Eq):
            raise TypeError(other)

        other_definition = getattr(other, 'definition', other)
        return type(
            str(self.definition) + '_and_' + str(other_definition),
            (self.definition, other_definition),
            {'expr': Eq(self.lhs + other.lhs, self.rhs + other.rhs)},
        )

    def subs(self, *args, **kwargs):  # should mirror sympy.core.basic.subs
        r"""Return a new equation with subs applied to both sides.

        **Examples:**

        >>> from essm.equations.leaf.energy_water import (
        ... eq_Rs_enbal, eq_El, eq_Hl, eq_Rll )
        >>> eq_Rs_enbal.subs(eq_El, eq_Hl, eq_Rll)
        Eq(R_s, E_lmol*M_w*lambda_E + a_sh*... + a_sh*h_c*(-T_a + T_l))
        >>> from essm.equations.physics.thermodynamics import (
        ... eq_Le, eq_Dva, eq_alphaa)
        >>> from essm.variables.physics.thermodynamics import (
        ... Le, D_va, alpha_a, T_a)
        >>> eq_Le.subs(D_va, eq_Dva.rhs)
        Eq(Le, alpha_a/(T_a*p_Dva1 - p_Dva2))
        >>> eq_Le.subs({D_va: eq_Dva.rhs, alpha_a: eq_alphaa.rhs})
        Eq(Le, (T_a*p_alpha1 - p_alpha2)/(T_a*p_Dva1 - p_Dva2))
        >>> eq_Le.subs(eq_Dva, eq_alphaa)
        Eq(Le, (T_a*p_alpha1 - p_alpha2)/(T_a*p_Dva1 - p_Dva2))
        """
        sequence = args
        only_eqs = all(isinstance(arg, Eq) for arg in args)

        if len(args) == 1:
            if isinstance(args[0], Eq):
                sequence = ({args[0].lhs: args[0].rhs}, )
        elif len(args) == 2 and not only_eqs:
                sequence = ({args[0]: args[1]}, )
        elif args and only_eqs:
            sub_eqs = {}
            for arg in args:
                sub_eqs[arg.lhs] = arg.rhs
            sequence = (sub_eqs, )

        return Eq(
            self.lhs.subs(*sequence, **kwargs),
            self.rhs.subs(*sequence, **kwargs),
        )


__all__ = ('Equation', 'EquationMeta')
