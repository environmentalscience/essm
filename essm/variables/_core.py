# -*- coding: utf-8 -*-
"""Core variable type."""

from __future__ import absolute_import

import warnings

from sage.all import SR, Expression

from ..bases import BaseExpression
from ..transformer import build_instance_expression
from .units import SHORT_UNIT_SYMBOLS


class VariableMeta(type):
    """Variable interface."""

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            unit = dct.pop('unit', None)
            definition = dct.pop('expr', None)

            dct.setdefault('name', name)
            dct.setdefault('domain', 'real')
            dct.setdefault('latex_name', dct['name'])
            dct.setdefault('unit', unit or 1/1)

            instance = super(VariableMeta, cls).__new__(
                cls, name, parents, dct)

            # In the below, domain=None is to avoid slow assume() process.
            expr = BaseVariable(
                SR.var(name, domain=None, latex_name=dct['latex_name']),
                instance,
            ).register()

            # Variable with definition expression.
            if definition is not None:
                definition = BaseVariable(
                    build_instance_expression(instance, definition),
                    instance,
                )
                instance.unit = definition.expand_units()
                if unit is not None and bool(unit == instance.unit):
                    raise ValueError(
                        'Invalid expression units: {0}'.format(unit))
                instance.__expressions__[expr] = instance.expr = definition

            # Store default variable only if it is defined.
            if 'default' in dct:
                instance.__defaults__[expr] = dct['default']

            # Store unit for each variable:
            instance.__units__[expr] = instance.unit
            return expr

        return super(VariableMeta, cls).__new__(cls, name, parents, dct)

    def __remove__(cls, expr):
        """Remove a variable from the registry."""
        if expr in cls.__registry__:
            warnings.warn(
                'Variable "{0}" will be unregistered.'.format(
                    cls.__registry__[expr].__module__),
                stacklevel=2)
            del cls.__registry__[expr]
        else:
            warnings.warn(
                'Variable "{0}" did not exist in registry.'.format(expr),
                stacklevel=2)
        if expr in cls.__units__:
            del cls.__units__[expr]
        if expr in cls.__defaults__:
            del cls.__defaults__[expr]

    def set_domain(cls):
        """Set domain for all registered variables."""
        for expr in cls.__registry__:
            expr.set_domain()


class Variable(object):
    """Base type for all physical variables."""
    __metaclass__ = VariableMeta
    __registry__ = {}
    __defaults__ = {}
    __units__ = {}
    __expressions__ = {}


class BaseVariable(BaseExpression):
    """Physical variable."""

    __registry__ = Variable.__registry__
    __units__ = Variable.__units__

    @property
    def __doc__(self):
        return self.definition.__doc__

    @property
    def short_unit(self):
        """Return short unit."""
        return (self * self.definition.unit / self).subs(SHORT_UNIT_SYMBOLS)

    def set_domain(self, domain=None):
        """Set domain to current variable."""
        if domain is not None:
            self.definition.domain = domain
        self.rebuild_symbol()

    def rebuild_symbol(self):
        """Rebuild symbolic representation."""
        SR.var(
            self.definition.name,
            domain=self.definition.domain,
            latex_name=self.definition.latex_name,
        )


__all__ = ('Variable', )
