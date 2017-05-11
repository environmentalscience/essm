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


class Equation(object):
    """Base type for all equation."""
    __metaclass__ = EquationMeta
    __registry__ = {}
    __defaults__ = {}

    @classmethod
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



from ..variables.chamber.insulation import *
from ..variables.chamber.mass import *
from ..variables.leaf.radiation import *
from ..variables.leaf.water_vapour import *


def register(cls):
    """Register symbolic variable instead of class definition."""
    return cls.expr


@register
class eq_Qi(Equation):
    """Calculate ....

    .. see-also: ...
    """
    expr = Q_i == dT_i*lambda_i*A_i/L_i


__all__ = (
    'eq_Qi',
) + tuple(str(variable) for variable in eq_Qi.arguments())
