# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017 ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
"""Transform expressions."""

from __future__ import absolute_import

import ast
import inspect
import sys

from sympy.core import numbers

_Number = ast.parse('numbers.Number', mode='eval').body


def get_num_func(node):
    """Get number wrapper."""
    return _Number


def extend_globals(f_globals):
    """Extend globals."""
    f_globals.setdefault('numbers', numbers)


class Numbers(ast.NodeTransformer):
    """Change Python numbers to 'symbolic' numbers."""

    def visit_Num(self, node):
        """Rewrite int / int to Fraction(int, int)."""
        func = get_num_func(node)

        if func is None:
            return node

        return ast.copy_location(
            ast.Call(
                func=func,
                args=[ast.Str(str(node.n))],
                keywords=[],
                starargs=None,
                kwargs=None,
            ), node
        )


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
        extend_globals(f_globals)

        # Include locally defined variables.
        f_locals = frame.f_locals.copy()
        for name in dir(instance):
            data = getattr(instance, name)
            if isinstance(data, BaseVariable):
                f_locals[name] = data
        expr = eval(class_def.expr, f_globals, f_locals)
    except (IOError, TypeError):  # pragma: no cover
        pass

    return expr
