# -*- coding: utf-8 -*-
"""Core equation type."""

from __future__ import absolute_import

import ast
import inspect
import sys
import warnings

from sage.all import SR, Expression
from sage.misc.latex import latex
from sage.rings import integer, real_mpfr

from ..utils import process_parents
from ..variables import SHORT_UNIT_SYMBOLS, Variable
from ..variables._core import BaseVariable


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

        result = BaseEquation(SR, self.subs(used_units) / self).convert()
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


_Integer = ast.parse('integer.Integer', mode='eval').body
_Float = ast.parse('real_mpfr.RR', mode='eval').body


class Numbers(ast.NodeTransformer):
    """Change Python numbers to Sage numbers."""

    def visit_Num(self, node):
        """Rewrite int / int to Fraction(int, int)."""
        func = _Integer
        if isinstance(node.n, float):
            func = _Float
        return ast.copy_location(
            ast.Call(
                func=func,
                args=[ast.Str(str(node.n))],
                keywords=[],
                starargs=None,
                kwargs=None, ), node)


class ClassDef(ast.NodeVisitor):
    """Extract expression definition."""

    def __init__(self):
        """Initialize class definition."""
        self.expr = None

    def visit_Assign(self, node):
        """Find 'expr = <expr>'."""
        for target in node.targets:
            if target.id != 'expr':
                continue
            expr = ast.Expression(Numbers().visit(node.value))
            ast.fix_missing_locations(expr)
            self.expr = compile(expr, '<string>', mode='eval')
            break


def build_instance_expression(instance, expr, back=1):
    """Return fixed expression."""
    try:
        # Evaluate expression in the original context.
        frame = sys._getframe(back + 1)

        # Find original code and convert numbers.
        code = ast.parse(inspect.getsource(instance))
        class_def = ClassDef()
        class_def.visit(code)

        # Include names used during number replacement.
        f_globals = frame.f_globals.copy()
        f_globals.setdefault('integer', integer)
        f_globals.setdefault('real_mpfr', real_mpfr)

        # Include locally defined variables.
        f_locals = frame.f_locals.copy()
        for name in dir(instance):
            data = getattr(instance, name)
            try:
                if isinstance(data, BaseVariable):
                    f_locals[name] = data
            except TypeError:
                pass  # It is not a class.
        expr = eval(class_def.expr, f_globals, f_locals)
    except TypeError:
        pass

    return BaseEquation(SR, expr)


class EquationMeta(type):
    """Equation interface."""

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            parents = process_parents(parents, BaseEquation)
            dct.setdefault('name', name)
            expr = dct.pop('expr')

            instance = super(EquationMeta, cls).__new__(
                cls, name, parents, dct)
            instance.expr = expr = build_instance_expression(instance, expr)

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
        return tuple(
            Variable.__registry__[arg].expr
            if arg in Variable.__registry__ else arg
            for arg in cls.expr.args())


__all__ = ('Equation', 'convert', )
