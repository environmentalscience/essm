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

    def __call__(self, *args, **kwargs):
        """Return wrapped object."""
        if args:
            return getattr(self.__wrapped__, args[0])(*args[1:], **kwargs)
        return self.__wrapped__

    def subs(self, *args, **kwargs):
        """Proxy to expression subtitution method."""
        expr = self.__wrapped__.subs(
            *(x.__wrapped__ if isinstance(x, ExpressionProxy) else x
              for x in args),
            **{key: x.__wrapped__ if isinstance(x, ExpressionProxy) else x
              for key, x in kwargs.items()}
        )
        return self.__class__(type(
            self.definition.__name__ + str(hash(str(expr))),
            (self.definition, ),
            {
                '__doc__': 'Subtituted "{0}" in "{1}".'.format(
                    str(expr), str(self.__wrapped__)
                ),
                'expr': expr,
            },
        ))

def register(cls):
    """Register an expression object instead of class definition."""
    return ExpressionProxy(cls)
