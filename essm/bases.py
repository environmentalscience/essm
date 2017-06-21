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
"""Base classes."""

from __future__ import absolute_import

import warnings

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

    result = convert(Expression(SR, expr.subs(used_units) / expr))
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

    def __init__(self, expr, definition, units=None):
        """Initialize expression."""
        super(BaseExpression, self).__init__(SR, expr)
        self.definition = definition
        self.__units__ = units or getattr(definition, '__units__', None)

    def register(self):
        """Register expression in registry."""
        if self in self.definition.__registry__:
            warnings.warn(
                '"{0}" will be overridden by "{1}"'.format(
                    self.definition.__registry__[self].__module__ + ':' +
                    self.definition.name,
                    self.definition.__module__ + ':' + str(self), ),
                stacklevel=2)
        self.definition.__registry__[self] = self.definition
        return self

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
