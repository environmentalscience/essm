# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017 ETH Zurich, Swiss Data Science Center.
# Copyright (C) 2018 LIST (Luxembourg Institute of Science and Technology).
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

from sympy import Abs, Add, Basic, Derivative, Function, Mul, Pow, S, Symbol
from sympy.physics.units import Dimension, Quantity, convert_to
from sympy.physics.units.dimensions import dimsys_default, dimsys_SI

from ..bases import RegistryType
from ..transformer import build_instance_expression
from .units import derive_unit


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
            dct.setdefault('assumptions', {'real': True})
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
                instance.expr, instance.unit = definition, unit

                dim_derived = dimsys_SI.get_dimensional_dependencies(
                    Quantity.get_dimensional_expr(derived_unit)
                )
                dim_unit = dimsys_SI.get_dimensional_dependencies(
                    Quantity.get_dimensional_expr(unit)
                )
                if dim_derived != dim_unit:
                    raise ValueError(
                        'Invalid expression units {0} should be {1}'.format(
                            instance.unit, unit
                        )
                    )

            expr = BaseVariable(
                instance,
                dct['name'],
                abbrev=dct['latex_name'],
                dimension=Dimension(Quantity.get_dimensional_expr(unit)),
                scale_factor=unit or S.One,
                **dct['assumptions']
            )
            instance[expr] = instance

            # Store definition as variable expression.
            if definition is not None:
                instance.__expressions__[expr] = definition

            # Store default variable only if it is defined.
            if 'default' in dct:
                instance.__defaults__[expr] = dct['default']

            # Store unit for each variable:
            instance.__units__[expr] = unit

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

    @staticmethod
    def get_dimensional_expr(expr):
        """Return dimensions of expression."""
        expr = Variable.check_unit(expr)
        if isinstance(expr, Mul):
            return Mul(*[Variable.get_dimensional_expr(i) for i in expr.args])
        elif isinstance(expr, Pow):
            return Variable.get_dimensional_expr(expr.base) ** expr.exp
        elif isinstance(expr, Add):
            return Variable.get_dimensional_expr(expr.args[0])
        elif isinstance(expr, Derivative):
            dim = Variable.get_dimensional_expr(expr.expr)
            for independent, count in expr.variable_count:
                dim /= Variable.get_dimensional_expr(independent) ** count
            return dim
        elif isinstance(expr, Function):
            args = [Variable.get_dimensional_expr(arg) for arg in expr.args]
            if all(i == 1 for i in args):
                return S.One
            return expr.func(*args)
        elif isinstance(expr, Quantity):
            return expr.dimension.name
        elif isinstance(expr, BaseVariable):
            return Quantity.get_dimensional_expr(expr.definition.unit)
        return S.One

    @staticmethod
    def check_unit(expr):
        """Construct postprocessor for the addition.

        Checks for dimension mismatches of the addends, thus preventing
        expressions like `meter + second` to be created.
        """
        if not expr.is_Add or expr.is_Equality:
            return expr
        deset = {
            tuple(
                sorted(
                    dimsys_default.get_dimensional_dependencies(
                        Dimension(
                            Variable.get_dimensional_expr(i)
                            if not i.is_number else 1
                        )
                    ).items()
                )
            )
            for i in expr.args
        }
        # If `deset` has more than one element, then some dimensions do not
        # match in the sum:
        if len(deset) > 1:
            raise ValueError(
                "summation of quantities of incompatible dimensions"
            )
        return expr


class BaseVariable(Symbol):
    """Physical variable."""

    def __new__(
            cls,
            definition,
            name,
            abbrev,
            dimension,
            scale_factor=S.One,
            unit_system='SI',
            **assumptions
    ):
        self = super(BaseVariable, cls).__new__(
            cls, name, abbrev=abbrev, **assumptions
        )
        # self.set_dimension(dimension, unit_system=unit_system)
        # self.set_scale_factor(scale_factor)
        self.definition = definition
        return self

    @property
    def __doc__(self):
        return self.definition.__doc__

    def _latex(self, printer):
        return self.definition.latex_name


def _Quantity_constructor_postprocessor_Add(expr):
    """Construct postprocessor for the addition.

    It checks for dimension mismatches of the addends, thus preventing
    expressions like ``meter + second`` to be created.
    """
    deset = {
        tuple(sorted(dimsys_default.get_dimensional_dependencies(Dimension(
            Quantity.get_dimensional_expr(i) if not i.is_number else 1
        )).items()))
        for i in expr.args
        if i.free_symbols == set()  # do not raise if there are symbols
        # (free symbols could contain the units corrections)
    }
    # If `deset` has more than one element, then some dimensions do not
    # match in the sum:
    if len(deset) > 1:
        raise ValueError("summation of quantities of incompatible dimensions")
    return expr


Basic._constructor_postprocessor_mapping[BaseVariable] = {
    "Add": [_Quantity_constructor_postprocessor_Add],
}

__all__ = ('Variable', )
