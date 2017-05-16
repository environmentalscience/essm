# -*- coding: utf-8 -*-

"""Core equation type."""

from __future__ import absolute_import

from functools import wraps

from sage.misc.latex import latex

from ..variables import SHORT_UNIT_SYMBOLS, Variable


def load_expr(f):
    """Use only on class methods with expr argument."""
    @wraps(f)
    def decorated(cls, expr=None, **kwargs):
        """Load expression from a class if not provided."""
        if expr is not None:
            cls = cls.from_expression(expr)
        return f(cls, **kwargs)
    return decorated


def convert(expr):
    op = expr.operator()
    ops = expr.operands()
    if op:
        if len(ops) == 2:
            return op(*map(convert, ops))
        return op(convert(ops[0]), reduce(op, map(convert, ops[1:])))
    return expr.convert() if hasattr(expr, 'convert') else expr


class EquationMeta(type):
    """Equation interface."""

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            name = dct.get('name', name)

        return super(EquationMeta, cls).__new__(cls, name, parents, dct)

    def __init__(cls, name, bases, dct):
        """Register variable."""
        if '__registry__' not in dct:
            expanded_units = cls.expand_units()
            if not expanded_units:
                raise ValueError(
                    'Invalid expression units: {0}'.format(expanded_units)
                )
            cls.__registry__[name] = cls
            cls.__expressions__[cls.expr] = cls


class Equation(object):
    """Base type for all equation."""
    __metaclass__ = EquationMeta
    __registry__ = {}
    __expressions__ = {}
    __defaults__ = {}

    @classmethod
    def from_expression(cls, expr):
        """Return class for given expression."""
        return cls.__expressions__[expr]

    @classmethod
    @load_expr
    def expand_units(cls, simplify_full=True):
        """Expand units of all arguments in expression."""
        used_units = {}
        # Need to multiply units with variable,
        # so that we can devide by the symbolic equation later:
        for variable in cls.expr.arguments():
            used_units[variable] = variable * Variable.__units__[variable]

        result = convert(cls.expr.subs(used_units)/cls.expr)
        if simplify_full:
            result = result.simplify_full()
        return result

    @classmethod
    @load_expr
    def short_units(cls):
        """Return short units of equation."""
        expanded = cls.expand_units()
        return expanded.lhs().subs(SHORT_UNIT_SYMBOLS) \
            == expanded.rhs().subs(SHORT_UNIT_SYMBOLS)


def register(cls):
    """Register symbolic variable instead of class definition."""
    return cls.expr


__all__ = (
    'Equation',
    'convert',
    'register',
)
