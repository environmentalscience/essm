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
"""Chamber insulation material."""

from __future__ import absolute_import

from essm.variables.units import joule, kelvin, kilogram, meter, second

from .._core import Variable


class c_pi(Variable):
    """Heat capacity of insulation material."""

    unit = joule / kilogram / kelvin
    latex_name = 'c_{pi}'


class lambda_i(Variable):
    """Heat conductivity of insulation material."""

    unit = joule / second / meter / kelvin


class rho_i(Variable):
    """Density of insulation material."""

    unit = kilogram / meter ** 3


class L_i(Variable):
    """Thickness of insulation material."""

    unit = meter


class A_i(Variable):
    """Conducting area of insulation material."""

    unit = meter ** 2


class Q_i(Variable):
    """Heat conduction through insulation material."""

    unit = joule / second


class dT_i(Variable):
    """Temperature increment of insulation material."""

    unit = kelvin


__all__ = (
    'c_pi',
    'lambda_i',
    'rho_i',
    'L_i',
    'A_i',
    'Q_i',
    'dT_i',
)
