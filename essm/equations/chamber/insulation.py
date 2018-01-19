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
"""Chamber insulation."""

from __future__ import absolute_import

from essm import Eq

from ...variables.chamber.insulation import A_i, L_i, Q_i, dT_i, lambda_i
from .._core import Equation


class eq_Qi(Equation):
    """Calculate ....

    :cite:`schymanski_leaf-scale_2017`
    """

    expr = Eq(Q_i, dT_i * lambda_i * A_i / L_i)
    """Describe how you got the equation."""


__all__ = ('eq_Qi', )
