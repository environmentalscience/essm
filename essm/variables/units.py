# -*- coding: utf-8 -*-

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
    watt: var('W'),
}

__all__ = (
    'SHORT_UNIT_SYMBOLS',
)
