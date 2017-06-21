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
"""Define unit symbols."""

from sage.all import var
from sage.symbolic.units import units

joule = units.energy.joule
kelvin = units.temperature.kelvin
kilogram = units.mass.kilogram
meter = units.length.meter
mole = units.amount_of_substance.mole
pascal = units.pressure.pascal
second = units.time.second
watt = units.power.watt

SHORT_UNIT_SYMBOLS = {
    joule: var('J'),
    kelvin: var('K'),
    kilogram: var('kg'),
    meter: var('m'),
    mole: var('mol'),
    pascal: var('Pa'),
    second: var('s'),
    watt: var('W'), }


def markdown(unit):
    """Return markdown representaion of a unit."""
    facs = unit.factor_list()
    str1 = ''
    for term1 in facs:
        op1 = term1[1]
        if op1 == 1:
            str1 = str(term1[0]) + ' ' + str1
        else:
            str1 += ' {0}$^{{{1}}}$ '.format(markdown(term1[0]), markdown(op1))
    return str1


__all__ = (
    'SHORT_UNIT_SYMBOLS', 'markdown', 'joule', 'kelvin', 'kilogram', 'meter',
    'mole', 'pascal', 'second', 'watt')
