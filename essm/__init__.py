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
"""ESSM contains helpers to deal with physical variables and units.

Creating variables
==================
To create custom variables, first import `Variable`:

    >>> from essm.variables import Variable

To define units, you can either import these units from the library:

    >>> from essm.variables.units import joule, kelvin, meter

Then you can define a custom variable with its name, description, domain,
latex_name, and unit, e.g.:

    >>> class demo_chamber_volume(Variable):
    ...    '''Volume of chamber.'''
    ...    latex_name = 'V_c'
    ...    domain = 'real'
    ...    name = 'V_c'
    ...    unit = meter ** 3
    ...    default = 1

Now, `demo_chamber_volume` is displayed as `V_c` and you can type
`help(demo_chamber_volume)`.

`Variable.__defaults__` returns a dictionary with all variables and
their default values, `Variable.__units__` returns their units, and
`demo_chamber_volume.short_unit()` can be used to obtain the units
in short notation.

You can import pre-defined variables as e.g.:

    >>> from essm.variables.chamber.insulation import *
    >>> from essm.variables.chamber.mass import *
    >>> from essm.variables.leaf.water_vapour import *

Creating equations
==================

To create custom equations, proceed similarly to avove, i.e. first import
`Equation`:

    >>> from essm.equations import Equation

Then define an equation, e.g.:

    >>> class demo_eq_Qi(Equation):
    ...    '''Calculate heat conduction through insulation material.
    ...
    ...    Uses :math:`Q_{i}` as a function of temperature difference
    ...    :math:`dT_{i}`, and material properties.
    ...    '''
    ...    expr = Q_i == dT_i * lambda_i * A_i / L_i

"""

from __future__ import absolute_import

from .bases import convert, expand_units

__all__ = ('convert', 'expand_units')
