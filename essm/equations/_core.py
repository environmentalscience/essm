# -*- coding: utf-8 -*-

"""Core equation type."""

from __future__ import absolute_import

from sage.all import Expression, SR
from sage.misc.latex import latex

from ..variables import SHORT_UNIT_SYMBOLS, Variable

def convert(expr):
    """Convert a given expression."""
    op = expr.operator()
    ops = expr.operands()
    if op:
        return op(*(convert(o) for o in ops))
    return expr.convert() if hasattr(expr, 'convert') else expr


class BaseEquation(Expression):
    """Add definition and short unit."""

    @property
    def definition(self):
        return Equation.__registry__[self]

    def expand_units(self, simplify_full=True):
        """Expand units of all arguments in expression."""
        used_units = {}
        # Need to multiply units with variable,
        # so that we can devide by the symbolic equation later:
        for variable in self.arguments():
            used_units[variable] = variable * Variable.__units__[variable]

        result = BaseEquation(SR, self.subs(used_units)/self).convert()
        if simplify_full:
            result = result.simplify_full()
        return result

    def short_units(self):
        """Return short units of equation."""
        expanded = self.expand_units()
        return expanded.lhs().subs(SHORT_UNIT_SYMBOLS) \
            == expanded.rhs().subs(SHORT_UNIT_SYMBOLS)

    def convert(self):
        return convert(self)


class EquationMeta(type):
    """Equation interface."""

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            name = dct.get('name', name)
            expr = BaseEquation(SR, dct['expr'])
            dct['expr'] = expr

            instance = super(EquationMeta, cls).__new__(cls, name, parents, dct)
            instance.__registry__[expr] = instance

            expanded_units = expr.expand_units()
            if not expanded_units:
                raise ValueError(
                    'Invalid expression units: {0}'.format(expanded_units)
                )
            return expr

        return super(EquationMeta, cls).__new__(cls, name, parents, dct)


class Equation(object):
    """Base type for all equation."""
    __metaclass__ = EquationMeta
    __registry__ = {}


__all__ = (
    'Equation',
    'convert',
)
