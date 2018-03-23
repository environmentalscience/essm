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
"""SI unit system.

Based on MKSA, which stands for "meter, kilogram, second, ampere".
This unit system adds kelvin and mole.
"""

from __future__ import division

from sympy.physics.units.definitions import cd, K, mol
from sympy.physics.units.dimensions import (
    amount_of_substance, luminous_intensity, temperature)

from sympy.physics.units.prefixes import PREFIXES, prefix_unit
from sympy.physics.units.systems.mksa import MKSA, _mksa_dim

derived_dims = ()
base_dims = (amount_of_substance, luminous_intensity, temperature)

# dimension system
_si_dim = _mksa_dim.extend(base=base_dims, dims=derived_dims, name='SI')


units = [mol, cd, K]
all_units = []
for u in units:
    all_units.extend(prefix_unit(u, PREFIXES))

all_units.extend([mol, cd, K])

SI = MKSA.extend(base=(mol, cd, K), units=all_units, name='SI')
