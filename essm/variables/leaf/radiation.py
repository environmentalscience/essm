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
"""Leaf radiation balance."""

from __future__ import absolute_import

from essm.variables.units import joule, kelvin, kilogram, meter, second, watt

from .._core import Variable


class alpha_l(Variable):
    """Leaf albedo, fraction of shortwave radiation reflected by the leaf."""

    unit = watt / watt


class R_d(Variable):
    """Downwelling global radiation."""

    unit = joule / second / meter ** 2


class R_la(Variable):
    """Longwave radiation absorbed by leaf."""

    unit = joule / second / meter ** 2
    latex_name = 'R_{la}'


class R_ld(Variable):
    """Downwards emitted/reflected global radiation from leaf."""

    unit = joule / second / meter ** 2
    latex_name = 'R_{ld}'


class R_lu(Variable):
    """Upwards emitted/reflected global radiation from leaf."""

    unit = joule / second / meter ** 2
    latex_name = 'R_{lu}'


class R_u(Variable):
    """Upwelling global radiation."""

    unit = joule / second / meter ** 2


class S_a(Variable):
    """Radiation sensor above leaf reading."""

    unit = joule / second / meter ** 2


class S_b(Variable):
    """Radiation sensor below leaf reading."""

    unit = joule / second / meter ** 2


class S_s(Variable):
    """Radiation sensor beside leaf reading."""

    unit = joule / second / meter ** 2


__all__ = (
    'alpha_l',
    'R_d',
    'R_la',
    'R_ld',
    'R_lu',
    'R_u',
    'S_a',
    'S_b',
    'S_s',
)
