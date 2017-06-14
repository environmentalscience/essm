# -*- coding: utf-8 -*-
"""Core equation type."""

from __future__ import absolute_import

import warnings

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
                SR, build_instance_expression(instance, expr)
            )

            if expr in instance.__registry__:
                warnings.warn(
                    'Equation "{0}" will be overridden by "{1}"'.format(
                        instance.__registry__[expr].__module__ + ':' + name,
                        instance.__module__ + ':' + name, ),
                    stacklevel=2)
            instance.__registry__[expr] = instance

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
        return tuple(Variable.__registry__[arg].expr
                     if arg in Variable.__registry__ else arg
                     for arg in cls.expr.args())


class BaseEquation(BaseExpression):
    """Add definition and short unit."""

    __registry__ = Equation.__registry__
    __units__ = Variable.__units__


__all__ = ('Equation', )
