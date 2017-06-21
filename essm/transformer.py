# -*- coding: utf-8 -*-
"""Transform expressions."""

from __future__ import absolute_import

import ast
import inspect
import sys

from sage.rings import integer, real_mpfr

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


def unindent(source):
    """Fix indentation."""
    counter = 0
    while source[counter] == ' ':
        counter += 1
    if counter:
        return '\n'.join(line[counter:] for line in source.split('\n'))
    return source


def build_instance_expression(instance, expr, back=1):
    """Return fixed expression."""
    from .variables._core import BaseVariable
    try:
        # Evaluate expression in the original context.
        frame = sys._getframe(back + 1)

        # Find original code and convert numbers.
        code = ast.parse(unindent(inspect.getsource(instance)))
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
            if isinstance(data, BaseVariable):
                f_locals[name] = data
        expr = eval(class_def.expr, f_globals, f_locals)
    except TypeError:  # pragma: no cover
        pass

    return expr
