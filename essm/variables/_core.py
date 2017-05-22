# -*- coding: utf-8 -*-

"""Core variable type."""

from __future__ import absolute_import

from sage.all import Expression, SR, var

from .units import SHORT_UNIT_SYMBOLS

class BaseVariable(Expression):
    """Add definition and short unit."""

    @property
    def definition(self):
        return Variable.__registry__[self]

    @property
    def unit(self):
        return Variable.__units__[self]

    @property
    def short_unit(self):
        """Return short unit."""
        return (self*self.unit/self).subs(
            SHORT_UNIT_SYMBOLS
        )


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
            latex_name = dct.get('latex_name')
            expr = BaseVariable(
                SR, SR.var(name, domain=domain, latex_name=latex_name)
            )
            dct['expr'] = expr
            dct['latex'] = expr._latex_()

            instance = super(VariableMeta, cls).__new__(cls, name, parents, dct)
            instance.__registry__[expr] = instance
            if 'default' in dct:
                instance.__defaults__[expr] = dct['default']
            # Store unit for each variable:
            instance.__units__[expr] = dct.get('unit', 1/1)
            return expr

        return super(VariableMeta, cls).__new__(cls, name, parents, dct)


class Variable(object):
    """Base type for all physical variables."""
    __metaclass__ = VariableMeta
    __registry__ = {}
    __defaults__ = {}
    __units__ = {}

__all__ = (
    'Variable',
    'register',
)
