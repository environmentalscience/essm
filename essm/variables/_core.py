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
"""Core variable type."""

from __future__ import absolute_import

import warnings

import six
from sympy import Basic, S
from sympy.physics.units import Dimension, Quantity
from sympy.physics.units.quantities import \
    _Quantity_constructor_postprocessor_Add

from .units import derive_unit
from ..bases import RegistryType
from ..transformer import build_instance_expression


class VariableMeta(RegistryType):
    """Variable interface."""

    def __new__(cls, name, parents, dct):
        """Build and register new variable."""
        if '__registry__' not in dct:
            unit = dct.pop('unit', S.One)
            if unit == 1:
                unit = S.One
            definition = dct.pop('expr', None)

            dct.setdefault('name', name)
            dct.setdefault('domain', 'real')
            dct.setdefault('latex_name', dct['name'])
            dct.setdefault('unit', unit)

            instance = super(VariableMeta,
                             cls).__new__(cls, name, parents, dct)

            # Variable with definition expression.
            if definition is not None:
                definition = build_instance_expression(instance, definition)
                derived_unit = derive_unit(definition, name=name)

                if unit == S.One:
                    unit = derived_unit  # only if unit is None
                instance.expr, instance.unit = definition, derived_unit

                if unit != instance.unit:
                    raise ValueError(
                        'Invalid expression units {0} should be {1}'.format(
                            instance.unit, unit
                        )
                    )

            expr = BaseVariable(
                instance,
                dct['name'],
                Dimension(Quantity.get_dimensional_expr(unit)),
                unit or S.One,
                abbrev=dct['latex_name'],
            )
            instance[expr] = instance

            # Store definition as variable expression.
            if definition is not None:
                instance.__expressions__[expr] = definition

            # Store default variable only if it is defined.
            if 'default' in dct:
                instance.__defaults__[expr] = dct['default']

            # Store unit for each variable:
            instance.__units__[expr] = instance.unit

            return expr

        return super(VariableMeta, cls).__new__(cls, name, parents, dct)

    def __delitem__(cls, expr):
        """Remove a variable from the registry."""
        super(VariableMeta, cls).__delitem__(expr)
        for name in ('__units__', '__defaults__', '__expressions__'):
            registry = getattr(cls, name)
            if expr in registry:
                del registry[expr]


@six.add_metaclass(VariableMeta)
class Variable(object):
    """Base type for all physical variables."""

    __registry__ = {}
    __defaults__ = {}
    __units__ = {}
    __expressions__ = {}


class BaseVariable(Quantity):
    """Physical variable."""

    def __new__(
            cls,
            definition,
            name,
            dimension,
            scale_factor=S.One,
            abbrev=None,
            **assumptions
    ):
        self = super(BaseVariable, cls).__new__(
            cls,
            name,
            dimension,
            scale_factor=scale_factor,
            abbrev=abbrev,
            **assumptions
        )
        self.definition = definition
        return self

    @property
    def __doc__(self):
        return self.definition.__doc__


Basic._constructor_postprocessor_mapping[BaseVariable] = {
    "Add": [_Quantity_constructor_postprocessor_Add],
}

__all__ = ('Variable', )
