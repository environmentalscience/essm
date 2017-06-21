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
"""Core equation type."""

from __future__ import absolute_import

from sage.all import SR
from sage.misc.latex import latex

from ..bases import BaseExpression, convert
from ..transformer import build_instance_expression
from ..variables import Variable
from ..variables._core import BaseVariable


class EquationMeta(type):
    """Equation interface."""

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            dct.setdefault('name', name)
            expr = dct.pop('expr')

            instance = super(EquationMeta, cls).__new__(
                cls, name, parents, dct)
            instance.expr = expr = BaseEquation(
                build_instance_expression(instance, expr),
                instance,
                units=Variable.__units__, ).register()

            expanded_units = expr.expand_units()
            if not expanded_units:
                raise ValueError(
                    'Invalid expression units: {0}'.format(expanded_units))
            return expr

        return super(EquationMeta, cls).__new__(cls, name, parents, dct)


class Equation(object):
    """Base type for all equations."""
    __metaclass__ = EquationMeta
    __registry__ = {}

    @classmethod
    def args(cls):
        return tuple(
            Variable.__registry__.get(arg, arg) for arg in cls.expr.args())


class BaseEquation(BaseExpression):
    """Add definition and short unit."""

    @property
    def __doc__(self):
        return self.definition.__doc__


__all__ = ('Equation', )
