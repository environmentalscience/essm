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


__all__ = ('SHORT_UNIT_SYMBOLS', 'markdown', 'joule', 'kelvin', 'kilogram',
           'meter', 'mole', 'pascal', 'second', 'watt')
