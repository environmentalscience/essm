from __future__ import absolute_import

from ...variables.chamber.insulation import A_i, L_i, Q_i, dT_i, lambda_i
from .._core import Equation


class eq_Qi(Equation):
    """Calculate ....

    :cite:`schymanski_leaf-scale_2016`
    """
    expr = Q_i == dT_i * lambda_i * A_i / L_i
    """Describe how you got the equation."""


__all__ = ('eq_Qi', )
