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

    @property
    def __doc__(self):
        return self.definition.__doc__

    @property
    def __name__(self):
        return self.definition.__name__

    @property
    def __module__(self):
        return self.definition.__module__


def register(cls):
    """Register an expression object instead of class definition."""
    return ExpressionProxy(cls)
