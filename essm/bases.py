# -*- coding: utf-8 -*-
"""Base classes."""

from __future__ import absolute_import

from sage.all import SR, Expression


def expand_units(expr, units=None, simplify_full=True):
    """Expand units of all arguments in expression."""
    from .variables._core import Variable

    units = units or Variable.__units__
    used_units = {}
    # Need to multiply units with variable,
    # so that we can devide by the symbolic equation later:
    for variable in expr.arguments():
        used_units[variable] = variable * units[variable]

    result = expr.__class__(SR, expr.subs(used_units) / expr).convert()
    if simplify_full:
        result = result.simplify_full()
    return result


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
        return expand_units(self, self.__units__, simplify_full=simplify_full)

    def short_units(self):
        """Return short units of equation."""
        from .variables.units import SHORT_UNIT_SYMBOLS
        return self.expand_units().subs(SHORT_UNIT_SYMBOLS)

    def convert(self):
        return convert(self)


__all__ = ('BaseExpression', 'convert', 'expand_units')
