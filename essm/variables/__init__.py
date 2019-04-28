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
latex_name, unit, and an optional default value.

Example:

.. code-block:: python

   from .variables.units import meter

   class demo_chamber_volume1(Variable):
      '''Volume of Chamber 1.'''

       name = 'V_c1'
       domain = 'real'
       latex_name = 'V_{c1}'
       unit = meter ** 3
       default = 1

Now, demo_chamber_volume is displayed as V_c1 and it will be
nicely rendered in LaTeX as :math:`V_{c1}`.

You can type `help(demo_chamber_volume)` to inspects its metadata.

`Variable.__defaults__` returns a dictionary with all variables and
their default values, `Variable.__units__` returns their units, and
`demo_chamber_volume.short_unit()` can be used to obtain the units
in short notation.

This module also contains libraries of pre-defined variables, which
can be imported into your session, e.g.:

     >>> from essm.variables.physics.thermodynamics import *
     >>> from essm.variables.leaf.energy_water import *

"""

from __future__ import absolute_import

from ._core import Variable

__all__ = (
    'Variable',
)
