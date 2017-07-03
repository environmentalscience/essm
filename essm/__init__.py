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
"""Variables module to deal with physical variables and units.

It allows attaching docstrings to variable names, defining their domains
(e.g. integer, real or complex), their units and LaTeX representations.
You can also provide a default value, which is particularly useful for
physical constants.

Creating variables
==================
To create custom variables, first import `Variable`:

    >>> from essm.variables import Variable

To define units, you must first import these units from the library:

    >>> from essm.variables.units import joule, kelvin, meter

Then you can define a custom variable with its name, description, domain,
latex_name, unit, and an optional default value, e.g.:

    >>> class demo_chamber_volume(Variable):
    ...    '''Volume of chamber.'''
    ...    latex_name = 'V_c'
    ...    domain = 'real'
    ...    name = 'V_c'
    ...    unit = meter ** 3
    ...    default = 1

    >>> class demo_chamber_length(Variable):
    ...    '''Length of chamber.'''
    ...    latex_name = 'L_c'
    ...    domain = 'real'
    ...    name = 'L_c'
    ...    unit = meter
    ...    default = 1

Now, `demo_chamber_volume` is displayed as `V_c` and
`demo_chamber_length` is displayed as `L_c`.
You can type `help(demo_chamber_volume)` to inspects its metadata.

`Variable.__defaults__` returns a dictionary with all variables and
their default values, `Variable.__units__` returns their units, and
`demo_chamber_volume.short_unit()` can be used to obtain the units
in short notation.

Creating equations
==================

To create custom equations, proceed similarly to above, i.e. first import
`Equation`:

    >>> from essm.equations import Equation

Then define an equation, e.g.:

    >>> class demo_eq_volume(Equation):
    ...    '''Calculate chamber volume.
    ...
    ...    Uses :math:`V_{l}` and assumes cubic shape.
    ...    '''
    ...    expr = demo_chamber_volume == demo_chamber_length ** 3

Importing variables and equations
=================================
You can import pre-defined variables and equations as e.g.:

    >>> from essm.variables.physics.thermodynamics import *
    >>> from essm.equations.physics.thermodynamics import *
"""

from __future__ import absolute_import

from sympy import E as e
from sympy import Eq, solve, sqrt
