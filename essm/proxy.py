# -*- coding: utf-8 -*-

"""Proxy to common types."""

import wrapt


class ExpressionProxy(wrapt.ObjectProxy):
    """Proxy an expression object."""

    definition = None
    """Original class definition."""

    def __init__(self, cls):
        super(ExpressionProxy, self).__init__(cls.expr)
        self.definition = cls
        self.__doc__ = cls.__doc__


def register(cls):
    """Register an expression object instead of class definition."""
    return ExpressionProxy(cls)
