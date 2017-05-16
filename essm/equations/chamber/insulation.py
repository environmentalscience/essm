from __future__ import absolute_import

from ...variables.chamber.insulation import A_i, L_i, Q_i, dT_i, lambda_i
from .._core import Equation, register


@register
class eq_Qi(Equation):
    """Calculate ....

    .. see-also: ...
    """
    expr = Q_i == dT_i*lambda_i*A_i/L_i


__all__ = (
    'eq_Qi',
)
