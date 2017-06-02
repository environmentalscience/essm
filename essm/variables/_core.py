# -*- coding: utf-8 -*-
"""Core variable type."""

from __future__ import absolute_import

import warnings

from sage.all import SR, Expression, var

from .units import SHORT_UNIT_SYMBOLS


class BaseVariable(Expression):
    """Physical variable."""

    @property
    def definition(self):
        return Variable.__registry__[self]

    @property
    def unit(self):
        return Variable.__units__[self]

    @property
    def short_unit(self):
        """Return short unit."""
        return (self * self.unit / self).subs(SHORT_UNIT_SYMBOLS)

    def delete(self):
        """Deletes variable from __registry__,
        __defaults__ and __units__.
        """
        del Variable.__registry__[self]
        if self in Variable.__defaults__.keys():
            del Variable.__defaults__[self]
        if self in Variable.__units__.keys():
            del Variable.__units__[self]


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
            unit = dct.get('unit', 1 / 1)
            latex_name = dct.get('latex_name')
            expr = BaseVariable(SR,
                                SR.var(
                                    name, domain=domain,
                                    latex_name=latex_name))
            dct.update({
                'domain': domain,
                'expr': expr,
                'latex': expr._latex_(),
                'name': name,
                'unit': unit,
            })
            instance = super(VariableMeta, cls).__new__(
                cls, name, parents, dct)
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


class Variable(object):
    """Base type for all physical variables."""
    __metaclass__ = VariableMeta
    __registry__ = {}
    __defaults__ = {}
    __units__ = {}


__all__ = ('Variable', 'register', )
