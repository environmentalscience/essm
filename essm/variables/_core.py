# -*- coding: utf-8 -*-

"""Core variable type."""

from __future__ import absolute_import

from sage.all import var

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
            latex_name = dct.get('latex_name')
            symbolic_variable = var(name, domain=domain, latex_name=latex_name)
            dct['symbolic_variable'] = symbolic_variable
            dct['latex'] = symbolic_variable._latex_()

        return super(VariableMeta, cls).__new__(cls, name, parents, dct)

    def __init__(cls, name, bases, dct):
        """Register variable."""
        if '__registry__' not in dct:
            cls.__registry__[name] = cls
            if hasattr(cls, 'default'):
                cls.__defaults__[name] = cls.default
            # Store unit for each variable:
            cls.__units__[cls.symbolic_variable] = getattr(cls, 'unit', 1/1)


class Variable(object):
    """Base type for all physical variables."""
    __metaclass__ = VariableMeta
    __registry__ = {}
    __defaults__ = {}
    __units__ = {}

    @classmethod
    def short_unit(cls, variable):
        """Return short unit."""
        return (variable*cls.__units__[variable]/variable).subs(
            SHORT_UNIT_SYMBOLS
        )



def register(cls):
    """Register symbolic variable instead of class definition."""
    return cls.symbolic_variable

__all__ = (
)
