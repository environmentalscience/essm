# -*- coding: utf-8 -*-
"""Core variable type."""

from __future__ import absolute_import

import warnings

from sage.all import SR, Expression

from ..bases import BaseExpression
from ..transformer import build_instance_expression
from .units import SHORT_UNIT_SYMBOLS


class VariableMeta(type):
    """Variable interface.

    1. register domain (default: real)
    2. store _latex_() name
    3. register default values for each variable
    """

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            name = dct.get('name', name)
            domain = dct.get('domain', 'real')
            unit = dct.get('unit', None)
            latex_name = dct.get('latex_name')
            definition = dct.pop('expr', None)
            # In the below, domain=None is to avoid slow assume() process.
            expr = BaseVariable(
                SR, SR.var(name, domain=None, latex_name=latex_name))
            dct.update({
                'domain': domain,
                'expr': expr,
                'name': name, })

            instance = super(VariableMeta, cls).__new__(
                cls, name, parents, dct)

            if definition is not None:
                definition = BaseVariable(SR, build_instance_expression(
                    instance, definition
                ))
                definition_unit = definition.expand_units()
                if unit is not None:
                    if bool(unit == definition_unit):
                        raise ValueError(
                            'Invalid expression units: {0}'.format(unit))
                else:
                    unit = definition_unit
                instance.__expressions__[expr] = instance.expr = definition

            instance.unit = unit

            if expr in instance.__registry__:
                warnings.warn(
                    'Variable "{0}" will be overridden by "{1}"'.format(
                        instance.__registry__[expr].__module__ + ':' + name,
                        instance.__module__ + ':' + name, ),
                    stacklevel=2)
            instance.__registry__[expr] = instance
            if 'default' in dct:
                instance.__defaults__[expr] = dct['default']
            # Store unit for each variable:
            instance.__units__[expr] = unit
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
        SR.var(
            self.definition.name,
            domain=self.definition.domain,
            latex_name=self.definition.latex_name,
        )


__all__ = ('Variable')
