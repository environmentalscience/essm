# -*- coding: utf-8 -*-
"""Base classes."""

from __future__ import absolute_import

from sage.all import SR, Expression

from .variables.units import SHORT_UNIT_SYMBOLS


def convert(expr):
    """Convert a given expression."""
    op = expr.operator()
    ops = expr.operands()
    if op:
        return op(*(convert(o) for o in ops))
    return expr.convert() if hasattr(expr, 'convert') else expr


class BaseExpression(Expression):
    """Add definition and instance documentation."""

    __registry__ = None
    """Override the class property when subclassing."""

    __units__ = None
    """Override the class property when subclassing."""

    @property
    def definition(self):
        return self.__registry__[self]

    @property
    def __doc__(self):
        return self.definition.__doc__

    def expand_units(self, simplify_full=True):
        """Expand units of all arguments in expression."""
        used_units = {}
        # Need to multiply units with variable,
        # so that we can devide by the symbolic equation later:
        for variable in self.arguments():
            used_units[variable] = variable * self.__units__[variable]

        result = self.__class__(SR, self.subs(used_units) / self).convert()
        if simplify_full:
            result = result.simplify_full()
        return result

    def short_units(self):
        """Return short units of equation."""
        return self.expand_units().subs(SHORT_UNIT_SYMBOLS)

    def convert(self):
        return convert(self)
